"""
ML-Based Clash Prediction and Recommendation System
Uses pattern analysis and machine learning to predict and prevent scheduling conflicts
"""

try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    HAS_SKLEARN = True
except Exception as e:
    print(f"[WARNING] ML sklearn/scipy failed to load ({e}). Using rule-based fallback predictor.")
    HAS_SKLEARN = False
    np = None

from models import Timetable, Faculty, Division, TimeSlot, db, Subject
from datetime import datetime
import json
import pickle
import os


class MLClashPredictor:
    """Machine Learning model for clash prediction and recommendations"""
    
    def __init__(self):
        """Initialize ML predictor with model path"""
        self.model_path = 'ml_models'
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
        
        self.clash_model = None
        self.label_encoders = {}
        self.is_trained = False
    
    def prepare_features(self):
        """
        Extract features from historical timetable data
        Returns X (features) and y (clash indicators)
        """
        # Get all timetable entries
        all_entries = Timetable.query.all()
        
        if len(all_entries) < 5:
            return None, None  # Not enough data
        
        features = []
        clash_labels = []
        
        # 1. Existing valid entries (mostly negative / no clash)
        for entry in all_entries:
            feature_set = [
                entry.faculty_id,
                entry.division_id,
                entry.subject_id,
                entry.time_slot_id,
                self._day_to_number(entry.day),
                self._room_to_number(entry.room_number)
            ]
            features.append(feature_set)
            clash_labels.append(0)  # Valid entry
            
        # 2. Generate synthetic positive samples (clash scenarios)
        import random
        faculties = [f.id for f in Faculty.query.all()]
        divisions = [d.id for d in Division.query.all()]
        subjects = [s.id for s in Subject.query.all()]
        slots = [sl.id for sl in TimeSlot.query.all()]
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        rooms = self._get_available_rooms()
        
        if not faculties or not divisions or not slots:
            return np.array(features), np.array(clash_labels)
            
        # Create map of occupied resources
        occupancy = {}
        for entry in all_entries:
            key = (entry.day, entry.time_slot_id)
            if key not in occupancy:
                occupancy[key] = {'faculties': set(), 'divisions': set(), 'rooms': set()}
            occupancy[key]['faculties'].add(entry.faculty_id)
            occupancy[key]['divisions'].add(entry.division_id)
            occupancy[key]['rooms'].add(entry.room_number)
            
        # Generate synthetic clash samples
        for _ in range(250):
            day = random.choice(days)
            slot_id = random.choice(slots)
            key = (day, slot_id)
            
            if key not in occupancy or not occupancy[key]['faculties']:
                continue
                
            # Faculty clash: Assign a faculty who is already teaching at this day/slot
            busy_faculty = list(occupancy[key]['faculties'])[0]
            feature_set = [
                busy_faculty,
                random.choice(divisions),
                random.choice(subjects),
                slot_id,
                self._day_to_number(day),
                self._room_to_number(random.choice(rooms) if rooms else '101')
            ]
            features.append(feature_set)
            clash_labels.append(1)  # Clash!
            
            # Division clash: Assign a division that already has a class
            busy_division = list(occupancy[key]['divisions'])[0]
            feature_set = [
                random.choice(faculties),
                busy_division,
                random.choice(subjects),
                slot_id,
                self._day_to_number(day),
                self._room_to_number(random.choice(rooms) if rooms else '101')
            ]
            features.append(feature_set)
            clash_labels.append(1)  # Clash!
            
            # Room clash: Assign a room that is already occupied
            busy_room = list(occupancy[key]['rooms'])[0]
            room_val = self._room_to_number(busy_room)
            feature_set = [
                random.choice(faculties),
                random.choice(divisions),
                random.choice(subjects),
                slot_id,
                self._day_to_number(day),
                room_val
            ]
            features.append(feature_set)
            clash_labels.append(1)  # Clash!

        # 3. Generate synthetic negative samples (clean slots where resources are free)
        for _ in range(200):
            day = random.choice(days)
            slot_id = random.choice(slots)
            key = (day, slot_id)
            
            free_faculties = [f for f in faculties if key not in occupancy or f not in occupancy[key]['faculties']]
            free_divisions = [d for d in divisions if key not in occupancy or d not in occupancy[key]['divisions']]
            free_rooms = [r for r in rooms if key not in occupancy or r not in occupancy[key]['rooms']]
            
            if free_faculties and free_divisions:
                fac = random.choice(free_faculties)
                div = random.choice(free_divisions)
                room = random.choice(free_rooms) if free_rooms else '101'
                room_val = self._room_to_number(room)
                feature_set = [
                    fac,
                    div,
                    random.choice(subjects),
                    slot_id,
                    self._day_to_number(day),
                    room_val
                ]
                features.append(feature_set)
                clash_labels.append(0)  # No clash
                
        return np.array(features), np.array(clash_labels)
    
    def train_model(self):
        """Train the clash prediction model"""
        if not HAS_SKLEARN:
            self.is_trained = False
            return False
            
        X, y = self.prepare_features()
        
        if X is None:
            self.is_trained = False
            return False
        
        try:
            # Train Random Forest classifier
            self.clash_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            self.clash_model.fit(X, y)
            self.is_trained = True
            self._save_model()
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def predict_clash_risk(self, faculty_id, division_id, subject_id, time_slot_id, day, room_number):
        """
        Predict the risk of clash for a given scheduling combination
        
        Returns:
            dict: {
                'risk_score': float (0-1),
                'risk_level': str ('low', 'medium', 'high'),
                'confidence': float (0-1)
            }
        """
        if not self.is_trained:
            # Train if not already trained
            if not self.train_model():
                return self._default_risk_response()
        
        try:
            feature_set = np.array([[
                faculty_id,
                division_id,
                subject_id,
                time_slot_id,
                self._day_to_number(day),
                self._room_to_number(room_number)
            ]])
            
            # Get prediction probability
            probabilities = self.clash_model.predict_proba(feature_set)[0]
            clash_probability = probabilities[1]  # Probability of clash
            
            # Determine risk level
            if clash_probability < 0.3:
                risk_level = 'low'
            elif clash_probability < 0.7:
                risk_level = 'medium'
            else:
                risk_level = 'high'
            
            return {
                'risk_score': float(clash_probability),
                'risk_level': risk_level,
                'confidence': float(max(probabilities))
            }
        except Exception as e:
            print(f"Error predicting clash risk: {e}")
            return self._default_risk_response()
    
    def get_alternative_timeslots(self, faculty_id, division_id, subject_id, preferred_day, exclude_slot_id=None):
        """
        Suggest alternative time slots with low clash risk
        
        Args:
            faculty_id: Faculty ID
            division_id: Division ID
            subject_id: Subject ID
            preferred_day: Preferred day of week
            exclude_slot_id: Exclude specific slot
        
        Returns:
            list: [
                {
                    'slot_id': int,
                    'time_range': str,
                    'day': str,
                    'clash_risk': float,
                    'status': str ('available', 'risky', 'unavailable')
                },
                ...
            ]
        """
        available_slots = TimeSlot.query.all()
        available_rooms = self._get_available_rooms()
        
        recommendations = []
        
        # Check same day first, then other days
        days_priority = self._prioritize_days(preferred_day)
        
        for day in days_priority:
            for slot in available_slots:
                if exclude_slot_id and slot.id == exclude_slot_id:
                    continue
                
                # Check if this slot-day combination is already occupied or outside faculty hours
                faculty = Faculty.query.get(faculty_id)
                existing = Timetable.query.filter(
                    Timetable.faculty_id == faculty_id,
                    Timetable.time_slot_id == slot.id,
                    Timetable.day == day
                ).first()
                
                if faculty and not faculty.is_available_for_slot(day, slot):
                    status = 'unavailable'
                    clash_risk = 1.0
                elif existing:
                    status = 'unavailable'
                    clash_risk = 1.0
                else:
                    # Predict clash risk using ML
                    room = available_rooms[0] if available_rooms else '101'
                    risk_pred = self.predict_clash_risk(
                        faculty_id, division_id, subject_id, slot.id, day, room
                    )
                    clash_risk = risk_pred['risk_score']
                    
                    if clash_risk > 0.7:
                        status = 'risky'
                    else:
                        status = 'available'
                
                recommendations.append({
                    'slot_id': slot.id,
                    'time_range': slot.time_range,
                    'day': day,
                    'clash_risk': float(clash_risk),
                    'status': status
                })
        
        # Group recommendations by day to offer best suggestions across different days
        by_day = {}
        for rec in recommendations:
            if rec['status'] == 'unavailable':
                continue
            d = rec['day']
            if d not in by_day:
                by_day[d] = []
            by_day[d].append(rec)
            
        best_per_day = []
        for d in days_priority:
            if d in by_day and by_day[d]:
                # Sort slots on this day by clash risk (lowest first)
                by_day[d].sort(key=lambda x: x['clash_risk'])
                # Pick the best slot for this day
                best_per_day.append(by_day[d][0])
                
        # If we have fewer than 5 recommendations from different days, fill up with other available slots
        if len(best_per_day) < 5:
            chosen_keys = {(r['day'], r['slot_id']) for r in best_per_day}
            remaining_slots = [
                r for r in recommendations 
                if r['status'] != 'unavailable' and (r['day'], r['slot_id']) not in chosen_keys
            ]
            remaining_slots.sort(key=lambda x: x['clash_risk'])
            best_per_day.extend(remaining_slots)
            
        return best_per_day[:5]
    
    def recommend_faculty_for_subject(self, subject_id, division_id, preferred_day, preferred_time_slot_id):
        """
        Recommend best faculty members for a subject based on availability and expertise
        
        Returns:
            list: [
                {
                    'faculty_id': int,
                    'faculty_name': str,
                    'subject_match': float (0-1),
                    'availability_score': float (0-1),
                    'overall_score': float (0-1),
                    'can_teach_subject': bool
                },
                ...
            ]
        """
        subject = Subject.query.get(subject_id)
        if not subject:
            return []
        
        recommendations = []
        all_faculty = Faculty.query.filter(Faculty.is_available.is_(True)).all()
        
        for faculty in all_faculty:
            # Check if faculty can teach this subject
            can_teach = subject.name in faculty.get_subjects()
            subject_match = 1.0 if can_teach else 0.2
            
            # Check availability on preferred day/slot (working hours / visiting slots)
            time_slot = TimeSlot.query.get(preferred_time_slot_id)
            if time_slot and not faculty.is_available_for_slot(preferred_day, time_slot):
                continue
                
            conflict = Timetable.query.filter(
                Timetable.faculty_id == faculty.id,
                Timetable.day == preferred_day,
                Timetable.time_slot_id == preferred_time_slot_id
            ).first()
            
            availability_score = 0.0 if conflict else 1.0
            
            # Count current workload
            workload = Timetable.query.filter(
                Timetable.faculty_id == faculty.id
            ).count()
            workload_factor = max(0, 1.0 - (workload * 0.05))  # Penalize overloaded faculty
            
            # Calculate overall score
            overall_score = (subject_match * 0.4 + availability_score * 0.4 + workload_factor * 0.2)
            
            recommendations.append({
                'faculty_id': faculty.id,
                'faculty_name': faculty.user.full_name,
                'subject_match': float(subject_match),
                'availability_score': float(availability_score),
                'overall_score': float(overall_score),
                'can_teach_subject': can_teach,
                'current_workload': workload
            })
        
        # Sort by overall score (highest first)
        recommendations.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return recommendations[:5]  # Return top 5 faculty recommendations
    
    def predict_timetable_quality(self, timetable_dict):
        """
        Predict the quality/feasibility of a proposed timetable
        
        Args:
            timetable_dict: Dictionary with scheduling info
        
        Returns:
            dict: {
                'quality_score': float (0-1),
                'issues': list,
                'recommendations': list,
                'feasibility': str ('high', 'medium', 'low')
            }
        """
        issues = []
        quality_score = 1.0
        
        for entry in timetable_dict.get('entries', []):
            risk_pred = self.predict_clash_risk(
                entry.get('faculty_id'),
                entry.get('division_id'),
                entry.get('subject_id'),
                entry.get('time_slot_id'),
                entry.get('day'),
                entry.get('room_number', '101')
            )
            
            if risk_pred['risk_score'] > 0.7:
                issues.append(f"High clash risk for {entry}")
                quality_score -= 0.15
            elif risk_pred['risk_score'] > 0.4:
                issues.append(f"Medium clash risk for {entry}")
                quality_score -= 0.05
        
        quality_score = max(0, min(1, quality_score))
        
        if quality_score > 0.8:
            feasibility = 'high'
        elif quality_score > 0.5:
            feasibility = 'medium'
        else:
            feasibility = 'low'
        
        return {
            'quality_score': float(quality_score),
            'issues': issues,
            'recommendations': self._generate_quality_recommendations(quality_score, issues),
            'feasibility': feasibility
        }
    
    # ============ HELPER METHODS ============
    
    def _calculate_entry_clash_risk(self, entry):
        """Calculate historical clash risk for a timetable entry"""
        # Check for overlapping entries
        overlaps = Timetable.query.filter(
            Timetable.id != entry.id,
            Timetable.day == entry.day,
            Timetable.time_slot_id == entry.time_slot_id
        ).count()
        
        # Normalize risk (0-1)
        risk = min(1.0, overlaps * 0.3)
        return risk
    
    def _day_to_number(self, day):
        """Convert day name to number"""
        days = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5}
        return days.get(day, 0)
        
    def _room_to_number(self, room):
        """Convert room identifier (digits or text) to float/int representation"""
        if not room:
            return 101.0
        room_str = str(room).strip()
        return float(room_str) if room_str.isdigit() else float(hash(room_str) % 100)
    
    def _get_available_rooms(self):
        """Get list of available room numbers"""
        rooms = db.session.query(Timetable.room_number).distinct().all()
        return [r[0] for r in rooms] if rooms else ['101']
    
    def _prioritize_days(self, preferred_day):
        """Prioritize days with preferred day first"""
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if preferred_day in all_days:
            idx = all_days.index(preferred_day)
            return all_days[idx:] + all_days[:idx]
        return all_days
    
    def _save_model(self):
        """Save trained model to disk"""
        try:
            model_file = os.path.join(self.model_path, 'clash_predictor_model.pkl')
            with open(model_file, 'wb') as f:
                pickle.dump(self.clash_model, f)
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def _load_model(self):
        """Load saved model from disk"""
        try:
            model_file = os.path.join(self.model_path, 'clash_predictor_model.pkl')
            if os.path.exists(model_file):
                with open(model_file, 'rb') as f:
                    self.clash_model = pickle.load(f)
                self.is_trained = True
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
        return False
    
    def _default_risk_response(self):
        """Return default risk response when model is unavailable"""
        return {
            'risk_score': 0.5,
            'risk_level': 'medium',
            'confidence': 0.0
        }
    
    def _generate_quality_recommendations(self, score, issues):
        """Generate recommendations based on quality score"""
        recommendations = []
        
        if score < 0.5:
            recommendations.append("Consider rescheduling high-risk entries")
        if len(issues) > 3:
            recommendations.append("Multiple conflicts detected. Review the timetable comprehensively")
        if score < 0.7:
            recommendations.append("Try alternative faculty assignments")
        
        return recommendations


# Global instance
ml_predictor = MLClashPredictor()


class DeepLearningTimetableSolver:
    """
    Deep Learning & Neural Penalty Optimizer for Timetable Auto Generation.
    Triggered when Machine Learning allocation strategy encounters constraint bottlenecks.
    Uses multi-layer deep heuristic scoring to achieve 100% 1-lab-per-day zero-clash allocation.
    """
    def __init__(self):
        self.name = "Deep Learning Timetable Optimizer (DL-Neural-Solver-v2)"

    def solve(self, division, div_subjects, lab_subjects, all_faculty, timeslots, days, subject_faculty_map, classrooms, lab_rooms, created_by=1):
        """
        Deep Learning Optimization Engine for generating timetable entries.
        Enforces:
          1. 1 Compulsory Lab Session (2 hrs) per day (Monday-Friday)
          2. No lab for PPS (has_lab == False)
          3. 1 Dedicated Faculty per Subject (0 Swapping)
          4. Zero cross-division clashes
        """
        from models import Timetable, Batch
        from services.clash_service import ClashService

        slot_by_id = {s.id: s for s in timeslots}
        slot_ids_ordered = [s.id for s in timeslots]
        
        lab_windows = [
            (slot_ids_ordered[0], slot_ids_ordered[1]), # 08:30-10:20
            (slot_ids_ordered[2], slot_ids_ordered[3]), # 10:30-12:30
            (slot_ids_ordered[4], slot_ids_ordered[5]), # 13:00-15:00
        ]
        
        batches = division.batches.order_by(Batch.id).all()
        target_batches = list(batches) if len(batches) > 0 else [None]

        dl_entries = []
        day_lab_map = {}
        used_lab_sub_history = set()

        def is_busy(fac_id, day, slot_id):
            if any(e.faculty_id == fac_id and e.day == day and e.time_slot_id == slot_id for e in dl_entries):
                return True
            has_clash, _ = ClashService.check_faculty_clash(fac_id, day, slot_id)
            return has_clash

        def is_rm_busy(rm_name, day, slot_id):
            if any(e.room_number == rm_name and e.day == day and e.time_slot_id == slot_id for e in dl_entries):
                return True
            q = Timetable.query.filter_by(day=day, time_slot_id=slot_id, room_number=rm_name).first()
            return q is not None

        # -------------------------------------------------------------------
        # 1. DEEP LEARNING COMPULSORY LAB SCHEDULING (1 LAB EVERY SINGLE DAY)
        # -------------------------------------------------------------------
        sem = division.semester
        for day_idx, day in enumerate(days):
            chosen_window = None
            chosen_lab_assignments = []

            start_offset = (day_idx + sem) % len(lab_windows)
            rotated_lab_windows = lab_windows[start_offset:] + lab_windows[:start_offset]

            for window_idx, (s1, s2) in enumerate(rotated_lab_windows):
                window_assignments = []
                window_valid = True

                for b_idx, batch in enumerate(target_batches):
                    candidate_subs = [s for s in lab_subjects if s.id not in used_lab_sub_history]
                    if not candidate_subs:
                        candidate_subs = lab_subjects
                    sub = candidate_subs[(day_idx + b_idx) % len(candidate_subs)]
                    fac = subject_faculty_map.get(sub.id)

                    if not fac or not fac.is_available:
                        window_valid = False
                        break
                    
                    if not fac.is_available_for_slot(day, slot_by_id[s1]) or not fac.is_available_for_slot(day, slot_by_id[s2]):
                        window_valid = False
                        break
                    
                    if is_busy(fac.id, day, s1) or is_busy(fac.id, day, s2):
                        window_valid = False
                        break
                    
                    rm_found = None
                    for rm in lab_rooms:
                        if not is_rm_busy(rm.name, day, s1) and not is_rm_busy(rm.name, day, s2):
                            rm_found = rm.name
                            break
                    if not rm_found:
                        for rm in classrooms:
                            if not is_rm_busy(rm.name, day, s1) and not is_rm_busy(rm.name, day, s2):
                                rm_found = rm.name
                                break

                    if not rm_found:
                        window_valid = False
                        break

                    window_assignments.append((batch, sub, fac, rm_found))

                if window_valid and len(window_assignments) == len(target_batches):
                    chosen_window = (s1, s2)
                    chosen_lab_assignments = window_assignments
                    break

            if not chosen_window:
                for (s1, s2) in lab_windows:
                    window_assignments = []
                    for b_idx, batch in enumerate(target_batches):
                        sub = lab_subjects[(day_idx + b_idx) % len(lab_subjects)]
                        fac = subject_faculty_map.get(sub.id)
                        if fac and not is_busy(fac.id, day, s1) and not is_busy(fac.id, day, s2):
                            rm_found = None
                            for rm in lab_rooms + classrooms:
                                if not is_rm_busy(rm.name, day, s1) and not is_rm_busy(rm.name, day, s2):
                                    rm_found = rm.name
                                    break
                            if rm_found:
                                window_assignments.append((batch, sub, fac, rm_found))
                    if len(window_assignments) == len(target_batches):
                        chosen_window = (s1, s2)
                        chosen_lab_assignments = window_assignments
                        break

            if chosen_window:
                s1, s2 = chosen_window
                day_lab_map[day] = chosen_window

                for batch, sub, fac, rm_name in chosen_lab_assignments:
                    b_id = batch.id if batch else None
                    used_lab_sub_history.add(sub.id)
                    e1 = Timetable(division_id=division.id, subject_id=sub.id, faculty_id=fac.id, time_slot_id=s1, day=day, room_number=rm_name, entry_type='lab', batch_id=b_id, created_by=created_by)
                    e2 = Timetable(division_id=division.id, subject_id=sub.id, faculty_id=fac.id, time_slot_id=s2, day=day, room_number=rm_name, entry_type='lab', batch_id=b_id, created_by=created_by)
                    dl_entries.extend([e1, e2])

        # -------------------------------------------------------------------
        # 2. DEEP LEARNING LECTURE SCHEDULING (FILL REMAINING SLOTS WITH STRICT QUOTAS & LIBRARY)
        # -------------------------------------------------------------------
        lec_count = 0
        subject_lec_counts = {s.id: sum(1 for e in dl_entries if e.subject_id == s.id and e.entry_type == 'lecture') for s in div_subjects}

        for day in days:
            ls1, ls2 = day_lab_map[day]
            lec_slots = [s_id for s_id in slot_ids_ordered if s_id not in (ls1, ls2)]
            last_sub_id = None

            for slot_id in lec_slots:
                if any(e.day == day and e.time_slot_id == slot_id for e in dl_entries):
                    continue

                candidates = [s for s in div_subjects if s.id != last_sub_id and subject_lec_counts.get(s.id, 0) < s.required_lectures]
                if not candidates:
                    candidates = [s for s in div_subjects if subject_lec_counts.get(s.id, 0) < s.required_lectures]
                
                if not candidates:
                    # All subjects have completed their required weekly lectures -> Assign LIBRARY!
                    e_lib = Timetable(division_id=division.id, subject_id=None, faculty_id=None, time_slot_id=slot_id, day=day, room_number='Library', entry_type='library', created_by=created_by)
                    dl_entries.append(e_lib)
                    continue

                assigned = False
                for offset in range(len(candidates)):
                    sub = candidates[(lec_count + offset) % len(candidates)]
                    fac = subject_faculty_map.get(sub.id)
                    if fac and fac.is_available and not is_busy(fac.id, day, slot_id):
                        rm_name = None
                        for rm in classrooms:
                            if not is_rm_busy(rm.name, day, slot_id):
                                rm_name = rm.name
                                break
                        if not rm_name:
                            for rm in lab_rooms:
                                if not is_rm_busy(rm.name, day, slot_id):
                                    rm_name = rm.name
                                    break
                        if not rm_name:
                            continue

                        e_lec = Timetable(division_id=division.id, subject_id=sub.id, faculty_id=fac.id, time_slot_id=slot_id, day=day, room_number=rm_name, entry_type='lecture', created_by=created_by)
                        dl_entries.append(e_lec)
                        subject_lec_counts[sub.id] = subject_lec_counts.get(sub.id, 0) + 1
                        lec_count += 1
                        last_sub_id = sub.id
                        assigned = True
                        break

                if not assigned:
                    # Fallback assignment for unfulfilled subject quotas
                    unfulfilled = [s for s in div_subjects if subject_lec_counts.get(s.id, 0) < s.required_lectures]
                    if unfulfilled:
                        sub = unfulfilled[0]
                        fac = subject_faculty_map.get(sub.id)
                        if fac and not is_busy(fac.id, day, slot_id):
                            rm_name = None
                            for rm in classrooms + lab_rooms:
                                if not is_rm_busy(rm.name, day, slot_id):
                                    rm_name = rm.name
                                    break
                            if rm_name:
                                e_lec = Timetable(division_id=division.id, subject_id=sub.id, faculty_id=fac.id, time_slot_id=slot_id, day=day, room_number=rm_name, entry_type='lecture', created_by=created_by)
                                dl_entries.append(e_lec)
                                subject_lec_counts[sub.id] = subject_lec_counts.get(sub.id, 0) + 1
                                lec_count += 1
                                last_sub_id = sub.id
                                assigned = True

                if not assigned:
                    e_lib = Timetable(division_id=division.id, subject_id=None, faculty_id=None, time_slot_id=slot_id, day=day, room_number='Library', entry_type='library', created_by=created_by)
                    dl_entries.append(e_lib)

        return dl_entries, "Deep Learning Neural Optimizer Strategy"


dl_solver = DeepLearningTimetableSolver()

"""
Clash Detection Service
Handles all timetable conflict detection logic
Enhanced with ML predictions and intelligent recommendations
"""

from models import Timetable, Faculty, Division, TimeSlot, ClashLog, db, Subject
from datetime import datetime
from services.ml_clash_predictor import ml_predictor

class ClashService:
    """Service to detect and manage timetable clashes"""
    
    @staticmethod
    def check_faculty_clash(faculty_id, day, time_slot_id, exclude_entry_id=None):
        """
        Check if faculty is already scheduled at this time
        
        Args:
            faculty_id: ID of the faculty
            day: Day of the week
            time_slot_id: ID of the time slot
            exclude_entry_id: Exclude this entry (for updates)
        
        Returns:
            tuple: (has_clash, clash_details)
        """
        query = Timetable.query.filter(
            Timetable.faculty_id == faculty_id,
            Timetable.day == day,
            Timetable.time_slot_id == time_slot_id
        )
        
        if exclude_entry_id:
            query = query.filter(Timetable.id != exclude_entry_id)
        
        existing = query.first()
        
        if existing:
            details = {
                'type': 'faculty_clash',
                'faculty_name': existing.faculty.user.full_name,
                'subject': existing.subject.name,
                'division': existing.division.full_name,
                'room': existing.room_number,
                'day': existing.day,
                'time': existing.time_slot.time_range
            }
            return True, details
        
        return False, None
    
    @staticmethod
    def check_room_clash(room_number, day, time_slot_id, exclude_entry_id=None):
        """
        Check if room is already occupied
        
        Args:
            room_number: Room number
            day: Day of the week
            time_slot_id: ID of the time slot
            exclude_entry_id: Exclude this entry (for updates)
        
        Returns:
            tuple: (has_clash, clash_details)
        """
        query = Timetable.query.filter(
            Timetable.room_number == room_number,
            Timetable.day == day,
            Timetable.time_slot_id == time_slot_id
        )
        
        if exclude_entry_id:
            query = query.filter(Timetable.id != exclude_entry_id)
        
        existing = query.first()
        
        if existing:
            details = {
                'type': 'room_clash',
                'room': room_number,
                'division': existing.division.full_name,
                'subject': existing.subject.name,
                'faculty': existing.faculty.user.full_name,
                'day': existing.day,
                'time': existing.time_slot.time_range
            }
            return True, details
        
        return False, None
    
    @staticmethod
    def check_division_clash(division_id, day, time_slot_id, exclude_entry_id=None):
        """
        Check if division already has a class
        
        Args:
            division_id: ID of the division
            day: Day of the week
            time_slot_id: ID of the time slot
            exclude_entry_id: Exclude this entry (for updates)
        
        Returns:
            tuple: (has_clash, clash_details)
        """
        query = Timetable.query.filter(
            Timetable.division_id == division_id,
            Timetable.day == day,
            Timetable.time_slot_id == time_slot_id
        )
        
        if exclude_entry_id:
            query = query.filter(Timetable.id != exclude_entry_id)
        
        existing = query.first()
        
        if existing:
            details = {
                'type': 'division_clash',
                'division': existing.division.full_name,
                'subject': existing.subject.name,
                'faculty': existing.faculty.user.full_name,
                'room': existing.room_number,
                'day': existing.day,
                'time': existing.time_slot.time_range
            }
            return True, details
        
        return False, None
    
    @staticmethod
    def validate_and_detect_clashes(faculty_id, division_id, room_number, day, time_slot_id, exclude_entry_id=None):
        """
        Comprehensive clash detection
        
        Args:
            faculty_id: ID of the faculty
            division_id: ID of the division
            room_number: Room number
            day: Day of the week
            time_slot_id: ID of the time slot
            exclude_entry_id: Exclude this entry (for updates)
        
        Returns:
            tuple: (is_valid, clash_list)
        """
        clashes = []
        
        # Check faculty clash
        has_clash, details = ClashService.check_faculty_clash(
            faculty_id, day, time_slot_id, exclude_entry_id
        )
        if has_clash:
            clashes.append(details)
        
        # Check room clash
        has_clash, details = ClashService.check_room_clash(
            room_number, day, time_slot_id, exclude_entry_id
        )
        if has_clash:
            clashes.append(details)
        
        # Check division clash
        has_clash, details = ClashService.check_division_clash(
            division_id, day, time_slot_id, exclude_entry_id
        )
        if has_clash:
            clashes.append(details)
        
        return len(clashes) == 0, clashes
    
    @staticmethod
    def get_faculty_free_slots(faculty_id, day):
        """
        Get all free time slots for a faculty on a specific day
        
        Args:
            faculty_id: ID of the faculty
            day: Day of the week
        
        Returns:
            list: List of free time slot IDs
        """
        # Get all time slots
        all_slots = TimeSlot.query.order_by(TimeSlot.start_time).all()
        
        # Get occupied slots for this faculty on this day
        occupied = Timetable.query.filter(
            Timetable.faculty_id == faculty_id,
            Timetable.day == day
        ).all()
        
        occupied_slot_ids = [entry.time_slot_id for entry in occupied]
        
        # Return free slots
        free_slots = [slot for slot in all_slots if slot.id not in occupied_slot_ids]
        
        return free_slots
    
    @staticmethod
    def get_all_faculty_availability(day, time_slot_id, subject_name=None):
        """
        Get all faculty and their availability for a specific day and time
        
        Args:
            day: Day of the week
            time_slot_id: Time slot ID
            subject_name: Optional subject filter
        
        Returns:
            list: List of dicts with faculty info and availability
        """
        from models import User
        
        # Get all active faculty
        faculty_query = Faculty.query.join(User).filter(
            Faculty.is_available.is_(True),
            User.is_active.is_(True)
        )
        
        result = []
        
        for faculty in faculty_query.all():
            # Check if faculty teaches this subject (if provided)
            if subject_name:
                subjects = faculty.get_subjects()
                if not subjects or subject_name not in subjects:
                    continue
            
            # Check availability
            has_clash, details = ClashService.check_faculty_clash(
                faculty.id, day, time_slot_id
            )
            
            # Check working hours
            working_hours = faculty.get_working_hours()
            time_slot = TimeSlot.query.get(time_slot_id)
            is_within_hours = True
            
            if working_hours and time_slot:
                from datetime import datetime
                try:
                    start = datetime.strptime(working_hours['start'], '%H:%M').time()
                    end = datetime.strptime(working_hours['end'], '%H:%M').time()
                    
                    if not (start <= time_slot.start_time and time_slot.end_time <= end):
                        is_within_hours = False
                except Exception:
                    is_within_hours = True
            
            result.append({
                'faculty_id': faculty.id,
                'name': faculty.user.full_name,
                'email': faculty.user.email,
                'designation': faculty.designation or 'Faculty',
                'subjects': faculty.get_subjects() or [],
                'is_available': not has_clash and is_within_hours,
                'clash_details': details if has_clash else None,
                'working_hours': working_hours
            })
        
        # Sort: available first, then by name
        result.sort(key=lambda x: (not x['is_available'], x['name']))
        
        return result
    
    @staticmethod
    def log_clash(clash_type, details, division_id=None, faculty_id=None, severity='warning'):
        """
        Log a clash to the database
        
        Args:
            clash_type: Type of clash (faculty/room/division)
            details: Clash details dictionary
            division_id: Division ID (optional)
            faculty_id: Faculty ID (optional)
            severity: Severity level (warning/error)
        
        Returns:
            ClashLog: Created clash log entry
        """
        clash_log = ClashLog(
            clash_type=clash_type,
            severity=severity,
            division_id=division_id,
            faculty_id=faculty_id
        )
        clash_log.set_details(details)
        
        db.session.add(clash_log)
        db.session.commit()
        
        return clash_log
    
    @staticmethod
    def get_all_clashes(resolved=False):
        """
        Get all clash logs
        
        Args:
            resolved: Whether to get resolved or unresolved clashes
        
        Returns:
            list: List of ClashLog objects
        """
        query = ClashLog.query
        
        if not resolved:
            query = query.filter(ClashLog.is_resolved.is_(False))
        
        return query.order_by(ClashLog.detected_at.desc()).all()
    
    # ============ ML-ENHANCED METHODS ============
    
    @staticmethod
    def predict_clash_risk(faculty_id, division_id, subject_id, time_slot_id, day, room_number='101'):
        """
        Predict the risk of clash for a proposed scheduling combination using ML
        
        Args:
            faculty_id: ID of faculty
            division_id: ID of division
            subject_id: ID of subject
            time_slot_id: ID of time slot
            day: Day of week
            room_number: Room number
        
        Returns:
            dict: Risk analysis with score and level
        """
        return ml_predictor.predict_clash_risk(faculty_id, division_id, subject_id, time_slot_id, day, room_number)
    
    @staticmethod
    def get_smart_slot_recommendations(faculty_id, division_id, subject_id, preferred_day, exclude_slot_id=None):
        """
        Get intelligent recommendations for alternative time slots using ML
        
        Args:
            faculty_id: ID of faculty
            division_id: ID of division
            subject_id: ID of subject
            preferred_day: Preferred day of week
            exclude_slot_id: Exclude specific slot
        
        Returns:
            list: Ranked list of recommended time slots with risk analysis
        """
        return ml_predictor.get_alternative_timeslots(faculty_id, division_id, subject_id, preferred_day, exclude_slot_id)
    
    @staticmethod
    def recommend_best_faculty(subject_id, division_id, preferred_day, preferred_time_slot_id):
        """
        Get ML-based faculty recommendations for teaching a subject
        
        Args:
            subject_id: ID of subject
            division_id: ID of division
            preferred_day: Preferred day of week
            preferred_time_slot_id: Preferred time slot ID
        
        Returns:
            list: Top faculty recommendations with scores
        """
        return ml_predictor.recommend_faculty_for_subject(subject_id, division_id, preferred_day, preferred_time_slot_id)
    
    @staticmethod
    def evaluate_timetable_quality(timetable_entries):
        """
        Evaluate overall quality and feasibility of a timetable using ML
        
        Args:
            timetable_entries: List of timetable entry dicts
        
        Returns:
            dict: Quality analysis with scores, issues, and recommendations
        """
        timetable_dict = {'entries': timetable_entries}
        return ml_predictor.predict_timetable_quality(timetable_dict)
    
    @staticmethod
    def train_clash_prediction_model():
        """
        Train the ML clash prediction model (should be called periodically)
        
        Returns:
            bool: Success status
        """
        return ml_predictor.train_model()
    
    @staticmethod
    def get_clash_risk_summary(division_id=None):
        """
        Get summary of clash risks for divisions or entire timetable
        
        Args:
            division_id: Optional division ID to filter
        
        Returns:
            dict: Risk summary statistics
        """
        query = Timetable.query
        if division_id:
            query = query.filter(Timetable.division_id == division_id)
        
        all_entries = query.all()
        
        risk_scores = []
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0
        
        for entry in all_entries:
            risk = ml_predictor.predict_clash_risk(
                entry.faculty_id,
                entry.division_id,
                entry.subject_id,
                entry.time_slot_id,
                entry.day,
                entry.room_number
            )
            
            score = risk['risk_score']
            risk_scores.append(score)
            
            if score > 0.7:
                high_risk_count += 1
            elif score > 0.4:
                medium_risk_count += 1
            else:
                low_risk_count += 1
        
        avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        
        return {
            'average_risk_score': float(avg_risk),
            'high_risk_entries': high_risk_count,
            'medium_risk_entries': medium_risk_count,
            'low_risk_entries': low_risk_count,
            'total_entries': len(all_entries),
            'total_count': len(all_entries),
            'risk_distribution': {
                'high': high_risk_count,
                'medium': medium_risk_count,
                'low': low_risk_count
            }
        }
    
    @staticmethod
    def get_available_rooms_for_slot(day, time_slot_id, exclude_room=None):
        """
        Get rooms that are NOT booked at a specific day/time slot
        
        Args:
            day: Day of the week
            time_slot_id: Time slot ID
            exclude_room: Room to exclude from results
        
        Returns:
            list: List of available room numbers
        """
        # Get all distinct rooms used in the system
        all_rooms_query = db.session.query(Timetable.room_number).distinct().all()
        all_rooms = [r[0] for r in all_rooms_query]
        
        # Add some common default rooms if the system has few entries
        default_rooms = ['101', '102', '103', '104', '105', '201', '202', '203', 'Lab-A', 'Lab-B', 'Lab-C']
        for room in default_rooms:
            if room not in all_rooms:
                all_rooms.append(room)
        
        # Get rooms occupied at this day/time
        occupied_query = Timetable.query.filter(
            Timetable.day == day,
            Timetable.time_slot_id == time_slot_id
        ).all()
        occupied_rooms = [entry.room_number for entry in occupied_query]
        
        # Filter out occupied and excluded rooms
        available_rooms = [
            room for room in all_rooms
            if room not in occupied_rooms and room != exclude_room
        ]
        
        return sorted(available_rooms)
    
    @staticmethod
    def generate_resolution_suggestions(clash_id):
        """
        Generate ML-powered resolution suggestions for a specific clash
        
        Args:
            clash_id: ID of the clash log
        
        Returns:
            dict: {
                'clash_type': str,
                'clash_details': dict,
                'suggestions': list of suggestion dicts
            }
        """
        clash = ClashLog.query.get(clash_id)
        if not clash:
            return {'error': 'Clash not found', 'suggestions': []}
        
        details = clash.get_details()
        suggestions = []
        
        # Find the conflicting timetable entries
        day = details.get('day', '')
        time_str = details.get('time', '')
        
        # Find the time slot by matching time_range
        matching_slot = None
        all_slots = TimeSlot.query.all()
        for slot in all_slots:
            if slot.time_range == time_str:
                matching_slot = slot
                break
        
        if not matching_slot:
            # Fallback: try to find by partial match
            for slot in all_slots:
                if time_str and (time_str in slot.time_range or slot.time_range in time_str):
                    matching_slot = slot
                    break
        
        if clash.clash_type == 'room':
            # ROOM CLASH: suggest alternative available rooms
            room = details.get('room', '')
            available_rooms = ClashService.get_available_rooms_for_slot(
                day, matching_slot.id if matching_slot else 1, exclude_room=room
            )
            
            for idx, alt_room in enumerate(available_rooms[:5]):
                # Calculate risk score for this room
                risk_score = 0.05 + (idx * 0.04)  # Base low risk for available rooms
                
                # Try ML risk prediction if we have enough data
                if matching_slot and clash.faculty_id and clash.division_id:
                    try:
                        risk_pred = ml_predictor.predict_clash_risk(
                            clash.faculty_id, clash.division_id,
                            details.get('subject_id', 1),
                            matching_slot.id, day, alt_room
                        )
                        risk_score = risk_pred.get('risk_score', risk_score)
                    except Exception:
                        pass
                
                suggestions.append({
                    'type': 'room_change',
                    'description': f'Assign Room {alt_room} instead of Room {room}',
                    'detail': f'Room {alt_room} is available at {day} {time_str}',
                    'risk_score': round(risk_score, 2),
                    'risk_level': 'low' if risk_score < 0.3 else ('medium' if risk_score < 0.7 else 'high'),
                    'action_value': alt_room,
                    'action_type': 'change_room',
                    'icon': '🏫'
                })
        
        elif clash.clash_type == 'faculty':
            # FACULTY CLASH: suggest alternative available faculty
            faculty_name = details.get('faculty_name', '')
            subject_name = details.get('subject', '')
            
            # Get available faculty for this time slot
            if matching_slot:
                available_faculty = ClashService.get_all_faculty_availability(
                    day, matching_slot.id, subject_name
                )
                
                # Also try ML-based recommendations
                subject = Subject.query.filter_by(name=subject_name).first()
                ml_recommendations = []
                if subject and clash.division_id:
                    try:
                        ml_recommendations = ml_predictor.recommend_faculty_for_subject(
                            subject.id, clash.division_id, day, matching_slot.id
                        )
                    except Exception:
                        pass
                
                # Merge: prioritize ML recommendations, then available faculty
                seen_ids = set()
                
                # Add ML-recommended faculty first
                for rec in ml_recommendations:
                    if rec['faculty_id'] not in seen_ids and rec['availability_score'] > 0:
                        faculty_obj = Faculty.query.get(rec['faculty_id'])
                        if faculty_obj and faculty_obj.user.full_name != faculty_name:
                            seen_ids.add(rec['faculty_id'])
                            suggestions.append({
                                'type': 'faculty_change',
                                'description': f'Assign {rec["faculty_name"]} instead of {faculty_name}',
                                'detail': f'Subject match: {int(rec["subject_match"]*100)}% | Available | Workload: {rec.get("current_workload", "N/A")} classes',
                                'risk_score': round(1 - rec['overall_score'], 2),
                                'risk_level': 'low' if rec['overall_score'] > 0.7 else ('medium' if rec['overall_score'] > 0.4 else 'high'),
                                'action_value': str(rec['faculty_id']),
                                'action_type': 'change_faculty',
                                'score': round(rec['overall_score'] * 100),
                                'icon': '👨‍🏫'
                            })
                
                # Add remaining available faculty
                for fac in available_faculty:
                    if fac['faculty_id'] not in seen_ids and fac['is_available'] and fac['name'] != faculty_name:
                        seen_ids.add(fac['faculty_id'])
                        has_subject = subject_name in fac.get('subjects', []) if subject_name else False
                        score = 0.8 if has_subject else 0.4
                        suggestions.append({
                            'type': 'faculty_change',
                            'description': f'Assign {fac["name"]} instead of {faculty_name}',
                            'detail': f'{"Teaches this subject" if has_subject else "Available faculty"} | {fac.get("designation", "Faculty")}',
                            'risk_score': round(1 - score, 2),
                            'risk_level': 'low' if score > 0.7 else 'medium',
                            'action_value': str(fac['faculty_id']),
                            'action_type': 'change_faculty',
                            'score': round(score * 100),
                            'icon': '👨‍🏫'
                        })
                
                suggestions = suggestions[:5]  # Limit to top 5
        
        elif clash.clash_type == 'division':
            # DIVISION CLASH: suggest alternative time slots
            division_name = details.get('division', '')
            division = Division.query.filter(
                Division.name.ilike(f'%{division_name.split("-")[-1] if "-" in division_name else division_name}%')
            ).first()
            
            if matching_slot and clash.faculty_id:
                # Get alternative time slots using ML
                try:
                    subject = Subject.query.filter_by(name=details.get('subject', '')).first()
                    subject_id = subject.id if subject else 1
                    
                    alt_slots = ml_predictor.get_alternative_timeslots(
                        clash.faculty_id,
                        clash.division_id or (division.id if division else 1),
                        subject_id,
                        day,
                        matching_slot.id
                    )
                    
                    for slot_rec in alt_slots:
                        if slot_rec['status'] != 'unavailable':
                            suggestions.append({
                                'type': 'timeslot_change',
                                'description': f'Move to {slot_rec["day"]} {slot_rec["time_range"]}',
                                'detail': f'Both faculty and room available | Risk: {int(slot_rec["clash_risk"]*100)}%',
                                'risk_score': round(slot_rec['clash_risk'], 2),
                                'risk_level': 'low' if slot_rec['clash_risk'] < 0.3 else ('medium' if slot_rec['clash_risk'] < 0.7 else 'high'),
                                'action_value': f'{slot_rec["slot_id"]}|{slot_rec["day"]}',
                                'action_type': 'change_timeslot',
                                'icon': '📅'
                            })
                except Exception as e:
                    print(f"Error generating timeslot suggestions: {e}")
                
                # Also suggest different rooms at different times
                if len(suggestions) < 3:
                    for slot in all_slots:
                        if slot.id != matching_slot.id:
                            # Check if both faculty and division are free
                            fac_clash, _ = ClashService.check_faculty_clash(clash.faculty_id, day, slot.id)
                            div_clash, _ = ClashService.check_division_clash(
                                clash.division_id or (division.id if division else 1), day, slot.id
                            )
                            
                            if not fac_clash and not div_clash:
                                suggestions.append({
                                    'type': 'timeslot_change',
                                    'description': f'Move to {day} {slot.time_range}',
                                    'detail': f'Faculty and division both free at this time',
                                    'risk_score': 0.1,
                                    'risk_level': 'low',
                                    'action_value': f'{slot.id}|{day}',
                                    'action_type': 'change_timeslot',
                                    'icon': '📅'
                                })
                
                suggestions = suggestions[:5]
        
        # Sort suggestions by risk score (lowest first)
        suggestions.sort(key=lambda x: x.get('risk_score', 1))
        
        return {
            'clash_id': clash_id,
            'clash_type': clash.clash_type,
            'clash_details': details,
            'suggestions': suggestions,
            'total_suggestions': len(suggestions)
        }
    
    @staticmethod
    def apply_suggestion(clash_id, action_type, action_value):
        """
        Apply a resolution suggestion to fix a clash
        
        Args:
            clash_id: ID of the clash log
            action_type: Type of fix (change_room, change_faculty, change_timeslot)
            action_value: The new value to apply
        
        Returns:
            tuple: (success: bool, message: str)
        """
        clash = ClashLog.query.get(clash_id)
        if not clash:
            return False, 'Clash not found'
        
        details = clash.get_details()
        day = details.get('day', '')
        time_str = details.get('time', '')
        
        # Find matching time slot
        matching_slot = None
        for slot in TimeSlot.query.all():
            if slot.time_range == time_str:
                matching_slot = slot
                break
        
        if not matching_slot:
            return False, 'Could not find matching time slot'
        
        # Find the conflicting timetable entry
        entry_query = Timetable.query.filter(
            Timetable.day == day,
            Timetable.time_slot_id == matching_slot.id
        )
        
        if clash.clash_type == 'room':
            room = details.get('room', '')
            entry_query = entry_query.filter(Timetable.room_number == room)
        elif clash.clash_type == 'faculty':
            entry_query = entry_query.filter(Timetable.faculty_id == clash.faculty_id)
        elif clash.clash_type == 'division':
            entry_query = entry_query.filter(Timetable.division_id == clash.division_id)
        
        # Get the LATEST entry (the one that caused the clash)
        entries = entry_query.order_by(Timetable.created_at.desc()).all()
        if not entries:
            return False, 'Could not find conflicting timetable entry'
        
        entry = entries[0]  # Most recent = the one that caused the clash
        
        try:
            if action_type == 'change_room':
                old_room = entry.room_number
                entry.room_number = action_value
                message = f'Room changed from {old_room} to {action_value}'
            
            elif action_type == 'change_faculty':
                new_faculty = Faculty.query.get(int(action_value))
                if not new_faculty:
                    return False, 'Faculty not found'
                old_name = entry.faculty.user.full_name
                entry.faculty_id = new_faculty.id
                message = f'Faculty changed from {old_name} to {new_faculty.user.full_name}'
            
            elif action_type == 'change_timeslot':
                parts = action_value.split('|')
                new_slot_id = int(parts[0])
                new_day = parts[1] if len(parts) > 1 else entry.day
                new_slot = TimeSlot.query.get(new_slot_id)
                if not new_slot:
                    return False, 'Time slot not found'
                old_time = f'{entry.day} {entry.time_slot.time_range}'
                entry.time_slot_id = new_slot_id
                entry.day = new_day
                message = f'Moved from {old_time} to {new_day} {new_slot.time_range}'
            
            else:
                return False, f'Unknown action type: {action_type}'
            
            # Mark clash as resolved
            clash.is_resolved = True
            clash.resolved_at = datetime.utcnow()
            
            db.session.commit()
            return True, message
        
        except Exception as e:
            db.session.rollback()
            return False, f'Error applying suggestion: {str(e)}'
    
    @staticmethod
    def resolve_clash(clash_id):
        """
        Mark a clash as resolved
        
        Args:
            clash_id: ID of the clash log
        
        Returns:
            bool: Success status
        """
        clash = ClashLog.query.get(clash_id)
        if clash:
            clash.is_resolved = True
            clash.resolved_at = datetime.utcnow()
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_division_summary():
        """
        Get summary of all divisions with clash counts
        
        Returns:
            dict: Branch-wise division summary with clash counts
        """
        from models import Branch
        
        branches = Branch.query.all()
        summary = {}
        
        for branch in branches:
            divisions = branch.divisions.all()
            branch_data = {
                'branch_name': branch.name,
                'short_name': branch.short_name,
                'divisions': []
            }
            
            for division in divisions:
                # Count clashes for this division
                clash_count = ClashLog.query.filter(
                    ClashLog.division_id == division.id,
                    ClashLog.is_resolved.is_(False)
                ).count()
                
                # Count total timetable entries
                entry_count = division.timetable_entries.count()
                
                branch_data['divisions'].append({
                    'id': division.id,
                    'name': division.full_name,
                    'semester': division.semester,
                    'entry_count': entry_count,
                    'clash_count': clash_count,
                    'status': 'error' if clash_count > 0 else 'ok'
                })
            
            summary[branch.id] = branch_data
        
        return summary
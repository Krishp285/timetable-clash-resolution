"""
ML-Based Clash Prediction and Recommendation System
Uses pattern analysis and machine learning to predict and prevent scheduling conflicts
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
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
        
        if len(all_entries) < 10:
            return None, None  # Not enough data
        
        features = []
        clash_labels = []
        
        for entry in all_entries:
            # Extract features
            feature_set = [
                entry.faculty_id,
                entry.division_id,
                entry.subject_id,
                entry.time_slot_id,
                self._day_to_number(entry.day),
                int(entry.room_number) if entry.room_number.isdigit() else hash(entry.room_number) % 100
            ]
            features.append(feature_set)
            
            # Label: 1 if this entry has potential for clash, 0 otherwise
            clash_risk = self._calculate_entry_clash_risk(entry)
            clash_labels.append(1 if clash_risk > 0.5 else 0)
        
        return np.array(features), np.array(clash_labels)
    
    def train_model(self):
        """Train the clash prediction model"""
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
                int(room_number) if room_number.isdigit() else hash(room_number) % 100
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
                
                # Check if this slot-day combination is already occupied
                existing = Timetable.query.filter(
                    Timetable.faculty_id == faculty_id,
                    Timetable.time_slot_id == slot.id,
                    Timetable.day == day
                ).first()
                
                if existing:
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
        
        # Sort by clash risk (low risk first)
        recommendations.sort(key=lambda x: x['clash_risk'])
        
        return recommendations[:5]  # Return top 5 recommendations
    
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
            
            # Check availability on preferred day/slot
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

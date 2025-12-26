"""
Clash Detection Service
Handles all timetable conflict detection logic
"""

from models import Timetable, Faculty, Division, TimeSlot, ClashLog, db, Subject
from datetime import datetime
from sqlalchemy import and_, or_

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
            Faculty.is_available == True,
            User.is_active == True
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
                except:
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
            query = query.filter(ClashLog.is_resolved == False)
        
        return query.order_by(ClashLog.detected_at.desc()).all()
    
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
                    ClashLog.is_resolved == False
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
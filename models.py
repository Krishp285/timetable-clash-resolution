from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
from flask_login import UserMixin

class User(UserMixin,db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'faculty'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    faculty_profile = db.relationship('Faculty', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username} - {self.role}>'


class Faculty(db.Model):
    """Faculty profile with subjects and availability"""
    __tablename__ = 'faculty'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone = db.Column(db.String(15))
    department = db.Column(db.String(100))
    designation = db.Column(db.String(100))  # Professor, Assistant Professor, etc.
    
    # Working hours stored as JSON: {"start": "09:00", "end": "17:00"}
    working_hours = db.Column(db.Text)
    
    # Subjects faculty can teach (stored as JSON array)
    # Format: ["Data Structures", "Algorithms", "DBMS"]
    subjects_can_teach = db.Column(db.Text)
    
    # Visiting faculty fields
    is_visiting = db.Column(db.Boolean, default=False)
    # Days visiting faculty is available: ["Monday", "Tuesday"]
    visiting_available_days = db.Column(db.Text)
    # Time slot IDs visiting faculty is available for (JSON list of ints): [1, 3]
    visiting_slot_ids = db.Column(db.Text)
    
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    timetable_entries = db.relationship('Timetable', backref='faculty', lazy='dynamic')
    
    def set_subjects(self, subjects_list):
        """Set subjects as JSON"""
        self.subjects_can_teach = json.dumps(subjects_list)
    
    def get_subjects(self):
        """Get subjects as list"""
        if self.subjects_can_teach:
            return json.loads(self.subjects_can_teach)
        return []
    
    def set_working_hours(self, start_time, end_time):
        """Set working hours"""
        self.working_hours = json.dumps({
            'start': start_time,
            'end': end_time
        })
    
    def get_working_hours(self):
        """Get working hours"""
        if self.working_hours:
            return json.loads(self.working_hours)
        return None
    
    def set_visiting_days(self, days_list):
        """Set visiting available days as JSON"""
        self.visiting_available_days = json.dumps(days_list)
    
    def get_visiting_days(self):
        """Get visiting available days as list"""
        if self.visiting_available_days:
            return json.loads(self.visiting_available_days)
        return []
    
    def set_visiting_slots(self, slot_data):
        """Set visiting slot IDs as JSON (supports list of ints or dict of day -> slot_ids)"""
        if isinstance(slot_data, dict):
            # Clean dictionary: {"Monday": [1, 2], ...}
            clean_dict = {}
            for day, slots in slot_data.items():
                clean_dict[day] = [int(s) for s in slots if str(s).isdigit()]
            self.visiting_slot_ids = json.dumps(clean_dict)
        elif isinstance(slot_data, list):
            self.visiting_slot_ids = json.dumps([int(s) for s in slot_data if str(s).isdigit()])

    def get_visiting_schedule(self):
        """Get visiting schedule as dict: {"Monday": [1, 2], ...}"""
        if self.visiting_slot_ids:
            try:
                data = json.loads(self.visiting_slot_ids)
                if isinstance(data, dict):
                    return {k: [int(x) for x in v if str(x).isdigit()] for k, v in data.items()}
                elif isinstance(data, list):
                    # Legacy fallback: apply global list to all visiting_days
                    days = self.get_visiting_days()
                    slots = [int(x) for x in data if str(x).isdigit()]
                    return {day: slots for day in days}
            except Exception:
                pass
        return {}

    def get_visiting_slots(self, day=None):
        """Get visiting slot IDs as list of ints for a given day (or all unique slots if day is None)"""
        schedule = self.get_visiting_schedule()
        if day:
            return schedule.get(day, [])
        all_slots = set()
        for slots in schedule.values():
            all_slots.update(slots)
        return list(all_slots)

    def is_available_for_slot(self, day, time_slot):
        """Check if this faculty is available for a given day and time slot."""
        if self.is_visiting:
            visiting_days = self.get_visiting_days()
            if day not in visiting_days:
                return False
            day_slots = self.get_visiting_slots(day)
            return time_slot.id in day_slots
        else:
            # Regular faculty: check working hours
            working_hours = self.get_working_hours()
            if not working_hours:
                return True  # No hours set = always available
            
            def parse_time_str(t_str, is_end=False):
                if not t_str:
                    return None
                t_str = str(t_str).strip().upper()
                from datetime import datetime as dt, time
                
                has_ampm = 'AM' in t_str or 'PM' in t_str
                parsed_time = None
                
                for fmt in ('%I:%M %p', '%I:%M%p', '%H:%M:%S', '%H:%M'):
                    try:
                        parsed_time = dt.strptime(t_str, fmt).time()
                        break
                    except ValueError:
                        continue
                
                if parsed_time:
                    h = parsed_time.hour
                    m = parsed_time.minute
                    if not has_ampm:
                        if h < 12:
                            if is_end or h < 7:
                                h += 12
                    return time(h, m)
                return None

            try:
                start = parse_time_str(working_hours.get('start'))
                end = parse_time_str(working_hours.get('end'), is_end=True)
                if not start or not end:
                    return True
                return start <= time_slot.start_time and time_slot.end_time <= end
            except Exception:
                return True
    
    def __repr__(self):
        return f'<Faculty {self.user.full_name}>'


class Branch(db.Model):
    """Academic branches created by admin"""
    __tablename__ = 'branches'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)  # e.g., "Computer Engineering"
    short_name = db.Column(db.String(10), unique=True, nullable=False)  # e.g., "CSE"
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    divisions = db.relationship('Division', backref='branch', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Branch {self.short_name}>'


class Division(db.Model):
    """Divisions/Sections within branches"""
    __tablename__ = 'divisions'
    
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)  # e.g., "A", "B", "C"
    semester = db.Column(db.Integer, nullable=False)  # 1-8
    academic_year = db.Column(db.String(20))  # e.g., "2024-2025"
    student_count = db.Column(db.Integer, default=60)
    num_batches = db.Column(db.Integer, default=1)  # 1 = no batches (regular)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('branch_id', 'name', 'semester', 'academic_year'),)
    
    # Relationships
    timetable_entries = db.relationship('Timetable', backref='division', lazy='dynamic', cascade='all, delete-orphan')
    batches = db.relationship('Batch', backref='division', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.branch.short_name}-{self.name}"
    
    def __repr__(self):
        return f'<Division {self.full_name}>'


class Batch(db.Model):
    """Lab batches within a division (e.g., D1, D2, D3 of CSE-A)"""
    __tablename__ = 'batches'
    
    id = db.Column(db.Integer, primary_key=True)
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)  # e.g., "D1", "D2", "D3"
    student_count = db.Column(db.Integer, default=20)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique per division
    __table_args__ = (db.UniqueConstraint('division_id', 'name'),)
    
    # Relationships
    timetable_entries = db.relationship('Timetable', backref='batch', lazy='dynamic')
    
    @property
    def full_label(self):
        return f"{self.division.full_name}-{self.name}"
    
    def __repr__(self):
        return f'<Batch {self.full_label}>'


class TimeSlot(db.Model):
    """Time slots created by admin"""
    __tablename__ = 'time_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    slot_label = db.Column(db.String(50))  # e.g., "Morning Slot 1"
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def time_range(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
    
    def __repr__(self):
        return f'<TimeSlot {self.time_range}>'


class Subject(db.Model):
    """Subjects in the system"""
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, default=3)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Subject {self.code} - {self.name}>'


class Room(db.Model):
    """Rooms/Resources created by admin"""
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # e.g., "101", "Lab-A"
    capacity = db.Column(db.Integer, default=60)
    room_type = db.Column(db.String(50), default='Classroom')      # Classroom, Lab, Seminar Hall
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Room {self.name}>'


class Timetable(db.Model):
    """Timetable entries - the core model"""
    __tablename__ = 'timetable'
    
    id = db.Column(db.Integer, primary_key=True)
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)  # Nullable for library/break
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=True)   # Nullable for library/break
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.id'), nullable=True)  # NULL = full-division
    
    day = db.Column(db.String(20), nullable=False)  # Monday-Saturday
    room_number = db.Column(db.String(50), nullable=True)  # Nullable for library/break
    entry_type = db.Column(db.String(20), default='lecture')  # 'lecture', 'lab', 'library', 'break'
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subject = db.relationship('Subject')
    time_slot = db.relationship('TimeSlot')
    
    @property
    def is_special(self):
        """Returns True for library/break entries that have no faculty/subject."""
        return self.entry_type in ('library', 'break')
    
    @property
    def display_label(self):
        """Human-readable label for the entry."""
        if self.entry_type == 'library':
            return 'LIBRARY'
        elif self.entry_type == 'break':
            return 'BREAK'
        elif self.subject:
            label = self.subject.name
            if self.batch:
                label = f"{self.batch.name}: {label}"
            return label
        return '—'
    
    def __repr__(self):
        return f'<Timetable {self.division.full_name} - {self.day}>'


class ClashLog(db.Model):
    """Log of clashes detected in the system"""
    __tablename__ = 'clash_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    clash_type = db.Column(db.String(50), nullable=False)  # faculty, room, division
    severity = db.Column(db.String(20), default='warning')  # warning, error
    
    # Details stored as JSON
    clash_details = db.Column(db.Text)
    
    # References
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    
    is_resolved = db.Column(db.Boolean, default=False)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    # Resolution tracking
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    resolution_method = db.Column(db.String(20))  # 'manual' or 'auto'
    resolution_note = db.Column(db.Text)
    
    def set_details(self, details_dict):
        self.clash_details = json.dumps(details_dict)
    
    def get_details(self):
        if self.clash_details:
            return json.loads(self.clash_details)
        return {}
    
    def get_duration(self):
        """Return formatted duration between detection and resolution."""
        if self.detected_at and self.resolved_at:
            delta = self.resolved_at - self.detected_at
            total_minutes = int(delta.total_seconds() / 60)
            if total_minutes < 60:
                return f"{total_minutes}m"
            return f"{total_minutes // 60}h {total_minutes % 60}m"
        return None
    
    def __repr__(self):
        return f'<ClashLog {self.clash_type} - {self.severity}>'
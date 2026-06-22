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
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('branch_id', 'name', 'semester', 'academic_year'),)
    
    # Relationships
    timetable_entries = db.relationship('Timetable', backref='division', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.branch.short_name}-{self.name}"
    
    def __repr__(self):
        return f'<Division {self.full_name}>'


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


class Timetable(db.Model):
    """Timetable entries - the core model"""
    __tablename__ = 'timetable'
    
    id = db.Column(db.Integer, primary_key=True)
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id'), nullable=False)
    
    day = db.Column(db.String(20), nullable=False)  # Monday-Saturday
    room_number = db.Column(db.String(50), nullable=False)
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subject = db.relationship('Subject')
    time_slot = db.relationship('TimeSlot')
    
    def __repr__(self):
        return f'<Timetable {self.division.full_name} - {self.day}>'


class ClashLog(db.Model):
    """Log of clashes detected in the system"""
    __tablename__ = 'clash_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    clash_type = db.Column(db.String(20), nullable=False)  # faculty, room, division
    severity = db.Column(db.String(20), default='warning')  # warning, error
    
    # Details stored as JSON
    clash_details = db.Column(db.Text)
    
    # References
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    
    is_resolved = db.Column(db.Boolean, default=False)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    def set_details(self, details_dict):
        self.clash_details = json.dumps(details_dict)
    
    def get_details(self):
        if self.clash_details:
            return json.loads(self.clash_details)
        return {}
    
    def __repr__(self):
        return f'<ClashLog {self.clash_type} - {self.severity}>'
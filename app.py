# ============================================
# 1️⃣ IMPORTS
# ============================================

import os
import csv
import io
import zipfile
from flask import Flask
from extensions import db
from models import ClashLog, User, Faculty, Branch, Division, Subject, TimeSlot, Timetable, Room, Batch, ActivityLog
from services.clash_service import ClashService
from services.auto_generator_service import AutoTimetableGenerator
from flask import render_template, request, redirect, url_for, flash, session, jsonify, make_response
from functools import wraps
from datetime import datetime, date
from flask_login import LoginManager, current_user, login_user, logout_user, login_required


# ============================================
# 2️⃣ APP CONFIGURATION
# ============================================


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Database URI: use DATABASE_URL env var (Render/Aiven), fallback to MySQL
database_url = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:root@localhost/timetable_system')
# Render PostgreSQL uses postgres:// but SQLAlchemy needs postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
# Aiven MySQL uses mysql:// but we need mysql+pymysql:// for PyMySQL driver
if database_url.startswith('mysql://'):
    database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)
# Strip ssl-mode param (PyMySQL doesn't support it as URL param)
needs_ssl = False
if 'ssl-mode' in database_url:
    needs_ssl = True
    import re
    database_url = re.sub(r'[?&]ssl-mode=[^&]*', '', database_url)
    database_url = database_url.replace('?&', '?').rstrip('?')

# Configure SSL options for primary DB if needed
engine_options = {}
if needs_ssl or 'aivencloud.com' in database_url:
    engine_options = {
        'connect_args': {
            'ssl': {'ssl_mode': 'REQUIRED'}
        }
    }

# Test connection to the primary database
from sqlalchemy import create_engine
try:
    test_engine_options = engine_options.copy()
    if 'connect_args' not in test_engine_options:
        test_engine_options['connect_args'] = {}
    
    # Set short connection timeout for testing connection
    if database_url.startswith('mysql'):
        test_engine_options['connect_args']['connect_timeout'] = 5
    elif database_url.startswith('postgresql'):
        test_engine_options['connect_args']['connect_timeout'] = 5
        
    engine = create_engine(database_url, **test_engine_options)
    with engine.connect() as conn:
        pass
    print("[OK] Successfully connected to the primary database.")
except Exception as db_err:
    print(f"[WARNING] Primary database connection failed: {db_err}")
    print("[INFO] Falling back to a local SQLite database for reliability.")
    database_url = 'sqlite:///timetable_system.db'
    engine_options = {}

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if engine_options:
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = engine_options
db.init_app(app)

# ============================================
# 3️⃣ LOGIN MANAGER + DECORATORS
# ============================================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'   # route name of login page


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Admin access required1", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def build_division_timetable_csv(division, entries):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    timeslots = TimeSlot.query.order_by(TimeSlot.start_time).all()

    cell_map = {slot.id: {day: [] for day in days} for slot in timeslots}
    for entry in entries:
        cell_map[entry.time_slot_id][entry.day].append(entry)

    output = io.StringIO()
    writer = csv.writer(output)

    branch_name = division.branch.name if division.branch else ""
    writer.writerow([f'{division.full_name} (Semester {division.semester}) Timetable - {branch_name}'])
    writer.writerow(['Time'] + days)

    for slot in timeslots:
        row = [slot.time_range]
        for day in days:
            day_entries = cell_map[slot.id][day]
            if day_entries:
                cell_texts = []
                for entry in day_entries:
                    if entry.entry_type == 'library':
                        cell_texts.append("LIBRARY")
                    elif entry.entry_type == 'break':
                        cell_texts.append("BREAK")
                    else:
                        sub = entry.subject.name if entry.subject else "—"
                        fac = entry.faculty.user.full_name if entry.faculty else "N/A"
                        room = f"Room {entry.room_number}" if entry.room_number else "N/A"
                        batch_str = f"[{entry.batch.name}] " if entry.batch else ""
                        cell_texts.append(f"{batch_str}{sub} | {fac} | {room}")
                row.append('\n'.join(cell_texts))
            else:
                row.append('')
        writer.writerow(row)

    return output.getvalue()


def build_timetable_zip_response(divisions, filename):
    output = io.BytesIO()

    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for division in divisions:
            entries = (
                Timetable.query
                .filter_by(division_id=division.id)
                .join(TimeSlot)
                .order_by(TimeSlot.start_time, Timetable.day)
                .all()
            )
            csv_content = build_division_timetable_csv(division, entries)
            safe_name = f"{division.full_name}_sem{division.semester}".lower().replace(' ', '_').replace('/', '_')
            archive.writestr(f'{safe_name}_timetable.csv', csv_content)

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.headers['Content-Type'] = 'application/zip'
    return response

# ============================================
# 4️⃣ AUTH ROUTES (LOGIN / SIGNUP / LOGOUT)
# ============================================

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('faculty_dashboard'))

    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form['username']
        ).first()

        if user and user.check_password(request.form['password']):
            login_user(user) 
            session['user_id'] = user.id
            session['name'] = user.full_name
            session['role'] = user.role
            flash('Login successful', 'success')

            # 🔥 ROLE BASED REDIRECT
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'faculty':
                return redirect(url_for('faculty_dashboard'))

        flash('Invalid credentials', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        role = request.form.get('role')

        user = User(
            username=request.form['username'],
            email=request.form['email'],
            full_name=request.form['full_name'],
            role=role
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()  # 🔴 MUST COMMIT FIRST (to get user.id)

        # ✅ CREATE FACULTY PROFILE AUTOMATICALLY
        if role == 'faculty':
            faculty = Faculty(
                user_id=user.id,
                department='',
                designation=''
            )
            db.session.add(faculty)
            db.session.commit()

        flash('Signup successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))


# ============================================
# 5️⃣ ADMIN DASHBOARD
# ============================================


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_branches = Branch.query.count()
    total_divisions = Division.query.count()
    total_faculty = Faculty.query.count()
    total_subjects = Subject.query.count()
    total_rooms = Room.query.count()

    # Recent clashes (optional)
    recent_clashes = ClashService.get_all_clashes(resolved=False)[:5]

    # Division summary (basic safe version)
    division_summary = {}

    for branch in Branch.query.all():
        division_summary[branch.id] = {
            "branch_name": branch.name,
            "divisions": []
        }

        for division in branch.divisions:
            division_summary[branch.id]["divisions"].append({
                "id": division.id,
                "name": division.full_name,
                "semester": division.semester,
                "entry_count": division.timetable_entries.count(),
                "clash_count": 0
            })

    return render_template(
        'admin_dashboard.html',
        total_branches=total_branches,
        total_divisions=total_divisions,
        total_faculty=total_faculty,
        total_subjects=total_subjects,
        total_rooms=total_rooms,
        recent_clashes=recent_clashes,
        division_summary=division_summary
    )


@app.route('/admin/timetable/export')
@admin_required
def export_admin_timetable():
    divisions = [
        division for division in Division.query.order_by(Division.branch_id, Division.name).all()
        if division.timetable_entries.count() > 0
    ]

    return build_timetable_zip_response(divisions, 'all_timetables.zip')


@app.route('/timetable/download/<int:division_id>')
@admin_required
def download_division_timetable(division_id):
    division = Division.query.get_or_404(division_id)
    entries = (
        Timetable.query
        .filter_by(division_id=division.id)
        .join(TimeSlot)
        .order_by(TimeSlot.start_time, Timetable.day)
        .all()
    )

    csv_content = build_division_timetable_csv(division, entries)
    safe_name = f"{division.full_name}_sem{division.semester}".lower().replace(' ', '_').replace('/', '_')
    response = make_response(csv_content)
    response.headers['Content-Disposition'] = f'attachment; filename={safe_name}_timetable.csv'
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    return response


@app.route('/timetable/export-master-csv')
@admin_required
def export_master_timetable_csv():
    divisions = [
        division for division in Division.query.order_by(Division.branch_id, Division.semester, Division.name).all()
        if division.timetable_entries.count() > 0
    ]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['==========================================================='])
    writer.writerow(['MASTER TIMETABLE - ALL SEMESTERS AND DIVISIONS'])
    writer.writerow(['==========================================================='])
    writer.writerow([])

    for division in divisions:
        entries = (
            Timetable.query
            .filter_by(division_id=division.id)
            .join(TimeSlot)
            .order_by(TimeSlot.start_time, Timetable.day)
            .all()
        )
        div_csv = build_division_timetable_csv(division, entries)
        for line in div_csv.splitlines():
            writer.writerow([line])
        writer.writerow([])
        writer.writerow(['-----------------------------------------------------------'])
        writer.writerow([])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=all_semesters_master_timetable.csv'
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    return response




# ============================================
# 6️⃣ ADMIN MANAGEMENT MODULES (ORDER MATTERS)
# ============================================

# ============================================
# 🔹 Branches
# ============================================

@app.route('/admin/branches')
@admin_required
def manage_branches():
    q = (request.args.get('q') or request.args.get('search') or '').strip()
    query = Branch.query
    if q:
        query = query.filter(
            (Branch.name.ilike(f'%{q}%')) |
            (Branch.short_name.ilike(f'%{q}%'))
        )
    branches = query.all()
    return render_template('manage_branches.html', branches=branches, q=q, search=q)


@app.route('/admin/branches/add', methods=['POST'])
@admin_required
def add_branch():
    name = request.form.get('name')
    short_name = request.form.get('short_name')

    if not name or not short_name:
        flash('Branch name and short name are required', 'danger')
        return redirect(url_for('manage_branches'))

    if Branch.query.filter_by(short_name=short_name).first():
        flash('Branch short name already exists', 'danger')
        return redirect(url_for('manage_branches'))

    branch = Branch(
        name=name,
        short_name=short_name,
        created_by=current_user.id
    )

    db.session.add(branch)
    db.session.commit()

    flash('Branch added successfully', 'success')
    return redirect(url_for('manage_branches'))

@app.route('/admin/branches/delete/<int:branch_id>', methods=['POST'])
@admin_required
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)

    db.session.delete(branch)
    db.session.commit()

    flash('Branch deleted successfully', 'success')
    return redirect(url_for('manage_branches'))

@app.route('/branch/edit', methods=['POST'])
@admin_required
def edit_branch():
    branch_id = request.form.get('branch_id', type=int)
    name = request.form.get('name')
    short_name = request.form.get('short_name')

    branch = Branch.query.get_or_404(branch_id)

    branch.name = name
    branch.short_name = short_name

    db.session.commit()

    flash('Branch updated successfully!', 'success')
    return redirect(url_for('manage_branches'))


# ============================================
# 🔹 Divisions
# ============================================


@app.route('/admin/divisions')
@admin_required
def manage_divisions():
    q = (request.args.get('q') or request.args.get('search') or '').strip()
    branches = Branch.query.all()
    query = Division.query.order_by(Division.semester)
    if q:
        query = query.join(Branch).filter(
            (Division.name.ilike(f'%{q}%')) |
            (Division.academic_year.ilike(f'%{q}%')) |
            (Branch.name.ilike(f'%{q}%')) |
            (Branch.short_name.ilike(f'%{q}%'))
        )
    divisions = query.all()
    return render_template(
        'manage_divisions.html',
        branches=branches,
        divisions=divisions,
        q=q,
        search=q
    )



@app.route('/admin/divisions/add', methods=['POST'])
@app.route('/admin/divisions', methods=['GET', 'POST'])
@admin_required
def add_division():
    if request.method == 'POST':
        branch_id = request.form.get('branch_id', type=int)
        name = (request.form.get('name') or '').strip()
        semester = request.form.get('semester', type=int)
        academic_year = (request.form.get('academic_year') or '').strip()
        student_count = request.form.get('student_count', type=int) or 60
        num_batches = request.form.get('num_batches', type=int) or 1

        if not branch_id or not name or not semester or not academic_year:
            flash('⚠️ All division fields (Branch, Name, Semester, Academic Year) are required!', 'danger')
            return redirect(url_for('manage_divisions'))

        # Check if division with same branch_id, name, semester, academic_year already exists
        existing = Division.query.filter_by(
            branch_id=branch_id,
            name=name,
            semester=semester,
            academic_year=academic_year
        ).first()

        if existing:
            branch = Branch.query.get(branch_id)
            b_name = branch.short_name if branch else ''
            flash(f"⚠️ Division '{name}' (Semester {semester}) already exists for {b_name} in academic year {academic_year}!", "danger")
            return redirect(url_for('manage_divisions'))
        
        division = Division(
            branch_id=branch_id,
            name=name,
            semester=semester,
            academic_year=academic_year,
            student_count=student_count,
            num_batches=num_batches
        )
        db.session.add(division)
        db.session.flush()  # Get division.id
        
        # Auto-create batch rows if num_batches > 1
        if num_batches > 1:
            batch_size = student_count // num_batches
            for i in range(1, num_batches + 1):
                batch = Batch(
                    division_id=division.id,
                    name=f'D{i}',
                    student_count=batch_size
                )
                db.session.add(batch)
        
        db.session.commit()
        
        flash(f'✨ Division {division.full_name} added successfully!', 'success')
        return redirect(url_for('manage_divisions'))
    
    return redirect(url_for('manage_divisions'))




@app.route('/division/edit', methods=['POST'])
@admin_required
def edit_division():
    division_id = request.form.get('division_id', type=int)
    branch_id = request.form.get('branch_id', type=int)
    name = request.form.get('name')
    semester = request.form.get('semester', type=int)
    academic_year = request.form.get('academic_year')
    student_count = request.form.get('student_count', type=int) or 60
    num_batches = request.form.get('num_batches', type=int) or 1

    division = Division.query.get_or_404(division_id)

    division.branch_id = branch_id
    division.name = name
    division.semester = semester
    division.academic_year = academic_year
    division.student_count = student_count
    division.num_batches = num_batches
    
    # Sync batches: delete old, create new if needed
    old_batch_count = division.batches.count()
    if num_batches != old_batch_count or (num_batches > 1 and old_batch_count == 0):
        # Only recreate if no timetable entries reference existing batches
        has_batch_entries = Timetable.query.filter(
            Timetable.batch_id.isnot(None),
            Timetable.division_id == division_id
        ).first()
        
        if not has_batch_entries:
            # Safe to recreate batches
            Batch.query.filter_by(division_id=division_id).delete()
            if num_batches > 1:
                batch_size = student_count // num_batches
                for i in range(1, num_batches + 1):
                    batch = Batch(
                        division_id=division_id,
                        name=f'D{i}',
                        student_count=batch_size
                    )
                    db.session.add(batch)
        else:
            flash('Cannot change batch count: existing lab entries use current batches.', 'warning')

    db.session.commit()

    flash('Division updated successfully!', 'success')
    return redirect(url_for('manage_divisions'))



@app.route('/division/delete/<int:division_id>', methods=['POST'])
@admin_required
def delete_division(division_id):
    division = Division.query.get_or_404(division_id)

    # ❗ Safety: unresolved clashes
    active_clash = ClashLog.query.filter_by(
        division_id=division.id,
        is_resolved=False
    ).first()

    if active_clash:
        flash("Cannot delete division. Unresolved clash exists.", "danger")
        return redirect(url_for('manage_divisions'))

    try:
        # ✅ DELETE CHILD RECORDS FIRST
        Batch.query.filter_by(division_id=division.id).delete()
        Timetable.query.filter_by(division_id=division.id).delete()
        ClashLog.query.filter_by(division_id=division.id).delete()

        db.session.delete(division)
        db.session.commit()

        flash("Division deleted successfully.", "success")

    except Exception as e:
        db.session.rollback()
        flash("Deletion failed due to linked records.", "danger")

    return redirect(url_for('manage_divisions'))


# ============================================
# 🔹 Rooms / Resources
# ============================================

@app.route('/admin/manage-rooms', methods=['GET'])
@admin_required
def manage_rooms():
    q = (request.args.get('q') or '').strip()
    query = Room.query.order_by(Room.name)
    if q:
        query = query.filter(Room.name.ilike(f'%{q}%') | Room.room_type.ilike(f'%{q}%'))
    rooms = query.all()
    return render_template('manage_rooms.html', rooms=rooms, q=q)

@app.route('/admin/manage-rooms/add', methods=['POST'])
@admin_required
def add_room():
    name = request.form.get('name', '').strip()
    capacity = request.form.get('capacity', type=int) or 60
    room_type = request.form.get('room_type', 'Classroom')
    
    if not name:
        flash("Room name is required.", "danger")
        return redirect(url_for('manage_rooms'))
        
    existing = Room.query.filter_by(name=name).first()
    if existing:
        flash(f"Room '{name}' already exists.", "danger")
        return redirect(url_for('manage_rooms'))
        
    try:
        room = Room(name=name, capacity=capacity, room_type=room_type, created_by=session.get('user_id'))
        db.session.add(room)
        db.session.commit()
        flash(f"Room '{name}' added successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Failed to add room.", "danger")
        
    return redirect(url_for('manage_rooms'))

@app.route('/admin/manage-rooms/edit', methods=['POST'])
@admin_required
def edit_room():
    room_id = request.form.get('room_id', type=int)
    name = request.form.get('name', '').strip()
    capacity = request.form.get('capacity', type=int) or 60
    room_type = request.form.get('room_type', 'Classroom')
    
    room = Room.query.get_or_404(room_id)
    
    if not name:
        flash("Room name is required.", "danger")
        return redirect(url_for('manage_rooms'))
        
    existing = Room.query.filter((Room.name == name) & (Room.id != room_id)).first()
    if existing:
        flash(f"Room '{name}' already exists.", "danger")
        return redirect(url_for('manage_rooms'))
        
    try:
        room.name = name
        room.capacity = capacity
        room.room_type = room_type
        db.session.commit()
        flash("Room updated successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Failed to update room.", "danger")
        
    return redirect(url_for('manage_rooms'))

@app.route('/admin/manage-rooms/delete/<int:room_id>', methods=['POST'])
@admin_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    try:
        db.session.delete(room)
        db.session.commit()
        flash("Room deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Failed to delete room.", "danger")
        
    return redirect(url_for('manage_rooms'))


# ============================================
# 🔹 Subjects
# ============================================

@app.route('/admin/subjects')
@admin_required
def manage_subjects():
    q = (request.args.get('q') or request.args.get('search') or '').strip()
    branch_id = request.args.get('branch_id', type=int)
    semester = request.args.get('semester', type=int)

    query = Subject.query.order_by(Subject.semester, Subject.code)
    if q:
        query = query.filter(
            (Subject.name.ilike(f'%{q}%')) |
            (Subject.code.ilike(f'%{q}%'))
        )
    if branch_id:
        query = query.filter(Subject.branch_id == branch_id)
    if semester:
        query = query.filter(Subject.semester == semester)

    subjects = query.all()
    branches = Branch.query.order_by(Branch.name).all()
    return render_template(
        'manage_subjects.html',
        subjects=subjects,
        branches=branches,
        selected_branch_id=branch_id,
        selected_semester=semester,
        q=q,
        search=q
    )


@app.route('/admin/subjects/add', methods=['POST'])
@admin_required
def add_subject():
    branch_id = request.form.get('branch_id', type=int)
    semester = request.form.get('semester', type=int)
    has_lab = request.form.get('has_lab', type=int, default=1) == 1
    weekly_lectures = request.form.get('weekly_lectures', type=int) or request.form.get('credits', type=int) or 3
    subject = Subject(
        name=request.form['name'],
        code=request.form['code'],
        credits=request.form['credits'],
        weekly_lectures=weekly_lectures,
        branch_id=branch_id,
        semester=semester,
        has_lab=has_lab,
        created_by=current_user.id
    )
    db.session.add(subject)
    db.session.commit()
    flash('Subject added successfully', 'success')
    return redirect(url_for('manage_subjects'))


@app.route('/subject/edit', methods=['POST'])
@admin_required
def edit_subject():
    subject_id = request.form.get('subject_id', type=int)
    name = request.form.get('name')
    code = request.form.get('code')
    credits = request.form.get('credits', type=int)
    weekly_lectures = request.form.get('weekly_lectures', type=int) or credits or 3
    branch_id = request.form.get('branch_id', type=int)
    semester = request.form.get('semester', type=int)
    has_lab = request.form.get('has_lab', type=int, default=1) == 1

    subject = Subject.query.get_or_404(subject_id)

    # Prevent duplicate subject code
    existing = Subject.query.filter(
        Subject.code == code,
        Subject.id != subject_id
    ).first()

    if existing:
        flash("Subject code already exists.", "danger")
        return redirect(url_for('manage_subjects'))

    subject.name = name
    subject.code = code
    subject.credits = credits
    subject.weekly_lectures = weekly_lectures
    subject.branch_id = branch_id
    subject.semester = semester
    subject.has_lab = has_lab

    db.session.commit()

    flash("Subject updated successfully!", "success")
    return redirect(url_for('manage_subjects'))

@app.route('/admin/subjects/delete/<int:subject_id>', methods=['POST'])
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    db.session.delete(subject)
    db.session.commit()

    flash('Subject deleted successfully', 'success')
    return redirect(url_for('manage_subjects'))


# ============================================
# 🔹 Timeslots
# ============================================

@app.route('/admin/timeslots')
@admin_required
def manage_timeslots():
    q = (request.args.get('q') or request.args.get('search') or '').strip()
    query = TimeSlot.query.order_by(TimeSlot.start_time)
    if q:
        query = query.filter(TimeSlot.slot_label.ilike(f'%{q}%'))
    timeslots = query.all()
    return render_template('manage_timeslots.html', timeslots=timeslots, q=q, search=q)

@app.route('/admin/timeslots/add', methods=['POST'])
@admin_required
def add_timeslot():
    start_time_str = request.form.get('start_time')
    end_time_str = request.form.get('end_time')
    slot_label = request.form.get('slot_label')
    
    # Convert to time objects
    start_time = datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time()
    
    # Validate
    if start_time >= end_time:
        flash('End time must be after start time', 'danger')
        return redirect(url_for('manage_timeslots'))
    
    timeslot = TimeSlot(
        start_time=start_time,
        end_time=end_time,
        slot_label=slot_label,
        created_by=session['user_id']
    )
    
    db.session.add(timeslot)
    db.session.commit()
    
    flash('Time slot added successfully!', 'success')
    return redirect(url_for('manage_timeslots'))


@app.route('/admin/timeslots/edit/<int:slot_id>', methods=['GET'])
@admin_required
def edit_timeslot(slot_id):
    slot = TimeSlot.query.get_or_404(slot_id)
    return render_template('edit_timeslot.html', slot=slot)



@app.route('/admin/timeslots/update/<int:slot_id>', methods=['POST'])
@admin_required
def update_timeslot(slot_id):
    slot = TimeSlot.query.get_or_404(slot_id)

    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    slot_label = request.form.get('slot_label')

    start_time = datetime.strptime(start_time, '%H:%M').time()
    end_time = datetime.strptime(end_time, '%H:%M').time()

    if start_time >= end_time:
        flash('End time must be after start time', 'danger')
        return redirect(url_for('edit_timeslot', slot_id=slot.id))

    # 🔒 OPTIONAL SAFETY CHECK
    used = Timetable.query.filter_by(time_slot_id=slot.id).first()
    if used:
        flash(
            'Cannot edit this time slot because it is already used in timetable.',
            'danger'
        )
        return redirect(url_for('manage_timeslots'))

    slot.start_time = start_time
    slot.end_time = end_time
    slot.slot_label = slot_label

    db.session.commit()
    flash('Time slot updated successfully!', 'success')
    return redirect(url_for('manage_timeslots'))


@app.route('/admin/timeslots/delete/<int:slot_id>', methods=['POST'])
@admin_required
def delete_timeslot(slot_id):
    slot = TimeSlot.query.get_or_404(slot_id)

    # 🔒 Check if used in timetable
    used = Timetable.query.filter_by(time_slot_id=slot.id).first()
    if used:
        flash(
            "Cannot delete this time slot. It is already used in timetable.",
            "danger"
        )
        return redirect(url_for('manage_timeslots'))

    db.session.delete(slot)
    db.session.commit()

    flash("Time slot deleted successfully", "success")
    return redirect(url_for('manage_timeslots'))

# ============================================
# 🔹 Faculty (ADMIN VIEW + DELETE ONLY)
# ============================================

@app.route('/admin/faculty')
@admin_required
def manage_faculty():
    search = request.args.get('search', '').strip()
    dept_filter = request.args.get('dept', '').strip()
    visiting_filter = request.args.get('visiting', '').strip()  # 'yes', 'no', or ''

    query = Faculty.query.join(User)
    if search:
        query = query.filter(
            (User.full_name.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (Faculty.department.ilike(f'%{search}%')) |
            (Faculty.designation.ilike(f'%{search}%'))
        )
    if dept_filter:
        query = query.filter(Faculty.department.ilike(f'%{dept_filter}%'))
    if visiting_filter == 'yes':
        query = query.filter(Faculty.is_visiting.is_(True))
    elif visiting_filter == 'no':
        query = query.filter(
            (Faculty.is_visiting.is_(False)) | (Faculty.is_visiting.is_(None))
        )

    faculty_list = query.all()
    # Build distinct department list for filter dropdown
    all_depts = sorted(set(
        f.department for f in Faculty.query.all() if f.department
    ))
    return render_template(
        'manage_faculty.html',
        faculty_list=faculty_list,
        search=search,
        dept_filter=dept_filter,
        visiting_filter=visiting_filter,
        all_depts=all_depts,
        workload=ClashService.get_faculty_workload()
    )

@app.route('/admin/faculty/delete/<int:faculty_id>', methods=['POST'])
@admin_required
def delete_faculty(faculty_id):
    faculty = Faculty.query.get_or_404(faculty_id)
    user = faculty.user

    db.session.delete(faculty)
    db.session.delete(user)
    db.session.commit()

    flash('Faculty deleted successfully', 'success')
    return redirect(url_for('manage_faculty'))


@app.route('/admin/faculty/<int:faculty_id>/timetable')
@admin_required
def admin_view_faculty_timetable(faculty_id):
    faculty = Faculty.query.get_or_404(faculty_id)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    timeslots = TimeSlot.query.order_by(TimeSlot.start_time).all()
    entries = Timetable.query.filter_by(faculty_id=faculty.id).all()

    # Build matrix: {day: {slot_id: [entries]}}
    timetable_matrix = {day: {slot.id: [] for slot in timeslots} for day in days}
    for entry in entries:
        if entry.day in timetable_matrix and entry.time_slot_id in timetable_matrix[entry.day]:
            timetable_matrix[entry.day][entry.time_slot_id].append({
                'id': entry.id,
                'subject': entry.subject.name if entry.subject else 'N/A',
                'subject_code': entry.subject.code if entry.subject else '',
                'division': entry.division.full_name if entry.division else 'N/A',
                'batch': entry.batch.name if entry.batch else None,
                'room': entry.room_number or 'N/A',
                'entry_type': entry.entry_type
            })

    return jsonify({
        'faculty_name': faculty.user.full_name,
        'department': faculty.department or 'N/A',
        'designation': faculty.designation or 'Faculty',
        'days': days,
        'timeslots': [{'id': s.id, 'time_range': s.time_range, 'label': s.slot_label or ''} for s in timeslots],
        'matrix': timetable_matrix
    })




# ============================================
# 7️⃣ TIMETABLE MODULE (ADMIN)
# ============================================

def get_dynamic_lab_start_slots(timeslots):
    """
    Dynamically identifies valid lab start slots from an ordered list of TimeSlot records.
    A lab is 2 hours long. A slot is a valid lab start slot if it forms a continuous
    2-hour block with the immediately following time slot (gap <= 15 minutes),
    and is the start of that 2-hour block.
    """
    valid_start_ids = set()
    i = 0
    n = len(timeslots)
    while i < n:
        if i + 1 < n:
            t1_end = timeslots[i].end_time
            t2_start = timeslots[i+1].start_time
            dt1 = datetime.combine(date.today(), t1_end)
            dt2 = datetime.combine(date.today(), t2_start)
            gap = (dt2 - dt1).total_seconds() / 60.0
            
            if 0 <= gap <= 15:
                valid_start_ids.add(timeslots[i].id)
                i += 2  # Skip 2nd hour slot as start slot
                continue
        i += 1
    return valid_start_ids

@app.route('/timetable/auto-generate/<int:division_id>', methods=['GET', 'POST'])
@admin_required
def auto_generate_timetable(division_id):
    division = Division.query.get_or_404(division_id)
    # Default to overwrite=True so newly generated timetable cleanly replaces old entries
    overwrite = request.args.get('overwrite', '1') != '0' and request.form.get('overwrite', '1') != '0'
    res = AutoTimetableGenerator.generate_timetable(division_id, overwrite=overwrite, created_by=session.get('user_id', 1))
    
    if res.get('success'):
        flash(f"✨ {res['message']}", 'success')
    else:
        flash(f"Error auto-generating timetable: {res.get('message')}", 'danger')
        
    return redirect(url_for('timetable_create', division_id=division_id, day='Monday'))


@app.route('/timetable/auto-generate-all', methods=['GET', 'POST'])
@admin_required
def auto_generate_all():
    divisions = Division.query.all()
    count = 0
    for div in divisions:
        res = AutoTimetableGenerator.generate_timetable(div.id, overwrite=True, created_by=session.get('user_id', 1))
        if res.get('success'):
            count += 1
    flash(f"✨ AI Auto-Generator successfully processed {count} active division timetables cleanly!", 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/timetable/preview-auto-generate/<int:division_id>')
@admin_required
def preview_auto_generate(division_id):
    division = Division.query.get_or_404(division_id)
    preview_data = AutoTimetableGenerator.preview_timetable(division_id)
    return render_template('timetable_preview.html', division=division, preview_data=preview_data)


@app.route('/timetable/select')
@admin_required
def timetable_select():
    branches = Branch.query.all()
    return render_template('timetable_select.html', branches=branches)

@app.route('/timetable/create')
@admin_required
def timetable_create():
    division_id = request.args.get('division_id', type=int)
    day = request.args.get('day', 'Monday')

    if not division_id:
        flash('Please select a division', 'warning')
        return redirect(url_for('timetable_select'))

    division = Division.query.get_or_404(division_id)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    timeslots = TimeSlot.query.order_by(TimeSlot.start_time).all()

    timetable_entries = Timetable.query.filter_by(
        division_id=division_id,
        day=day
    ).all()

    # Build multi-entry map: {slot_id: [entries]} to support batches
    timetable_map = {}
    for slot in timeslots:
        timetable_map[slot.id] = []
    for entry in timetable_entries:
        timetable_map.setdefault(entry.time_slot_id, []).append(entry)

    # Build next-slot map: slot_id -> next consecutive slot
    # Used so that lab (2-hr) checks faculty availability in BOTH slots
    next_slot_map = {}
    for i, slot in enumerate(timeslots):
        if i + 1 < len(timeslots):
            next_slot_map[slot.id] = timeslots[i + 1]
        else:
            next_slot_map[slot.id] = None

    faculty_availability = {}
    lab_faculty_availability = {}   # faculty checked against slot + next-slot
    occupied_rooms = {}
    for slot in timeslots:
        avail = ClashService.get_all_faculty_availability(day, slot.id)
        faculty_availability[slot.id] = avail

        # For lab form: mark unavailable if busy in EITHER this slot OR the next slot
        next_slot = next_slot_map.get(slot.id)
        if next_slot:
            next_avail_map = {
                f['faculty_id']: f['is_available']
                for f in ClashService.get_all_faculty_availability(day, next_slot.id)
            }
            lab_avail = []
            for f in avail:
                free_next = next_avail_map.get(f['faculty_id'], True)
                lab_avail.append(dict(f, is_available=f['is_available'] and free_next,
                                      lab_blocked_next=(not free_next and f['is_available'])))
            lab_faculty_availability[slot.id] = lab_avail
        else:
            # Last slot: no next slot, normal availability
            lab_faculty_availability[slot.id] = [
                dict(f, lab_blocked_next=False) for f in avail
            ]

        # Find all occupied rooms in this slot (any entry where room_number is not null)
        occupied_entries = Timetable.query.filter(
            Timetable.day == day,
            Timetable.time_slot_id == slot.id,
            Timetable.room_number.isnot(None)
        ).all()
        occupied_rooms[slot.id] = {entry.room_number for entry in occupied_entries}

    # Filter subjects strictly by division semester and branch_id
    subjects = Subject.query.filter(
        (Subject.semester == division.semester) | (Subject.semester.is_(None)),
        (Subject.branch_id == division.branch_id) | (Subject.branch_id.is_(None))
    ).order_by(Subject.name).all()
    if not subjects:
        subjects = Subject.query.order_by(Subject.name).all()
    rooms = Room.query.order_by(Room.name).all()

    # Subject load for this division (count of scheduled lectures per subject)
    subject_load = {}
    for entry in Timetable.query.filter_by(division_id=division_id, entry_type='lecture').all():
        if entry.subject_id:
            subject_load[entry.subject_id] = subject_load.get(entry.subject_id, 0) + 1

    # Get batches for this division
    div_batches = division.batches.order_by(Batch.name).all() if division.num_batches and division.num_batches > 1 else []

    # Calculate exact slot status for UI form rendering
    valid_lab_start_ids = get_dynamic_lab_start_slots(timeslots)
    slot_status = {}
    for slot in timeslots:
        entries = timetable_map.get(slot.id, [])
        has_full_div = any(e.batch_id is None for e in entries)
        is_library_or_break = any(e.entry_type in ('library', 'break') for e in entries)
        assigned_batch_ids = {e.batch_id for e in entries if e.batch_id is not None}
        all_batches_assigned = bool(div_batches and len(assigned_batch_ids) >= len(div_batches))
        is_fully_occupied = is_library_or_break or has_full_div or all_batches_assigned
        
        is_lab_start_slot = slot.id in valid_lab_start_ids

        slot_status[slot.id] = {
            'has_full_div': has_full_div,
            'is_library_or_break': is_library_or_break,
            'assigned_batch_ids': assigned_batch_ids,
            'all_batches_assigned': all_batches_assigned,
            'is_fully_occupied': is_fully_occupied,
            'is_lab_start_slot': is_lab_start_slot
        }

    # Faculty workload for display
    workload = ClashService.get_faculty_workload()

    return render_template(
        'timetable_create.html',
        division=division,
        days=days,
        current_day=day,
        timeslots=timeslots,
        timetable_map=timetable_map,
        faculty_availability=faculty_availability,
        lab_faculty_availability=lab_faculty_availability,
        subjects=subjects,
        rooms=rooms,
        div_batches=div_batches,
        workload=workload,
        occupied_rooms=occupied_rooms,
        subject_load=subject_load,
        slot_status=slot_status
    )

@app.route('/timetable/add-entry', methods=['POST'])
@admin_required
def add_timetable_entry():

    division_id = request.form.get('division_id', type=int)
    time_slot_id = request.form.get('time_slot_id', type=int)
    day = request.form.get('day')
    entry_type = request.form.get('entry_type', 'lecture')
    batch_id = request.form.get('batch_id', type=int) or None

    # Enforce lab start slot restrictions dynamically (labs can only start at the beginning of a 2-hour continuous block before a break)
    if entry_type == 'lab':
        all_slots = TimeSlot.query.order_by(TimeSlot.start_time).all()
        valid_start_ids = get_dynamic_lab_start_slots(all_slots)
        if time_slot_id not in valid_start_ids:
            flash('Labs can only start at the beginning of a 2-hour continuous block before a break.', 'danger')
            return redirect(url_for('timetable_create', division_id=division_id, day=day))

    # Library / Break entries: no faculty, subject, or room needed
    if entry_type in ('library', 'break'):
        # Check division clash (can't overlap with existing entries)
        is_valid, clashes = ClashService.validate_and_detect_clashes(
            faculty_id=None, division_id=division_id, room_number=None,
            day=day, time_slot_id=time_slot_id,
            entry_type=entry_type
        )
        if not is_valid:
            for clash in clashes:
                flash(f"Clash detected: {clash['type']}", 'danger')
            return redirect(url_for('timetable_create', division_id=division_id, day=day))

        entry = Timetable(
            division_id=division_id,
            subject_id=None,
            faculty_id=None,
            time_slot_id=time_slot_id,
            batch_id=None,
            day=day,
            room_number=None,
            entry_type=entry_type,
            is_manual=True,
            created_by=session['user_id']
        )
        db.session.add(entry)
        db.session.commit()
        flash(f'{entry_type.capitalize()} period added!', 'success')
        return redirect(url_for('timetable_create', division_id=division_id, day=day))

    # Normal lecture / lab entry
    subject_id = request.form.get('subject_id', type=int)
    faculty_id = request.form.get('faculty_id', type=int)
    room_number = request.form.get('room_number')

    # GET FACULTY OBJECT
    faculty = Faculty.query.get_or_404(faculty_id)

    # Validate clashes (batch-aware)
    is_valid, clashes = ClashService.validate_and_detect_clashes(
        faculty.id, division_id, room_number, day, time_slot_id,
        batch_id=batch_id, entry_type=entry_type, subject_id=subject_id
    )

    if not is_valid:
        for clash in clashes:
            ClashService.log_clash(
                clash_type=clash['type'].replace('_clash', ''),
                details=clash,
                division_id=division_id,
                faculty_id=faculty.id,
                severity='error'
            )
            # Build a descriptive flash message
            ct = clash.get('type', '')
            if ct == 'faculty_clash':
                msg = f"Faculty clash: {clash.get('faculty_name')} is already teaching {clash.get('subject')} ({clash.get('division')}) at {clash.get('time')}."
            elif ct == 'faculty_next_slot_clash':
                msg = clash.get('message', 'Faculty is busy in the next slot — cannot assign for a 2-hour lab.')
            elif ct == 'room_clash':
                msg = f"Room clash: {clash.get('room')} is already occupied by {clash.get('division')} at {clash.get('time')}."
            elif ct == 'division_clash':
                msg = f"Division clash: {clash.get('division')} already has {clash.get('subject')} at {clash.get('time')}."
            elif ct == 'faculty_availability_clash':
                msg = clash.get('message', 'Faculty is unavailable at this time.')
            elif ct == 'batch_lab_limit_clash':
                msg = clash.get('message', 'Batch weekly lab limit reached.')
            else:
                msg = f"Clash detected: {ct}"
            flash(msg, 'danger')

        return redirect(url_for(
            'timetable_create',
            division_id=division_id,
            day=day
        ))

    entry = Timetable(
        division_id=division_id,
        subject_id=subject_id,
        faculty_id=faculty.id,
        time_slot_id=time_slot_id,
        batch_id=batch_id,
        day=day,
        room_number=room_number,
        entry_type=entry_type,
        is_manual=True,
        created_by=session['user_id']
    )

    db.session.add(entry)
    db.session.commit()

    autofill_next_slot = request.form.get('autofill_next_slot') == '1'
    if entry_type == 'lab' and autofill_next_slot:
        current_slot = TimeSlot.query.get(time_slot_id)
        if current_slot:
            next_slot = TimeSlot.query.filter(
                TimeSlot.start_time >= current_slot.end_time
            ).order_by(TimeSlot.start_time).first()
            
            if next_slot:
                # Validate clashes for the next slot as a single slot (second hour of lab)
                is_valid_next, clashes_next = ClashService.validate_and_detect_clashes(
                    faculty.id, division_id, room_number, day, next_slot.id,
                    batch_id=batch_id, entry_type='lecture', subject_id=subject_id
                )
                if is_valid_next:
                    next_entry = Timetable(
                        division_id=division_id,
                        subject_id=subject_id,
                        faculty_id=faculty.id,
                        time_slot_id=next_slot.id,
                        batch_id=batch_id,
                        day=day,
                        room_number=room_number,
                        entry_type=entry_type,
                        is_manual=True,
                        created_by=session['user_id']
                    )
                    db.session.add(next_entry)
                    db.session.commit()
                    flash(f'Timetable entry and next slot ({next_slot.time_range}) added successfully!', 'success')
                    return redirect(url_for('timetable_create', division_id=division_id, day=day))
                else:
                    for clash in clashes_next:
                        ClashService.log_clash(
                            clash_type=clash['type'].replace('_clash', ''),
                            details=clash,
                            division_id=division_id,
                            faculty_id=faculty.id,
                            severity='warning'
                        )
                    
                    clash_messages = []
                    for c in clashes_next:
                        ct = c.get('type', '')
                        if ct == 'faculty_clash':
                            clash_messages.append(f"Faculty {c.get('faculty_name', 'N/A')} is busy")
                        elif ct == 'faculty_next_slot_clash':
                            clash_messages.append(c.get('message', f"Faculty {c.get('faculty_name', 'N/A')} is busy in the next slot"))
                        elif ct == 'room_clash':
                            clash_messages.append(f"Room {c.get('room', 'N/A')} is occupied")
                        elif ct == 'division_clash':
                            clash_messages.append(f"Division/Batch {c.get('division', 'N/A')} already has an entry")
                        elif ct == 'faculty_availability_clash':
                            clash_messages.append(c.get('message', 'Faculty is unavailable'))
                        elif ct == 'batch_lab_limit_clash':
                            clash_messages.append(c.get('message', 'Batch weekly lab limit reached'))
                        else:
                            clash_messages.append(c.get('message', ct.replace('_', ' ').title() if ct else 'Schedule conflict'))
                    
                    clash_str = ", ".join(clash_messages) if clash_messages else "Schedule conflict"
                    flash(f'Main entry added, but could not auto-fill next slot ({next_slot.time_range}) due to: {clash_str}.', 'warning')
                    return redirect(url_for('timetable_create', division_id=division_id, day=day))

    flash('Timetable entry added successfully!', 'success')
    return redirect(url_for(
        'timetable_create',
        division_id=division_id,
        day=day
    ))

@app.route('/timetable/edit-entry/<int:entry_id>', methods=['GET', 'POST'])
@admin_required
def edit_timetable_entry(entry_id):
    entry = Timetable.query.get_or_404(entry_id)
    
    if request.method == 'POST':
        faculty_id = request.form.get('faculty_id', type=int)
        room_number = request.form.get('room_number')
        
        # Validate clashes (excluding current entry)
        is_valid, clashes = ClashService.validate_and_detect_clashes(
            faculty_id, entry.division_id, room_number,
            entry.day, entry.time_slot_id, entry.id,
            batch_id=entry.batch_id, entry_type=entry.entry_type,
            subject_id=entry.subject_id
        )
        
        if not is_valid:
            for clash in clashes:
                flash(f"Clash detected: {clash['type']}", 'danger')
            return redirect(url_for('edit_timetable_entry', entry_id=entry_id))
        
        entry.faculty_id = faculty_id
        entry.room_number = room_number
        
        db.session.commit()
        
        flash('Entry updated successfully!', 'success')
        return redirect(url_for('timetable_create',
                              division_id=entry.division_id,
                              day=entry.day))
    
    # Get available faculty
    faculty_list = ClashService.get_all_faculty_availability(
        entry.day,
        entry.time_slot_id
    )
    rooms = Room.query.order_by(Room.name).all()
    
    return render_template('edit_timetable_entry.html',
                         entry=entry,
                         faculty_list=faculty_list,
                         rooms=rooms)

@app.route('/timetable/delete-entry/<int:entry_id>', methods=['POST'])
@admin_required
def delete_timetable_entry(entry_id):
    entry = Timetable.query.get_or_404(entry_id)
    division_id = entry.division_id
    day = entry.day
    
    db.session.delete(entry)
    db.session.commit()
    
    flash('Entry deleted successfully', 'success')
    return redirect(url_for('timetable_create',
                          division_id=division_id,
                          day=day))

@app.route('/timetable/view/<int:division_id>')
@login_required
def view_timetable(division_id):
    """View complete timetable for a division"""
    division = Division.query.get_or_404(division_id)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    timeslots = TimeSlot.query.order_by(TimeSlot.start_time).all()
    
    # Get all entries
    entries = Timetable.query.filter_by(division_id=division_id).all()
    
    # Create grid: grid[day][time_slot_id] = list of entries
    grid = {}
    for day in days:
        grid[day] = {}
        for slot in timeslots:
            grid[day][slot.id] = []
    
    for entry in entries:
        grid[entry.day][entry.time_slot_id].append(entry)
    
    user = User.query.get(session['user_id'])
    
    return render_template('view_timetable.html',
                         division=division,
                         days=days,
                         timeslots=timeslots,
                         grid=grid,
                         user=user)


@app.route('/timetable/final-view')
@admin_required
def final_timetable_view():
    branches = Branch.query.all()
    all_timetables = {}

    has_any_division = False

    for branch in branches:
        divisions_with_entries = [
            d for d in branch.divisions
            if d.timetable_entries.count() > 0
        ]

        if divisions_with_entries:
            has_any_division = True

        all_timetables[branch.id] = {
            'branch': branch,
            'divisions': divisions_with_entries
        }

    return render_template(
        'final_timetable_view.html',
        all_timetables=all_timetables,
        has_any_division=has_any_division
    )


# ============================================
# 8️⃣ FACULTY MODULE (SEPARATE)
# ============================================


@app.route('/faculty/dashboard')
@login_required
def faculty_dashboard():

    faculty = current_user.faculty_profile

    if not faculty:
        flash("Faculty profile not found", "danger")
        return redirect(url_for('logout'))

    timetable_entries = (
        Timetable.query
        .filter(Timetable.faculty_id == faculty.id)
        .order_by(Timetable.day, Timetable.time_slot_id)
        .all()
    )

    return render_template(
        'faculty_dashboard.html',
        faculty=faculty,
        timetable_entries=timetable_entries
    )


@app.route('/faculty/timetable/download')
@login_required
def download_faculty_timetable():
    if current_user.role != 'faculty':
        flash('Access denied', 'danger')
        return redirect(url_for('admin_dashboard'))

    faculty = current_user.faculty_profile

    if not faculty:
        flash('Faculty profile not found', 'danger')
        return redirect(url_for('logout'))

    entries = (
        Timetable.query
        .filter(Timetable.faculty_id == faculty.id)
        .join(Division)
        .join(TimeSlot)
        .order_by(Timetable.day, TimeSlot.start_time)
        .all()
    )

    safe_name = current_user.full_name.lower().replace(' ', '_')
    return build_timetable_csv_response(
        entries,
        f'{safe_name}_timetable.csv',
        f'{current_user.full_name} Timetable Export'
    )

@app.route('/faculty/profile', methods=['GET', 'POST'])
@login_required
def faculty_profile():

    if current_user.role != 'faculty':
        flash('Access denied', 'danger')
        return redirect(url_for('admin_dashboard'))

    faculty = current_user.faculty_profile

    if not faculty:
        flash('Faculty profile not found', 'danger')
        return redirect(url_for('logout'))

    # 🔹 SAVE PROFILE
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        if full_name:
            current_user.full_name = full_name
            
        faculty.phone = request.form.get('phone')
        faculty.department = request.form.get('department')
        faculty.designation = request.form.get('designation')

        # Handle visiting vs regular faculty
        is_visiting = request.form.get('is_visiting') == 'on'
        faculty.is_visiting = is_visiting

        if is_visiting:
            # Save visiting days and per-day slot IDs
            visiting_days = request.form.getlist('visiting_days')  # multi-select
            all_weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            schedule = {}
            for day in all_weekdays:
                if day in visiting_days:
                    day_slots = request.form.getlist(f'visiting_slots_{day}')
                    schedule[day] = [int(s) for s in day_slots if str(s).isdigit()]
            
            # Fallback if no per-day slots were posted (legacy format)
            if not schedule and request.form.getlist('visiting_slot_ids'):
                legacy_slots = [int(s) for s in request.form.getlist('visiting_slot_ids') if str(s).isdigit()]
                schedule = {day: legacy_slots for day in visiting_days}

            faculty.set_visiting_days(visiting_days)
            faculty.set_visiting_slots(schedule)
        else:
            # Save regular working hours
            start_t = request.form.get('start_time')
            end_t = request.form.get('end_time')
            if start_t and end_t:
                faculty.set_working_hours(start_t, end_t)

        # Save subjects from checkboxes and custom input
        selected_subjects = request.form.getlist('subject_select')
        subjects_raw = request.form.get('subjects', '')
        raw_list = [s.strip() for s in subjects_raw.split(',') if s.strip()]
        
        combined_subjects = []
        for s in selected_subjects + raw_list:
            if s and s not in combined_subjects:
                combined_subjects.append(s)

        faculty.set_subjects(combined_subjects)

        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('faculty_profile'))

    # 🔹 FETCH FACULTY TIMETABLE & SUBJECTS
    timetable_entries = (
        Timetable.query
        .filter_by(faculty_id=faculty.id)
        .order_by(Timetable.day, Timetable.time_slot_id)
        .all()
    )

    timeslots = TimeSlot.query.order_by(TimeSlot.start_time).all()
    system_subjects = Subject.query.order_by(Subject.semester, Subject.code).all()

    return render_template(
        'faculty_profile.html',
        faculty=faculty,
        timetable_entries=timetable_entries,
        timeslots=timeslots,
        system_subjects=system_subjects
    )




@app.route('/faculty/timetable/<int:division_id>')
@login_required
def faculty_view_timetable(division_id):
    if current_user.role != 'faculty':
        flash('Access denied', 'danger')
        return redirect(url_for('login'))

    division = Division.query.get_or_404(division_id)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    timeslots = TimeSlot.query.order_by(TimeSlot.start_time).all()

    # Get all entries for this faculty and division
    entries = Timetable.query.filter_by(
        division_id=division_id,
        faculty_id=current_user.faculty_profile.id
    ).all()


    # Create grid: grid[day][time_slot_id] = entry
    grid = {}
    for day in days:
        grid[day] = {}
        for slot in timeslots:
            grid[day][slot.id] = None

    for entry in entries:
        grid[entry.day][entry.time_slot_id] = entry

    return render_template('faculty_view_timetable.html',
                         division=division,
                         days=days,
                         timeslots=timeslots,
                         grid=grid)

# ============================================
# 9️⃣ API ROUTES (BOTTOM)
# ============================================

@app.route('/api/divisions/<int:branch_id>')
def api_get_divisions(branch_id):
    divisions = Division.query.filter_by(branch_id=branch_id).all()
    return jsonify({
        'divisions': [{
            'id': d.id,
            'name': d.full_name,
            'semester': d.semester,
            'academic_year': d.academic_year
        } for d in divisions]
    })

@app.route('/api/faculty-availability')
def api_faculty_availability():
    day = request.args.get('day')
    time_slot_id = request.args.get('time_slot_id', type=int)
    subject = request.args.get('subject', '')
    
    faculty_list = ClashService.get_all_faculty_availability(day, time_slot_id, subject)
    
    return jsonify({'faculty': faculty_list})


@app.route('/api/faculty-matrix')
@admin_required
def api_faculty_matrix():
    """Return faculty x timeslot availability matrix for a given day."""
    day = request.args.get('day', 'Monday')
    division_id = request.args.get('division_id', type=int)

    timeslots = TimeSlot.query.order_by(TimeSlot.start_time).all()
    faculty_list = Faculty.query.join(User).filter(
        Faculty.is_available.is_(True),
        User.is_active.is_(True)
    ).all()

    matrix = []
    for fac in faculty_list:
        row = {
            'faculty_id': fac.id,
            'name': fac.user.full_name,
            'department': fac.department or '',
            'designation': fac.designation or '',
            'subjects': fac.get_subjects() or [],
            'is_visiting': fac.is_visiting,
            'slots': {}
        }
        for slot in timeslots:
            in_hours = fac.is_available_for_slot(day, slot)
            has_clash, _ = ClashService.check_faculty_clash(fac.id, day, slot.id)
            if has_clash:
                status = 'busy'
            elif not in_hours:
                status = 'unavailable'
            else:
                status = 'available'
            row['slots'][slot.id] = status
        matrix.append(row)

    return jsonify({
        'day': day,
        'timeslots': [{'id': s.id, 'time_range': s.time_range, 'label': s.slot_label or ''} for s in timeslots],
        'matrix': matrix
    })

@app.route('/api/subjects/search')
def api_search_subjects():
    query = request.args.get('q', '')
    semester = request.args.get('semester', type=int)
    branch_id = request.args.get('branch_id', type=int)

    q_filter = (Subject.name.ilike(f'%{query}%')) | (Subject.code.ilike(f'%{query}%'))
    base_query = Subject.query.filter(q_filter)

    if semester:
        base_query = base_query.filter((Subject.semester == semester) | (Subject.semester.is_(None)))
    if branch_id:
        base_query = base_query.filter((Subject.branch_id == branch_id) | (Subject.branch_id.is_(None)))

    subjects = base_query.limit(15).all()
    
    return jsonify({
        'subjects': [{
            'id': s.id,
            'name': s.name,
            'code': s.code,
            'display_name': s.display_name,
            'semester': s.semester,
            'branch': s.branch.short_name if s.branch else None
        } for s in subjects]
    })


@app.route('/search')
@admin_required
def global_search():
    """Global search across all entities in the system."""
    q = request.args.get('q', '').strip()
    results = {'faculty': [], 'subjects': [], 'divisions': [], 'branches': [], 'rooms': [], 'clashes': []}

    if q:
        # Faculty
        fac_q = Faculty.query.join(User).filter(
            (User.full_name.ilike(f'%{q}%')) |
            (User.email.ilike(f'%{q}%')) |
            (Faculty.department.ilike(f'%{q}%')) |
            (Faculty.designation.ilike(f'%{q}%'))
        ).limit(10).all()
        results['faculty'] = [{
            'id': f.id,
            'name': f.user.full_name,
            'email': f.user.email,
            'department': f.department or '',
            'is_visiting': f.is_visiting
        } for f in fac_q]

        # Subjects
        sub_q = Subject.query.filter(
            (Subject.name.ilike(f'%{q}%')) |
            (Subject.code.ilike(f'%{q}%'))
        ).limit(10).all()
        results['subjects'] = [{'id': s.id, 'name': s.name, 'code': s.code, 'credits': s.credits} for s in sub_q]

        # Divisions
        div_q = Division.query.join(Branch).filter(
            (Division.name.ilike(f'%{q}%')) |
            (Branch.name.ilike(f'%{q}%')) |
            (Branch.short_name.ilike(f'%{q}%')) |
            (Division.academic_year.ilike(f'%{q}%'))
        ).limit(10).all()
        results['divisions'] = [{'id': d.id, 'name': d.full_name, 'semester': d.semester, 'branch': d.branch.name} for d in div_q]

        # Branches
        br_q = Branch.query.filter(
            (Branch.name.ilike(f'%{q}%')) |
            (Branch.short_name.ilike(f'%{q}%'))
        ).limit(10).all()
        results['branches'] = [{'id': b.id, 'name': b.name, 'short_name': b.short_name} for b in br_q]

        # Rooms (from timetable entries)
        room_q = db.session.query(Timetable.room_number).filter(
            Timetable.room_number.ilike(f'%{q}%')
        ).distinct().limit(10).all()
        results['rooms'] = [r[0] for r in room_q if r[0]]

        # Clashes
        clash_q = ClashLog.query.filter(
            (ClashLog.clash_type.ilike(f'%{q}%')) |
            (ClashLog.severity.ilike(f'%{q}%')) |
            (ClashLog.clash_details.ilike(f'%{q}%'))
        ).order_by(ClashLog.detected_at.desc()).limit(10).all()
        results['clashes'] = [{
            'id': c.id,
            'type': c.clash_type,
            'severity': c.severity,
            'is_resolved': c.is_resolved,
            'detected_at': c.detected_at.strftime('%Y-%m-%d %H:%M'),
            'details': c.get_details()
        } for c in clash_q]

    total = sum(len(v) for v in results.values())
    return render_template('search_results.html', q=q, results=results, total=total)


# ============================================
# 🔟 ERROR HANDLERS (VERY BOTTOM)
# ============================================


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500


# ============================================
# 1️⃣1️⃣ CLASH MANAGEMENT
# ============================================

@app.route('/admin/clashes')
@admin_required
def view_clashes():
    """View all detected clashes"""
    clashes = ClashService.get_all_clashes(resolved=False)
    resolved_clashes = ClashService.get_all_clashes(resolved=True)
    
    return render_template('view_clashes.html',
                         clashes=clashes,
                         resolved_clashes=resolved_clashes)

@app.route('/admin/clashes/resolve/<int:clash_id>', methods=['POST'])
@admin_required
def resolve_clash(clash_id):
    ClashService.resolve_clash(clash_id, resolved_by_id=current_user.id)
    flash('Clash marked as resolved', 'success')
    return redirect(url_for('view_clashes'))

@app.route('/admin/clashes/clear-all', methods=['POST'])
@admin_required
def clear_all_clashes():
    """Clear all logged clashes from database"""
    try:
        count = db.session.query(ClashLog).delete()
        db.session.commit()
        flash(f'🧹 Successfully cleared all {count} logged clashes!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error clearing clashes: {str(e)}', 'danger')
    return redirect(url_for('view_clashes'))

@app.route('/api/ml/clash-suggestions/<int:clash_id>', methods=['GET'])
@admin_required
def api_clash_suggestions(clash_id):
    """Get ML-powered resolution suggestions for a specific clash"""
    try:
        result = ClashService.generate_resolution_suggestions(clash_id)
        return jsonify({
            'success': True,
            **result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'suggestions': []
        }), 400

@app.route('/admin/clashes/auto-resolve/<int:clash_id>', methods=['POST'])
@admin_required
def auto_resolve_clash(clash_id):
    """Apply an ML suggestion to auto-resolve a clash"""
    action_type = request.form.get('action_type')
    action_value = request.form.get('action_value')
    
    if not action_type or not action_value:
        flash('Missing action details', 'danger')
        return redirect(url_for('view_clashes'))
    
    success, message = ClashService.apply_suggestion(clash_id, action_type, action_value)
    
    if success:
        flash(f'✅ Clash auto-resolved: {message}', 'success')
    else:
        flash(f'❌ Could not resolve: {message}', 'danger')
    
    return redirect(url_for('view_clashes'))


# ============================================
# 🤖 ML-ENHANCED API ROUTES
# ============================================

@app.route('/api/ml/predict-clash-risk', methods=['POST'])
@admin_required
def api_predict_clash_risk():
    """Predict clash risk for a proposed timetable entry"""
    data = request.json
    
    try:
        risk = ClashService.predict_clash_risk(
            faculty_id=data.get('faculty_id'),
            division_id=data.get('division_id'),
            subject_id=data.get('subject_id'),
            time_slot_id=data.get('time_slot_id'),
            day=data.get('day'),
            room_number=data.get('room_number', '101')
        )
        
        return jsonify({
            'success': True,
            'risk': risk
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/ml/slot-recommendations', methods=['GET', 'POST'])
@admin_required
def api_slot_recommendations():
    """Get smart slot recommendations for a faculty"""
    if request.method == 'POST':
        data = request.json
        faculty_id = data.get('faculty_id')
        division_id = data.get('division_id')
        subject_id = data.get('subject_id')
        preferred_day = data.get('preferred_day', 'Monday')
    else:
        faculty_id = request.args.get('faculty_id', type=int)
        division_id = request.args.get('division_id', type=int)
        subject_id = request.args.get('subject_id', type=int)
        preferred_day = request.args.get('preferred_day', 'Monday')
    
    try:
        recommendations = ClashService.get_smart_slot_recommendations(
            faculty_id, division_id, subject_id, preferred_day
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/ml/recommend-faculty', methods=['GET', 'POST'])
@admin_required
def api_recommend_faculty():
    """Get ML-based faculty recommendations"""
    if request.method == 'POST':
        data = request.json
        subject_id = data.get('subject_id')
        division_id = data.get('division_id')
        preferred_day = data.get('preferred_day', 'Monday')
        preferred_time_slot_id = data.get('preferred_time_slot_id')
    else:
        subject_id = request.args.get('subject_id', type=int)
        division_id = request.args.get('division_id', type=int)
        preferred_day = request.args.get('preferred_day', 'Monday')
        preferred_time_slot_id = request.args.get('preferred_time_slot_id', type=int)
    
    try:
        recommendations = ClashService.recommend_best_faculty(
            subject_id, division_id, preferred_day, preferred_time_slot_id
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/ml/evaluate-timetable', methods=['POST'])
@admin_required
def api_evaluate_timetable():
    """Evaluate quality of entire timetable"""
    data = request.json
    timetable_entries = data.get('entries', [])
    division_id = data.get('division_id')
    
    try:
        if division_id and not timetable_entries:
            # Get all entries for division
            entries = Timetable.query.filter_by(division_id=division_id).all()
            timetable_entries = [
                {
                    'faculty_id': e.faculty_id,
                    'division_id': e.division_id,
                    'subject_id': e.subject_id,
                    'time_slot_id': e.time_slot_id,
                    'day': e.day,
                    'room_number': e.room_number
                }
                for e in entries
            ]
        
        quality = ClashService.evaluate_timetable_quality(timetable_entries)
        
        return jsonify({
            'success': True,
            'quality': quality
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/ml/clash-risk-summary', methods=['GET'])
@admin_required
def api_clash_risk_summary():
    """Get clash risk summary for divisions"""
    division_id = request.args.get('division_id', type=int)
    
    try:
        summary = ClashService.get_clash_risk_summary(division_id)
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# ============================================
# 🔹 AJAX APIs (Asynchronous Un-refreshed UI Operations)
# ============================================

@app.route('/api/division/<int:division_id>/subjects')
@login_required
def api_get_division_subjects(division_id):
    division = Division.query.get_or_404(division_id)
    subjects = Subject.query.filter(
        (Subject.semester == division.semester) | (Subject.semester.is_(None)),
        (Subject.branch_id == division.branch_id) | (Subject.branch_id.is_(None))
    ).order_by(Subject.name).all()
    if not subjects:
        subjects = Subject.query.order_by(Subject.name).all()
    
    subject_list = []
    for s in subjects:
        subject_list.append({
            'id': s.id,
            'name': s.name,
            'code': s.code,
            'display_name': s.display_name,
            'has_lab': s.has_lab,
            'required_lectures': s.required_lectures
        })
    return jsonify({'success': True, 'division_id': division_id, 'subjects': subject_list})


@app.route('/api/subject/<int:subject_id>/faculties')
@login_required
def api_get_subject_faculties(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    all_faculty = Faculty.query.filter_by(is_available=True).all()
    qualified = []
    
    sub_name_clean = subject.name.strip().lower()
    sub_code_clean = subject.code.strip().lower()

    for fac in all_faculty:
        fac_subs = [s.strip().lower() for s in fac.get_subjects()]
        is_qualified = any(
            sub_name_clean == fs or sub_code_clean == fs or sub_name_clean in fs or fs in sub_name_clean
            for fs in fac_subs
        )
        if not is_qualified and subject.branch:
            is_qualified = bool(fac.department and fac.department.lower() in subject.branch.name.lower())
        
        if is_qualified or not qualified:
            qualified.append({
                'id': fac.id,
                'name': fac.user.full_name,
                'department': fac.department or 'General',
                'is_visiting': fac.is_visiting
            })
            
    return jsonify({'success': True, 'subject_id': subject_id, 'faculties': qualified})


@app.route('/api/division/<int:division_id>/timetable-data')
@login_required
def api_get_timetable_data(division_id):
    division = Division.query.get_or_404(division_id)
    entries = Timetable.query.filter_by(division_id=division_id).all()
    timeslots = TimeSlot.query.order_by(TimeSlot.start_time).all()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    grid = {d: {ts.id: [] for ts in timeslots} for d in days}
    for e in entries:
        if e.day in grid and e.time_slot_id in grid[e.day]:
            grid[e.day][e.time_slot_id].append({
                'id': e.id,
                'entry_type': e.entry_type,
                'subject_name': e.subject.name if e.subject else ('LIBRARY' if e.entry_type == 'library' else 'BREAK'),
                'subject_code': e.subject.code if e.subject else '',
                'faculty_name': e.faculty.user.full_name if e.faculty and e.faculty.user else '',
                'room_number': e.room_number or '',
                'batch_name': e.batch.name if e.batch else '',
                'is_manual': e.is_manual
            })
            
    timeslots_info = [{'id': ts.id, 'time_range': ts.time_range, 'label': ts.slot_label} for ts in timeslots]
    
    return jsonify({
        'success': True,
        'division': {
            'id': division.id,
            'full_name': division.full_name,
            'semester': division.semester,
            'academic_year': division.academic_year
        },
        'days': days,
        'timeslots': timeslots_info,
        'grid': grid,
        'total_entries': len(entries)
    })


@app.route('/api/timetable/add-entry', methods=['POST'])
@login_required
def api_add_timetable_entry():
    data = request.get_json() or request.form
    division_id = int(data.get('division_id'))
    day = data.get('day')
    time_slot_id = int(data.get('time_slot_id'))
    entry_type = data.get('entry_type', 'lecture')
    
    if entry_type in ('library', 'break'):
        entry = Timetable(
            division_id=division_id, subject_id=None, faculty_id=None,
            time_slot_id=time_slot_id, batch_id=None, day=day, room_number='Library' if entry_type == 'library' else None,
            entry_type=entry_type, is_manual=True, created_by=current_user.id
        )
        db.session.add(entry)
        db.session.commit()
        return jsonify({'success': True, 'message': f'{entry_type.capitalize()} added successfully!', 'entry_id': entry.id})

    subject_id = int(data.get('subject_id'))
    faculty_id = int(data.get('faculty_id'))
    room_number = data.get('room_number')
    batch_id = int(data.get('batch_id')) if data.get('batch_id') else None

    faculty = Faculty.query.get_or_404(faculty_id)
    is_valid, clashes = ClashService.validate_and_detect_clashes(
        faculty.id, division_id, room_number, day, time_slot_id,
        batch_id=batch_id, entry_type=entry_type, subject_id=subject_id
    )

    if not is_valid:
        return jsonify({'success': False, 'message': clashes[0].get('message', 'Clash detected'), 'clashes': clashes}), 400

    entry = Timetable(
        division_id=division_id, subject_id=subject_id, faculty_id=faculty.id,
        time_slot_id=time_slot_id, batch_id=batch_id, day=day, room_number=room_number,
        entry_type=entry_type, is_manual=True, created_by=current_user.id
    )
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Entry added successfully!', 'entry_id': entry.id})


@app.route('/api/timetable/delete-entry/<int:entry_id>', methods=['POST', 'DELETE'])
@login_required
def api_delete_timetable_entry(entry_id):
    entry = Timetable.query.get_or_404(entry_id)
    division_id = entry.division_id
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Entry deleted successfully!', 'division_id': division_id})


@app.route('/api/auto-generate/<int:division_id>', methods=['POST'])
@login_required
def api_auto_generate(division_id):
    result = AutoTimetableGenerator.generate_timetable(division_id, overwrite=True, created_by=current_user.id)
    if result.get('success'):
        div = Division.query.get(division_id)
        d_name = div.full_name if div else f"ID #{division_id}"
        ActivityLog.log(
            action_type='AUTO_GENERATE',
            description=f'✨ Auto-generated 100% clash-free timetable for Division {d_name} ({result.get("total_entries", 0)} entries created)',
            user_id=current_user.id,
            user_name=getattr(current_user, 'full_name', 'User'),
            entity_type='division',
            entity_id=division_id,
            details=result
        )
    return jsonify(result)


# ============================================
# 📜 ACTIVITY HISTORY & USER PROFILE ROUTES
# ============================================

@app.route('/admin/activity-log')
@login_required
def activity_log():
    """View overall system activity history log"""
    q = (request.args.get('q') or '').strip()
    action_type = (request.args.get('action_type') or '').strip()
    
    query = ActivityLog.query.order_by(ActivityLog.created_at.desc())
    
    if action_type:
        query = query.filter(ActivityLog.action_type == action_type)
    if q:
        query = query.filter(
            (ActivityLog.description.ilike(f'%{q}%')) |
            (ActivityLog.user_name.ilike(f'%{q}%')) |
            (ActivityLog.entity_type.ilike(f'%{q}%'))
        )
    
    logs = query.limit(300).all()
    return render_template('activity_log.html', logs=logs, q=q, selected_action=action_type)


@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    """View and edit current user's profile settings"""
    user = User.query.get_or_404(current_user.id)
    faculty = Faculty.query.filter_by(user_id=user.id).first()
    
    if request.method == 'POST':
        full_name = (request.form.get('full_name') or '').strip()
        username = (request.form.get('username') or '').strip()
        email = (request.form.get('email') or '').strip()
        new_password = request.form.get('new_password')
        
        department = request.form.get('department')
        designation = request.form.get('designation')
        
        # Check duplicate username/email if changed
        if username != user.username and User.query.filter_by(username=username).first():
            flash('⚠️ Username is already taken!', 'danger')
            return redirect(url_for('admin_profile'))
            
        if email != user.email and User.query.filter_by(email=email).first():
            flash('⚠️ Email address is already registered!', 'danger')
            return redirect(url_for('admin_profile'))
            
        user.full_name = full_name
        user.username = username
        user.email = email
        
        if new_password and len(new_password.strip()) > 0:
            user.set_password(new_password.strip())
            
        if faculty:
            faculty.department = department
            faculty.designation = designation
            
        db.session.commit()
        
        # Update session info
        session['name'] = user.full_name
        session['username'] = user.username
        
        ActivityLog.log(
            action_type='PROFILE_UPDATE',
            description=f'Updated account profile details for {user.full_name} (@{user.username})',
            user_id=user.id,
            user_name=user.full_name,
            entity_type='user',
            entity_id=user.id
        )
        
        flash('✨ Your profile details have been updated successfully!', 'success')
        return redirect(url_for('admin_profile'))
        
    return render_template('admin_profile.html', user=user, faculty=faculty)


# ============================================
# 1️⃣2️⃣RUN APP (LAST LINE)
# ============================================

# Auto-create tables (needed for Render deployment)
try:
    with app.app_context():
        db.create_all()
        
        # Auto-migrate missing columns for existing databases
        from sqlalchemy import text
        migrations = [
            "ALTER TABLE faculty ADD COLUMN is_visiting BOOLEAN DEFAULT FALSE",
            "ALTER TABLE faculty ADD COLUMN visiting_available_days TEXT",
            "ALTER TABLE faculty ADD COLUMN visiting_slot_ids TEXT",
            "ALTER TABLE clash_logs ADD COLUMN resolved_by INT",
            "ALTER TABLE clash_logs ADD COLUMN resolution_method VARCHAR(20)",
            "ALTER TABLE clash_logs ADD COLUMN resolution_note TEXT",
            "ALTER TABLE clash_logs MODIFY COLUMN clash_type VARCHAR(50)",
            # Batch / Library / Workload migrations
            "ALTER TABLE divisions ADD COLUMN student_count INT DEFAULT 60",
            "ALTER TABLE divisions ADD COLUMN num_batches INT DEFAULT 1",
            "ALTER TABLE timetable ADD COLUMN batch_id INT",
            "ALTER TABLE timetable ADD COLUMN entry_type VARCHAR(20) DEFAULT 'lecture'",
            "ALTER TABLE timetable MODIFY COLUMN subject_id INT NULL",
            "ALTER TABLE timetable MODIFY COLUMN faculty_id INT NULL",
            "ALTER TABLE timetable MODIFY COLUMN room_number VARCHAR(50) NULL",
        ]
        for stmt in migrations:
            try:
                db.session.execute(text(stmt))
                db.session.commit()
            except Exception:
                db.session.rollback()  # Column already exists or table structure matches

        # Seed default admin user if it does not exist
        from models import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@timetable.com',
                full_name='System Administrator',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("[OK] Seeded default admin user ('admin' / 'admin123')")
except Exception as e:
    print(f"[WARNING] Could not initialize database tables: {e}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
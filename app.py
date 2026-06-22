# ============================================
# 1️⃣ IMPORTS
# ============================================

import os
from flask import Flask
from extensions import db
from models import ClashLog, User, Faculty, Branch, Division, Subject, TimeSlot, Timetable
from services.clash_service import ClashService
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from datetime import datetime
from flask_login import LoginManager, current_user, login_user, logout_user, login_required


# ============================================
# 2️⃣ APP CONFIGURATION
# ============================================


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Database URI: use DATABASE_URL env var (Render/Aiven), fallback to SQLite
database_url = os.environ.get('DATABASE_URL', 'sqlite:///timetable.db')
# Render PostgreSQL uses postgres:// but SQLAlchemy needs postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
# Aiven MySQL uses mysql:// but we need mysql+pymysql:// for PyMySQL driver
if database_url.startswith('mysql://'):
    database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
        recent_clashes=recent_clashes,
        division_summary=division_summary
    )




# ============================================
# 6️⃣ ADMIN MANAGEMENT MODULES (ORDER MATTERS)
# ============================================

# ============================================
# 🔹 Branches
# ============================================

@app.route('/admin/branches')
@admin_required
def manage_branches():
    branches = Branch.query.all()
    return render_template('manage_branches.html', branches=branches)


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
    branches = Branch.query.all()
    divisions = Division.query.order_by(Division.semester).all()

    return render_template(
        'manage_divisions.html',
        branches=branches,
        divisions=divisions
    )



@app.route('/admin/divisions', methods=['GET', 'POST'])
@admin_required
def add_division():
    if request.method == 'POST':
        branch_id = request.form.get('branch_id', type=int)
        name = request.form.get('name')
        semester = request.form.get('semester', type=int)
        academic_year = request.form.get('academic_year')
        
        division = Division(
            branch_id=branch_id,
            name=name,
            semester=semester,
            academic_year=academic_year
        )
        db.session.add(division)
        db.session.commit()
        
        flash('Division added successfully', 'success')
        return redirect(url_for('add_division'))
    
    branches = Branch.query.all()
    divisions = Division.query.all()
    return render_template('manage_divisions.html',
                         branches=branches,
                         divisions=divisions)




@app.route('/division/edit', methods=['POST'])
@admin_required
def edit_division():
    division_id = request.form.get('division_id', type=int)
    branch_id = request.form.get('branch_id', type=int)
    name = request.form.get('name')
    semester = request.form.get('semester', type=int)
    academic_year = request.form.get('academic_year')

    division = Division.query.get_or_404(division_id)

    division.branch_id = branch_id
    division.name = name
    division.semester = semester
    division.academic_year = academic_year

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
# 🔹 Subjects
# ============================================

@app.route('/admin/subjects')
@admin_required
def manage_subjects():
    subjects = Subject.query.order_by(Subject.code).all()
    return render_template(
        'manage_subjects.html',
        subjects=subjects
    )



@app.route('/admin/subjects/add', methods=['POST'])
@admin_required
def add_subject():
    subject = Subject(
        name=request.form['name'],
        code=request.form['code'],
        credits=request.form['credits'],
        created_by=current_user.id
    )
    db.session.add(subject)
    db.session.commit()
    flash('Subject added', 'success')
    return redirect(url_for('manage_subjects'))


@app.route('/subject/edit', methods=['POST'])
@admin_required
def edit_subject():
    subject_id = request.form.get('subject_id', type=int)
    name = request.form.get('name')
    code = request.form.get('code')
    credits = request.form.get('credits', type=int)

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
    timeslots = TimeSlot.query.order_by(TimeSlot.start_time).all()
    return render_template('manage_timeslots.html', timeslots=timeslots)

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
    search = request.args.get('search', '')
    
    query = Faculty.query.join(User)
    if search:
        query = query.filter(
            (User.full_name.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )
    
    faculty_list = query.all()
    return render_template('manage_faculty.html', faculty_list=faculty_list, search=search)

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




# ============================================
# 7️⃣ TIMETABLE MODULE (ADMIN)
# ============================================

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

    timetable_map = {entry.time_slot_id: entry for entry in timetable_entries}

    faculty_availability = {}
    for slot in timeslots:
        faculty_availability[slot.id] = ClashService.get_all_faculty_availability(day, slot.id)

    # ✅ THIS WAS MISSING
    subjects = Subject.query.order_by(Subject.name).all()


    return render_template(
    'timetable_create.html',
    division=division,
    days=days,
    current_day=day,
    timeslots=timeslots,
    timetable_map=timetable_map,
    faculty_availability=faculty_availability,
    subjects=subjects
)

@app.route('/timetable/add-entry', methods=['POST'])
@admin_required
def add_timetable_entry():

    division_id = request.form.get('division_id', type=int)
    subject_id = request.form.get('subject_id', type=int)
    faculty_id = request.form.get('faculty_id', type=int)  # from dropdown
    time_slot_id = request.form.get('time_slot_id', type=int)
    day = request.form.get('day')
    room_number = request.form.get('room_number')

    # ✅ GET FACULTY OBJECT
    faculty = Faculty.query.get_or_404(faculty_id)

    # Validate clashes (PASS faculty.id)
    is_valid, clashes = ClashService.validate_and_detect_clashes(
        faculty.id, division_id, room_number, day, time_slot_id
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
            flash(f"Clash detected: {clash['type']}", 'danger')

        return redirect(url_for(
            'timetable_create',
            division_id=division_id,
            day=day
        ))

    # ✅ SAVE faculty.id (THIS IS THE KEY)
    entry = Timetable(
        division_id=division_id,
        subject_id=subject_id,
        faculty_id=faculty.id,   # ✅ FIXED
        time_slot_id=time_slot_id,
        day=day,
        room_number=room_number,
        created_by=session['user_id']
    )

    db.session.add(entry)
    db.session.commit()

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
            entry.day, entry.time_slot_id, entry.id
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
        entry.time_slot_id,
        entry.subject.name
    )
    
    return render_template('edit_timetable_entry.html',
                         entry=entry,
                         faculty_list=faculty_list)

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
    
    # Create grid: grid[day][time_slot_id] = entry
    grid = {}
    for day in days:
        grid[day] = {}
        for slot in timeslots:
            grid[day][slot.id] = None
    
    for entry in entries:
        grid[entry.day][entry.time_slot_id] = entry
    
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
        faculty.phone = request.form.get('phone')
        faculty.department = request.form.get('department')
        faculty.designation = request.form.get('designation')

        faculty.set_working_hours(
            request.form.get('start_time'),
            request.form.get('end_time')
        )

        subjects_raw = request.form.get('subjects', '')
        subjects_list = [
        s.strip()
        for s in subjects_raw.split(',')
            if s.strip()
        ]

        faculty.set_subjects(subjects_list)

        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('faculty_profile'))

    # 🔹 FETCH FACULTY TIMETABLE
    timetable_entries = (
        Timetable.query
        .filter_by(faculty_id=faculty.id)
        .order_by(Timetable.day, Timetable.time_slot_id)
        .all()
    )

    return render_template(
        'faculty_profile.html',
        faculty=faculty,
        timetable_entries=timetable_entries
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

@app.route('/api/subjects/search')
def api_search_subjects():
    query = request.args.get('q', '')
    subjects = Subject.query.filter(
        (Subject.name.ilike(f'%{query}%')) |
        (Subject.code.ilike(f'%{query}%'))
    ).limit(10).all()
    
    return jsonify({
        'subjects': [{
            'id': s.id,
            'name': s.name,
            'code': s.code
        } for s in subjects]
    })


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
    ClashService.resolve_clash(clash_id)
    flash('Clash marked as resolved', 'success')
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

@app.route('/api/ml/train-model', methods=['POST'])
@admin_required
def api_train_model():
    """Train/retrain the ML clash prediction model"""
    try:
        success = ClashService.train_clash_prediction_model()
        
        return jsonify({
            'success': success,
            'message': 'Model trained successfully' if success else 'Model training failed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


# ============================================
# 1️⃣2️⃣RUN APP (LAST LINE)
# ============================================

# Auto-create tables (needed for Render deployment)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
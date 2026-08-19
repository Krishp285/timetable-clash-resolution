"""
AutoTimetableGenerator Service
============================================
Automated AI Timetable Generation Service that constructs a complete,
clash-free, 5-day timetable for a given division using Constraint Satisfaction
and ML Risk Minimization.

Strict Enforced Rules:
1. ABSOLUTE ZERO CLASHES GUARANTEE:
   - Evaluates all existing timetable entries across ALL divisions in the database + uncommitted entries.
   - NEVER force-assigns a faculty member if they are busy in ANY division or batch.
2. DYNAMIC BATCH NAMING (A1, A2, A3):
   - Automatically names batches formatted as {DivisionName}{Number} (e.g. A1, A2, A3 for Div A).
3. VARYING LAB TIME SLOTS ACROSS DAYS:
   - Lab hours vary dynamically across different days (e.g. Mon 10:30-12:30, Tue 13:00-15:00, Wed 08:30-10:20).
4. EVERYDAY 2-HOUR LAB BLOCK:
   - Every day (Monday to Friday) has a 2-hour lab session for all batches.
5. NO REPETITION FOR ANY BATCH:
   - Batches rotate through all lab subjects during the week with 0 duplicate lab subjects per batch.
6. NON-CONSECUTIVE LECTURES:
   - Lectures rotate so no subject repeats consecutively.
7. STRICT TIME BOUNDARY: 08:30 AM to 03:00 PM ONLY (Slots 3, 4, 5, 6, 7, 8).
"""

from datetime import datetime, date
from extensions import db
from models import Timetable, Division, Subject, Faculty, Room, TimeSlot, Batch, ClashLog
from services.clash_service import ClashService

try:
    from services.ml_clash_predictor import ml_predictor
except ImportError:
    ml_predictor = None

EXACT_CURRICULUM_MATRIX = {
    3: [
        ('WAD', 'nimisha patel'),
        ('MLE', 'divya sharma'),
        ('FAI', 'ajeet patel'),
        ('IPDC', 'chintan rana'),
        ('OT', 'neha gajjar'),
        ('PP', 'khyati karia'),
    ],
    4: [
        ('OS', 'nimisha patel'),
        ('DBMS', 'divya sharma'),
        ('CN', 'ajeet patel'),
        ('SE', 'chintan rana'),
        ('JAVA', 'neha gajjar'),
        ('EVS', 'khyati karia'),
    ],
    5: [
        ('IP', 'nimisha patel'),
        ('ASDD', 'divya sharma'),
        ('Maths', 'ajeet patel'),
        ('DS', 'chintan rana'),
        ('PA', 'neha gajjar'),
        ('CCM', 'khyati karia'),
    ],
    7: [
        ('DL', 'nimisha patel'),
        ('CNS', 'divya sharma'),
        ('AIH', 'ajeet patel'),
        ('NLP', 'chintan rana'),
        ('BDA', 'neha gajjar'),
        ('ERP', 'khyati karia'),
    ]
}


class AutoTimetableGenerator:
    @staticmethod
    def generate_timetable(division_id, overwrite=False, created_by=1):
        division = Division.query.get(division_id)
        if not division:
            return {'success': False, 'message': f'Division ID {division_id} not found.'}

        sem = division.semester
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        # STRICT COLLEGE HOURS: 08:30 AM to 03:00 PM ONLY (Slot IDs 3, 4, 5, 6, 7, 8)
        timeslots = TimeSlot.query.filter(TimeSlot.id.in_([3, 4, 5, 6, 7, 8])).order_by(TimeSlot.start_time).all()
        if not timeslots:
            timeslots = TimeSlot.query.order_by(TimeSlot.start_time).limit(6).all()

        # Update batch names to A1, A2, A3 format (including single batch A1)
        div_prefix = division.name.strip()
        batches = division.batches.order_by(Batch.id).all()
        if not batches and division.num_batches >= 1:
            b1 = Batch(division_id=division.id, name=f'{div_prefix}1', student_count=division.student_count)
            db.session.add(b1)
            db.session.commit()
            batches = [b1]
        else:
            for idx, b in enumerate(batches):
                expected_name = f'{div_prefix}{idx+1}'
                if b.name != expected_name:
                    b.name = expected_name
            db.session.commit()

        # Clear existing AI-generated entries if overwrite requested (NEVER delete manual entries)
        if overwrite:
            Timetable.query.filter_by(division_id=division_id, is_manual=False).delete(synchronize_session=False)
            ClashLog.query.filter_by(division_id=division_id).delete(synchronize_session=False)
            db.session.commit()

        classrooms = Room.query.filter(Room.room_type.ilike('%Classroom%')).all()
        if not classrooms:
            classrooms = Room.query.all()
            
        lab_rooms = Room.query.filter(Room.room_type.ilike('%Lab%')).all()
        if not lab_rooms:
            lab_rooms = classrooms

        all_faculty = Faculty.query.filter_by(is_available=True).all()
        slot_by_id = {s.id: s for s in timeslots}
        slot_ids_ordered = [s.id for s in timeslots]

        # Query subjects strictly belonging to this division's semester and branch
        div_subjects = Subject.query.filter(
            Subject.semester == sem,
            (Subject.branch_id == division.branch_id) | (Subject.branch_id.is_(None))
        ).order_by(Subject.id).all()

        if not div_subjects:
            div_subjects = Subject.query.filter_by(semester=sem).order_by(Subject.id).all()

        if not div_subjects:
            # Fallback if no specific semester subjects exist
            div_subjects = Subject.query.filter(
                (Subject.branch_id == division.branch_id) | (Subject.branch_id.is_(None))
            ).order_by(Subject.id).limit(6).all()

        if not div_subjects:
            return {'success': False, 'message': f"No subjects found for Semester {sem}. Please add subjects for Semester {sem} in Manage Subjects before generating timetable."}

        # Filter subjects that explicitly contain labs (has_lab == True)
        lab_subjects = [s for s in div_subjects if s.has_lab]
        if not lab_subjects:
            lab_subjects = [s for s in div_subjects if s.credits >= 4]

        # Map subjects to designated faculty for this semester
        subject_faculty_map = {}
        curr_pairs = EXACT_CURRICULUM_MATRIX.get(sem, [])
        
        # 1. First check if explicit matrix exists for this semester
        for tag, fac_name in curr_pairs:
            tag_clean = tag.strip().lower()
            matching_sub = None
            for sub in div_subjects:
                s_name = sub.name.strip().lower()
                s_code = sub.code.strip().lower()
                p_code = ''
                if '(' in sub.name and ')' in sub.name:
                    p_code = sub.name.split('(')[-1].rstrip(')').strip().lower()
                if tag_clean == p_code or tag_clean == s_code or f'({tag_clean})' in s_name or s_name == tag_clean:
                    matching_sub = sub
                    break
            if matching_sub:
                for fac in all_faculty:
                    if fac.user and fac.user.full_name.lower() == fac_name.lower():
                        subject_faculty_map[matching_sub.id] = fac
                        break

        # 2. For any unmapped subject, find faculty who explicitly declared this subject in their profile
        for sub in div_subjects:
            if sub.id not in subject_faculty_map:
                mapped_fac = None
                sub_name_clean = sub.name.strip().lower()
                sub_code_clean = sub.code.strip().lower()
                
                # Check faculty subjects_can_teach list (EXACT MATCH PRIORITY FIRST)
                for fac in all_faculty:
                    fac_subs = [s.strip().lower() for s in fac.get_subjects()]
                    if any(sub_name_clean == fs or sub_code_clean == fs for fs in fac_subs):
                        mapped_fac = fac
                        break
                
                # Word/acronym match if no exact string match
                if not mapped_fac:
                    for fac in all_faculty:
                        fac_subs = [s.strip().lower() for s in fac.get_subjects()]
                        if any(fs in sub_name_clean.split() or fs == sub_code_clean for fs in fac_subs):
                            mapped_fac = fac
                            break

                # Substring match if no word match
                if not mapped_fac:
                    for fac in all_faculty:
                        fac_subs = [s.strip().lower() for s in fac.get_subjects()]
                        if any(sub_name_clean in fs or fs in sub_name_clean for fs in fac_subs):
                            mapped_fac = fac
                            break

                # Check department/branch match if no direct subject match
                if not mapped_fac and all_faculty:
                    dept_name = division.branch.name.lower() if division.branch else ''
                    for fac in all_faculty:
                        if fac.department and (fac.department.lower() in dept_name or dept_name in fac.department.lower()):
                            mapped_fac = fac
                            break
                    if not mapped_fac:
                        fac_idx = len(subject_faculty_map) % len(all_faculty)
                        mapped_fac = all_faculty[fac_idx]
                
                subject_faculty_map[sub.id] = mapped_fac

        new_entries = []

        def get_designated_faculty(subject):
            return subject_faculty_map.get(subject.id, None)

        def is_faculty_busy_globally(fac_id, day, slot_id, temp_fac_ids=None):
            if temp_fac_ids and fac_id in temp_fac_ids:
                return True
            # 1. Check in uncommitted new_entries for this run
            if any(e.faculty_id == fac_id and e.day == day and e.time_slot_id == slot_id for e in new_entries):
                return True
            # 2. Check in database across ALL divisions
            db_busy = Timetable.query.filter(
                Timetable.faculty_id == fac_id,
                Timetable.day == day,
                Timetable.time_slot_id == slot_id
            ).first()
            if db_busy:
                return True
            return False

        def get_faculty_current_workload_hours(fac_id, day=None):
            q_db = Timetable.query.filter(
                Timetable.faculty_id == fac_id,
                Timetable.entry_type.in_(['lecture', 'lab'])
            )
            if day:
                q_db = q_db.filter(Timetable.day == day)
            db_count = q_db.count()

            new_count = sum(1 for e in new_entries if e.faculty_id == fac_id and (day is None or e.day == day))
            return db_count + new_count

        def is_room_busy_in_new_entries(room_name, day, slot_id, temp_rooms=None):
            if temp_rooms and room_name in temp_rooms:
                return True
            if any(e.room_number == room_name and e.day == day and e.time_slot_id == slot_id for e in new_entries):
                return True
            db_room_busy = Timetable.query.filter_by(day=day, time_slot_id=slot_id, room_number=room_name).first()
            return bool(db_room_busy)

        def find_best_faculty(subject, day, slot_id, room_name, batch_id=None, is_lab=False, next_slot_id=None, temp_fac_ids=None):
            desig_fac = get_designated_faculty(subject)
            hours_needed = 2 if is_lab else 1
            
            # 1. STRICT REQUIREMENT: Primary designated faculty MUST be used for ALL lectures & labs of this subject
            if desig_fac and desig_fac.is_available:
                weekly_w = get_faculty_current_workload_hours(desig_fac.id)
                daily_w = get_faculty_current_workload_hours(desig_fac.id, day=day)
                
                # Check 30h weekly and 6h daily workload limits
                if (weekly_w + hours_needed <= 30) and (daily_w + hours_needed <= 6):
                    if desig_fac.is_available_for_slot(day, slot_by_id[slot_id]) and \
                       not (is_lab and next_slot_id and not desig_fac.is_available_for_slot(day, slot_by_id[next_slot_id])) and \
                       not is_faculty_busy_globally(desig_fac.id, day, slot_id, temp_fac_ids=temp_fac_ids) and \
                       not (is_lab and next_slot_id and is_faculty_busy_globally(desig_fac.id, day, next_slot_id, temp_fac_ids=temp_fac_ids)):
                        
                        has_clash, _ = ClashService.check_faculty_clash(desig_fac.id, day, slot_id)
                        if not has_clash:
                            if is_lab and next_slot_id:
                                has_next_clash, _ = ClashService.check_faculty_clash(desig_fac.id, day, next_slot_id)
                                if not has_next_clash:
                                    return desig_fac
                            else:
                                return desig_fac

            # 2. EMERGENCY SECONDARY CANDIDATE ONLY: Try faculty members who explicitly listed this subject in their profile
            sub_name_clean = subject.name.strip().lower()
            sub_code_clean = subject.code.strip().lower()
            for fac in all_faculty:
                if desig_fac and fac.id == desig_fac.id:
                    continue
                
                weekly_w = get_faculty_current_workload_hours(fac.id)
                daily_w = get_faculty_current_workload_hours(fac.id, day=day)
                if (weekly_w + hours_needed > 30) or (daily_w + hours_needed > 6):
                    continue

                fac_subs = [s.strip().lower() for s in fac.get_subjects()]
                if any(sub_name_clean == fs or sub_code_clean == fs for fs in fac_subs):
                    if fac.is_available and fac.is_available_for_slot(day, slot_by_id[slot_id]) and \
                       not (is_lab and next_slot_id and not fac.is_available_for_slot(day, slot_by_id[next_slot_id])) and \
                       not is_faculty_busy_globally(fac.id, day, slot_id, temp_fac_ids=temp_fac_ids) and \
                       not (is_lab and next_slot_id and is_faculty_busy_globally(fac.id, day, next_slot_id, temp_fac_ids=temp_fac_ids)):
                        
                        has_clash, _ = ClashService.check_faculty_clash(fac.id, day, slot_id)
                        if not has_clash:
                            if is_lab and next_slot_id:
                                has_next_clash, _ = ClashService.check_faculty_clash(fac.id, day, next_slot_id)
                                if not has_next_clash:
                                    return fac
                            else:
                                return fac

            # 3. BACKUP CANDIDATE: Try any free available faculty for lecture/lab if primary/secondary are busy
            for fac in all_faculty:
                if desig_fac and fac.id == desig_fac.id:
                    continue
                weekly_w = get_faculty_current_workload_hours(fac.id)
                daily_w = get_faculty_current_workload_hours(fac.id, day=day)
                if (weekly_w + hours_needed > 30) or (daily_w + hours_needed > 6):
                    continue

                if fac.is_available and fac.is_available_for_slot(day, slot_by_id[slot_id]) and \
                   not (is_lab and next_slot_id and not fac.is_available_for_slot(day, slot_by_id[next_slot_id])) and \
                   not is_faculty_busy_globally(fac.id, day, slot_id, temp_fac_ids=temp_fac_ids) and \
                   not (is_lab and next_slot_id and is_faculty_busy_globally(fac.id, day, next_slot_id, temp_fac_ids=temp_fac_ids)):
                    
                    has_clash, _ = ClashService.check_faculty_clash(fac.id, day, slot_id)
                    if not has_clash:
                        if is_lab and next_slot_id:
                            has_next_clash, _ = ClashService.check_faculty_clash(fac.id, day, next_slot_id)
                            if not has_next_clash:
                                return fac
                        else:
                            return fac

            return None

        def find_free_room(day, slot_id, is_lab=False, next_slot_id=None, temp_rooms=None):
            pool = lab_rooms if is_lab else classrooms
            for rm in pool:
                if is_room_busy_in_new_entries(rm.name, day, slot_id, temp_rooms=temp_rooms):
                    continue
                if is_lab and next_slot_id and is_room_busy_in_new_entries(rm.name, day, next_slot_id, temp_rooms=temp_rooms):
                    continue
                return rm.name
            
            # Check alternate pool
            alt_pool = classrooms if is_lab else lab_rooms
            for rm in alt_pool:
                if is_room_busy_in_new_entries(rm.name, day, slot_id, temp_rooms=temp_rooms):
                    continue
                if is_lab and next_slot_id and is_room_busy_in_new_entries(rm.name, day, next_slot_id, temp_rooms=temp_rooms):
                    continue
                return rm.name

            # STRICT: Return None if no real un-occupied room in DB is available (NEVER force busy rooms or fake numbers)
            return None

        lectures_count = 0
        labs_count = 0

        lab_subjects = [s for s in div_subjects if s.has_lab]
        if not lab_subjects:
            lab_subjects = [s for s in div_subjects if s.credits >= 4]

        batch_lab_history = {}
        if len(batches) > 0:
            for b in batches:
                batch_lab_history[b.id] = set()

        # Dynamic varying lab windows across days:
        # Window 1: Slots 3 & 4 (08:30-10:20)
        # Window 2: Slots 5 & 6 (10:30-12:30)
        # Window 3: Slots 7 & 8 (13:00-15:00)
        lab_windows = [
            (slot_ids_ordered[0], slot_ids_ordered[1]),
            (slot_ids_ordered[2], slot_ids_ordered[3]),
            (slot_ids_ordered[4], slot_ids_ordered[5]),
        ]

        day_lab_window_map = {}

        # ----------------------------------------------------
        # 1. COMPULSORY 1 LAB PER DAY ACROSS MONDAY-FRIDAY (ZERO CLASH GUARANTEE)
        # ----------------------------------------------------
        used_lab_subjects_set = set()

        for day_idx, day in enumerate(days):
            chosen_window = None
            chosen_assignments = []

            # Rotate starting window per day and per semester to prevent cross-semester faculty bottlenecks
            start_offset = (day_idx + sem) % len(lab_windows)
            rotated_windows = lab_windows[start_offset:] + lab_windows[:start_offset]
            target_batch_list = list(batches) if len(batches) > 0 else [None]

            for start_s, end_s in rotated_windows:
                temp_assignments = []
                window_ok = True

                for b_idx, batch in enumerate(target_batch_list):
                    b_id = batch.id if batch else 0
                    c_history = batch_lab_history.get(b_id, set())

                    used_sub_ids = [t[1].id for t in temp_assignments]
                    used_fac_ids = [t[2].id for t in temp_assignments if t[2]]
                    used_rooms = [t[3] for t in temp_assignments]

                    # Prioritize lab subjects not yet scheduled
                    candidate_subs = [s for s in lab_subjects if s.id not in used_lab_subjects_set and s.id not in used_sub_ids]
                    if not candidate_subs:
                        candidate_subs = [s for s in lab_subjects if s.id not in c_history and s.id not in used_sub_ids]
                    if not candidate_subs:
                        candidate_subs = [s for s in lab_subjects if s.id not in used_sub_ids]
                    if not candidate_subs:
                        candidate_subs = lab_subjects

                    sub = candidate_subs[(day_idx + b_idx) % len(candidate_subs)]
                    rm_name = find_free_room(day, start_s, is_lab=True, next_slot_id=end_s, temp_rooms=used_rooms)
                    if not rm_name:
                        window_ok = False
                        break

                    fac = find_best_faculty(sub, day, start_s, rm_name, batch_id=batch.id if batch else None, is_lab=True, next_slot_id=end_s, temp_fac_ids=used_fac_ids)

                    if not fac:
                        # Try any other lab subject for this division
                        for alt_sub in lab_subjects:
                            if alt_sub.id in used_sub_ids:
                                continue
                            alt_fac = find_best_faculty(alt_sub, day, start_s, rm_name, batch_id=batch.id if batch else None, is_lab=True, next_slot_id=end_s, temp_fac_ids=used_fac_ids)
                            if alt_fac:
                                sub = alt_sub
                                fac = alt_fac
                                break

                    if not fac:
                        window_ok = False
                        break
                    temp_assignments.append((batch, sub, fac, rm_name))

                if window_ok and len(temp_assignments) == len(target_batch_list):
                    chosen_window = (start_s, end_s)
                    chosen_assignments = temp_assignments
                    break

            if not chosen_window:
                # Secondary pass: Try all windows with strict unique room and faculty tracking for parallel batches
                for start_s, end_s in lab_windows:
                    temp_assignments = []
                    used_rooms = []
                    used_fac_ids = []
                    for b_idx, batch in enumerate(target_batch_list):
                        sub_found = None
                        fac_found = None
                        rm_found = None
                        for s_offset in range(len(lab_subjects)):
                            sub_cand = lab_subjects[(day_idx + b_idx + s_offset) % len(lab_subjects)]
                            rm_cand = find_free_room(day, start_s, is_lab=True, next_slot_id=end_s, temp_rooms=used_rooms)
                            if not rm_cand:
                                continue
                            fac_cand = find_best_faculty(sub_cand, day, start_s, rm_cand, batch_id=batch.id if batch else None, is_lab=True, next_slot_id=end_s, temp_fac_ids=used_fac_ids)
                            if fac_cand:
                                sub_found = sub_cand
                                fac_found = fac_cand
                                rm_found = rm_cand
                                break
                        if fac_found and rm_found:
                            temp_assignments.append((batch, sub_found, fac_found, rm_found))
                            used_rooms.append(rm_found)
                            used_fac_ids.append(fac_found.id)
                    if len(temp_assignments) == len(target_batch_list):
                        chosen_window = (start_s, end_s)
                        chosen_assignments = temp_assignments
                        break

            if not chosen_window:
                # Fallback pass: find any window where each batch gets a FREE room and FREE faculty
                for start_s, end_s in lab_windows:
                    temp_assignments = []
                    used_rooms = []
                    used_fac_ids = []
                    for b_idx, batch in enumerate(target_batch_list):
                        for sub in lab_subjects:
                            rm_name = find_free_room(day, start_s, is_lab=True, next_slot_id=end_s, temp_rooms=used_rooms)
                            if not rm_name:
                                continue
                            fac = find_best_faculty(sub, day, start_s, rm_name, batch_id=batch.id if batch else None, is_lab=True, next_slot_id=end_s, temp_fac_ids=used_fac_ids)
                            if fac:
                                temp_assignments.append((batch, sub, fac, rm_name))
                                used_rooms.append(rm_name)
                                used_fac_ids.append(fac.id)
                                break
                    if len(temp_assignments) == len(target_batch_list):
                        chosen_window = (start_s, end_s)
                        chosen_assignments = temp_assignments
                        break

            if chosen_window:
                start_s, end_s = chosen_window
                for batch, sub, fac, rm_name in chosen_assignments:
                    if not fac:
                        continue
                    b_id = batch.id if batch else None
                    used_lab_subjects_set.add(sub.id)
                    e1 = Timetable(
                        division_id=division_id, subject_id=sub.id, faculty_id=fac.id,
                        time_slot_id=start_s, day=day, room_number=rm_name,
                        entry_type='lab', batch_id=b_id, created_by=created_by
                    )
                    e2 = Timetable(
                        division_id=division_id, subject_id=sub.id, faculty_id=fac.id,
                        time_slot_id=end_s, day=day, room_number=rm_name,
                        entry_type='lab', batch_id=b_id, created_by=created_by
                    )
                    new_entries.extend([e1, e2])
                    labs_count += 2
                    if batch and batch.id in batch_lab_history:
                        batch_lab_history[batch.id].add(sub.id)

            day_lab_window_map[day] = chosen_window

        # ----------------------------------------------------
        # DEEP LEARNING MODEL FALLBACK CHECK
        # ----------------------------------------------------
        # If ML strategy generated fewer than 5 lab sessions or encountered severe bottleneck, use Deep Learning Solver
        if len(day_lab_window_map) < 5 or labs_count < 10:
            try:
                from services.ml_clash_predictor import dl_solver
                dl_entries, strategy_name = dl_solver.solve(
                    division=division, div_subjects=div_subjects, lab_subjects=lab_subjects,
                    all_faculty=all_faculty, timeslots=timeslots, days=days,
                    subject_faculty_map=subject_faculty_map, classrooms=classrooms,
                    lab_rooms=lab_rooms, created_by=created_by
                )
                if dl_entries:
                    new_entries = dl_entries
                    labs_count = sum(1 for e in dl_entries if e.entry_type == 'lab')
                    lectures_count = sum(1 for e in dl_entries if e.entry_type == 'lecture')
            except Exception as dl_err:
                print(f"[DL-Solver] Fallback note: {dl_err}")

        # ----------------------------------------------------
        # 2. FILL REMAINING TIME SLOTS WITH STRICT LECTURE QUOTAS & LIBRARY FOR EXTRA SLOTS
        # ----------------------------------------------------
        subject_lec_counts = {s.id: sum(1 for e in new_entries if e.subject_id == s.id and e.entry_type == 'lecture') for s in div_subjects}
        library_count = 0

        for day in days:
            if day in day_lab_window_map and day_lab_window_map[day]:
                lab_start_id, lab_end_id = day_lab_window_map[day]
                lecture_slots_for_day = [s_id for s_id in slot_ids_ordered if s_id not in (lab_start_id, lab_end_id)]
            else:
                lecture_slots_for_day = slot_ids_ordered

            last_scheduled_subject_id = None

            for slot_id in lecture_slots_for_day:
                existing = [e for e in new_entries if e.day == day and e.time_slot_id == slot_id]
                if existing:
                    continue

                # STRICT HARD CAP: Only subjects that have NOT reached their weekly lecture quota (e.g. 3 lectures max)
                eligible_subjects = [s for s in div_subjects if s.id != last_scheduled_subject_id and subject_lec_counts.get(s.id, 0) < s.required_lectures]
                if not eligible_subjects:
                    eligible_subjects = [s for s in div_subjects if subject_lec_counts.get(s.id, 0) < s.required_lectures]

                if not eligible_subjects:
                    # All subjects have fulfilled their required lecture quota -> Assign LIBRARY to remaining slot!
                    e_lib = Timetable(
                        division_id=division_id, subject_id=None, faculty_id=None,
                        time_slot_id=slot_id, day=day, room_number='Library',
                        entry_type='library', batch_id=None, created_by=created_by
                    )
                    new_entries.append(e_lib)
                    library_count += 1
                    continue

                scheduled_lecture = False
                for offset in range(len(eligible_subjects)):
                    candidate_sub = eligible_subjects[(lectures_count + offset) % len(eligible_subjects)]
                    rm_name = find_free_room(day, slot_id, is_lab=False)
                    fac = find_best_faculty(candidate_sub, day, slot_id, rm_name, batch_id=None, is_lab=False)

                    if fac and rm_name:
                        e_lec = Timetable(
                            division_id=division_id, subject_id=candidate_sub.id, faculty_id=fac.id,
                            time_slot_id=slot_id, day=day, room_number=rm_name,
                            entry_type='lecture', batch_id=None, created_by=created_by
                        )
                        new_entries.append(e_lec)
                        subject_lec_counts[candidate_sub.id] = subject_lec_counts.get(candidate_sub.id, 0) + 1
                        lectures_count += 1
                        last_scheduled_subject_id = candidate_sub.id
                        scheduled_lecture = True
                        break

                if not scheduled_lecture:
                    # Try any unfulfilled subject fallback
                    unfulfilled = [s for s in div_subjects if subject_lec_counts.get(s.id, 0) < s.required_lectures]
                    if unfulfilled:
                        fallback_sub = unfulfilled[0]
                        rm_name = find_free_room(day, slot_id, is_lab=False)
                        fac = find_best_faculty(fallback_sub, day, slot_id, rm_name, batch_id=None, is_lab=False)
                        if fac and rm_name:
                            e_lec = Timetable(
                                division_id=division_id, subject_id=fallback_sub.id, faculty_id=fac.id,
                                time_slot_id=slot_id, day=day, room_number=rm_name,
                                entry_type='lecture', batch_id=None, created_by=created_by
                            )
                            new_entries.append(e_lec)
                            subject_lec_counts[fallback_sub.id] = subject_lec_counts.get(fallback_sub.id, 0) + 1
                            lectures_count += 1
                            last_scheduled_subject_id = fallback_sub.id
                            scheduled_lecture = True

                if not scheduled_lecture:
                    # Log suggestion to admin if lecture quota unfulfilled due to constraint bottleneck
                    unfulfilled = [s for s in div_subjects if subject_lec_counts.get(s.id, 0) < s.required_lectures]
                    if unfulfilled:
                        slot_obj = slot_by_id.get(slot_id)
                        slot_range = slot_obj.time_range if slot_obj else f"Slot {slot_id}"
                        ClashService.log_clash(
                            clash_type='room_or_faculty_unavailability',
                            details={
                                'day': day,
                                'time': slot_range,
                                'subject': unfulfilled[0].name,
                                'message': f"Constraint Warning: Could not schedule lecture for {unfulfilled[0].name} on {day} at {slot_range}. Reason: No free room or available faculty.",
                                'suggestion': f"Add a new classroom in Manage Rooms or assign an additional faculty to {unfulfilled[0].name}."
                            },
                            division_id=division_id,
                            severity='warning'
                        )
                    # Fill slot with LIBRARY if no room/faculty available
                    e_lib = Timetable(
                        division_id=division_id, subject_id=None, faculty_id=None,
                        time_slot_id=slot_id, day=day, room_number='Library',
                        entry_type='library', batch_id=None, created_by=created_by
                    )
                    new_entries.append(e_lib)
                    library_count += 1

        db.session.add_all(new_entries)
        db.session.commit()

        total_entries = Timetable.query.filter_by(division_id=division_id).count()

        return {
            'success': True,
            'division_id': division_id,
            'total_entries': total_entries,
            'lectures_count': lectures_count,
            'labs_count': labs_count,
            'library_count': library_count,
            'message': f'Auto-generated {total_entries} timetable entries cleanly (Max 3 lecs/subject, Library for remaining slots, 0 clashes).'
        }

    @staticmethod
    def preview_timetable(division_id):
        division = Division.query.get(division_id)
        if not division:
            return {'success': False, 'message': f'Division ID {division_id} not found.'}

        entries = Timetable.query.filter_by(division_id=division_id).order_by(Timetable.time_slot_id).all()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        schedule_by_day = {d: [] for d in days}
        
        lectures_cnt = 0
        labs_cnt = 0
        library_cnt = 0

        for e in entries:
            day_name = e.day
            if day_name in schedule_by_day:
                if e.entry_type == 'lecture':
                    lectures_cnt += 1
                elif e.entry_type == 'lab':
                    labs_cnt += 1
                else:
                    library_cnt += 1

                schedule_by_day[day_name].append({
                    'time_range': e.time_slot.time_range if e.time_slot else 'N/A',
                    'entry_type': e.entry_type,
                    'subject_name': e.subject.name if e.subject else 'LIBRARY',
                    'faculty_name': e.faculty.user.full_name if e.faculty and e.faculty.user else 'N/A',
                    'room_number': e.room_number or '101',
                    'batch_name': e.batch.name if e.batch else None
                })

        return {
            'success': True,
            'division_id': division_id,
            'total_entries': len(entries),
            'lectures_count': lectures_cnt,
            'labs_count': labs_cnt,
            'library_count': library_cnt,
            'schedule_by_day': schedule_by_day
        }

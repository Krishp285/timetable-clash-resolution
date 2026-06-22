#!/usr/bin/env python
"""Script to create test timetable data for ML model training."""

from app import app, db
from models import Timetable, Faculty, Division, Subject, TimeSlot
from datetime import datetime

def create_test_data():
    """Create test timetable entries for training."""
    with app.app_context():
        # Get sample data
        divisions = Division.query.all()
        faculties = Faculty.query.all()
        subjects = Subject.query.all()
        timeslots = TimeSlot.query.all()
        
        if not divisions or not faculties or not subjects or not timeslots:
            print("⚠️  Missing required data. Ensure branches, divisions, faculties, subjects, and timeslots are created.")
            return
        
        print(f"Found: {len(divisions)} divisions, {len(faculties)} faculties, {len(subjects)} subjects, {len(timeslots)} timeslots")
        
        # Create test entries
        test_entries = []
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        rooms = ['101', '102', '103', '104', '105', '201', '202', '203']
        
        div = divisions[0]
        count = 0
        
        # Create entries for each faculty and subject combination
        for fac in faculties[:3]:  # Use first 3 faculties
            for subj in subjects[:4]:  # Use first 4 subjects
                for day_idx, day in enumerate(days):
                    slot = timeslots[day_idx % len(timeslots)]
                    room = rooms[count % len(rooms)]
                    
                    # Check if entry already exists
                    existing = Timetable.query.filter_by(
                        division_id=div.id,
                        day=day,
                        time_slot_id=slot.id,
                        faculty_id=fac.id
                    ).first()
                    
                    if not existing:
                        entry = Timetable(
                            division_id=div.id,
                            faculty_id=fac.id,
                            subject_id=subj.id,
                            day=day,
                            time_slot_id=slot.id,
                            room_number=room
                        )
                        test_entries.append(entry)
                        count += 1
        
        # Save to database
        if test_entries:
            db.session.add_all(test_entries)
            db.session.commit()
            print(f"✅ Created {len(test_entries)} test timetable entries")
        else:
            print("ℹ️  No new entries created (may already exist)")
        
        # Show total count
        total = Timetable.query.count()
        print(f"📊 Total timetable entries in database: {total}")

if __name__ == '__main__':
    create_test_data()

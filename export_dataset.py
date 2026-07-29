#!/usr/bin/env python
"""
Dataset Exporter Script
Generates human-readable and model-ready CSV files from the ML training dataset.
Run: python export_dataset.py
"""

import csv
import os
import numpy as np
from app import app
from models import Timetable, Faculty, Division, Subject, TimeSlot
from services.ml_clash_predictor import ml_predictor

def export_dataset():
    with app.app_context():
        print("=" * 60)
        print("ML Training Dataset Exporter")
        print("=" * 60)

        # Get all timetable entries
        all_entries = Timetable.query.all()
        if not all_entries:
            print("❌ No timetable entries found in the database. Please add entries or run create_test_data.py first.")
            return

        # Fetch lookup tables for human-readable names
        faculty_map = {f.id: f.user.full_name for f in Faculty.query.all()}
        division_map = {d.id: d.full_name for d in Division.query.all()}
        subject_map = {s.id: s.name for s in Subject.query.all()}
        timeslot_map = {ts.id: ts.time_range for ts in TimeSlot.query.all()}

        # Re-run feature preparation to get the actual features X and labels y
        X, y = ml_predictor.prepare_features()
        if X is None or len(X) == 0:
            print("❌ Error preparing features.")
            return

        print(f"Total samples prepared for model training: {len(X)}")
        print(f"  - Non-clash samples (label 0): {np.sum(y == 0)}")
        print(f"  - Clash samples (label 1):     {np.sum(y == 1)}")
        print()

        # 1. Export Model-Ready Features CSV (Numerical)
        numerical_file = "ml_model_features.csv"
        print(f"Writing numerical dataset to: {numerical_file}...")
        with open(numerical_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["faculty_id", "division_id", "subject_id", "time_slot_id", "day_number", "room_hashed", "is_clash"])
            for features, label in zip(X, y):
                writer.writerow([int(features[0]), int(features[1]), int(features[2]), int(features[3]), int(features[4]), float(features[5]), int(label)])
        print(f"[OK] Created {numerical_file}")

        # 2. Export Human-Readable Dataset CSV
        # We will decode the IDs and numbers back to strings
        day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday'}
        
        # To decode room hashed values, let's keep a reverse lookup or fetch distinct rooms
        distinct_rooms = [r[0] for r in db_session_rooms()]
        room_hashes = {float(r if r.isdigit() else hash(r) % 100): r for r in distinct_rooms}
        # default fallback
        room_hashes[101.0] = '101'

        human_file = "ml_training_dataset.csv"
        print(f"Writing human-readable dataset to: {human_file}...")
        with open(human_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Faculty Name", "Division Name", "Subject Name", "Time Slot", "Day of Week", "Room Number", "Is Clash"])
            for features, label in zip(X, y):
                fac_name = faculty_map.get(int(features[0]), f"Faculty {int(features[0])}")
                div_name = division_map.get(int(features[1]), f"Division {int(features[1])}")
                subj_name = subject_map.get(int(features[2]), f"Subject {int(features[2])}")
                slot_time = timeslot_map.get(int(features[3]), f"Slot {int(features[3])}")
                day_name = day_names.get(int(features[4]), "Monday")
                
                # Retrieve room name
                room_val = float(features[5])
                room_name = room_hashes.get(room_val, str(int(room_val)) if room_val.is_integer() else "101")
                
                writer.writerow([fac_name, div_name, subj_name, slot_time, day_name, room_name, "Yes (1)" if label == 1 else "No (0)"])
        print(f"[OK] Created {human_file}")
        print("\n" + "=" * 60)
        print("EXPORTS COMPLETED SUCCESSFULLY!")
        print("You can open 'ml_training_dataset.csv' in Excel to show your teacher.")
        print("=" * 60)

def db_session_rooms():
    from extensions import db
    rooms = db.session.query(Timetable.room_number).distinct().all()
    return rooms

if __name__ == '__main__':
    export_dataset()

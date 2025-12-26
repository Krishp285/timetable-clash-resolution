"""
Database Initialization Script
Creates all tables and default admin user

Usage: python create_db.py
"""

from app import app
from extensions import db
from models import User

def create_database():
    """Create all database tables and default admin user"""
    
    with app.app_context():
        print("=" * 60)
        print("College Timetable Management System - Database Setup")
        print("=" * 60)
        print()
        
        # Drop all tables (CAUTION: Use only for fresh setup)
        print("Dropping existing tables (if any)...")
        db.drop_all()
        print("✓ Tables dropped")
        print()
        
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ All tables created successfully!")
        print()
        
        # Create default admin user
        print("Creating default admin user...")
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
            
            print("✓ Default admin user created!")
        else:
            print("! Admin user already exists")
        
        print()
        print("=" * 60)
        print("DATABASE SETUP COMPLETE!")
        print("=" * 60)
        print()
        print("Tables Created:")
        print("  ✓ users              - User authentication")
        print("  ✓ faculty            - Faculty profiles")
        print("  ✓ branches           - Academic branches")
        print("  ✓ divisions          - Division/sections")
        print("  ✓ subjects           - Course subjects")
        print("  ✓ time_slots         - Time slots")
        print("  ✓ timetable          - Timetable entries")
        print("  ✓ clash_logs         - Clash detection logs")
        print()
        print("Default Login Credentials:")
        print("-" * 60)
        print("  Username: admin")
        print("  Password: admin123")
        print("-" * 60)
        print()
        print("Next Steps:")
        print("  1. Run: python app.py")
        print("  2. Open: http://localhost:5000")
        print("  3. Login with admin credentials")
        print("  4. Start adding branches, divisions, subjects, and time slots")
        print()
        print("=" * 60)

if __name__ == '__main__':
    create_database()
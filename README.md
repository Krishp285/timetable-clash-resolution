# ============================================
# README.md
# ============================================

# 🎓 College Timetable Management System

A comprehensive, interactive timetable management system built with Flask, MySQL, and modern web technologies.

## ✨ Features

### For Admin
- ✅ **Complete User Management**: Create and manage branches, divisions, subjects, and time slots
- ✅ **Interactive Timetable Creation**: Side-by-side view showing time slots and faculty availability
- ✅ **Real-time Clash Detection**: Prevents faculty, room, and division conflicts
- ✅ **Comprehensive Dashboard**: View all divisions with clash indicators
- ✅ **Faculty Management**: View all registered faculty with their subjects and availability
- ✅ **Search Functionality**: Quick search for subjects and faculty
- ✅ **Final Timetable View**: See all created timetables across branches

### For Faculty
- ✅ **Profile Management**: Set working hours and subjects they can teach
- ✅ **Schedule View**: See personal teaching schedule organized by day
- ✅ **Automatic Availability**: System shows availability based on working hours

### Clash Detection System
- **Faculty Clash**: Same faculty cannot teach multiple classes at the same time (global check)
- **Room Clash**: Same room cannot be occupied twice at the same time
- **Division Clash**: Same division cannot have multiple classes at the same time

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   mkdir timetable_system
   cd timetable_system
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install Flask Flask-SQLAlchemy PyMySQL cryptography Werkzeug
   ```

4. **Setup MySQL Database**
   ```sql
   -- Open MySQL
   mysql -u root -p
   
   -- Create database
   CREATE DATABASE timetable_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   -- Exit MySQL
   EXIT;
   ```

5. **Configure Database Connection**
   
   Edit `app.py` (Line ~15):
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/timetable_system'
   ```
   
   Replace `YOUR_PASSWORD` with your MySQL root password.

6. **Create Database Tables**
   ```bash
   python create_db.py
   ```

7. **Run the Application**
   ```bash
   python app.py
   ```

8. **Access the System**
   
   Open your browser and go to: `http://localhost:5000`
   
   **Default Admin Login:**
   - Username: `admin`
   - Password: `admin123`

## 📁 Project Structure

```
timetable_system/
├── app.py                  # Main Flask application
├── models.py               # Database models
├── create_db.py           # Database initialization
├── services/
│   └── clash_service.py   # Clash detection logic
├── templates/
│   ├── base.html
│   ├── signup.html
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── faculty_dashboard.html
│   ├── faculty_profile.html
│   ├── manage_branches.html
│   ├── manage_divisions.html
│   ├── manage_subjects.html
│   ├── manage_timeslots.html
│   ├── manage_faculty.html
│   ├── timetable_select.html
│   ├── timetable_create.html
│   ├── view_timetable.html
│   ├── edit_timetable_entry.html
│   ├── final_timetable_view.html
│   ├── view_clashes.html
│   ├── 404.html
│   └── 500.html
├── requirements.txt
└── README.md
```

## 🎯 User Workflow

### Admin Workflow

1. **Sign Up / Login**
   - Create admin account or login with credentials

2. **Setup System**
   - Add Branches (e.g., CSE, ICT, ECE)
   - Add Divisions (e.g., CSE-A, CSE-B for different semesters)
   - Add Subjects (e.g., Data Structures, DBMS)
   - Add Time Slots (e.g., 09:00-10:00, 10:00-11:00)

3. **Create Timetable**
   - Select Branch and Division
   - Choose Day
   - For each time slot:
     - Select Subject
     - System shows all faculty availability (Available/Busy)
     - Select available faculty
     - Enter room number
     - System validates for clashes
     - Add entry if no conflicts

4. **Monitor Dashboard**
   - View all divisions with clash indicators
   - See recent clashes
   - Access quick management links

### Faculty Workflow

1. **Sign Up**
   - Create faculty account
   - System creates faculty profile

2. **Complete Profile**
   - Enter phone, department, designation
   - Set working hours (e.g., 09:00 - 17:00)
   - List subjects they can teach (comma-separated)

3. **View Schedule**
   - See personal teaching schedule
   - Organized by day
   - Shows subject, division, room, and time

## 🔧 Key Features Explained

### Side-by-Side Timetable View

**Left Side**: Time slots with entry forms
- Shows existing entries
- Allows adding new entries
- Edit/Delete options for each entry

**Right Side**: Faculty availability
- Real-time availability for each time slot
- Shows subjects each faculty teaches
- Indicates busy/available status
- Click to select faculty

### Clash Detection Logic

```python
# Faculty Clash
- Checks if faculty is teaching another class at same day+time
- Scope: Global (across all branches and divisions)

# Room Clash
- Checks if room is already occupied at same day+time
- Prevents double booking of physical spaces

# Division Clash
- Checks if division already has a class at same day+time
- Students can only attend one class at a time
```

### Dashboard Error Indicators

Admin dashboard shows:
- **Green**: Division with no clashes
- **Red**: Division with detected clashes
- Entry count per division
- Direct links to view/edit timetables

## 📊 Database Schema

### Core Tables

**users**: Authentication (admin, faculty)
**faculty**: Faculty profiles with subjects and working hours
**branches**: Academic branches
**divisions**: Branch divisions/sections
**subjects**: Course subjects
**time_slots**: Time slots for scheduling
**timetable**: Core timetable entries
**clash_logs**: Detected clashes history

## 🎨 UI Features

- **Modern Gradient Design**: Beautiful purple/blue gradients
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Hover effects, smooth animations
- **Icon Integration**: Font Awesome icons throughout
- **Search Functionality**: Quick search for subjects and faculty
- **Color-Coded Status**: Green (success), Red (error), Blue (info)
- **Print-Friendly**: Timetable view optimized for printing

## 🔐 Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **Session Management**: Flask's secure session handling
- **Role-Based Access**: Decorators enforce admin/faculty permissions
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **Input Validation**: Server-side validation for all forms

## 🐛 Troubleshooting

### Database Connection Error
```
Error: Can't connect to MySQL server
```
**Solution**: 
- Check if MySQL is running
- Verify credentials in app.py
- Ensure database exists

### Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**:
```bash
pip install Flask Flask-SQLAlchemy PyMySQL cryptography Werkzeug
```

### Clash Detection Not Working
**Check**:
- Faculty profile has subjects set
- Working hours are configured
- Time slots exist in database

## 📝 API Endpoints

```
GET  /api/divisions/<branch_id>    # Get divisions by branch
GET  /api/faculty-availability     # Get faculty availability
GET  /api/subjects/search          # Search subjects
```

## 🚀 Production Deployment

1. **Change Secret Key**
   ```python
   app.config['SECRET_KEY'] = 'your-super-secret-key-here'
   ```

2. **Disable Debug Mode**
   ```python
   app.run(debug=False)
   ```

3. **Use Production Database**
   - Configure production MySQL server
   - Update connection string

4. **Deploy with Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

5. **Use Nginx as Reverse Proxy**
   - Setup SSL certificate
   - Configure domain

## 🆘 Support

For issues or questions:
1. Check this README
2. Review code comments
3. Test with default admin account
4. Verify database connectivity

## 📄 License

This project is for educational purposes.

---

**Built with ❤️ using Flask, MySQL, and modern web technologies**
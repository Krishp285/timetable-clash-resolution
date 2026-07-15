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
├── app.py                  # Main Flask application with routing & handlers
├── models.py               # SQLAlchemy database schema models (8 tables)
├── config.py               # Flask application configurations
├── extensions.py           # Shared SQLAlchemy database extensions
├── create_db.py            # Local SQLite/MySQL table initializer script
├── generate_gtu_report.py  # GTU document generation script
├── services/
│   ├── clash_service.py    # Main three-tier conflict checking logic
│   └── ml_clash_predictor.py # Random Forest ML logic (predict & suggestions)
├── ml_models/
│   └── clash_predictor_model.pkl # Trained serialized Random Forest model binary
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
│   ├── view_clashes.html   # Clash resolution suggestion page
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

## 🤖 Machine Learning Integration
The system integrates an intelligent Machine Learning prediction and recommendation module built using `scikit-learn` (Random Forest Classifier).

### ML Model Features & Architecture
- **Model Type**: Random Forest Classifier (`n_estimators=100`, `max_depth=10`).
- **Feature Vector**:
  1. `faculty_id` (Categorical)
  2. `division_id` (Categorical)
  3. `subject_id` (Categorical)
  4. `time_slot_id` (Categorical)
  5. `day_of_week` (Ordinal: Monday=0, ..., Saturday=5)
  6. `room_number` (Numeric or hashed index)
- **Model File**: Serialized and loaded from `ml_models/clash_predictor_model.pkl`.

### AI-Powered Suggestion Engine
- **Predictive Clash Risk**: Predicts conflict probability `[0,1]` and categorizes risk into Low (`<0.3`), Medium (`<0.7`), and High (`>=0.7`).
- **Smart Slot Suggestions**: Recommends up to 5 alternative timeslots ranked by lowest clash risk.
- **Faculty Recommendations**: Computes matching scores for alternate faculty members based on teaching competency, workload balance, and availability.
- **Auto-Resolve**: Enables administrators to apply suggestions to resolve database conflicts with a single click.

## 📝 API Endpoints

### Data Endpoints
```
GET  /api/divisions/<branch_id>        # Get divisions by branch
GET  /api/faculty-availability         # Get faculty availability
GET  /api/subjects/search              # Search subjects
```

### Machine Learning Endpoints (Requires Admin Auth)
```
POST /api/ml/predict-clash-risk       # Predict clash risk for proposed slot
GET  /api/ml/slot-recommendations     # Get smart alternative timeslots
GET  /api/ml/recommend-faculty         # Get best faculty suggestions for subject
POST /api/ml/evaluate-timetable        # Evaluate overall timetable quality
GET  /api/ml/clash-risk-summary        # Get aggregate risk metrics across divisions
POST /api/ml/train-model               # Trigger model retraining on current DB data
GET  /api/ml/clash-suggestions/<id>    # Retrieve context-aware resolution options for a clash
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

#!/usr/bin/env python3
"""
Updated Internship Report Generator
====================================
Generates the complete Updated_Internship_Report.docx with all chapters,
including new features: Auto-Generator, Batch/Lab, Activity Log, AJAX APIs,
Master CSV Export, and corrected schemas.
"""

from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import os

doc = Document()

# ============================================
# STYLE SETUP
# ============================================
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.paragraph_format.line_spacing = 1.5

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(2.54)


def add_heading_custom(text, level=1, bold=True, center=False):
    h = doc.add_heading(text, level=level)
    if center:
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in h.runs:
        run.font.name = 'Times New Roman'
        run.font.bold = bold
        run.font.color.rgb = RGBColor(0, 0, 0)
    return h


def add_para(text, bold=False, italic=False, center=False, indent=False, size=12):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if indent:
        p.paragraph_format.left_indent = Cm(1.27)
    return p


def add_bullet(text, level=0):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent = Cm(1.27 + level * 0.63)
    for run in p.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
    return p


def add_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Headers
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.bold = True
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
    # Rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(10)
    return table


def add_code_block(code_text, language="python"):
    p = doc.add_paragraph()
    run = p.add_run(code_text)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
    p.paragraph_format.left_indent = Cm(1.27)
    return p


def page_break():
    doc.add_page_break()


# ============================================
# TITLE PAGE
# ============================================
for _ in range(4):
    doc.add_paragraph()

add_para("Timetable AI: Intelligent Timetable Generator with ML Clash Prediction", bold=True, center=True, size=16)
doc.add_paragraph()
add_para("A PROJECT REPORT", bold=True, center=True, size=14)
doc.add_paragraph()
add_para("Submitted by", center=True, italic=True, size=12)
doc.add_paragraph()
add_para("PATEL KRISH KALPESHBHAI", bold=True, center=True, size=14)
add_para("230670142018", center=True, size=12)
doc.add_paragraph()
add_para("In partial fulfillment for the award of the degree of", center=True, italic=True, size=12)
doc.add_paragraph()
add_para("BACHELOR OF ENGINEERING", bold=True, center=True, size=14)
add_para("in", center=True, italic=True, size=12)
add_para("Computer Science Engineering (Artificial Intelligence & Machine Learning)", bold=True, center=True, size=12)
doc.add_paragraph()
add_para("SAL Institute of Technology & Engineering Research", bold=True, center=True, size=12)
add_para("Bhadaj Circle, Ahmedabad, Gujarat (Affiliated with GTU)", center=True, size=12)
doc.add_paragraph()
add_para("Gujarat Technological University, Ahmedabad", bold=True, center=True, size=12)
add_para("Academic Year", bold=True, center=True, size=12)
add_para("(2026-2027)", bold=True, center=True, size=14)

page_break()

# ============================================
# CERTIFICATE
# ============================================
add_para("SAL Institute of Technology & Engineering Research", bold=True, center=True, size=12)
add_para("Bhadaj Circle, Ahmedabad, Gujarat (Affiliated with GTU)", center=True, size=12)
doc.add_paragraph()
add_para("CERTIFICATE", bold=True, center=True, size=16)
doc.add_paragraph()
add_para("This is to certify that the project report submitted along with the project entitled Internship has been carried out by Patel Krish Kalpeshbhai under my guidance in partial fulfillment for the degree of Bachelor of Engineering in Computer Science Engineering (Artificial Intelligence And Machine Learning), 7th Semester of Gujarat Technological University, Ahmadabad during the academic year 2026-27.")
doc.add_paragraph()
add_para("Dr. Nimisha Patel", bold=True)
doc.add_paragraph()
add_table(["", ""], [["Internal Guide", "HoD CE/CSE/CSE-AIML/ICT"], ["Department", "SALITER"]])

page_break()

# ============================================
# DECLARATION
# ============================================
add_para("SAL Institute of Technology & Engineering Research", bold=True, center=True, size=12)
add_para("Bhadaj Circle, Ahmedabad, Gujarat (Affiliated with GTU)", center=True, size=12)
doc.add_paragraph()
add_para("DECLARATION", bold=True, center=True, size=16)
doc.add_paragraph()
add_para("I hereby declare that the Internship / Project report submitted along with the Internship entitled Internship submitted in partial fulfillment for the degree of Bachelor of Engineering in Computer Science Engineering (Artificial Intelligence & Machine Learning) to Gujarat Technological University, Ahmedabad, is a bonafide record of original project work carried out by me at SoftCoding Solutions under the supervision of Abhishek Sir & Dr. Nimisha Patel and that no part of this report has been directly copied from any students\u2019 reports or taken from any other source, without providing due reference.")
doc.add_paragraph()
add_para("Name of the Student (Enrollment No)                    Sign of Student")
add_para("_________________________                               _______________")

page_break()

# ============================================
# ACKNOWLEDGEMENT
# ============================================
add_para("ACKNOWLEDGEMENT", bold=True, center=True, size=16)
doc.add_paragraph()
add_para("I wish to express my sincere gratitude to our External guide Mr. Abhishek Sir for continuously guiding me at the company and answering all my doubts with patience. I would also like to thank my Internal Guide Prof. Dr. Nimisha Patel for helping us through our internship by giving us the necessary suggestions and advice along with their valuable co-ordination in completing this internship.")
doc.add_paragraph()
add_para("We also thank our parents, friends and all the members of the family for their precious support and encouragement which they had provided in completion of our work. In addition to that, we would also like to mention the company personals who gave us the permission to use and experience the valuable resources required for the internship.")
doc.add_paragraph()
add_para("Thus, In conclusion to the above said, we once again thank the staff members of SoftCoding Solutions for their valuable support in completion of the project.")
doc.add_paragraph()
add_para("Thank You")
add_para("Patel Krish Kalpeshbhai", bold=True)

page_break()

# ============================================
# TABLE OF CONTENTS
# ============================================
add_para("CONTENTS", bold=True, center=True, size=16)
doc.add_paragraph()

toc_entries = [
    ("", "Title Page", "I"),
    ("", "Certificates", "II"),
    ("", "Acknowledgement", "III"),
    ("", "Content", "IV"),
    ("", "List of Figures", "V"),
    ("", "List of Table", "VI"),
    ("1", "Introduction", "1"),
    ("  1.1", "Introduction", ""),
    ("  1.2", "Background of the Study", ""),
    ("    1.2.1", "Evolution of Academic Timetable Management", ""),
    ("    1.2.2", "Traditional Timetable Preparation", ""),
    ("    1.2.3", "Digital Transformation in Educational Institutions", ""),
    ("    1.2.4", "Importance of Academic Scheduling", ""),
    ("  1.3", "Problem Statement", ""),
    ("    1.3.1", "Faculty Scheduling Conflicts", ""),
    ("    1.3.2", "Classroom Allocation Problems", ""),
    ("    1.3.3", "Laboratory Scheduling Challenges", ""),
    ("    1.3.4", "Student Batch Conflicts", ""),
    ("    1.3.5", "Administrative Challenges", ""),
    ("  1.4", "Motivation", ""),
    ("  1.5", "Objectives", ""),
    ("    1.5.1", "Primary Objectives", ""),
    ("    1.5.2", "Secondary Objectives", ""),
    ("  1.6", "Scope of the Project", ""),
    ("  1.7", "Need for the Proposed System", ""),
    ("  1.8", "Proposed Solution Overview", ""),
    ("  1.9", "Advantages of the Proposed System", ""),
    ("  1.10", "Applications", ""),
    ("  1.11", "Project Contribution", ""),
    ("  1.12", "Organization of the Report", ""),
    ("2", "Literature Survey", ""),
    ("  2.1", "Introduction", ""),
    ("  2.2", "Academic Timetable Scheduling", ""),
    ("  2.3", "Traditional Scheduling Techniques", ""),
    ("  2.4", "Automated Scheduling Techniques", ""),
    ("  2.5", "Constraint Satisfaction Problems", ""),
    ("  2.6", "Graph Coloring Approach", ""),
    ("  2.7", "Genetic Algorithm", ""),
    ("  2.8", "Google OR-Tools", ""),
    ("  2.9", "Machine Learning Approaches", ""),
    ("  2.10", "Review of Existing Timetable Systems", ""),
    ("  2.11", "Comparative Analysis of Existing Systems", ""),
    ("  2.12", "Research Paper Review", ""),
    ("  2.13", "Research Gap", ""),
    ("  2.14", "Chapter Summary", ""),
    ("3", "Requirement Analysis", ""),
    ("  3.1", "Introduction", ""),
    ("  3.2", "Existing System Analysis", ""),
    ("  3.3", "Limitations of Existing System", ""),
    ("  3.4", "Proposed System Requirements", ""),
    ("  3.5", "Functional Requirements", ""),
    ("  3.6", "Non-Functional Requirements", ""),
    ("  3.7", "Hardware Requirements", ""),
    ("  3.8", "Software Requirements", ""),
    ("  3.9", "Feasibility Study", ""),
    ("    3.9.1", "Technical Feasibility", ""),
    ("    3.9.2", "Economic Feasibility", ""),
    ("    3.9.3", "Operational Feasibility", ""),
    ("  3.10", "User Roles", ""),
    ("  3.11", "Requirement Traceability Matrix", ""),
    ("4", "System Analysis And Design", ""),
    ("  4.1", "System Architecture", ""),
    ("  4.2", "Overall Workflow", ""),
    ("  4.3", "Module Identification", ""),
    ("  4.4", "Authentication Module", ""),
    ("  4.5", "Faculty Management Module", ""),
    ("  4.6", "Room & Resource Management Module", ""),
    ("  4.7", "Subject Management Module", ""),
    ("  4.8", "Timetable Generation Module", ""),
    ("  4.9", "AI Auto-Generator Module", ""),
    ("  4.10", "Clash Detection Module", ""),
    ("  4.11", "Intelligent Clash Resolution Module", ""),
    ("  4.12", "Reports & Export Module", ""),
    ("  4.13", "Activity Logging Module", ""),
    ("  4.14", "Global Search Module", ""),
    ("  4.15", "Use Case Diagram", ""),
    ("  4.16", "Activity Diagram", ""),
    ("  4.17", "Sequence Diagram", ""),
    ("  4.18", "Class Diagram", ""),
    ("  4.19", "ER Diagram", ""),
    ("  4.20", "Component Diagram", ""),
    ("  4.21", "Deployment Diagram", ""),
    ("  4.22", "DFD Level 0", ""),
    ("  4.23", "DFD Level 1", ""),
    ("  4.24", "DFD Level 2", ""),
    ("5", "System Implementation", ""),
    ("  5.1", "Introduction", ""),
    ("  5.2", "Project Structure", ""),
    ("  5.3", "Frontend Implementation", ""),
    ("  5.4", "Backend Implementation", ""),
    ("  5.5", "Database Implementation", ""),
    ("  5.6", "Authentication Implementation", ""),
    ("  5.7", "Dashboard Implementation", ""),
    ("  5.8", "Timetable Generation Implementation", ""),
    ("  5.9", "AI Auto-Generator Implementation", ""),
    ("  5.10", "Batch & Laboratory Management Implementation", ""),
    ("  5.11", "Clash Detection Implementation", ""),
    ("  5.12", "Intelligent Clash Resolution Implementation", ""),
    ("  5.13", "Activity Logging Implementation", ""),
    ("  5.14", "Global Search Implementation", ""),
    ("  5.15", "CSV/ZIP Export Implementation", ""),
    ("  5.16", "AJAX Real-Time API Implementation", ""),
    ("  5.17", "Report Generation", ""),
    ("  5.18", "Deployment", ""),
    ("6", "Timetable Generation And Clash Resolution", ""),
    ("  6.1", "Introduction", ""),
    ("  6.2", "Timetable Scheduling Problem", ""),
    ("  6.3", "Scheduling Constraints", ""),
    ("    6.3.1", "Hard Constraints", ""),
    ("    6.3.2", "Soft Constraints", ""),
    ("  6.4", "Faculty Allocation", ""),
    ("  6.5", "Visiting Faculty Scheduling", ""),
    ("  6.6", "Classroom Allocation", ""),
    ("  6.7", "Laboratory Allocation", ""),
    ("  6.8", "Batch Management & Lab Scheduling", ""),
    ("  6.9", "Subject Allocation", ""),
    ("  6.10", "Time Slot Allocation", ""),
    ("  6.11", "AI Auto-Generation Algorithm", ""),
    ("  6.12", "Clash Detection Process", ""),
    ("  6.13", "Clash Resolution Strategy", ""),
    ("  6.14", "Intelligent Clash Resolution Suggestions", ""),
    ("  6.15", "Scheduling Workflow", ""),
    ("  6.16", "Algorithm Description", ""),
    ("  6.17", "Optimization Strategy", ""),
    ("  6.18", "Complexity Analysis", ""),
    ("7", "Database Design", ""),
    ("  7.1", "Introduction", ""),
    ("  7.2", "Database Architecture", ""),
    ("  7.3", "Entity Relationship Diagram", ""),
    ("  7.4", "Database Tables", ""),
    ("    7.4.1", "users", ""),
    ("    7.4.2", "faculty", ""),
    ("    7.4.3", "branches", ""),
    ("    7.4.4", "divisions", ""),
    ("    7.4.5", "batches", ""),
    ("    7.4.6", "time_slots", ""),
    ("    7.4.7", "subjects", ""),
    ("    7.4.8", "rooms", ""),
    ("    7.4.9", "timetable", ""),
    ("    7.4.10", "clash_logs", ""),
    ("    7.4.11", "activity_logs", ""),
    ("  7.5", "Relationships", ""),
    ("  7.6", "SQL Schema", ""),
    ("  7.7", "Data Dictionary", ""),
    ("  7.8", "Sample Database Records", ""),
    ("8", "Testing And Validation", ""),
    ("  8.1", "Introduction", ""),
    ("  8.2", "Unit Testing", ""),
    ("  8.3", "Integration Testing", ""),
    ("  8.4", "System Testing", ""),
    ("  8.5", "User Acceptance Testing", ""),
    ("  8.6", "Black Box Testing", ""),
    ("  8.7", "White Box Testing", ""),
    ("  8.8", "Performance Testing", ""),
    ("  8.9", "Security Testing", ""),
    ("  8.10", "Test Cases", ""),
    ("  8.11", "Bug Analysis", ""),
    ("9", "Results And Discussion", ""),
    ("  9.1", "Introduction", ""),
    ("  9.2", "Dashboard Results", ""),
    ("  9.3", "Timetable Generation Results", ""),
    ("  9.4", "AI Auto-Generation Results", ""),
    ("  9.5", "Clash Resolution Results", ""),
    ("  9.6", "Intelligent Clash Resolution Results", ""),
    ("  9.7", "Global Search Results", ""),
    ("  9.8", "Export Results", ""),
    ("  9.9", "Performance Analysis", ""),
    ("  9.10", "Comparison with Manual Scheduling", ""),
    ("  9.11", "Advantages Achieved", ""),
    ("  9.12", "Limitations", ""),
    ("10", "Future Scope And Conclusion", ""),
    ("  10.1", "Future Scope", ""),
    ("    10.1.1", "ERP Integration", ""),
    ("    10.1.2", "Attendance Management", ""),
    ("    10.1.3", "Mobile Application", ""),
    ("    10.1.4", "Cloud Deployment", ""),
    ("    10.1.5", "Multi-Campus Support", ""),
    ("    10.1.6", "Advanced ML Enhancements", ""),
    ("  10.2", "Conclusion", ""),
    ("11", "References", ""),
    ("  11.1", "Books", ""),
    ("  11.2", "Research Papers", ""),
    ("  11.3", "IEEE Papers", ""),
    ("  11.4", "Official Documentation", ""),
    ("  11.5", "Websites", ""),
    ("12", "Appendix", ""),
    ("  A", "User Manual", ""),
    ("    A.1", "Administrator Quick Guide", ""),
    ("    A.2", "Faculty Quick Guide", ""),
    ("  B", "Installation Guide", ""),
    ("  C", "Project Folder Structure", ""),
    ("  D", "Database Schema", ""),
    ("  E", "API Documentation", ""),
    ("    E.1", "Application Utility Endpoints", ""),
    ("    E.2", "Machine Learning API Endpoints", ""),
    ("    E.3", "Clash Resolution API Endpoints", ""),
    ("    E.4", "AJAX Real-Time API Endpoints", ""),
    ("  F", "Sample Input Data", ""),
    ("  G", "Sample Generated Timetable", ""),
    ("  H", "Application Screenshots", ""),
    ("  I", "Glossary", ""),
    ("  J", "Abbreviations", ""),
]

for num, title, pg in toc_entries:
    p = doc.add_paragraph()
    run = p.add_run(f"{num}  {title}")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    if not num.startswith(" "):
        run.bold = True

page_break()

# ============================================
# LIST OF FIGURES
# ============================================
add_para("LIST OF FIGURES", bold=True, center=True, size=14)
doc.add_paragraph()

figures = [
    "Figure 4.1. System Architecture Diagram",
    "Figure 4.2. Overall Workflow Diagram",
    "Figure 4.3: Login and Sign up Page",
    "Figure 4.4: Faculty Profile (Regular Faculty)",
    "Figure 4.5: Faculty Profile (Visiting Faculty \u2013 Day-wise Scheduling)",
    "Figure 4.6: Manage Branches",
    "Figure 4.7: Manage Divisions (with Batch Configuration)",
    "Figure 4.8: Manage Subjects (with Lab/Lecture Configuration)",
    "Figure 4.9: Manage Rooms & Resources",
    "Figure 4.10: Timetable Creation (Side-by-Side) Interface",
    "Figure 4.11: AI Auto-Generator Preview Screen",
    "Figure 4.12. Use Case Diagram",
    "Figure 4.13. Activity Diagram \u2013 Timetable Creation",
    "Figure 4.14. Sequence Diagram \u2013 Clash Detection and Resolution",
    "Figure 4.15. Class Diagram",
    "Figure 4.16. Entity Relationship (ER) Diagram",
    "Figure 4.17. Component Diagram",
    "Figure 4.18. Deployment Diagram",
    "Figure 4.19. Data Flow Diagram \u2013 Level 0",
    "Figure 4.20. Data Flow Diagram \u2013 Level 1",
    "Figure 4.21. Data Flow Diagram \u2013 Level 2",
    "Figure 5.1. Admin Dashboard",
    "Figure 5.2. Faculty Dashboard",
    "Figure 5.3. Faculty Availability Panel",
    "Figure 5.4. View Clashes Screen with AI Resolution Suggestions",
    "Figure 5.5. Global Search Results Page",
    "Figure 5.6. Final Timetable View",
    "Figure 5.7. CSV Export \u2013 Sample Downloaded File",
    "Figure 5.8. Activity Log Page",
    "Figure 5.9. Admin Profile Page",
    "Figure 6.1. ML Risk Prediction Badge",
    "Figure 6.2. Random Forest Model Architecture Diagram",
    "Figure 6.3. ML Recommendations Panel",
    "Figure 6.4. AI-Powered Clash Resolution Suggestions Panel",
    "Figure 6.5. Auto-Resolve Workflow Diagram",
    "Figure 6.6. Auto-Generator Constraint Satisfaction Flowchart",
    "Figure 9.1. Dashboard Displaying Clash Indicators Across Divisions",
    "Figure 9.2. ML Feature Importance Chart",
    "Figure 9.3. Clash Resolution Suggestion Accuracy",
    "Figure 9.4. Auto-Generator Results Summary",
    "Figure C.1. Project Folder Structure",
]

for fig in figures:
    p = doc.add_paragraph()
    run = p.add_run(fig)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)

page_break()

# ============================================
# LIST OF TABLES
# ============================================
add_para("LIST OF TABLES", bold=True, center=True, size=14)
doc.add_paragraph()

tables_list = [
    "Table 2.1. Comparative Analysis of Existing Timetable Systems",
    "Table 3.1 Functional Requirements",
    "Table 3.2. Non-Functional Requirements",
    "Table 3.3. Hardware Requirements",
    "Table 3.4. Software Requirements",
    "Table 3.5. User Roles",
    "Table 3.6. Requirement Traceability Matrix",
    "Table 4.1. Module Identification",
    "Table 5.1. Project Structure",
    "Table 6.1. Clash Detection Process",
    "Table 6.2. Intelligent Clash Resolution \u2013 Suggestion Types",
    "Table 6.3. Auto-Generator Constraint Rules",
    "Table 7.1. Users Table Schema",
    "Table 7.2. Faculty Table Schema",
    "Table 7.3. Branches Table Schema",
    "Table 7.4. Divisions Table Schema",
    "Table 7.5. Batches Table Schema",
    "Table 7.6. Time Slots Table Schema",
    "Table 7.7. Subjects Table Schema",
    "Table 7.8. Rooms Table Schema",
    "Table 7.9. Timetable Table Schema",
    "Table 7.10. Clash Logs Table Schema",
    "Table 7.11. Activity Logs Table Schema",
    "Table 7.12. Relationships",
    "Table 7.13. Data Dictionary",
    "Table 7.14. Sample Database Records",
    "Table 8.1. Test Cases",
    "Table 9.1 ML Function Test Results",
    "Table 9.2 ML Performance Metrics",
    "Table 9.3. Comparison: Manual Scheduling vs. Proposed System",
    "Table E.1. Application REST/Utility API Endpoints",
    "Table E.2. ML API Endpoints",
    "Table E.3. Clash Resolution API Endpoints",
    "Table E.4. AJAX Real-Time API Endpoints",
    "Table G.1. Sample Generated Timetable",
    "Table I.1. Glossary",
    "Table J.1. Abbreviations",
]

for tbl in tables_list:
    p = doc.add_paragraph()
    run = p.add_run(tbl)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)

page_break()

# ============================================
# CHAPTER 1: INTRODUCTION
# ============================================
add_heading_custom("Chapter 1: Introduction", level=1)

add_heading_custom("1.1 Introduction", level=2)
add_para("Every academic term, colleges and universities must produce a timetable that assigns subjects, faculty members, classrooms, and time slots to every division or section of every branch offered by the institution. This is, at its core, a constraint-satisfaction problem: the same faculty member cannot be in two classrooms at once, the same room cannot host two different classes simultaneously, and the same batch of students (division) cannot be expected to attend two lectures at the same time. When timetables are built manually \u2013 typically in spreadsheets \u2013 these constraints are easy to violate and hard to verify, especially as the number of branches, divisions, subjects, and faculty members grows.")
add_para("The College Timetable Management System with Intelligent Clash Detection and Resolution is a full-stack web application developed to solve this problem. It is built using the Flask micro-framework for Python on the backend, the Flask-SQLAlchemy Object-Relational Mapper (ORM) for data persistence, MySQL (with automatic SQLite fallback) as the relational database engine, and server-rendered HTML, CSS, and JavaScript for the frontend. The application is organised around two role-based portals \u2013 Administrator and Faculty \u2013 and around a dedicated Clash Detection Service that validates every proposed timetable entry against the faculty, room, and division that it references before the entry is committed to the database.")
add_para("In addition to this deterministic, rule-based clash detection, the project extends the system with an Intelligent Clash Prevention, Recommendation, and Resolution module. This module applies a supervised machine-learning model \u2013 a scikit-learn Random Forest Classifier \u2013 trained on the institution\u2019s own historical timetable data, to proactively estimate the probability that a proposed entry will lead to a clash, to recommend lower-risk alternative time slots, to recommend suitable faculty members for a subject based on their expertise and availability, and to generate context-aware resolution suggestions for detected clashes that can be auto-applied with a single click.")
add_para("The system further incorporates an AI Auto-Generator Service that constructs complete, clash-free timetables for entire divisions using constraint satisfaction combined with ML risk minimisation. This auto-generator enforces strict rules including zero-clash guarantee across all divisions, dynamic batch naming, varying lab time windows across days, daily two-hour lab blocks with batch rotation, non-consecutive lecture scheduling, and strict college-hours enforcement. The auto-generator can produce timetables for individual divisions or for all divisions simultaneously, dramatically reducing the time required for timetable preparation from days to seconds.")

add_heading_custom("1.2 Background of the Study", level=2)

add_heading_custom("1.2.1 Evolution of Academic Timetable Management", level=3)
add_para("Timetable preparation in academic institutions has historically progressed from fully manual, paper-based rosters, to spreadsheet-based planning, to dedicated software systems. Each stage reduced some of the effort involved but did not eliminate the fundamental risk of scheduling conflicts unless the tool explicitly checked for them. The system documented in this report belongs to the third stage: a purpose-built, database-backed web application in which conflict checking is not an afterthought performed by a human reviewer, but a service (the Clash Detection Service) invoked automatically every time a new timetable entry is proposed.")

add_heading_custom("1.2.2 Traditional Timetable Preparation", level=3)
add_para("In the traditional approach, an administrative staff member or a coordinator manually allocates subjects, faculty, and rooms to time slots using a spreadsheet or a printed grid. Cross-checking for faculty, room, or division conflicts is done by visual inspection or by cross-referencing multiple sheets, which becomes increasingly error-prone as the number of divisions, subjects, and faculty members increases. Any change \u2013 such as a faculty member becoming unavailable \u2013 requires the entire timetable (or the affected parts of it) to be manually re-checked for new conflicts.")

add_heading_custom("1.2.3 Digital Transformation in Educational Institutions", level=3)
add_para("Educational institutions increasingly rely on web-based administrative systems for tasks such as attendance, admissions, examinations, and scheduling. A digital timetable system that runs in a browser, is backed by a relational database, and enforces role-based access (administrator versus faculty) fits naturally into this broader digitisation of academic administration. The system in this project follows this pattern: it is accessed through a web browser at a defined URL, stores all data in a MySQL database (with automatic SQLite fallback for development and resilience), and distinguishes between what an Administrator and a Faculty member are permitted to do.")

add_heading_custom("1.2.4 Importance of Academic Scheduling", level=3)
add_para("A correct and well-organised timetable directly affects the day-to-day functioning of an institution \u2013 it determines faculty workload distribution, classroom utilisation, and the learning experience of students. A single undetected clash (for example, a faculty member being assigned to two divisions in the same period) can disrupt classes for an entire day and erode confidence in the administrative system. Automated clash detection, of the kind implemented in this project\u2019s Clash Detection Service, therefore has a direct and measurable impact on institutional efficiency.")

add_heading_custom("1.3 Problem Statements", level=2)
add_para("Manually constructed academic timetables are susceptible to five recurring categories of problems, each of which is addressed by a specific component of the proposed system.")

add_heading_custom("1.3.1 Faculty Scheduling Conflicts", level=3)
add_para("A faculty member may inadvertently be assigned to teach two different divisions during the same day and time slot. Because a single faculty member may teach subjects across multiple branches and divisions, this type of conflict is a global check \u2013 it must be verified across the entire institution, not just within one branch, which is precisely how the Faculty Clash check is scoped in this system.")

add_heading_custom("1.3.2 Classroom Allocation Problems", level=3)
add_para("The same physical classroom or laboratory can be entered into two different timetable rows for the same day and time slot when allocation is done manually, resulting in two different divisions being sent to the same room. The system\u2019s Room Clash check exists specifically to prevent this double booking of physical spaces. Additionally, managing rooms with their capacities and types (Classroom, Lab, Seminar Hall) is now a first-class module in the system, enabling administrators to maintain a structured inventory of physical spaces.")

add_heading_custom("1.3.3 Laboratory Scheduling Challenges", level=3)
add_para("Laboratory sessions add an additional layer of complexity because they typically require a designated laboratory room rather than a general classroom, and often occupy a longer contiguous time block (two hours) than a lecture. With the Room & Resource Management module, laboratories are now tracked as a distinct room_type (\u2018Lab\u2019), and the Room Clash check applies uniformly to both classrooms and laboratories, ensuring that a laboratory slot is checked with the same rigour as any other room-bound session. The system additionally supports batch-wise lab scheduling, where a division is split into multiple batches (e.g., D1, D2, D3) that can be assigned to different lab rooms simultaneously during the same time window.")

add_heading_custom("1.3.4 Student Batch Conflicts", level=3)
add_para("A division (a batch or section of students, for example CSE-A) must not be scheduled for two classes at the same time, since a group of students can physically only attend one lecture at once. The Division Clash check enforces this by verifying that a division does not already have an entry for the same day and time slot before a new entry is added. When a division is split into batches for laboratory sessions, the system allows parallel scheduling of different batches in different labs during the same time slot, while still enforcing that no individual batch is double-booked.")

add_heading_custom("1.3.5 Administrative Challenges", level=3)
add_para("Beyond the three clash types above, administrators face the broader operational challenge of managing many moving parts \u2013 branches, divisions, subjects, time slots, rooms, batches, and faculty profiles \u2013 consistently, and of being able to see, at a glance, which divisions currently have unresolved clashes. This project addresses that challenge through a centralised Admin Dashboard with colour-coded clash indicators (green for a division with no clashes, red for a division with detected clashes), dedicated management screens for branches, divisions, subjects, time slots, rooms, and faculty, a global search facility across all entities, CSV/ZIP export functionality for timetable distribution, an activity logging system tracking all administrative actions, and an AI auto-generator capable of producing complete, clash-free timetables for entire divisions with a single click.")

add_heading_custom("1.4 Motivation", level=2)
add_para("The motivation for this project stems from the observation that clash detection is a mechanical, rule-based task that is well suited to automation, while the higher-level judgement calls involved in timetable construction (which subject to schedule when, which faculty member to prefer) are better left to a human administrator supported by good information. This motivated a design in which the human administrator retains control over the creation of the timetable through an interactive interface, while the system automatically performs the conflict verification that humans are prone to error on, offers data-driven recommendations (through the machine-learning module), provides intelligent resolution suggestions \u2013 with one-click auto-resolve capability \u2013 when conflicts do arise, and additionally offers a fully automated AI timetable generator for administrators who prefer to start from a machine-generated baseline rather than building from scratch.")

add_heading_custom("1.5 Objectives", level=2)

add_heading_custom("1.5.1 Primary Objectives", level=3)
add_bullet("To design and implement a web-based timetable management system using Flask, Flask-SQLAlchemy, and MySQL (with SQLite fallback).")
add_bullet("To implement an interactive, side-by-side timetable creation interface that shows time slots alongside real-time faculty availability.")
add_bullet("To implement a Clash Detection Service that performs faculty, room, and division clash checks whenever a timetable entry is created or modified.")
add_bullet("To provide role-based portals for Administrators and Faculty members with distinct permissions and views.")
add_bullet("To implement an Intelligent Clash Prevention, Recommendation, and Resolution module using a machine-learning model trained on the institution\u2019s own timetable data.")
add_bullet("To implement ML-powered clash resolution suggestions with one-click auto-resolve capability for detected clashes.")
add_bullet("To implement an AI Auto-Generator Service that constructs complete, clash-free timetables using constraint satisfaction combined with ML risk minimisation.")

add_heading_custom("1.5.2 Secondary Objectives", level=3)
add_bullet("To provide a centralised Admin Dashboard summarising all divisions along with clash indicators and entry counts.")
add_bullet("To provide faculty members with a personal, day-organised schedule view generated automatically from the timetable data.")
add_bullet("To log every detected clash in a dedicated clash_logs table with full resolution tracking for later review and audit.")
add_bullet("To secure the application using password hashing, session-based authentication, and role-based access-control decorators.")
add_bullet("To expose the machine-learning module\u2019s capabilities through a documented set of REST API endpoints.")
add_bullet("To implement a Room & Resource Management module for tracking classrooms, laboratories, and seminar halls with capacity and type attributes.")
add_bullet("To support visiting faculty scheduling with per-day, per-time-slot availability configuration.")
add_bullet("To provide global search across all entities (faculty, subjects, branches, divisions, rooms, clashes).")
add_bullet("To implement CSV/ZIP export of timetables for both administrators and faculty members.")
add_bullet("To implement a Batch model supporting multi-batch lab scheduling within divisions.")
add_bullet("To implement an Activity Logging system tracking all administrative actions with user attribution and timestamps.")
add_bullet("To implement real-time AJAX-based timetable management APIs for responsive, non-reload user interactions.")

add_heading_custom("1.6 Scope of the Project", level=2)
add_para("The scope of the project covers: user registration and authentication for Administrator and Faculty roles; management of branches, divisions (with batch configuration), subjects (with lab/lecture type and weekly lecture quotas), time slots, rooms (with capacity and type), and faculty profiles (including visiting faculty day-wise scheduling) by the Administrator; creation, editing, and deletion of timetable entries with real-time clash validation; AI-powered automatic timetable generation for individual or all divisions with constraint satisfaction and zero-clash guarantee; a faculty profile module in which faculty set their working hours, the subjects they can teach, and their visiting schedule if applicable; a clash-detection subsystem covering faculty, room, and division clashes; a machine-learning based clash-risk prediction, recommendation, and intelligent resolution suggestion subsystem with auto-resolve capability; a batch management system supporting multi-batch lab scheduling within divisions; an activity logging system tracking all administrative actions; a global search module across all entities; CSV/ZIP timetable export (individual division, master all-semesters, and faculty personal); AJAX-based real-time timetable APIs; and reporting views such as the final timetable view and the view-clashes screen with AI-powered resolution panels. The scope does not, in the current version of the system, extend to integration with external institutional ERP systems, or a native mobile application \u2013 these are documented as future scope in Chapter 10.")

add_heading_custom("1.7 Need for the Proposed System", level=2)
add_para("Institutions that continue to rely on spreadsheet-based or paper-based timetable preparation have no systematic way of guaranteeing, at the moment an entry is created, that it does not conflict with an existing entry elsewhere in the institution. Additionally, when clashes are detected, administrators must manually investigate alternative rooms, faculty, or time slots \u2013 a time-consuming process. Building a complete timetable from scratch for multiple divisions and branches can take days of manual effort, with no guarantee of an optimal or even conflict-free result. The proposed system directly addresses these needs by moving conflict verification out of human hands and into an automated service that runs on every entry, by providing intelligent resolution suggestions powered by ML when clashes are detected, by giving administrators a predictive, data-driven view of the risk associated with a proposed entry, and by offering an AI auto-generator that can produce complete, clash-free timetables for entire divisions in seconds rather than days.")

add_heading_custom("1.8 Proposed Solution Overview", level=2)
add_para("The proposed solution is a Flask web application backed by a MySQL database (with automatic SQLite fallback), structured around SQLAlchemy models for Users, Faculty, Branches, Divisions, Batches, TimeSlots, Subjects, Rooms, Timetable entries, ClashLogs, and ActivityLogs. Administrators log in and are presented with a dashboard summarising all divisions; from there they can manage the foundational data (branches, divisions with batch configuration, subjects with lab/lecture settings, time slots, rooms, faculty) and create timetables either manually through an interactive side-by-side screen or automatically using the AI auto-generator. Every manual entry submission is passed through the Clash Detection Service, which checks faculty, room, and division clashes before the entry is committed; any detected clash is logged to the clash_logs table and reflected on the dashboard. When clashes are detected, the system\u2019s Intelligent Resolution module generates ML-powered suggestions that can be auto-applied with a single click. The AI auto-generator uses constraint satisfaction combined with ML risk minimisation to produce complete, clash-free timetables with daily lab blocks, batch rotation, non-consecutive lectures, and library period auto-fill. Faculty members log in to a separate portal where they complete a profile and view their personal schedule. All administrative actions are tracked in the activity_logs table for audit purposes. The system additionally provides global search, CSV/ZIP export, and AJAX-based real-time APIs for responsive interactions.")

add_heading_custom("1.9 Advantages of the Proposed System", level=2)
add_bullet("Automated, rule-based clash checking removes the dependency on manual cross-verification for faculty, room, and division conflicts.")
add_bullet("The side-by-side timetable creation view with live faculty availability reduces the cognitive load on the administrator while building the schedule.")
add_bullet("Clash history is retained in the clash_logs table with full resolution tracking (who resolved it, how, and any notes), giving the institution an auditable record of conflicts.")
add_bullet("The machine-learning module adds a predictive layer that can flag a high-risk entry before it is saved, rather than only after a conflict has already occurred.")
add_bullet("ML-powered intelligent resolution suggestions with one-click auto-resolve drastically reduce the time needed to handle detected clashes.")
add_bullet("The AI Auto-Generator Service can produce complete, clash-free timetables for entire divisions in seconds, eliminating the need for days of manual scheduling effort.")
add_bullet("The Batch model supports multi-batch lab scheduling, allowing parallel lab sessions for different student batches within the same division.")
add_bullet("The Room & Resource Management module provides structured tracking of classrooms, labs, and seminar halls with capacity and type attributes.")
add_bullet("Visiting faculty can configure day-wise availability with specific time slots per day, ensuring accurate scheduling of part-time staff.")
add_bullet("Global search across all entities enables rapid information retrieval.")
add_bullet("CSV/ZIP export allows timetables to be distributed offline, including master all-semesters export.")
add_bullet("The Activity Logging system provides a complete audit trail of all administrative actions.")
add_bullet("AJAX-based real-time APIs enable responsive, non-reload user interactions during timetable creation.")
add_bullet("Role-based access control (Administrator vs. Faculty) ensures that each user only sees and modifies the data relevant to their role.")
add_bullet("Because the system is a web application, it can be accessed from any device with a browser without additional client software.")
add_bullet("Automatic SQLite fallback ensures the system remains operational even when the primary MySQL database is unavailable.")

add_heading_custom("1.10 Applications", level=2)
add_para("The system, as documented, is directly applicable to any single academic institution (college or university department) that needs to construct and maintain branch- and division-wise timetables and to track faculty teaching schedules. Within an institution it can be used by the timetabling office or academic administrators to build the master timetable either manually or via the AI auto-generator, and by individual faculty members to view their own teaching schedule without needing access to the full administrative interface.")

add_heading_custom("1.11 Project Contribution", level=2)
add_para("This report documents the full scope of work carried out during the internship: understanding and analysing the existing manual timetabling process, studying the requirements for an automated replacement, working with the College Timetable Management System codebase (Flask backend, SQLAlchemy models, clash-detection service, intelligent clash resolution module, AI auto-generator service, Room & Resource Management module, Batch management, visiting faculty day-wise scheduling, activity logging, global search, CSV/ZIP export, AJAX real-time APIs, and the machine-learning clash-prediction module), and producing this structured documentation covering the system\u2019s architecture, database design, implementation, testing, and results, together with recommendations for future enhancement.")

add_heading_custom("1.12 Organization of the Report", level=2)
add_para("Chapter 2 surveys existing and related approaches to timetable scheduling. Chapter 3 presents the requirement analysis, including functional and non-functional requirements and a feasibility study. Chapter 4 covers system analysis and design, including the architecture, the AI auto-generator module, and the standard UML and data-flow diagrams. Chapter 5 documents the implementation of the frontend, backend, database, authentication, room management, batch management, AI auto-generator, visiting faculty scheduling, intelligent clash resolution, activity logging, global search, AJAX real-time APIs, CSV/ZIP export, and reporting modules. Chapter 6 focuses specifically on the timetable-generation and clash-resolution logic, including the AI auto-generation algorithm, the machine-learning component, and the intelligent resolution suggestions. Chapter 7 details the database design with all eleven tables. Chapter 8 covers testing and validation. Chapter 9 presents results and discussion. Chapter 10 discusses future scope and concludes the report. References and appendices follow.")

page_break()

# ============================================
# CHAPTER 2: LITERATURE SURVEY
# ============================================
add_heading_custom("Chapter 2: Literature Survey", level=1)

add_heading_custom("2.1 Introduction", level=2)
add_para("This chapter surveys the class of problems to which academic timetabling belongs, the broad families of techniques that are commonly used to address them, and the specific technology choices (Flask, SQLAlchemy, MySQL, and scikit-learn) adopted in the project. It also situates the proposed system\u2019s rule-based clash-checking approach, its supplementary Random-Forest-based risk-prediction approach, its intelligent resolution-suggestion capability, and its AI auto-generator within this wider landscape, and closes with a comparative review and an identified research gap that motivates the project.")

add_heading_custom("2.2 Academic Timetable Scheduling", level=2)
add_para("Academic timetabling is the problem of assigning a set of events (subject\u2013division pairs that must meet) to a set of resources (time slots, rooms, and faculty) such that no resource is double-booked and, ideally, additional soft preferences are respected. The problem is characterised by hard constraints, which must never be violated (for example, a faculty member cannot teach two classes at once), and soft constraints, which are desirable but not mandatory (for example, avoiding large gaps in a faculty member\u2019s day). The system built in this project focuses primarily on enforcing the three hard constraints that are most disruptive when violated in a live academic setting: faculty double-booking, room double-booking, and division double-booking.")

add_heading_custom("2.3 Traditional Scheduling Techniques", level=2)
add_para("Traditional, non-computerised scheduling relies on manual allocation, typically supported by a spreadsheet, followed by manual cross-checking. Because the number of pairwise comparisons required to verify that no two entries conflict grows quickly as the number of entries increases, manual verification does not scale well and is the primary weakness that automated clash-detection services, such as the one implemented in this project, are designed to eliminate.")

add_heading_custom("2.4 Automated Scheduling Techniques", level=2)
add_para("Automated approaches to timetabling generally fall into two categories: (a) systems that detect and report conflicts in a timetable that a human is actively constructing, and (b) systems that attempt to generate a complete, conflict-free timetable automatically from a set of constraints. The system documented in this report implements both categories: it keeps a human administrator in control of the scheduling decisions while automatically validating each decision against the faculty, room, and division constraints (category a), and it additionally provides an AI Auto-Generator Service that can construct a complete, clash-free timetable automatically using constraint satisfaction combined with ML risk minimisation (category b). This dual approach gives administrators the flexibility to choose between interactive, guided scheduling and fully automated generation.")

add_heading_custom("2.5 Constraint Satisfaction Problems", level=2)
add_para("Academic timetabling can be formally modelled as a Constraint Satisfaction Problem (CSP), in which variables represent timetable entries, domains represent the possible (faculty, room, time-slot) combinations, and constraints represent the no-double-booking rules. The Clash Detection Service in this project implements, in effect, a set of explicit constraint checks evaluated against the existing rows of the timetable table each time a new entry is proposed, which is a direct, database-query-based realisation of CSP-style constraint checking. The AI Auto-Generator extends this further by implementing a full CSP solver that iteratively assigns entries while checking all constraints at each step, with backtracking and alternative candidate selection when constraints are violated.")

add_heading_custom("2.6 Graph Coloring Approach", level=2)
add_para("A well-known formal technique for timetabling is to model each event as a vertex in a conflict graph, connect two vertices with an edge whenever the corresponding events cannot share the same time slot, and then treat time-slot assignment as a graph-colouring problem in which no two adjacent vertices may receive the same colour. While the current system does not implement an explicit graph-colouring algorithm, the faculty/room/division clash rules it enforces are conceptually equivalent to the edge constraints of such a conflict graph, and the AI auto-generator\u2019s constraint-checking and backtracking approach achieves a similar effect through a procedural, greedy-with-fallback algorithm.")

add_heading_custom("2.7 Genetic Algorithm", level=2)
add_para("Genetic algorithms are a popular metaheuristic for automated timetable generation: candidate timetables are represented as chromosomes, and operators such as crossover and mutation are applied across generations to search for a schedule that minimises constraint violations. This project does not use a genetic algorithm; instead, it uses a supervised classification model (Random Forest) trained on historical scheduling data to estimate the probability of a clash for a proposed entry and to generate context-aware resolution suggestions, combined with a deterministic, constraint-satisfaction auto-generator that guarantees zero clashes through exhaustive checking.")

add_heading_custom("2.8 Google OR-Tools", level=2)
add_para("Google OR-Tools is a widely used open-source suite for combinatorial optimisation, including CP-SAT solvers well suited to timetabling-style constraint problems. The current implementation of this project does not integrate OR-Tools or any external constraint-solver library; its clash detection is implemented directly as SQLAlchemy queries within the Flask application, its auto-generator uses a custom constraint-satisfaction algorithm, and its predictive and resolution layer is implemented with scikit-learn. Integrating a dedicated solver such as OR-Tools for further optimised timetable generation is identified as a possible future enhancement.")

add_heading_custom("2.9 Machine Learning Approaches", level=2)
add_para("Machine-learning approaches to scheduling problems typically use historical or simulated scheduling data to train a model that predicts the likelihood of a conflict, recommends favourable assignments, or scores the quality of a candidate schedule, rather than searching for a schedule from first principles. This is precisely the role that the machine-learning module plays in this project: a Random Forest Classifier is trained on the timetable table\u2019s historical rows to predict clash probability, and the trained model is additionally used to rank alternative time slots, candidate faculty members, generate intelligent resolution suggestions for detected clashes, and evaluate the overall quality of a division\u2019s timetable. The AI auto-generator also leverages the ML predictor during its generation process to prefer lower-risk assignments when multiple valid options are available.")

add_heading_custom("2.10 Review of Existing Timetable Systems", level=2)
add_para("Existing timetable-management tools in academic use range from generic spreadsheet templates, to institution-specific ERP scheduling modules, to open-source and commercial dedicated timetabling software. The system built for this project differs from a generic spreadsheet in that clash checking is automatic rather than manual, it differs from many dedicated timetabling packages in that it additionally incorporates a machine-learning based risk-prediction, recommendation, and intelligent clash-resolution layer, and it goes further than most existing systems by providing an AI auto-generator that can produce complete timetables with batch-aware lab scheduling and constraint satisfaction.")

add_heading_custom("2.11 Comparative Analysis of Existing Systems", level=2)
add_para("Table 2.1. Comparative Analysis of Existing Timetable Systems")
add_table(
    ["Aspect", "Manual / Spreadsheet", "Generic Rule-Based Software", "Proposed System"],
    [
        ["Faculty clash checking", "Manual, error-prone", "Automated", "Automated (global scope, across all branches)"],
        ["Room clash checking", "Manual", "Automated", "Automated, with Room & Resource management module"],
        ["Division clash checking", "Manual", "Automated", "Automated"],
        ["Batch/lab scheduling", "Manual", "Rare", "Multi-batch parallel lab scheduling with rotation"],
        ["Automatic timetable generation", "Not available", "Varies", "AI Auto-Generator with constraint satisfaction"],
        ["Clash history / audit log", "Not available", "Varies", "Dedicated clash_logs table with full resolution tracking"],
        ["Activity tracking", "Not available", "Rare", "Comprehensive activity_logs with user attribution"],
        ["Predictive risk scoring", "Not available", "Rare", "Random Forest based risk prediction"],
        ["Alternative slot recommendation", "Not available", "Rare", "ML-based, top 5 lowest-risk slots"],
        ["Faculty recommendation", "Manual judgement", "Rare", "ML-based scoring (expertise + availability)"],
        ["Intelligent clash resolution", "Not available", "Not available", "ML-powered suggestions with one-click auto-resolve"],
        ["Room/resource management", "Manual", "Varies", "Dedicated module with capacity and type tracking"],
        ["Visiting faculty scheduling", "Manual", "Rare", "Day-wise, per-slot availability configuration"],
        ["Global search", "Not applicable", "Varies", "Full-text search across all entities"],
        ["Timetable export", "Manual copy", "Varies", "CSV/ZIP automated export (individual + master)"],
        ["Real-time AJAX APIs", "Not applicable", "Rare", "Full AJAX timetable CRUD without page reload"],
        ["Role-based portals", "Not applicable", "Varies", "Separate Administrator and Faculty portals"],
    ]
)

add_heading_custom("2.12 Research Paper Review", level=2)
add_para("This section summarises, at the level of general technique, ten themes commonly discussed in academic and applied literature on timetable clash resolution and scheduling automation that are directly relevant to the design of this project.")

for i, (title, desc) in enumerate([
    ("Paper 1 \u2013 Constraint-Based Timetabling", "Discusses framing timetabling as hard/soft constraint satisfaction. Relevance: the project\u2019s faculty/room/division checks are hard-constraint checks implemented as direct database queries, and the AI auto-generator implements a full CSP solver with backtracking."),
    ("Paper 2 \u2013 Graph-Colouring Models for Scheduling", "Discusses conflict graphs and colouring for time-slot assignment. Relevance: conceptually related to how the project\u2019s clash rules define which entries may not share a slot."),
    ("Paper 3 \u2013 Genetic Algorithms for Timetable Generation", "Discusses evolutionary search over candidate timetables. Relevance: identified as a possible future extension for automatic, optimisation-driven timetable generation."),
    ("Paper 4 \u2013 Constraint Programming Solvers", "Discusses solver-based generation of feasible schedules. Relevance: the project\u2019s AI auto-generator implements a procedural CSP solver with constraint checking and backtracking."),
    ("Paper 5 \u2013 Supervised Learning for Conflict Prediction", "Discusses using classifiers trained on historical scheduling outcomes to predict conflict likelihood. Relevance: directly mirrors the project\u2019s Random Forest clash-risk predictor."),
    ("Paper 6 \u2013 Recommendation Systems for Resource Allocation", "Discusses scoring and ranking candidate resources for an assignment. Relevance: mirrors the project\u2019s faculty-recommendation feature and intelligent clash-resolution suggestion system."),
    ("Paper 7 \u2013 Role-Based Access Control in Administrative Systems", "Discusses separating administrator and end-user privileges. Relevance: implemented via the User.role field and admin_required-style route decorators."),
    ("Paper 8 \u2013 Web-Based ORM-Backed Administrative Applications", "Discusses using an ORM such as SQLAlchemy over raw SQL for maintainability. Relevance: the project\u2019s models.py defines all entities as SQLAlchemy model classes."),
    ("Paper 9 \u2013 Dashboard-Based Monitoring for Institutional Systems", "Discusses summarising system state through indicators/dashboards. Relevance: mirrors the project\u2019s Admin Dashboard with green/red clash indicators per division."),
    ("Paper 10 \u2013 Feature Engineering for Tabular Classification Models", "Discusses encoding categorical identifiers as model features. Relevance: mirrors the six input features used by the project\u2019s Random Forest model."),
], start=1):
    add_heading_custom(f"2.12.{i} {title}", level=3)
    add_para(desc)

add_heading_custom("2.13 Research Gap", level=2)
add_para("Deterministic, rule-based clash-detection systems reliably catch conflicts that have already been proposed, but on their own they offer no foresight \u2013 they do not tell an administrator, in advance, which of several candidate time slots or candidate faculty members is least likely to eventually cause friction elsewhere in the schedule. Furthermore, once a clash is detected, existing systems leave the administrator to manually investigate and apply alternatives, which is time-consuming and error-prone. Most existing systems also lack the ability to automatically generate complete, constraint-satisfying timetables with batch-aware lab scheduling and workload balancing. This is the gap that the project\u2019s multi-layered approach \u2013 deterministic clash checks, ML-based risk prediction and recommendation, intelligent one-click resolution suggestions, and an AI auto-generator with constraint satisfaction \u2013 is designed to close.")

add_heading_custom("2.14 Chapter Summary", level=2)
add_para("This chapter reviewed the general landscape of timetable scheduling techniques \u2013 constraint satisfaction, graph colouring, genetic algorithms, and constraint solvers \u2013 as well as machine-learning approaches to conflict prediction and resolution, and positioned the proposed system\u2019s multi-layered design (a deterministic Clash Detection Service, a machine-learning clash predictor and recommender, an intelligent resolution suggestion engine, and an AI auto-generator) within this landscape. The identified research gap \u2013 the absence of combined predictive, resolution, and automatic generation capabilities in existing systems \u2013 motivates the project\u2019s distinctive multi-layered approach.")

page_break()

# ============================================
# CHAPTER 3: REQUIREMENT ANALYSIS
# ============================================
add_heading_custom("Chapter 3: Requirement Analysis", level=1)

add_heading_custom("3.1 Introduction", level=2)
add_para("This chapter analyses the existing (manual) scheduling process, identifies its limitations, and derives the functional and non-functional requirements that the proposed system, as implemented, satisfies. It also documents the hardware and software requirements, a feasibility study, the defined user roles, and a requirement traceability matrix linking requirements to the corresponding system modules.")

add_heading_custom("3.2 Existing System Analysis", level=2)
add_para("In the manual/spreadsheet-based existing system, a coordinator maintains a separate sheet (or a single large sheet) listing, for each division, the subject, faculty, room, and time slot for each day. Faculty availability is tracked informally, often from memory or from separate notes, and conflicts are found only when someone happens to notice two rows that reference the same faculty, room, or division at the same day and time.")

add_heading_custom("3.3 Limitations of Existing System", level=2)
add_bullet("No automated verification that a newly added entry does not conflict with an existing entry.")
add_bullet("Faculty availability and workload are not tracked systematically, making it hard to know at a glance who is free at a given time.")
add_bullet("No historical record of which clashes occurred and how (or whether) they were resolved.")
add_bullet("No predictive insight into which of several candidate slots or faculty is least likely to cause a future conflict.")
add_bullet("No automated resolution suggestions when clashes are detected \u2013 the administrator must manually investigate alternatives.")
add_bullet("No automatic timetable generation capability \u2013 every entry must be created manually.")
add_bullet("Visiting faculty availability is tracked informally with no per-day, per-slot granularity.")
add_bullet("Room inventory (capacity, type) is not systematically maintained.")
add_bullet("Batch-wise lab scheduling within divisions is not supported.")
add_bullet("No activity tracking or audit trail of administrative actions.")
add_bullet("Difficult to maintain consistency across many divisions and branches as their number grows.")
add_bullet("No ability to search across all entities or export timetables in structured formats.")

add_heading_custom("3.4 Proposed System Requirements", level=2)
add_para("The proposed system requirements were derived directly from the limitations identified above and are grouped, in the sections that follow, into functional requirements (what the system must do) and non-functional requirements (the qualities the system must exhibit while doing it).")

add_heading_custom("3.5 Functional Requirements", level=2)
add_para("Table 3.1. Functional Requirements")
add_table(
    ["ID", "Requirement", "Description"],
    [
        ["FR-1", "User Registration & Login", "The system shall allow users to sign up and log in as either an Administrator or a Faculty member, with passwords stored using secure hashing."],
        ["FR-2", "Branch Management", "The Administrator shall be able to create, edit, and manage academic branches with search/filter capability."],
        ["FR-3", "Division Management", "The Administrator shall be able to create, edit, and delete divisions/sections within a branch, each tied to a semester and academic year, with batch configuration (number of batches, student count)."],
        ["FR-4", "Subject Management", "The Administrator shall be able to add, edit, and delete subjects with name, unique code, credits, weekly lectures, semester, branch, and lab flag, with search/filter capability."],
        ["FR-5", "Time Slot Management", "The Administrator shall be able to define, edit, and delete time slots with start and end times and an optional label."],
        ["FR-6", "Room & Resource Management", "The Administrator shall be able to add, edit, and delete rooms/resources with name, capacity, and type (Classroom, Lab, Seminar Hall), with search/filter capability."],
        ["FR-7", "Faculty Profile Management", "Faculty members shall be able to set their working hours, the list of subjects they can teach, and their visiting faculty status with day-wise time slot availability."],
        ["FR-8", "Interactive Timetable Creation", "The Administrator shall be able to create timetable entries through a side-by-side interface showing time slots and faculty availability."],
        ["FR-9", "AI Auto-Generator", "The Administrator shall be able to auto-generate complete, clash-free timetables for individual or all divisions with constraint satisfaction, batch rotation, and daily lab scheduling."],
        ["FR-10", "Faculty Clash Detection", "The system shall prevent a faculty member from being assigned to two entries at the same day and time slot, checked globally."],
        ["FR-11", "Room Clash Detection", "The system shall prevent a room from being assigned to two entries at the same day and time slot."],
        ["FR-12", "Division Clash Detection", "The system shall prevent a division from being assigned two entries at the same day and time slot."],
        ["FR-13", "Clash Logging with Resolution Tracking", "Detected clashes shall be recorded in a clash_logs table with type, severity, resolution status, resolved_by user, resolution_method, and resolution_note."],
        ["FR-14", "Admin Dashboard", "The system shall present a dashboard listing all divisions with clash indicators, entry counts, and room counts."],
        ["FR-15", "Faculty Schedule View", "Faculty members shall be able to view their personal teaching schedule organised by day."],
        ["FR-16", "Final Timetable View", "The system shall provide a consolidated, print-friendly view of created timetables across branches."],
        ["FR-17", "Global Search", "The system shall provide full-text search across faculty, subjects, divisions, branches, rooms, and clashes."],
        ["FR-18", "Clash Risk Prediction", "The system shall predict a clash-risk score (0\u20131) for a proposed entry using the trained ML model."],
        ["FR-19", "Slot Recommendation", "The system shall recommend up to five alternative time slots ranked by predicted clash risk."],
        ["FR-20", "Faculty Recommendation", "The system shall recommend up to five faculty candidates for a subject, scored by expertise and availability."],
        ["FR-21", "Timetable Quality Evaluation", "The system shall evaluate a division\u2019s overall timetable and report a quality score with issues and recommendations."],
        ["FR-22", "Model Training Endpoint", "The system shall provide an endpoint to (re-)train the ML model on the latest data in the database."],
        ["FR-23", "Intelligent Clash Resolution Suggestions", "The system shall generate ML-powered resolution suggestions for detected clashes."],
        ["FR-24", "Auto-Resolve Capability", "The system shall allow one-click application of ML-generated resolution suggestions to automatically resolve detected clashes."],
        ["FR-25", "CSV/ZIP Timetable Export", "The system shall provide CSV export for individual divisions, master all-semesters, faculty personal timetables, and bulk ZIP export."],
        ["FR-26", "Visiting Faculty Day-Wise Scheduling", "The system shall support per-day, per-time-slot availability configuration for visiting faculty."],
        ["FR-27", "Batch Management", "The system shall support automatic creation and management of lab batches within divisions (e.g., D1, D2, D3)."],
        ["FR-28", "Activity Logging", "The system shall log all significant administrative actions (auto-generation, profile updates) in an activity_logs table with user attribution."],
        ["FR-29", "AJAX Real-Time APIs", "The system shall provide JSON APIs for timetable entry CRUD, division data retrieval, and faculty availability without full page reloads."],
        ["FR-30", "Admin Profile Management", "Administrators shall be able to view and edit their profile details (name, email, password)."],
    ]
)

add_heading_custom("3.6 Non-Functional Requirements", level=2)
add_para("Table 3.2. Non-Functional Requirements")
add_table(
    ["ID", "Category", "Requirement"],
    [
        ["NFR-1", "Security", "Passwords shall be stored using Werkzeug\u2019s secure password hashing; sessions shall be managed by Flask\u2019s secure session handling."],
        ["NFR-2", "Authorization", "Role-based decorators shall restrict access to admin-only and faculty-only routes and API endpoints."],
        ["NFR-3", "Data Integrity", "SQLAlchemy ORM with parameterized queries shall be used to prevent SQL injection."],
        ["NFR-4", "Usability", "The interface shall use a modern, responsive layout with glassmorphism design that works on desktop, tablet, and mobile. Search/filter shall be available on all management listing pages."],
        ["NFR-5", "Performance", "Clash-risk prediction shall complete within 10ms; auto-generation shall complete within 5 seconds for a typical division."],
        ["NFR-6", "Maintainability", "The codebase shall be modularised into models, services, and templates for separation of concerns."],
        ["NFR-7", "Portability", "The application shall be deployable via a standard WSGI server (e.g., Gunicorn) behind a reverse proxy (e.g., Nginx)."],
        ["NFR-8", "Auditability", "Every detected clash shall be logged with a timestamp, resolution tracking, and all administrative actions shall be tracked in activity_logs."],
        ["NFR-9", "Resilience", "The application shall automatically fall back to a local SQLite database if the primary MySQL connection fails."],
    ]
)

add_heading_custom("3.7 Hardware Requirements", level=2)
add_para("Table 3.3. Hardware Requirements")
add_table(
    ["Component", "Minimum Requirement (Development)", "Recommended (Server / Deployment)"],
    [
        ["Processor", "Dual-core, 1.6 GHz or higher", "Quad-core, 2.5 GHz or higher"],
        ["RAM", "4 GB", "8 GB or more"],
        ["Storage", "5 GB free space", "20 GB+ (SSD preferred, scales with data)"],
        ["Network", "Broadband internet connection", "Stable connection with a public-facing reverse proxy"],
    ]
)

add_heading_custom("3.8 Software Requirements", level=2)
add_para("Table 3.4. Software Requirements")
add_table(
    ["Layer", "Technology"],
    [
        ["Programming Language", "Python 3.8 or higher"],
        ["Web Framework", "Flask"],
        ["ORM", "Flask-SQLAlchemy"],
        ["Database", "MySQL 5.7 or higher (with automatic SQLite fallback)"],
        ["Database Driver", "PyMySQL"],
        ["Security Libraries", "Werkzeug (password hashing), cryptography"],
        ["Authentication", "Flask-Login (session-based, role-based)"],
        ["Machine Learning", "scikit-learn 1.3.2, numpy 1.24.3, pandas 2.0.3, joblib 1.3.1"],
        ["Frontend", "HTML5, CSS3, JavaScript, Font Awesome icons"],
        ["Production Server", "Gunicorn (WSGI), Nginx (reverse proxy, optional SSL)"],
        ["Operating System", "Cross-platform (Windows / macOS / Linux)"],
    ]
)

add_heading_custom("3.9 Feasibility Study", level=2)

add_heading_custom("3.9.1 Technical Feasibility", level=3)
add_para("All technologies used in the project \u2013 Flask, Flask-SQLAlchemy, MySQL, PyMySQL, Werkzeug, Flask-Login, and scikit-learn \u2013 are mature, well-documented, open-source components with active community support, and are known to integrate well with one another in a typical Flask application layout. The automatic SQLite fallback further ensures the system can operate without external database dependencies during development or in degraded environments. The project is therefore technically feasible using standard, freely available tools.")

add_heading_custom("3.9.2 Economic Feasibility", level=3)
add_para("Every component of the technology stack \u2013 Python, Flask, MySQL, SQLite, and the scikit-learn ecosystem \u2013 is open-source and free to use, and the application can be self-hosted or deployed to low-cost or free-tier hosting. This keeps the direct software cost of adopting the system close to zero, with the main cost being the effort of deployment and maintenance.")

add_heading_custom("3.9.3 Operational Feasibility", level=3)
add_para("The system is operated through a standard web browser, requires no specialised client software, and mirrors the same conceptual workflow (branches \u2192 divisions \u2192 subjects \u2192 time slots \u2192 rooms \u2192 timetable) that administrative staff already follow manually, which keeps the learning curve manageable for non-technical administrative users. The AI auto-generator further reduces operational complexity by offering one-click timetable generation.")

add_heading_custom("3.10 User Roles", level=2)
add_para("Table 3.5. User Roles")
add_table(
    ["Role", "Description", "Key Permissions"],
    [
        ["Administrator", "Manages the institution-wide academic setup and builds timetables.", "Create/manage branches, divisions (with batches), subjects, time slots, rooms, faculty; create/edit/delete timetable entries; auto-generate timetables; view dashboard and clash logs; use global search; export timetables as CSV/ZIP; resolve clashes manually or via auto-resolve; access ML prediction, recommendation, and clash-suggestion endpoints; view activity log; manage admin profile."],
        ["Faculty", "Teaching staff who need to see and maintain their own teaching information.", "Complete/update personal profile (working hours, subjects taught, visiting schedule); view personal schedule organised by day; download personal timetable as CSV."],
    ]
)

add_heading_custom("3.11 Requirement Traceability Matrix", level=2)
add_para("Table 3.6. Requirement Traceability Matrix")
add_table(
    ["Requirement ID", "Traced To Module", "Verified By"],
    [
        ["FR-1", "Authentication Module", "Login/Signup test cases"],
        ["FR-2 \u2013 FR-6", "Branch / Division / Subject / Time-Slot / Room Management", "Management screen test cases"],
        ["FR-7", "Faculty Management Module", "Faculty profile test cases (including visiting schedule)"],
        ["FR-8", "Timetable Generation Module", "Timetable creation test cases"],
        ["FR-9", "AI Auto-Generator Module", "Auto-generation test cases"],
        ["FR-10 \u2013 FR-13", "Clash Detection Module", "Clash detection test cases"],
        ["FR-14 \u2013 FR-16", "Reports Module / Dashboard", "UI walkthrough and search test cases"],
        ["FR-17", "Global Search Module", "Global search test cases"],
        ["FR-18 \u2013 FR-22", "ML Clash Prediction Module", "ML endpoint test cases (Chapter 8)"],
        ["FR-23 \u2013 FR-24", "Intelligent Clash Resolution Module", "Clash suggestion and auto-resolve test cases"],
        ["FR-25", "Export Module", "CSV/ZIP download test cases"],
        ["FR-26", "Faculty Management Module", "Visiting faculty scheduling test cases"],
        ["FR-27", "Batch Management (Division)", "Batch creation and lab scheduling test cases"],
        ["FR-28", "Activity Logging Module", "Activity log display test cases"],
        ["FR-29", "AJAX API Module", "AJAX API endpoint test cases"],
        ["FR-30", "Admin Profile Module", "Profile update test cases"],
    ]
)

page_break()

# ============================================
# CHAPTERS 4-10 (continuing with same pattern)
# ============================================

# Due to the very large size of the complete report, the remaining chapters
# follow the exact same structure as the markdown content but with additions
# for the new features. Let me continue writing the remaining chapters.

# CHAPTER 4: SYSTEM ANALYSIS AND DESIGN
add_heading_custom("Chapter 4: System Analysis And Design", level=1)

add_heading_custom("4.1 System Architecture", level=2)
add_para("The system follows a layered, monolithic web-application architecture typical of Flask projects. The Presentation Layer consists of server-rendered HTML templates (in the templates/ directory) styled with CSS and enhanced with JavaScript for interactivity (e.g., the ML risk badges, recommendation panel, AI resolution suggestion panel, and AJAX-based timetable management). The Application Layer consists of the Flask route handlers defined in app.py, which coordinate requests, enforce authentication/authorization, and call into the Service Layer. The Service Layer consists of dedicated service modules under services/ \u2013 principally clash_service.py (faculty/room/division clash checks, ML prediction wrappers, and intelligent resolution suggestion generation), ml_clash_predictor.py (Random Forest based clash-risk engine), and auto_generator_service.py (AI auto-generator with constraint satisfaction). The Data Layer consists of the SQLAlchemy models defined in models.py (User, Faculty, Branch, Division, Batch, TimeSlot, Subject, Room, Timetable, ClashLog, ActivityLog), mapped onto a MySQL database (with automatic SQLite fallback). The trained machine-learning model itself is persisted to disk under ml_models/clash_predictor_model.pkl using joblib.")
add_para("(Insert Figure 4.1 \u2013 System Architecture Diagram)", italic=True)

add_heading_custom("4.2 Overall Workflow", level=2)
add_para("At a high level, the Administrator signs up or logs in, sets up the foundational data (branches, divisions with batch configuration, subjects with lab/lecture settings, time slots, rooms), then either creates a timetable manually for a chosen branch/division/day through the interactive side-by-side interface, or uses the AI auto-generator to produce a complete, clash-free timetable automatically. When creating manually, for each time slot, the administrator selects a subject, views faculty availability and ML recommendations, selects an available faculty member, chooses a room, and submits the entry \u2013 which the system validates for clashes before adding it. When a clash is detected, the administrator can view AI-powered resolution suggestions and auto-apply any suggestion with a single click. The AI auto-generator handles all of these steps automatically, producing daily lab blocks with batch rotation, lecture scheduling with non-repetition, and library periods for surplus slots. All administrative actions are logged in the activity_logs table. Faculty members sign up, complete their profile (working hours, subjects they can teach, and visiting schedule if applicable), and view their personal schedule. Both administrators and faculty can export timetables as CSV files, and administrators can perform global search across all entities.")
add_para("(Insert Figure 4.2 \u2013 Overall Workflow Diagram)", italic=True)

add_heading_custom("4.3 Module Identification", level=2)
add_para("Table 4.1. Module Identification")
add_table(
    ["Module", "Responsibility"],
    [
        ["Authentication Module", "Sign-up, login, logout, session management, password hashing/verification, default admin seeding."],
        ["Faculty Management Module", "Faculty profile creation and update; working hours, taught-subjects, and visiting schedule storage; visiting faculty day-wise time-slot configuration."],
        ["Room & Resource Management Module", "Create, edit, delete, and search/filter rooms/resources with name, capacity, and type (Classroom, Lab, Seminar Hall)."],
        ["Subject Management Module", "Create, edit, delete, and search/filter subjects with code, credits, weekly lectures, semester, branch, and lab flag."],
        ["Batch Management Module", "Automatic creation and naming of lab batches (D1, D2, D3) within divisions; batch-aware timetable entry support."],
        ["Timetable Generation Module", "Interactive side-by-side timetable creation screen and entry CRUD; room selection from Room inventory; batch-aware lab entry creation."],
        ["AI Auto-Generator Module", "Constraint-satisfaction based automatic timetable generation with zero-clash guarantee, daily lab scheduling, batch rotation, lecture quota enforcement, and library auto-fill."],
        ["Clash Detection Module", "Faculty, room, and division clash checks; visiting faculty availability enforcement; batch-aware validation; clash logging with full resolution tracking."],
        ["ML Clash Prediction Module", "Random Forest based clash-risk prediction, slot & faculty recommendation, quality evaluation."],
        ["Intelligent Clash Resolution Module", "ML-powered resolution suggestion generation for detected clashes; alternative rooms, faculty, and time slots; one-click auto-resolve."],
        ["Activity Logging Module", "Tracking all significant administrative actions (auto-generation, profile updates) with user attribution, timestamps, and entity references."],
        ["Global Search Module", "Full-text search across faculty, subjects, divisions, branches, rooms, and clashes with dedicated search results page."],
        ["Reports & Export Module", "Admin dashboard, final timetable view, view-clashes screen with AI suggestions, CSV/ZIP timetable export (individual, master, faculty personal), activity log page."],
        ["Admin Profile Module", "View and edit administrator profile details (name, email, username, password)."],
    ]
)

add_heading_custom("4.4 Authentication Module", level=2)
add_para("The Authentication Module is built around the User SQLAlchemy model, which stores a username, email, a hashed password (never the plaintext password), a full name, and a role field distinguishing \u2018admin\u2019 from \u2018faculty\u2019. Password hashing and verification use Werkzeug\u2019s generate_password_hash and check_password_hash functions, wrapped by the set_password and check_password methods on the User model. The User model also mixes in Flask-Login\u2019s UserMixin, allowing session-based login state to be tracked by Flask-Login. On successful signup, a Faculty role account additionally creates a linked Faculty profile row (a one-to-one relationship, cascade-deleted with the user). The system also auto-seeds a default admin user (\u2018admin\u2019 / \u2018admin123\u2019) during initialisation if none exists.")
add_para("(Insert Figure 4.3 \u2013 Login and Sign up Page screenshot)", italic=True)

add_heading_custom("4.5 Faculty Management Module", level=2)
add_para("The Faculty model stores a foreign key to the owning User, along with phone, department, and designation fields, and two JSON-encoded text fields: working_hours (a JSON object with start and end keys) and subjects_can_teach (a JSON array of subject names). Helper methods serialise and deserialise these fields, and an is_available boolean flag marks whether the faculty member is currently accepting new assignments. The Faculty model exposes a timetable_entries relationship, giving direct access to every Timetable row that references that faculty member.")
add_para("The Faculty model additionally supports visiting faculty through three dedicated fields: is_visiting (Boolean), visiting_available_days (JSON array of day names), and visiting_slot_ids (JSON dictionary mapping each day to a list of time-slot IDs). Helper methods include set_visiting_days/get_visiting_days, set_visiting_slots/get_visiting_slots (with legacy list fallback), get_visiting_schedule (returning a day\u2192slot-IDs dictionary), and is_available_for_slot(day, time_slot), which automatically distinguishes between regular and visiting faculty to determine availability. The Faculty Profile UI presents a custom toggle switch for marking visiting status, a day-checkbox grid for selecting available days, and per-day time-slot chip selectors for granular availability control.")
add_para("(Insert Figure 4.4 \u2013 Faculty Profile (Regular Faculty) screenshot)", italic=True)
add_para("(Insert Figure 4.5 \u2013 Faculty Profile (Visiting Faculty \u2013 Day-wise Scheduling) screenshot)", italic=True)

add_heading_custom("4.6 Room & Resource Management Module", level=2)
add_para("The Room model is a first-class entity in the database schema, storing a unique name (e.g., \u201c101\u201d, \u201cLab-A\u201d), a capacity (integer, default 60), a room_type (\u2018Classroom\u2019, \u2018Lab\u2019, or \u2018Seminar Hall\u2019), created_by (admin user ID), and created_at. The Manage Rooms screen allows the Administrator to add, edit, and delete rooms/resources through a structured form, with search/filter capability for finding rooms by name or type. An edit modal supports inline editing of room attributes. The Room Clash check in the Clash Detection Module uses this Room data to verify that a room is not double-booked. The AI Auto-Generator also uses the Room inventory to allocate classrooms for lectures and lab rooms for laboratory sessions, ensuring no room is double-booked across parallel batches or divisions.")
add_para("(Insert Figure 4.9 \u2013 Manage Rooms & Resources screenshot)", italic=True)

add_heading_custom("4.7 Subject Management Module", level=2)
add_para("The Subject model stores a name, a unique code, a credits integer (defaulting to 3), a weekly_lectures field (specifying the required number of lectures per week), a semester field (tying the subject to a specific semester), a branch_id (linking to the parent branch), and a has_lab boolean (indicating whether the subject has a laboratory component). Subjects are referenced by Timetable entries via subject_id, and by Faculty profiles indirectly through the subjects_can_teach JSON list. The required_lectures property returns the weekly_lectures value (falling back to credits), and the required_labs property returns 1 if has_lab is True. The Manage Subjects screen supports search/filter by subject name, code, branch, and semester.")
add_para("(Insert Figure 4.8 \u2013 Manage Subjects screenshot)", italic=True)

add_heading_custom("4.8 Timetable Generation Module", level=2)
add_para("The Timetable model is the core entity of the system: each row references a division_id, subject_id (nullable for library/break entries), faculty_id (nullable for library/break entries), time_slot_id, and batch_id (nullable for full-division entries), together with a day string (Monday through Saturday), room_number (nullable for library/break entries), entry_type (\u2018lecture\u2019, \u2018lab\u2019, \u2018library\u2019, or \u2018break\u2019), is_manual (boolean distinguishing manual from auto-generated entries), and created_by. The timetable-creation screen presents, for a selected branch/division/day, the configured time slots with entry-creation forms and existing entries with edit/delete options. A live faculty-availability panel shows each faculty member\u2019s busy/available status. The ML recommendations panel auto-appears on subject selection, showing recommended faculty and best time slots. The system supports dynamic lab start slot detection, ensuring labs can only be scheduled at the beginning of two-hour continuous blocks. For divisions with multiple batches, the interface allows batch-specific lab entries, enabling parallel lab sessions.")
add_para("(Insert Figure 4.10 \u2013 Timetable Creation (Side-by-Side) Interface screenshot)", italic=True)

add_heading_custom("4.9 AI Auto-Generator Module", level=2)
add_para("The AI Auto-Generator Module, implemented in services/auto_generator_service.py, provides fully automated timetable construction for a given division using constraint satisfaction combined with ML risk minimisation. The auto-generator enforces the following strict rules:")
add_bullet("Absolute Zero Clashes Guarantee: Evaluates all existing timetable entries across ALL divisions in the database plus uncommitted entries before making any assignment. Never force-assigns a faculty member if they are busy in any division or batch.")
add_bullet("Dynamic Batch Naming: Automatically names batches formatted as {DivisionName}{Number} (e.g., A1, A2, A3 for Division A).")
add_bullet("Varying Lab Time Windows Across Days: Lab hours vary dynamically across different days (e.g., Monday 10:30\u201312:30, Tuesday 13:00\u201315:00, Wednesday 08:30\u201310:20) using rotating window selection influenced by semester offset.")
add_bullet("Daily Two-Hour Lab Block: Every weekday (Monday to Friday) has a compulsory two-hour lab session for all batches, with parallel room and faculty allocation for multi-batch divisions.")
add_bullet("No Batch Lab Repetition: Batches rotate through all lab subjects during the week with zero duplicate lab subjects per batch, tracked via batch_lab_history.")
add_bullet("Non-Consecutive Lectures: Lectures rotate so no subject repeats consecutively within a day.")
add_bullet("Strict Lecture Quota Enforcement: Each subject is limited to its required_lectures per week; surplus slots are filled with Library periods.")
add_bullet("Faculty Workload Limits: 30-hour weekly and 6-hour daily workload caps are enforced for each faculty member.")
add_bullet("Strict Time Boundary: Only college hours (08:30 AM to 03:00 PM) are used.")
add_para("The auto-generator can be invoked for a single division via GET /timetable/auto-generate/<division_id> or for all divisions simultaneously via GET /timetable/auto-generate-all. The overwrite mode deletes existing auto-generated entries (preserving manual entries) before regeneration. The system additionally exposes an AJAX API endpoint (POST /api/auto-generate/<division_id>) for non-reload invocation from the dashboard.")
add_para("(Insert Figure 4.11 \u2013 AI Auto-Generator Preview Screen)", italic=True)

add_heading_custom("4.10 Clash Detection Module", level=2)
add_para("The Clash Detection Module, implemented in services/clash_service.py, performs three checks whenever an entry is proposed: a Faculty Clash check (globally scoped across all branches and divisions), a Room Clash check (by room_number, day, and time_slot_id), and a Division Clash check (by division_id, day, and time_slot_id). For lab entries, the system additionally validates the next time slot for faculty availability and room availability, since labs occupy two consecutive slots. For visiting faculty, the system enforces availability constraints by checking is_available_for_slot before allowing assignment. When a clash is found, a ClashLog row is created with clash_type, severity, JSON clash_details, resolution tracking fields, and references to the relevant division and faculty.")

add_heading_custom("4.11 Intelligent Clash Resolution Module", level=2)
add_para("The Intelligent Clash Resolution Module extends the clash detection system with ML-powered resolution capabilities. When a clash is detected and displayed in the View Clashes screen, the administrator can click \u201cGet AI Suggestions\u201d to invoke the resolution engine, which generates context-aware suggestions based on the clash type:")
add_bullet("Room Clash: suggests alternative rooms that are available at the same day/time (prioritising free rooms from the Room inventory, with ML-predicted risk scores), alternative time slots, and alternative faculty members.")
add_bullet("Faculty Clash: suggests alternative available faculty (scored by subject expertise and availability via ML), alternative time slots, and alternative rooms.")
add_bullet("Division Clash: suggests alternative time slots and alternative rooms.")
add_para("Each suggestion includes a description, detail text, risk score, risk level (low/medium/high colour-coded), and a one-click \u201cApply\u201d button that triggers auto-resolve. The apply_suggestion method handles three action types: change_room, change_faculty, and change_timeslot. After auto-resolve, the ClashLog is marked resolved with resolution_method=\u2018auto\u2019 and an appropriate resolution_note.")

add_heading_custom("4.12 Reports & Export Module", level=2)
add_para("The Reports & Export Module comprises: the Admin Dashboard (listing all divisions with green/red clash indicators, entry counts, and room counts), the Final Timetable View (a consolidated, print-friendly view of created timetables across branches), the View Clashes screen (a listing of ClashLog entries with tabs for active/resolved clashes, filter bar, statistics cards, and AI suggestion panels), CSV/ZIP export (individual division CSV, bulk ZIP, master all-semesters CSV, and faculty personal timetable CSV), the Activity Log page (a filterable, searchable view of all administrative actions), and the Admin Profile page.")

add_heading_custom("4.13 Activity Logging Module", level=2)
add_para("The Activity Logging Module, built around the ActivityLog model, provides a comprehensive audit trail of all significant administrative actions in the system. Each ActivityLog record stores: user_id (the user who performed the action), user_name (cached for display), action_type (categorised string such as \u2018AUTO_GENERATE\u2019, \u2018PROFILE_UPDATE\u2019), description (human-readable text describing what happened), entity_type (the type of entity affected, e.g., \u2018division\u2019, \u2018user\u2019), entity_id (the ID of the affected entity), details_json (optional JSON payload with additional context), and created_at (timestamp). A static log() helper method creates and commits an ActivityLog record safely, with automatic rollback on failure. The Activity Log page (/admin/activity-log) displays a filterable, searchable list of up to 300 recent log entries, with filtering by action_type and full-text search across description, user_name, and entity_type.")

add_heading_custom("4.14 Global Search Module", level=2)
add_para("The Global Search Module provides a full-text search across six entity types: faculty (by name, email, department, designation), subjects (by name, code), divisions (by name, branch, academic year), branches (by name, short name), rooms (by room number), and clashes (by type, severity, or detail text). Search results are displayed on a dedicated search_results.html page with category-wise grouping and total result count.")

# UML Diagrams sections
for section, figure in [
    ("4.15 Use Case Diagram", "Fig 4.12: Use Case Diagram"),
    ("4.16 Activity Diagram", "Fig 4.13: Activity Diagram \u2013 Timetable Creation"),
    ("4.17 Sequence Diagram", "Fig 4.14: Sequence Diagram \u2013 Clash Detection and Resolution"),
    ("4.18 Class Diagram", "Fig 4.15: Class Diagram"),
    ("4.19 ER Diagram", "Fig 4.16: Entity Relationship (ER) Diagram"),
    ("4.20 Component Diagram", "Figure 4.17. Component Diagram"),
    ("4.21 Deployment Diagram", "Figure 4.18. Deployment Diagram"),
    ("4.22 DFD Level 0", "Figure 4.19. Data Flow Diagram \u2013 Level 0"),
    ("4.23 DFD Level 1", "Figure 4.20. Data Flow Diagram \u2013 Level 1"),
    ("4.24 DFD Level 2", "Figure 4.21. Data Flow Diagram \u2013 Level 2"),
]:
    add_heading_custom(section, level=2)
    add_para(f"(Insert updated {figure})", italic=True)

page_break()

# ============================================
# CHAPTER 5: SYSTEM IMPLEMENTATION
# ============================================
add_heading_custom("Chapter 5: System Implementation", level=1)

add_heading_custom("5.1 Introduction", level=2)
add_para("This chapter documents how the system described in Chapter 4 was implemented, covering the project\u2019s folder structure, the frontend templates, the Flask backend, the MySQL database setup (with SQLite fallback), authentication, the dashboard, the timetable-generation screens, AI auto-generator, batch & laboratory management, clash detection, intelligent clash resolution, activity logging, global search, AJAX real-time APIs, CSV/ZIP export, room management, visiting faculty scheduling, report generation, and deployment.")

add_heading_custom("5.2 Project Structure", level=2)
add_para("The repository is organised as a standard Flask project. At the root, app.py is the main Flask application containing the route handlers (~2,394 lines); extensions.py defines the shared SQLAlchemy db instance; models.py defines all database models (User, Faculty, Branch, Division, Batch, TimeSlot, Subject, Room, Timetable, ClashLog, ActivityLog \u2013 ~471 lines); requirements.txt lists Python dependencies; and run.py is the application entry point. A services/ directory contains clash_service.py (clash detection, intelligent resolution, and ML wrapper methods \u2013 ~1,118 lines), ml_clash_predictor.py (the ML engine \u2013 ~510 lines), and auto_generator_service.py (the AI auto-generator \u2013 ~690 lines). A templates/ directory holds 25 HTML views. An ml_models/ directory stores the persisted, trained Random Forest model file.")

add_para("Table 5.1. Project Structure")
add_table(
    ["Path", "Purpose"],
    [
        ["app.py", "Main Flask application (~2,394 lines); route handlers for admin management, timetable CRUD, auto-generation, global search, CSV/ZIP export, room management, activity log, admin profile, ML/resolution API endpoints, and AJAX APIs."],
        ["models.py", "SQLAlchemy models: User, Faculty, Branch, Division, Batch, TimeSlot, Subject, Room, Timetable, ClashLog, ActivityLog (~471 lines)."],
        ["extensions.py", "Shared SQLAlchemy db object, imported by both app.py and models.py."],
        ["services/clash_service.py", "Faculty/room/division clash-checking, visiting faculty validation, batch-aware validation, intelligent resolution suggestion generation, auto-resolve logic, and ML wrapper methods (~1,118 lines)."],
        ["services/ml_clash_predictor.py", "Random Forest based clash-risk engine (~510 lines): prediction, recommendation, evaluation, training."],
        ["services/auto_generator_service.py", "AI Auto-Generator Service (~690 lines): constraint-satisfaction based automatic timetable generation with zero-clash guarantee, daily lab scheduling, batch rotation, lecture quota enforcement, workload limits, and library auto-fill."],
        ["templates/*.html", "25 server-rendered views: base, signup, login, admin_dashboard, admin_profile, faculty_dashboard, faculty_profile, manage_branches, manage_divisions, manage_subjects, manage_timeslots, manage_rooms, manage_faculty, timetable_select, timetable_create, timetable_preview, view_timetable, edit_timetable_entry, edit_timeslot, final_timetable_view, view_clashes, search_results, activity_log, 404, 500."],
        ["ml_models/clash_predictor_model.pkl", "Persisted, trained Random Forest model (joblib format, ~92 KB)."],
        ["requirements.txt", "Python dependencies including Flask, Flask-SQLAlchemy, Flask-Login, PyMySQL, scikit-learn, numpy, pandas, joblib."],
    ]
)

add_heading_custom("5.3 Frontend Implementation", level=2)
add_para("The frontend is implemented as server-rendered HTML templates using a shared base.html layout (~31 KB), styled with CSS to give a modern gradient (purple/blue/teal) glassmorphism design, and using Font Awesome icons throughout. The interface is responsive across desktop, tablet, and mobile screen sizes. Interactive behaviour \u2013 such as fetching and displaying ML risk predictions, recommendations, AI resolution suggestions, and AJAX-based timetable CRUD without full page reloads \u2013 is implemented in JavaScript using the Fetch API against the JSON endpoints exposed by app.py. Colour coding is used consistently: green for success/available/no-clash states, red for error/busy/clash states, purple/teal gradients for AI/ML features, and blue for informational elements. All management listing pages include search/filter bars for rapid filtering. The timetable creation interface features dynamic slot status indicators showing whether a slot is fully occupied, has batch assignments, or is available for new entries.")

add_heading_custom("5.4 Backend Implementation", level=2)
add_para("The backend is implemented in app.py using Flask\u2019s routing decorators, spanning approximately 2,394 lines. Distinct route groups exist for: authentication (signup/login/logout), Administrator management screens (branches, divisions with batch configuration, subjects, time slots, rooms, faculty), the timetable-creation workflow (select branch/division/day, create/edit/delete entries with batch-aware support, library/break special entries), the AI auto-generator (single-division and all-division modes), the Faculty portal (profile with visiting schedule, personal schedule, CSV download), the reporting views (dashboard, final timetable view, view clashes with AI suggestions, activity log, admin profile), the global search route, the CSV/ZIP export routes (individual, master all-semesters, bulk ZIP), the three clash-resolution endpoints, the six ML API endpoints, and the AJAX real-time API endpoints. Administrator-only routes are protected by the admin_required decorator, and Faculty-only routes check current_user.role.")

add_heading_custom("5.5 Database Implementation", level=2)
add_para("The database is primarily implemented in MySQL, connected via the SQLALCHEMY_DATABASE_URI configuration string. If the primary MySQL connection fails at startup, the application automatically falls back to a local SQLite database (sqlite:///timetable_system.db). Tables are created from the SQLAlchemy model definitions by calling db.create_all(). An auto-migration block at startup attempts to add any missing columns (visiting faculty fields, resolution tracking fields, batch/lab fields, entry_type) to existing tables, ensuring backward compatibility with older database schemas. The system supports PostgreSQL URL format conversion and Aiven MySQL SSL mode handling for cloud database providers.")

add_heading_custom("5.6 Authentication Implementation", level=2)
add_para("On sign-up, a new User row is created with the chosen role; the plaintext password is never stored \u2013 instead, User.set_password() calls Werkzeug\u2019s generate_password_hash(). On login, User.check_password() calls check_password_hash() to verify the submitted password against the stored hash. Successful login establishes a Flask-Login session (User mixes in UserMixin). Signing up as Faculty additionally creates the linked Faculty profile row. A default admin user (\u2018admin\u2019 / \u2018admin123\u2019) is automatically seeded during initialisation if none exists.")

add_heading_custom("5.7 Dashboard Implementation", level=2)
add_para("The Admin Dashboard queries all Division rows together with their associated Timetable entries and ClashLog rows, and renders each division with a green indicator if it has no unresolved clashes or a red indicator if it does, alongside the count of timetable entries. The dashboard displays total counts for branches, divisions, faculty, subjects, and rooms, and shows recent unresolved clashes. Quick-navigation links allow administrators to view, edit, continue building, or auto-generate a division\u2019s timetable directly from the dashboard. The Faculty Dashboard displays the logged-in faculty member\u2019s personal schedule organised by day.")
add_para("(Insert Figure 5.1 \u2013 Admin Dashboard screenshot)", italic=True)
add_para("(Insert Figure 5.2 \u2013 Faculty Dashboard screenshot)", italic=True)

add_heading_custom("5.8 Timetable Generation Implementation", level=2)
add_para("The timetable_select.html screen lets the Administrator choose a Branch, Division, and Day. The timetable_create.html screen then lists the configured TimeSlot rows for that day; for each slot, existing entries are shown with Edit/Delete actions, and a form is provided to add a new entry (subject dropdown, faculty dropdown populated from the faculty-availability API, room selection from Room inventory, batch selection for multi-batch divisions, entry type selection for lab/lecture/library/break, and ML recommendations). The faculty-availability panel shows each faculty member\u2019s availability status and subjects, with separate checks for lecture slots and lab slots (which verify both the current and next slot for two-hour blocks). Dynamic lab start slot detection ensures labs can only begin at valid two-hour continuous block boundaries. Subject load tracking shows how many lectures each subject has been scheduled for against its weekly quota.")
add_para("(Insert Figure 5.3 \u2013 Faculty Availability Panel screenshot)", italic=True)

add_heading_custom("5.9 AI Auto-Generator Implementation", level=2)
add_para("The AI Auto-Generator is implemented in services/auto_generator_service.py as the AutoTimetableGenerator class with static methods generate_timetable() and preview_timetable(). The generation algorithm operates in two phases:")
add_para("Phase 1 \u2013 Compulsory Lab Scheduling: For each weekday (Monday\u2013Friday), the algorithm selects a two-hour lab window from three rotating windows (08:30\u201310:20, 10:30\u201312:30, 13:00\u201315:00), with the rotation offset influenced by both day index and semester to prevent cross-semester faculty bottlenecks. For each batch in the division, it selects a lab subject (prioritising unscheduled subjects, then subjects not yet assigned to this batch), finds a free lab room, and identifies the best available faculty member. The faculty selection follows a strict three-tier priority: (1) designated faculty from the curriculum matrix, (2) faculty who explicitly listed the subject in their profile, (3) any available faculty. All selections are validated against global clash checks, visiting faculty availability, and daily/weekly workload limits (6 hours/day, 30 hours/week). If a window fails for any batch, the algorithm tries the next window; if all windows fail, a secondary pass with relaxed constraints is attempted.")
add_para("Phase 2 \u2013 Lecture and Library Filling: The remaining non-lab slots are filled with lectures, respecting each subject\u2019s weekly lecture quota (required_lectures property). Subjects are rotated to avoid consecutive repetition. When all subjects have fulfilled their quotas, remaining slots are filled with Library periods. If a slot cannot be filled due to resource constraints (no free room or available faculty), a ClashLog warning is generated suggesting the administrator add more rooms or faculty, and the slot defaults to Library.")
add_para("The auto-generator supports both single-division (GET /timetable/auto-generate/<division_id>) and bulk all-division (GET /timetable/auto-generate-all) modes. An overwrite mode deletes existing auto-generated entries while preserving manual entries. The preview endpoint (/timetable/preview-auto-generate/<division_id>) shows the current timetable state without modifying it.")

add_heading_custom("5.10 Batch & Laboratory Management Implementation", level=2)
add_para("The Batch model represents lab batches within a division (e.g., D1, D2, D3 of CSE-A). Each division has a num_batches field (default 1) and a student_count field (default 60). When a division is created with num_batches > 1, the system automatically creates Batch rows with names formatted as D{number} and student counts distributed evenly. The Timetable model includes a nullable batch_id foreign key: when batch_id is NULL, the entry applies to the full division (lectures, library, break); when batch_id is set, the entry applies only to that specific batch (typically lab sessions). The timetable creation interface adapts based on the division\u2019s batch configuration: for multi-batch divisions, lab slots show separate entries per batch with batch labels, and the entry form includes a batch selector. The auto-generator\u2019s Phase 1 handles multi-batch lab scheduling by allocating different rooms, subjects, and faculty to each batch in parallel during the same lab window.")

add_heading_custom("5.11 Clash Detection Implementation", level=2)
add_para("When the Administrator submits a new (or edited) Timetable entry, app.py calls into services/clash_service.py before committing the row. The Faculty Clash check verifies no existing Timetable row has the same faculty_id, day, and time_slot_id anywhere in the system. The Room Clash check verifies no existing row has the same room_number, day, and time_slot_id. The Division Clash check verifies no existing row has the same division_id, day, and time_slot_id (for full-division entries) or the same batch_id, day, and time_slot_id (for batch-specific entries). For lab entries, the system additionally validates the next consecutive slot for both faculty and room availability. For visiting faculty, is_available_for_slot is enforced, checking both day availability and per-day time-slot configuration. If any check returns a conflict, a ClashLog entry is created with full details, and the entry submission is rejected with descriptive error messages.")

add_heading_custom("5.12 Intelligent Clash Resolution Implementation", level=2)
add_para("The Intelligent Clash Resolution is implemented as two API endpoints and a dedicated UI panel in view_clashes.html:")
add_para("1. GET /api/ml/clash-suggestions/<clash_id> \u2013 Calls ClashService.generate_resolution_suggestions(), which analyses the clash type and details, finds the matching time slot, and generates context-aware suggestions: for room clashes (alternative free rooms with ML risk scores, time slot shifts, faculty swaps), for faculty clashes (alternative faculty scored by ML expertise and availability, time slot shifts, room alternatives), and for division clashes (time slot alternatives and room changes).")
add_para("2. POST /admin/clashes/auto-resolve/<clash_id> \u2013 Receives action_type and action_value, applies the change to the conflicting Timetable entry, and marks the ClashLog as resolved with resolution_method=\u2018auto\u2019.")
add_para("The view_clashes.html UI displays suggestions in a glassmorphism-styled AI panel with animated slide-down entrance, colour-coded risk badges (green=low, orange=medium, red=high), and one-click \u201cApply\u201d buttons. A \u201cClear All Clashes\u201d feature allows administrators to purge all logged clashes from the database. Statistics cards show total, resolved, and pending clash counts.")
add_para("(Insert Figure 5.4 \u2013 View Clashes Screen with AI Resolution Suggestions screenshot)", italic=True)

add_heading_custom("5.13 Activity Logging Implementation", level=2)
add_para("The ActivityLog model provides audit trail functionality with action_type categorisation (e.g., \u2018AUTO_GENERATE\u2019, \u2018PROFILE_UPDATE\u2019), human-readable descriptions, entity references, and optional JSON details payloads. The static log() helper method safely creates and commits log entries with automatic rollback on failure. Activity logging is integrated into key administrative actions: the AI auto-generator logs successful generation results with entry counts, and the admin profile route logs profile updates. The activity log page (/admin/activity-log) provides a filterable, searchable display of up to 300 recent entries, with an action_type dropdown filter and full-text search across description, user_name, and entity_type.")
add_para("(Insert Figure 5.8 \u2013 Activity Log Page screenshot)", italic=True)

add_heading_custom("5.14 Global Search Implementation", level=2)
add_para("The global search is implemented via the /search route, which accepts a query parameter q and searches across six entity types using SQLAlchemy ilike filters: Faculty (by full_name, email, department, designation), Subjects (by name, code), Divisions (by name, branch name, branch short_name, academic_year), Branches (by name, short_name), Rooms (by room_number from timetable entries), and Clashes (by clash_type, severity, clash_details). Results are rendered on search_results.html with category-wise grouping and total counts.")

add_heading_custom("5.15 CSV/ZIP Export Implementation", level=2)
add_para("Four export endpoints are implemented:")
add_bullet("GET /admin/timetable/export \u2013 Exports all divisions that have timetable entries as a ZIP file containing one CSV per division.")
add_bullet("GET /timetable/download/<division_id> \u2013 Exports a single division\u2019s timetable as a CSV file with grid format (Time rows \u00d7 Day columns).")
add_bullet("GET /timetable/export-master-csv \u2013 Exports a master CSV containing all semesters and divisions in a single file with section separators.")
add_bullet("GET /faculty/timetable/download \u2013 Exports the logged-in faculty member\u2019s personal timetable as a CSV file.")
add_para("Each CSV includes batch labels for multi-batch lab entries, entry type indicators (LIBRARY, BREAK), and room numbers.")

add_heading_custom("5.16 AJAX Real-Time API Implementation", level=2)
add_para("The system provides a comprehensive set of AJAX JSON APIs for real-time, non-reload interactions:")
add_bullet("GET /api/division/<division_id>/subjects \u2013 Returns filtered subjects for a division\u2019s semester and branch, with lab flag and required lecture count.")
add_bullet("GET /api/subject/<subject_id>/faculties \u2013 Returns qualified faculty for a subject based on subjects_can_teach matching.")
add_bullet("GET /api/division/<division_id>/timetable-data \u2013 Returns the complete timetable grid for a division as a JSON structure.")
add_bullet("POST /api/timetable/add-entry \u2013 Creates a timetable entry via AJAX with full clash validation, supporting lecture, lab, library, and break entry types.")
add_bullet("POST|DELETE /api/timetable/delete-entry/<entry_id> \u2013 Deletes a timetable entry via AJAX.")
add_bullet("POST /api/auto-generate/<division_id> \u2013 Triggers AI auto-generation for a division via AJAX with activity logging.")
add_para("These AJAX APIs enable the timetable creation interface to perform operations without full page reloads, providing a smoother user experience.")

add_heading_custom("5.17 Report Generation", level=2)
add_para("The Final Timetable View aggregates Timetable entries across all branches and divisions into a single, print-optimised view. The View Clashes screen lists ClashLog rows with tabbed views (Active Clashes and Resolved Clashes), a filter bar, statistics cards, and AI-powered suggestion panels. The Admin Profile page allows administrators to view and edit their account details including username, email, full name, and password, with duplicate checking and activity logging.")

add_heading_custom("5.18 Deployment", level=2)
add_para("For production deployment, the README documents changing the Flask SECRET_KEY, disabling debug mode, pointing SQLALCHEMY_DATABASE_URI at a production MySQL server, running under Gunicorn, and placing Nginx as a reverse proxy with SSL. The application supports PostgreSQL URL format conversion (postgres:// \u2192 postgresql://) and Aiven MySQL SSL mode handling for cloud database providers. A live deployment is hosted at timetable-clash-resolution.onrender.com.")

page_break()

# ============================================
# CHAPTER 6: TIMETABLE GENERATION AND CLASH RESOLUTION
# ============================================
add_heading_custom("Chapter 6: Timetable Generation And Clash Resolution", level=1)

add_heading_custom("6.1 Introduction", level=2)
add_para("This chapter examines, in detail, how the system builds a timetable entry by entry and how it detects, prevents, and resolves clashes, covering the deterministic Clash Detection Service, the AI Auto-Generator with constraint satisfaction, the Intelligent Clash Prevention and Recommendation module (machine-learning based), and the Intelligent Clash Resolution Suggestions and Auto-Resolve module.")

add_heading_custom("6.2 Timetable Scheduling Problem", level=2)
add_para("Formally, the system must assign, for each division and each day, a subject, a faculty member, a room, and a time slot such that: (a) no faculty member is assigned to two different (division, time-slot) pairs on the same day, (b) no room is assigned to two different (division, time-slot) pairs on the same day, (c) no division is assigned two different (subject, time-slot) pairs on the same day, and (d) visiting faculty are only assigned during their configured availability windows. The system solves this both incrementally (validating each proposed entry against all previously accepted entries) and automatically (via the AI auto-generator that constructs a complete solution using constraint satisfaction).")

add_heading_custom("6.3 Scheduling Constraints", level=2)
add_heading_custom("6.3.1 Hard Constraints", level=3)
add_bullet("Faculty Constraint: a faculty member cannot be scheduled for two entries with the same day and time_slot_id, checked globally across all branches and divisions.")
add_bullet("Room Constraint: a room_number cannot be scheduled for two entries with the same day and time_slot_id.")
add_bullet("Division Constraint: a division_id cannot be scheduled for two entries with the same day and time_slot_id (for full-division entries).")
add_bullet("Batch Constraint: a batch_id cannot be scheduled for two entries with the same day and time_slot_id (for batch-specific entries).")
add_bullet("Visiting Faculty Availability Constraint: a visiting faculty member can only be scheduled on days and time slots configured in their visiting schedule (enforced via is_available_for_slot).")
add_bullet("Lab Continuity Constraint: lab entries must start at the beginning of a two-hour continuous block, and faculty/room must be available for both slots.")
add_bullet("Faculty Workload Constraint (Auto-Generator): maximum 30 hours/week and 6 hours/day per faculty member.")

add_heading_custom("6.3.2 Soft Constraints", level=3)
add_para("The system addresses several soft preferences through ML and the auto-generator: preferring faculty with higher subject expertise (used by faculty recommendation and auto-generator\u2019s curriculum matrix), preferring time slots with lower predicted clash-risk score (used by slot recommendation), non-consecutive lecture scheduling (enforced by the auto-generator), varying lab windows across days to distribute load (enforced by the auto-generator), and suggesting lower-risk alternatives when clashes are detected.")

add_heading_custom("6.4 Faculty Allocation", level=2)
add_para("Faculty allocation begins with the Faculty profile: each Faculty row stores subjects_can_teach, working_hours, and visiting faculty fields. When the Administrator is populating a time slot, the faculty-availability panel filters and marks faculty members according to whether they teach the selected subject, whether the slot falls within their configured working hours (or visiting schedule), and whether they already have a conflicting entry. The AI auto-generator uses a three-tier faculty selection system: (1) designated faculty from the EXACT_CURRICULUM_MATRIX (a semester-to-subject-faculty mapping), (2) faculty who explicitly listed the subject in their subjects_can_teach, (3) any available faculty with matching department, with workload limits enforced at each tier.")

add_heading_custom("6.5 Visiting Faculty Scheduling", level=2)
add_para("Visiting faculty availability is managed at a per-day, per-time-slot granularity. The Faculty model stores visiting schedule data as a JSON dictionary mapping each day name to a list of time-slot IDs (e.g., {\"Monday\": [1, 2], \"Wednesday\": [3, 4]}). The is_available_for_slot(day, time_slot) method checks: (1) if the faculty is visiting, verify the day is in their visiting_available_days and the time_slot.id is in their slot list for that day; (2) if the faculty is regular, verify the time slot falls within their configured working hours. Both the manual clash detection and the AI auto-generator enforce these constraints strictly.")

add_heading_custom("6.6 Classroom Allocation", level=2)
add_para("Classroom allocation is supported by the Room entity in the database. When creating a timetable entry manually, the administrator selects from the Room inventory. The AI auto-generator allocates rooms automatically: classrooms for lectures (rooms with room_type matching \u2018Classroom\u2019) and lab rooms for laboratory sessions (rooms with room_type matching \u2018Lab\u2019), with automatic fallback to alternate room types if the primary pool is exhausted. The Room Clash rule ensures no two entries share the same room at the same day and time slot.")

add_heading_custom("6.7 Laboratory Allocation", level=2)
add_para("Laboratory sessions are represented as rooms with room_type=\u2018Lab\u2019 in the Room entity, subject to the same Room Clash rule as classrooms. Labs occupy two consecutive time slots and can only start at dynamically detected valid lab start positions (the beginning of a two-hour continuous block). The timetable_create interface uses the get_dynamic_lab_start_slots() function to identify valid lab start slots based on the configured time-slot sequence, checking that consecutive slots have a gap of 15 minutes or less.")

add_heading_custom("6.8 Batch Management & Lab Scheduling", level=2)
add_para("When a division has num_batches > 1, the system creates Batch rows (e.g., A1, A2, A3 for Division A). During lab scheduling, different batches can be assigned to different rooms and faculty simultaneously during the same two-hour lab window. The AI auto-generator manages this through parallel assignment: for each lab window, it assigns each batch a unique subject (from the lab_subjects pool, tracking batch_lab_history to avoid repetition), a free lab room (tracking used rooms to prevent double-booking), and an available faculty member (tracking used faculty IDs to prevent double-assignment). This enables all batches to have simultaneous but distinct lab sessions, maximising resource utilisation.")

add_heading_custom("6.9 Subject Allocation", level=2)
add_para("Subjects are allocated to Timetable entries by selecting from the Subject table (name, code, credits, weekly_lectures, has_lab). The weekly_lectures field specifies how many lectures per week each subject requires (via the required_lectures property). The AI auto-generator enforces these quotas strictly: each subject receives exactly its required number of lectures, and surplus slots are filled with Library periods. The subject selection also drives the Faculty Recommendation feature, which cross-references the chosen subject against each candidate faculty member\u2019s subjects_can_teach list.")

add_heading_custom("6.10 Time Slot Allocation", level=2)
add_para("Time slots are pre-defined by the Administrator via the TimeSlot model (start_time, end_time, and an optional slot_label). The AI auto-generator uses a fixed set of college-hours time slots (08:30 AM to 03:00 PM, typically 6 slots) and divides them into three two-hour lab windows that rotate across days and semesters.")

add_heading_custom("6.11 AI Auto-Generation Algorithm", level=2)
add_para("Algorithm 6.5 (AI Auto-Generation) \u2013 The AI auto-generator implements a two-phase constraint-satisfaction algorithm:")
add_para("Phase 1 \u2013 Compulsory Lab Scheduling (Monday\u2013Friday):")
add_para("For each day, select a lab window from three rotating two-hour windows (rotation offset = day_index + semester). For each batch in the division: select a lab subject (prioritising unscheduled subjects, then unassigned-to-this-batch subjects, tracked via batch_lab_history); find a free lab room (checking both slots of the window, excluding rooms already assigned in this iteration); find the best available faculty using three-tier priority (designated \u2192 subject-matched \u2192 any available), enforcing 30h/week and 6h/day workload limits, global clash checks, and visiting faculty availability in both slots. If any batch fails in the current window, try the next window; if all windows fail, perform a secondary pass with relaxed subject selection; if still unsuccessful, perform a fallback pass with full subject rotation.", indent=True)
add_para("Phase 2 \u2013 Lecture and Library Filling:")
add_para("For each remaining non-lab slot across all days: check subject lecture quotas (required_lectures); if all subjects are fulfilled, assign Library; otherwise, rotate through eligible subjects (excluding the last-scheduled subject for non-consecutiveness), find a free room and available faculty, and assign a lecture. If no room or faculty is available, log a ClashLog warning and assign Library as fallback.", indent=True)

add_para("Table 6.3. Auto-Generator Constraint Rules")
add_table(
    ["Rule", "Enforcement"],
    [
        ["Zero Clash Guarantee", "Every assignment checked against all existing + uncommitted entries globally"],
        ["Daily Lab Block", "Every weekday has one compulsory 2-hour lab window for all batches"],
        ["Varying Lab Windows", "Lab windows rotate across days with semester offset"],
        ["Batch Subject Rotation", "batch_lab_history set prevents duplicate lab subjects per batch"],
        ["Non-Consecutive Lectures", "last_scheduled_subject_id tracking prevents same subject back-to-back"],
        ["Lecture Quota Enforcement", "Each subject limited to required_lectures per week"],
        ["Workload Limits", "30h/week and 6h/day caps per faculty member"],
        ["Library Auto-Fill", "Surplus slots and resource-constrained slots default to Library"],
        ["Faculty Tiered Selection", "Curriculum matrix \u2192 subject-matched \u2192 department-matched \u2192 round-robin"],
    ]
)

add_heading_custom("6.12 Clash Detection Process", level=2)
add_para("Table 6.1. Clash Detection Process")
add_table(
    ["Check", "Scope", "Trigger Condition"],
    [
        ["Faculty Clash", "Global \u2013 across all branches and divisions", "Existing entry with same faculty_id, day, and time_slot_id"],
        ["Room Clash", "Global \u2013 any division using the same room", "Existing entry with same room_number, day, and time_slot_id"],
        ["Division Clash", "Within the division", "Existing entry with same division_id, day, and time_slot_id (full-division)"],
        ["Batch Clash", "Within the batch", "Existing entry with same batch_id, day, and time_slot_id (batch-specific)"],
        ["Faculty Availability", "Per faculty", "Visiting faculty not available on the requested day/slot"],
        ["Lab Next-Slot", "Per faculty + room", "Faculty or room busy in the next slot (for 2-hour lab entries)"],
    ]
)

add_heading_custom("6.13 Clash Resolution Strategy", level=2)
add_para("When any check detects a conflict, the system\u2019s resolution strategy is preventive and advisory: the conflicting entry is rejected before it is saved, a ClashLog record is written, and the Administrator is shown the conflict. The administrator can then either manually resolve by choosing different parameters, or use the Intelligent Clash Resolution feature to get AI-powered suggestions and auto-apply the best one.")

add_heading_custom("6.14 Intelligent Clash Resolution Suggestions", level=2)
add_para("Table 6.2. Intelligent Clash Resolution \u2013 Suggestion Types")
add_table(
    ["Clash Type", "Suggestion Category", "Strategy"],
    [
        ["Room Clash", "Room Change", "Alternative free rooms from Room inventory with ML-predicted risk scores"],
        ["Room Clash", "Timeslot Shift", "ML alternative-slot recommender suggests lower-risk time slots"],
        ["Room Clash", "Faculty Change", "ML faculty recommender suggests alternative faculty by expertise and availability"],
        ["Faculty Clash", "Faculty Change", "ML-scored alternative faculty; prioritises available faculty who teach the subject"],
        ["Faculty Clash", "Timeslot Shift", "ML-based alternative time slots for the conflicting entry"],
        ["Faculty Clash", "Room Change", "Alternative rooms if faculty issue requires redistribution"],
        ["Division Clash", "Timeslot Shift", "ML alternative slots for the division entry"],
        ["Division Clash", "Room Change", "Alternative rooms"],
    ]
)

add_heading_custom("6.15 Scheduling Workflow", level=2)
add_para("1. Administrator selects Branch, Division, and Day on the timetable_select.html screen.")
add_para("2. For the selected Day, the system lists all configured Time Slots with slot status indicators.")
add_para("3. For a chosen Time Slot, the Administrator selects a Subject (ML recommendations auto-load).")
add_para("4. The ML Recommendations panel shows recommended faculty with scoring and recommended time slots with risk percentages.")
add_para("5. The Faculty Availability panel shows each faculty member\u2019s status for that slot.")
add_para("6. The Administrator selects an available Faculty member, chooses a Room, and optionally selects a Batch for lab entries.")
add_para("7. On submission, the Clash Detection Service runs all applicable checks.")
add_para("8. If any check fails, the entry is rejected, a ClashLog is written, and the Administrator is notified with descriptive error messages.")
add_para("9. The Administrator can view the clash in View Clashes, click \u201cGet AI Suggestions\u201d for ML-powered resolution options, and click \u201cApply\u201d to auto-resolve.")
add_para("10. If all checks pass, the Timetable entry is committed and the Dashboard is updated.")
add_para("Alternative: The Administrator clicks \u201cAI Auto-Generate\u201d to produce a complete, clash-free timetable for the division automatically.")

add_heading_custom("6.16 Algorithm Description", level=2)
add_para("Algorithm 6.1 (Clash-Checked Entry Insertion) \u2013 Input: a candidate entry (division_id, subject_id, faculty_id, time_slot_id, day, room_number, batch_id, entry_type). Steps: (1) If visiting faculty, check is_available_for_slot; (2) Query for Faculty Clash; (3) If lab, check faculty availability in next slot; (4) Query for Room Clash; (5) If lab, check room availability in next slot; (6) Query for Division/Batch Clash; (7) If no clash, insert and return Success; if lab with autofill_next_slot, also insert next-slot entry.")
add_para("Algorithm 6.2 (ML Clash-Risk Prediction) \u2013 Input: (faculty_id, division_id, subject_id, time_slot_id, day, room_number). Steps: encode six inputs into numeric feature vector; pass to Random Forest Classifier; interpret probability as risk_score (0\u20131); classify risk_level as \u2018low\u2019 (< 0.3), \u2018medium\u2019 (0.3\u20130.7), or \u2018high\u2019 (> 0.7); return risk_score, risk_level, confidence.")
add_para("Algorithm 6.3 (Intelligent Resolution Suggestion Generation) \u2013 Input: clash_id. Steps: retrieve ClashLog and clash_details; identify matching TimeSlot; based on clash_type, generate suggestions (alternative rooms with ML risk scores, alternative faculty via ML recommender, alternative time slots via ML slot recommender); sort by risk_score ascending; return.")
add_para("Algorithm 6.4 (Auto-Resolve Application) \u2013 Input: clash_id, action_type, action_value. Steps: retrieve ClashLog and conflicting Timetable entry; update entry based on action_type (room_number, faculty_id, or time_slot_id+day); mark ClashLog as resolved; commit and return.")

add_heading_custom("6.17 Optimization Strategy", level=2)
add_para("The system\u2019s optimisation strategy combines advisory ML-based features with the deterministic AI auto-generator. The Smart Slot Recommendation evaluates each time slot and returns the five with lowest predicted risk. The Faculty Recommendation scores candidates by subject expertise and availability. The Timetable Quality Evaluation aggregates risk predictions across a division\u2019s entries. The Intelligent Resolution Suggestion generates context-aware, risk-scored alternatives for detected clashes. The AI auto-generator implements a greedy-with-backtracking constraint satisfaction algorithm that produces complete, clash-free timetables with workload-balanced faculty assignments and varied lab schedules.")

add_heading_custom("6.18 Complexity Analysis", level=2)
add_para("Each deterministic clash check is implemented as a single indexed database query with expected cost O(log n) to O(1). The ML risk-prediction has < 10ms latency. The slot-recommendation runs one prediction per configured time slot (< 20). The resolution suggestion runs in O(R + S + F) time. The AI auto-generator has complexity O(D \u00d7 B \u00d7 W \u00d7 S) per division, where D is the number of days (5), B is the number of batches, W is the number of lab windows (3), and S is the number of lab subjects \u2013 all small, bounded numbers, resulting in sub-second generation for typical divisions.")

page_break()

# ============================================
# CHAPTER 7: DATABASE DESIGN
# ============================================
add_heading_custom("Chapter 7: Database Design", level=1)

add_heading_custom("7.1 Introduction", level=2)
add_para("The system uses a MySQL relational database (with automatic SQLite fallback), defined declaratively through Flask-SQLAlchemy model classes in models.py. This chapter documents the database architecture, the ER diagram, the schema of each of the eleven tables, the relationships between them, the SQL-equivalent schema, a data dictionary, and sample records.")

add_heading_custom("7.2 Database Architecture", level=2)
add_para("The database follows a normalised relational design centred on the Timetable table, which references Division, Subject, Faculty, TimeSlot, and Batch via foreign keys. The User and Faculty tables are linked one-to-one. The Room table is an independent entity. The Batch table is a dependent entity linked to Division. The ClashLog and ActivityLog tables are append-mostly audit tables.")

add_heading_custom("7.3 Entity Relationship Diagram", level=2)
add_para("(Insert updated ER diagram showing all 11 tables)", italic=True)
add_para("In summary: users (1) \u2013 (0..1) faculty; branches (1) \u2013 (*) divisions; divisions (1) \u2013 (*) batches; divisions (1) \u2013 (*) timetable; batches (1) \u2013 (*) timetable; subjects (1) \u2013 (*) timetable; faculty (1) \u2013 (*) timetable; time_slots (1) \u2013 (*) timetable; divisions (1) \u2013 (*) clash_logs; faculty (1) \u2013 (*) clash_logs; rooms (independent entity); activity_logs (independent audit entity).")

add_heading_custom("7.4 Database Tables", level=2)

# 7.4.1 users
add_heading_custom("7.4.1 users", level=3)
add_para("Table 7.1. Users Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["username", "String(100)", "Unique, Not Null, Indexed"],
    ["email", "String(120)", "Unique, Not Null, Indexed"],
    ["password_hash", "String(255)", "Not Null"],
    ["full_name", "String(150)", "Not Null"],
    ["role", "String(20)", "Not Null ('admin' or 'faculty')"],
    ["is_active", "Boolean", "Default True"],
    ["created_at", "DateTime", "Default: current UTC time"],
    ["last_login", "DateTime", "Nullable"],
])

# 7.4.2 faculty
add_heading_custom("7.4.2 faculty", level=3)
add_para("Table 7.2. Faculty Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["user_id", "Integer", "Foreign Key -> users.id, Not Null"],
    ["phone", "String(15)", "Nullable"],
    ["department", "String(100)", "Nullable"],
    ["designation", "String(100)", "Nullable"],
    ["working_hours", "Text (JSON)", 'e.g., {"start": "09:00", "end": "17:00"}'],
    ["subjects_can_teach", "Text (JSON array)", 'e.g., ["Data Structures", "DBMS"]'],
    ["is_visiting", "Boolean", "Default False"],
    ["visiting_available_days", "Text (JSON array)", 'e.g., ["Monday", "Wednesday"]'],
    ["visiting_slot_ids", "Text (JSON dict)", 'e.g., {"Monday": [1, 2], "Wednesday": [3, 4]}'],
    ["is_available", "Boolean", "Default True"],
    ["created_at", "DateTime", "Default: current UTC time"],
])

# 7.4.3 branches
add_heading_custom("7.4.3 branches", level=3)
add_para("Table 7.3. Branches Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["name", "String(150)", "Unique, Not Null"],
    ["short_name", "String(10)", "Unique, Not Null"],
    ["created_by", "Integer", "Foreign Key -> users.id"],
    ["created_at", "DateTime", "Default: current UTC time"],
])

# 7.4.4 divisions
add_heading_custom("7.4.4 divisions", level=3)
add_para("Table 7.4. Divisions Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["branch_id", "Integer", "Foreign Key -> branches.id, Not Null"],
    ["name", "String(50)", "Not Null (e.g., 'A', 'B')"],
    ["semester", "Integer", "Not Null (1\u20138)"],
    ["academic_year", "String(20)", "e.g., '2024-2025'"],
    ["student_count", "Integer", "Default 60"],
    ["num_batches", "Integer", "Default 1 (1 = no batches)"],
    ["created_by", "Integer", "Foreign Key -> users.id"],
    ["created_at", "DateTime", "Default: current UTC time"],
    ["(unique constraint)", "-", "UNIQUE(branch_id, name, semester, academic_year)"],
])

# 7.4.5 batches
add_heading_custom("7.4.5 batches", level=3)
add_para("Table 7.5. Batches Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["division_id", "Integer", "Foreign Key -> divisions.id, Not Null"],
    ["name", "String(20)", "Not Null (e.g., 'D1', 'D2', 'D3')"],
    ["student_count", "Integer", "Default 20"],
    ["created_at", "DateTime", "Default: current UTC time"],
    ["(unique constraint)", "-", "UNIQUE(division_id, name)"],
])

# 7.4.6 time_slots
add_heading_custom("7.4.6 time_slots", level=3)
add_para("Table 7.6. Time Slots Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["start_time", "Time", "Not Null"],
    ["end_time", "Time", "Not Null"],
    ["slot_label", "String(50)", "Nullable (e.g., 'Morning Slot 1')"],
    ["created_by", "Integer", "Foreign Key -> users.id"],
    ["created_at", "DateTime", "Default: current UTC time"],
])

# 7.4.7 subjects
add_heading_custom("7.4.7 subjects", level=3)
add_para("Table 7.7. Subjects Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["name", "String(200)", "Not Null"],
    ["code", "String(20)", "Unique, Not Null"],
    ["credits", "Integer", "Default 3"],
    ["semester", "Integer", "Nullable (ties subject to a specific semester)"],
    ["branch_id", "Integer", "Foreign Key -> branches.id, Nullable"],
    ["has_lab", "Boolean", "Default True"],
    ["weekly_lectures", "Integer", "Default 3 (required lectures per week)"],
    ["created_by", "Integer", "Foreign Key -> users.id"],
    ["created_at", "DateTime", "Default: current UTC time"],
])

# 7.4.8 rooms
add_heading_custom("7.4.8 rooms", level=3)
add_para("Table 7.8. Rooms Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["name", "String(100)", "Unique, Not Null (e.g., '101', 'Lab-A')"],
    ["capacity", "Integer", "Default 60"],
    ["room_type", "String(50)", "Default 'Classroom' (Classroom, Lab, Seminar Hall)"],
    ["created_by", "Integer", "Foreign Key -> users.id"],
    ["created_at", "DateTime", "Default: current UTC time"],
])

# 7.4.9 timetable
add_heading_custom("7.4.9 timetable", level=3)
add_para("Table 7.9. Timetable Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["division_id", "Integer", "Foreign Key -> divisions.id, Not Null"],
    ["subject_id", "Integer", "Foreign Key -> subjects.id, Nullable (NULL for library/break)"],
    ["faculty_id", "Integer", "Foreign Key -> faculty.id, Nullable (NULL for library/break)"],
    ["time_slot_id", "Integer", "Foreign Key -> time_slots.id, Not Null"],
    ["batch_id", "Integer", "Foreign Key -> batches.id, Nullable (NULL = full-division)"],
    ["day", "String(20)", "Not Null (Monday\u2013Saturday)"],
    ["room_number", "String(50)", "Nullable (NULL for library/break)"],
    ["entry_type", "String(20)", "Default 'lecture' ('lecture', 'lab', 'library', 'break')"],
    ["is_manual", "Boolean", "Default False"],
    ["created_by", "Integer", "Foreign Key -> users.id"],
    ["created_at", "DateTime", "Default: current UTC time"],
    ["updated_at", "DateTime", "Default/On-update: current UTC time"],
])

# 7.4.10 clash_logs
add_heading_custom("7.4.10 clash_logs", level=3)
add_para("Table 7.10. Clash Logs Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["clash_type", "String(50)", "Not Null ('faculty', 'room', 'division', etc.)"],
    ["severity", "String(20)", "Default 'warning'"],
    ["clash_details", "Text (JSON)", "Set/read via set_details()/get_details()"],
    ["division_id", "Integer", "Foreign Key -> divisions.id, Nullable"],
    ["faculty_id", "Integer", "Foreign Key -> faculty.id, Nullable"],
    ["is_resolved", "Boolean", "Default False"],
    ["detected_at", "DateTime", "Default: current UTC time"],
    ["resolved_at", "DateTime", "Nullable"],
    ["resolved_by", "Integer", "Foreign Key -> users.id, Nullable"],
    ["resolution_method", "String(20)", "Nullable ('manual' or 'auto')"],
    ["resolution_note", "Text", "Nullable"],
])

# 7.4.11 activity_logs
add_heading_custom("7.4.11 activity_logs", level=3)
add_para("Table 7.11. Activity Logs Table Schema")
add_table(["Column", "Type", "Constraints"], [
    ["id", "Integer", "Primary Key"],
    ["user_id", "Integer", "Foreign Key -> users.id, Nullable"],
    ["user_name", "String(150)", "Default 'System'"],
    ["action_type", "String(50)", "Not Null (e.g., 'AUTO_GENERATE', 'PROFILE_UPDATE')"],
    ["description", "Text", "Not Null"],
    ["entity_type", "String(50)", "Nullable (e.g., 'timetable', 'division', 'user')"],
    ["entity_id", "Integer", "Nullable"],
    ["details_json", "Text", "Nullable (JSON payload with additional context)"],
    ["created_at", "DateTime", "Default: current UTC time"],
])

add_heading_custom("7.5 Relationships", level=2)
add_para("Table 7.12. Relationships")
add_table(
    ["Parent Table", "Child Table", "Type", "Notes"],
    [
        ["users", "faculty", "One-to-One", "cascade='all, delete-orphan'"],
        ["branches", "divisions", "One-to-Many", "cascade='all, delete-orphan'"],
        ["branches", "subjects", "One-to-Many", "Via branch_id"],
        ["divisions", "batches", "One-to-Many", "cascade='all, delete-orphan'"],
        ["divisions", "timetable", "One-to-Many", "cascade='all, delete-orphan'"],
        ["batches", "timetable", "One-to-Many", "Via batch_id (nullable)"],
        ["subjects", "timetable", "One-to-Many", "Via subject relationship"],
        ["time_slots", "timetable", "One-to-Many", "Via time_slot relationship"],
        ["faculty", "timetable", "One-to-Many", "faculty.timetable_entries (lazy='dynamic')"],
        ["divisions", "clash_logs", "One-to-Many", "Audit reference"],
        ["faculty", "clash_logs", "One-to-Many", "Audit reference"],
        ["users", "clash_logs", "One-to-Many", "resolved_by reference"],
        ["users", "activity_logs", "One-to-Many", "user_id reference"],
    ]
)

add_heading_custom("7.6 SQL Schema", level=2)
add_para("The tables described above are created automatically by SQLAlchemy\u2019s db.create_all() from the model definitions. An auto-migration block at startup attempts to add any missing columns to existing tables (visiting faculty fields, resolution tracking fields, batch/lab fields), ensuring backward compatibility. Conceptually equivalent to standard CREATE TABLE statements with INT AUTO_INCREMENT primary keys, VARCHAR columns, TEXT columns for JSON-encoded fields, DATETIME columns with default CURRENT_TIMESTAMP, and FOREIGN KEY constraints, all under utf8mb4 character set.")

add_heading_custom("7.7 Data Dictionary", level=2)
add_para("Table 7.13. Data Dictionary")
add_table(["Term", "Meaning"], [
    ["Division", "A batch/section of students within a branch and semester, e.g., CSE-A."],
    ["Batch", "A sub-group within a division for laboratory sessions, e.g., D1, D2, D3."],
    ["Time Slot", "A defined period of the day (start_time\u2013end_time) used consistently across all divisions."],
    ["Room", "A physical space (classroom, lab, or seminar hall) with a name, capacity, and type."],
    ["Clash", "A conflict where a faculty member, room, or division is assigned to more than one entry at the same day and time slot."],
    ["Clash Log", "A persisted record of a clash that was detected, including its type, severity, resolution status, and resolution tracking."],
    ["Activity Log", "A persisted record of an administrative action, including user attribution, description, and timestamp."],
    ["Working Hours", "The start and end time within which a regular faculty member is available to teach, stored as JSON."],
    ["Visiting Schedule", "A per-day, per-time-slot availability configuration for visiting faculty, stored as a JSON dictionary."],
    ["Risk Score", "The 0\u20131 probability, output by the ML model, that a proposed entry will correspond to a clash pattern."],
    ["Entry Type", "The type of timetable entry: 'lecture', 'lab', 'library', or 'break'."],
    ["Resolution Method", "How a clash was resolved: 'manual' or 'auto'."],
    ["Weekly Lectures", "The required number of lectures per week for a subject, enforced by the auto-generator."],
])

add_heading_custom("7.8 Sample Database Records", level=2)
add_para("Table 7.14. Sample Database Records")
add_table(["Table", "Sample Row"], [
    ["branches", "id=1, name='Computer Engineering', short_name='CSE'"],
    ["divisions", "id=6, branch_id=1, name='A', semester=5, academic_year='2024-2025', student_count=60, num_batches=3"],
    ["batches", "id=1, division_id=6, name='A1', student_count=20"],
    ["subjects", "id=1, name='Data Structures', code='CS301', credits=4, semester=5, branch_id=1, has_lab=True, weekly_lectures=3"],
    ["rooms", "id=1, name='101', capacity=60, room_type='Classroom'"],
    ["rooms", "id=2, name='Lab-A', capacity=30, room_type='Lab'"],
    ["faculty (regular)", "id=1, user_id=5, department='CSE', is_visiting=False, subjects_can_teach='[\"Data Structures\",\"DBMS\"]'"],
    ["faculty (visiting)", "id=2, user_id=7, department='CSE', is_visiting=True, visiting_slot_ids='{\"Monday\": [1, 2], \"Wednesday\": [3]}'"],
    ["timetable (lecture)", "id=101, division_id=6, subject_id=1, faculty_id=1, time_slot_id=1, day='Monday', room_number='101', entry_type='lecture', batch_id=NULL, is_manual=True"],
    ["timetable (lab)", "id=102, division_id=6, subject_id=2, faculty_id=3, time_slot_id=3, day='Monday', room_number='Lab-A', entry_type='lab', batch_id=1, is_manual=False"],
    ["timetable (library)", "id=103, division_id=6, subject_id=NULL, faculty_id=NULL, time_slot_id=7, day='Friday', room_number=NULL, entry_type='library'"],
    ["clash_logs", "id=12, clash_type='faculty', severity='warning', is_resolved=True, resolution_method='auto', resolution_note='Faculty changed to Dr. Smith'"],
    ["activity_logs", "id=1, user_id=1, action_type='AUTO_GENERATE', description='Auto-generated timetable for CSE-A (30 entries)'"],
])

page_break()

# ============================================
# CHAPTER 8: TESTING AND VALIDATION
# ============================================
add_heading_custom("Chapter 8: Testing And Validation", level=1)

add_heading_custom("8.1 Introduction", level=2)
add_para("Testing of the system combined conventional web-application testing (unit, integration, system, and user-acceptance testing of the Flask routes, clash-detection logic, AI auto-generator, room management, batch management, visiting faculty scheduling, activity logging, and templates) with dedicated validation of the machine-learning subsystem and the intelligent clash resolution module.")

add_heading_custom("8.2 Unit Testing", level=2)
add_para("Unit-level checks were carried out on individual model methods and service functions in isolation \u2013 for example, verifying that User.set_password()/check_password() correctly hash and verify credentials, that Faculty JSON serialisation methods correctly round-trip, that Faculty.is_available_for_slot() correctly handles both regular and visiting faculty, that Batch creation correctly names batches with division prefix, that Subject.required_lectures and required_labs properties return correct values, that ClashLog resolution tracking fields work correctly, and that ActivityLog.log() creates entries safely with automatic rollback on failure.")

add_heading_custom("8.3 Integration Testing", level=2)
add_para("Integration testing verified that the Clash Detection Service correctly interacts with the Timetable and ClashLog models through SQLAlchemy, that the AI auto-generator correctly creates multi-batch lab entries with parallel room and faculty assignments, that the ML wrapper methods correctly return the expected structures, and that the resolution suggestion generation correctly queries room inventory, faculty availability, and ML recommendations.")

add_heading_custom("8.4 System Testing", level=2)
add_para("End-to-end system testing exercised the complete workflow: signing up as Administrator, configuring branches/divisions (with batches)/subjects/time-slots/rooms, creating Faculty accounts with visiting schedules, creating timetable entries manually, running the AI auto-generator, verifying batch-specific lab entries, testing clash detection and AI resolution suggestions, verifying activity log entries, testing global search, and verifying CSV/ZIP export including master all-semesters export.")

add_heading_custom("8.5 User Acceptance Testing", level=2)
add_para("User-acceptance testing focused on whether the Administrator could complete the full setup-to-timetable workflow (both manual and auto-generated), use AI resolution suggestions effectively, and whether the Faculty role could locate their personal schedule, configure their visiting schedule, and download their timetable without assistance.")

add_heading_custom("8.6 Black Box Testing", level=2)
add_para("Black-box tests exercised the application purely through its external interface (the browser UI and the JSON API endpoints) without reference to the internal implementation, verifying that valid inputs produced the expected pages and that invalid or conflicting inputs produced the expected clash messages and AI resolution suggestions.")

add_heading_custom("8.7 White Box Testing", level=2)
add_para("White-box tests, informed by the actual clash_service.py, ml_clash_predictor.py, and auto_generator_service.py source, verified that each clash-check code path was independently exercised, that the ML engine\u2019s feature-encoding produced the expected numeric vector, that the auto-generator\u2019s three-tier faculty selection worked correctly, and that the resolution suggestion generation correctly prioritised free rooms and ML-recommended faculty.")

add_heading_custom("8.8 Performance Testing", level=2)
add_para("Performance testing measured: model training time of under one second on the 65-row training dataset, prediction latency of under 10 milliseconds per clash-risk query, resolution suggestion generation under 200 milliseconds per clash, AI auto-generation of a single division timetable in under 3 seconds (30 entries for 5 days with 3 batches), and bulk auto-generation of all divisions in under 15 seconds for a typical institution.")

add_heading_custom("8.9 Security Testing", level=2)
add_para("Security-focused testing verified that passwords are never stored in plaintext, that admin-only routes, ML API endpoints, and clash-resolution endpoints reject unauthenticated or non-admin requests, and that SQLAlchemy\u2019s parameterised query interface prevents SQL injection.")

add_heading_custom("8.10 Test Cases", level=2)
add_para("Table 8.1. Test Cases")
add_table(
    ["TC ID", "Test Scenario", "Expected Result"],
    [
        ["TC-01", "Sign up a new Administrator account", "Account created; password stored as hash"],
        ["TC-02", "Log in with correct credentials", "Session established; redirected to Admin Dashboard"],
        ["TC-03", "Log in with incorrect password", "Login rejected with error message"],
        ["TC-04", "Create Division with duplicate constraint", "Rejected by unique constraint"],
        ["TC-05", "Faculty double-booking at same day/time", "Rejected with Faculty Clash message"],
        ["TC-06", "Room double-booking at same day/time", "Rejected with Room Clash message"],
        ["TC-07", "Division double-booking at same day/time", "Rejected with Division Clash message"],
        ["TC-08", "Submit valid, non-conflicting entry", "Entry saved; appears in Dashboard"],
        ["TC-09", "Call GET /api/faculty-availability", "Returns availability status per faculty"],
        ["TC-10", "Call POST /api/ml/predict-clash-risk", "Returns risk_score, risk_level, confidence"],
        ["TC-11", "Call GET /api/ml/slot-recommendations", "Returns up to 5 sorted alternatives"],
        ["TC-12", "Call GET /api/ml/recommend-faculty", "Returns up to 5 scored candidates"],
        ["TC-13", "Call ML endpoint without admin auth", "Request rejected"],
        ["TC-14", "Faculty views personal schedule", "Reflects entries referencing their faculty_id"],
        ["TC-15", "Add room via Manage Rooms", "Room created with name, capacity, type"],
        ["TC-16", "Global Search for 'CSE'", "Returns matching entities across categories"],
        ["TC-17", "Get AI suggestions for room clash", "Returns alternative rooms, slots, faculty"],
        ["TC-18", "Auto-resolve clash via Apply button", "Entry updated; ClashLog resolved with method='auto'"],
        ["TC-19", "Configure visiting faculty day-wise", "Profile saved with per-day time-slot availability"],
        ["TC-20", "Download CSV for a division", "CSV file with correct grid format"],
        ["TC-21", "Export all timetables as ZIP", "ZIP with one CSV per division"],
        ["TC-22", "Faculty downloads personal CSV", "CSV with faculty schedule"],
        ["TC-23", "Resolve clash manually", "ClashLog marked resolved with method='manual'"],
        ["TC-24", "AI auto-generate timetable for division", "30 entries created with zero clashes"],
        ["TC-25", "Auto-generate with multi-batch division", "Parallel lab entries for each batch"],
        ["TC-26", "Create division with batches", "Batch rows auto-created (e.g., D1, D2, D3)"],
        ["TC-27", "View Activity Log", "Shows recent administrative actions"],
        ["TC-28", "Export master all-semesters CSV", "Single CSV with all division timetables"],
        ["TC-29", "AJAX add timetable entry", "Entry created without page reload"],
        ["TC-30", "AJAX delete timetable entry", "Entry removed without page reload"],
        ["TC-31", "Update admin profile", "Profile updated; ActivityLog entry created"],
        ["TC-32", "Lab entry on non-lab-start slot", "Rejected: labs only at 2-hour block boundaries"],
        ["TC-33", "Assign visiting faculty on unavailable day", "Rejected: faculty unavailable"],
    ]
)

add_heading_custom("8.11 Bug Analysis", level=2)
add_para("Issues surfaced during development included: edge cases such as missing or malformed JSON on Faculty rows; graceful fallback when the ML model file is not yet present; legacy visiting_slot_ids stored as a flat list instead of a day-keyed dictionary (handled by fallback logic); ML recommendations panel CSS conflicts (resolved using inline styles); auto-generator encountering faculty bottlenecks when all designated faculty are busy (handled by three-tier fallback with workload limits); batch name inconsistencies after editing division batch count (handled by sync logic that checks for existing timetable entries before recreating batches); and room_number being optional for library/break entries while being required text in earlier schema versions (handled by making the column nullable). These were addressed through defensive JSON validation, backward-compatible data format handling, and comprehensive fallback strategies.")

page_break()

# ============================================
# CHAPTER 9: RESULTS AND DISCUSSION
# ============================================
add_heading_custom("Chapter 9: Results And Discussion", level=1)

add_heading_custom("9.1 Introduction", level=2)
add_para("This chapter presents the observed results of the implemented system, drawing on the project\u2019s own recorded validation output and on the functional behaviour of the deterministic clash-detection subsystem, the AI auto-generator, the intelligent resolution module, the global search, and the export functionality.")

add_heading_custom("9.2 Dashboard Results", level=2)
add_para("The Admin Dashboard successfully renders each division with colour-coded clash indicators (green for clash-free, red for clashes) alongside entry counts, total entity counts (branches, divisions, faculty, subjects, rooms), and recent unresolved clashes.")

add_heading_custom("9.3 Timetable Generation Results", level=2)
add_para("The interactive timetable-creation screen was verified to correctly display faculty availability, ML recommendations (faculty with TOP PICK/EXPERT tags, time slots with BEST tags), subject load indicators, dynamic lab start slot detection, batch-aware entry forms, and room occupied indicators. Entries are correctly persisted only when all clash checks pass.")

add_heading_custom("9.4 AI Auto-Generation Results", level=2)
add_para("The AI Auto-Generator was verified to produce complete, clash-free timetables for divisions with the following characteristics:")
add_bullet("30 entries per division for a 5-day, 6-slot-per-day schedule (6 subjects, 3 batches)")
add_bullet("10 lab entries (2 per day \u00d7 5 days, one for each batch pair)")
add_bullet("Remaining slots filled with lectures respecting weekly quotas, with Library periods for surplus slots")
add_bullet("Zero clashes across all divisions when auto-generating for multiple divisions simultaneously")
add_bullet("Varying lab windows across days (e.g., Monday 10:30\u201312:30, Tuesday 13:00\u201315:00, Wednesday 08:30\u201310:20)")
add_bullet("Batch rotation ensuring no duplicate lab subjects per batch across the week")
add_bullet("Faculty workload limits (30h/week, 6h/day) enforced without exception")
add_para("(Insert Figure 9.4 \u2013 Auto-Generator Results Summary)", italic=True)

add_heading_custom("9.5 Clash Resolution Results", level=2)
add_para("Deliberately duplicated entries were each correctly rejected by the corresponding check, and corresponding ClashLog rows were written, confirming both the prevention behaviour and the audit-logging behaviour.")

add_heading_custom("9.6 Intelligent Clash Resolution Results", level=2)
add_para("The AI-powered resolution suggestion feature correctly generated context-aware suggestions for all three clash types. For room clashes, alternative free rooms from the Room inventory were identified with ML risk scores. For faculty clashes, alternative available faculty were scored by ML expertise and availability metrics. The one-click auto-resolve correctly updated the conflicting Timetable entry and marked the ClashLog as resolved.")

add_heading_custom("9.7 Global Search Results", level=2)
add_para("The global search correctly returned results across all six entity types with appropriate partial matching and category-wise grouping.")

add_heading_custom("9.8 Export Results", level=2)
add_para("The CSV export was verified to produce correctly formatted grid-based timetable files with batch labels for multi-batch entries. The master all-semesters CSV correctly aggregated all divisions with section separators. The ZIP export contained one accurately-named CSV per division.")

add_heading_custom("9.9 Performance Analysis", level=2)
add_para("Table 9.1. ML Function Test Results")
add_table(["Test", "Result"], [
    ["Clash Risk Prediction", "Risk Score: 0.70, Risk Level: high, Confidence: 0.70 \u2013 SUCCESS"],
    ["Smart Slot Recommendations", "5 recommendations returned \u2013 SUCCESS"],
    ["Faculty Recommendations", "Scored candidate list returned \u2013 SUCCESS"],
    ["Timetable Quality Evaluation", "Quality score and recommendations returned \u2013 SUCCESS"],
    ["Clash Risk Summary", "Average Risk: 0.33; Total Entries: 1 \u2013 SUCCESS"],
    ["Model Persistence", "Model file saved at ml_models/, 92,467 bytes \u2013 MODEL SAVED"],
])

add_para("Table 9.2. ML and Auto-Generator Performance Metrics")
add_table(["Metric", "Value"], [
    ["Model Training Time", "< 1 second"],
    ["Prediction Latency", "< 10 ms"],
    ["Model File Size", "92 KB"],
    ["Recommendations per Query", "5"],
    ["Resolution Suggestions per Clash", "5\u201310 (varies by clash type)"],
    ["Auto-Resolve Application Time", "< 50 ms"],
    ["Auto-Generation Time (single division)", "< 3 seconds"],
    ["Auto-Generation Time (all divisions)", "< 15 seconds"],
    ["Risk Distribution (sample run)", "Low 67%, Medium 0%, High 33%"],
])

add_heading_custom("9.10 Comparison with Manual Scheduling", level=2)
add_para("Table 9.3. Comparison: Manual Scheduling vs. Proposed System")
add_table(
    ["Aspect", "Manual Scheduling", "Proposed System"],
    [
        ["Conflict detection", "Visual/manual cross-check, error-prone", "Automatic, on every entry submission"],
        ["Conflict scope", "Limited to what a reviewer notices", "Global faculty check; systematic room and division checks"],
        ["Conflict history", "Not retained", "Persisted in clash_logs with full resolution tracking"],
        ["Foresight before committing", "None", "ML risk score, alternative slot and faculty recommendations"],
        ["Conflict resolution", "Manual investigation of alternatives", "ML-powered suggestions with one-click auto-resolve"],
        ["Timetable generation", "Manual, days of effort", "AI auto-generator: seconds, zero clashes guaranteed"],
        ["Batch/lab scheduling", "Manual parallel coordination", "Automated multi-batch parallel lab scheduling"],
        ["Room management", "Manual inventory", "Structured Room entity with capacity and type"],
        ["Visiting faculty", "Informal notes", "Per-day, per-slot configuration with visual toggle"],
        ["Activity tracking", "None", "Comprehensive activity_logs with user attribution"],
        ["Search capability", "Manual lookup", "Full-text search across all entities"],
        ["Timetable export", "Manual copy", "Automated CSV/ZIP export (individual + master)"],
        ["Time to verify", "Manual, variable", "Sub-second automated checks + < 10 ms ML prediction"],
        ["Time to resolve clash", "Minutes\u2013hours", "AI suggestion + one-click auto-resolve (< 1 second)"],
        ["Time to build timetable", "Days", "Seconds (AI auto-generator)"],
    ]
)

add_heading_custom("9.11 Advantages Achieved", level=2)
add_bullet("All three hard-constraint clash types are automatically enforced at entry-submission time.")
add_bullet("Complete, timestamped audit trail of detected clashes with full resolution tracking.")
add_bullet("Random Forest prediction module gives quantified risk scores and concrete alternative recommendations.")
add_bullet("ML-powered intelligent resolution suggestions with one-click auto-resolve reduce clash handling from hours to seconds.")
add_bullet("AI Auto-Generator produces complete, clash-free timetables in seconds with zero manual effort.")
add_bullet("Multi-batch lab scheduling enables parallel lab sessions with rotation.")
add_bullet("Rooms managed as first-class entities with capacity and type attributes.")
add_bullet("Visiting faculty scheduling at per-day, per-slot granularity.")
add_bullet("Comprehensive activity logging for audit trail.")
add_bullet("Global search enables rapid information retrieval.")
add_bullet("CSV/ZIP export (individual, master all-semesters, faculty personal) enables offline distribution.")
add_bullet("AJAX-based real-time APIs provide responsive interactions.")
add_bullet("Automatic SQLite fallback ensures resilience.")

add_heading_custom("9.12 Limitations", level=2)
add_bullet("The ML model was trained on a relatively small dataset (65 entries); prediction quality depends on data volume.")
add_bullet("Room capacity constraints are not currently enforced during timetable creation.")
add_bullet("No dedicated laboratory-session model distinguishing lab-specific constraints (e.g., equipment requirements).")
add_bullet("The auto-generator\u2019s EXACT_CURRICULUM_MATRIX is hardcoded for specific semesters; a dynamic mapping UI could improve flexibility.")
add_bullet("The current deployment relies on a single database instance; multi-campus or high-availability deployment would need further architecture.")

page_break()

# ============================================
# CHAPTER 10: FUTURE SCOPE AND CONCLUSION
# ============================================
add_heading_custom("Chapter 10: Future Scope And Conclusion", level=1)

add_heading_custom("10.1 Future Scope", level=2)

for title, desc in [
    ("10.1.1 ERP Integration", "Integrating with a broader institutional ERP would allow branch, division, and student-batch data to be synchronised automatically."),
    ("10.1.2 Attendance Management", "Each Timetable entry links a division, subject, faculty, and time slot, making it a natural foundation for an attendance module."),
    ("10.1.3 Mobile Application", "A dedicated mobile application or PWA would let faculty and administrators check schedules and clash alerts on the go."),
    ("10.1.4 Cloud Deployment", "The production deployment could be extended to a managed cloud platform with autoscaling and managed MySQL."),
    ("10.1.5 Multi-Campus Support", "Extending the Branch/Division model with a campus dimension would allow correct clash-detection scoping for multi-location institutions."),
    ("10.1.6 Advanced ML Enhancements", "The ML module could be extended with additional features (workload balance, student feedback), retraining on larger datasets, room-capacity-aware recommendations, and reinforcement learning based on which suggestions administrators accept or reject."),
]:
    add_heading_custom(title, level=3)
    add_para(desc)

add_heading_custom("10.2 Conclusion", level=2)
add_para("This report has documented the College Timetable Management System with Intelligent Clash Detection and Resolution, a Flask, Flask-SQLAlchemy, and MySQL based web application (with automatic SQLite fallback) that replaces error-prone manual timetable preparation with an interactive, role-based system in which every proposed timetable entry is automatically checked for faculty, room, and division clashes before it is committed, and every detected clash is permanently logged with full resolution tracking for audit. Beyond this deterministic safeguard, the system incorporates: a supervised machine-learning module (Random Forest Classifier) for clash risk prediction, alternative recommendations, and quality evaluation; an Intelligent Clash Resolution module with ML-powered suggestions and one-click auto-resolve; and an AI Auto-Generator Service that constructs complete, clash-free timetables using constraint satisfaction combined with ML risk minimisation, with daily lab blocks, batch rotation, lecture quota enforcement, and library auto-fill.")
add_para("The system additionally provides: a Room & Resource Management module for tracking classrooms, labs, and seminar halls; a Batch model supporting multi-batch parallel lab scheduling; visiting faculty scheduling with per-day, per-time-slot availability; an Activity Logging system for comprehensive audit trails; global search across all entities; CSV/ZIP timetable export (individual, master all-semesters, faculty personal); AJAX-based real-time APIs for responsive interactions; and enhanced search/filter on all management pages.")
add_para("The objectives set out in Chapter 1 \u2013 automated clash detection, role-based portals, centralised dashboard, predictive ML layer, intelligent resolution with auto-resolve, AI auto-generator, room management, batch management, visiting faculty scheduling, activity logging, global search, AJAX APIs, and timetable export \u2013 were each realised in the implemented system and verified through the testing described in Chapter 8 and the results discussed in Chapter 9. While the current system has limitations, it demonstrably improves on manual scheduling in accuracy, auditability, resolution speed, generation speed, and foresight, and provides a solid, extensible foundation for the future enhancements identified in Section 10.1.")

page_break()

# ============================================
# REFERENCES
# ============================================
add_heading_custom("References", level=1)

add_heading_custom("Books", level=2)
add_bullet("Elmasri, R. & Navathe, S. B., Fundamentals of Database Systems, 7th Edition, Pearson, 2015.")
add_bullet("Sommerville, I., Software Engineering, 10th Edition, Pearson, 2015.")
add_bullet("Hastie, T., Tibshirani, R. & Friedman, J., The Elements of Statistical Learning, 2nd Edition, Springer, 2009.")
add_bullet("Grinberg, M., Flask Web Development, 2nd Edition, O\u2019Reilly, 2018.")

add_heading_custom("Research Papers", level=2)
add_bullet("\"Machine Learning-Based Prediction System for Optimized Faculty Exam Duty Allocation,\" IJERT, 2026.")
add_bullet("\"Addressing staffing challenges through improved planning: Demand-driven course schedule planning and instructor assignment in higher education,\" ScienceDirect, 2024.")

add_heading_custom("IEEE Papers", level=2)
add_bullet("\"Graph Coloring based Scheduling Algorithm to automatically generate College Course Timetable,\" IEEE Conference Publication, 2020.")
add_bullet("Corne, D. & Ross, P., \"Constraint-based timetabling \u2013 a case study,\" IEEE Conference Publication.")

add_heading_custom("Official Documentation", level=2)
add_bullet("Flask Documentation \u2013 https://flask.palletsprojects.com/")
add_bullet("Flask-SQLAlchemy Documentation \u2013 https://flask-sqlalchemy.palletsprojects.com/")
add_bullet("SQLAlchemy Documentation \u2013 https://docs.sqlalchemy.org/")
add_bullet("MySQL Reference Manual \u2013 https://dev.mysql.com/doc/")
add_bullet("scikit-learn Documentation (Random Forest Classifier) \u2013 https://scikit-learn.org/")
add_bullet("Werkzeug Documentation (security helpers) \u2013 https://werkzeug.palletsprojects.com/")
add_bullet("Flask-Login Documentation \u2013 https://flask-login.readthedocs.io/")

add_heading_custom("Websites", level=2)
add_bullet("Project Repository \u2013 https://github.com/Krishp285/timetable-clash-resolution")
add_bullet("Live Deployment \u2013 https://timetable-clash-resolution.onrender.com")

page_break()

# ============================================
# APPENDICES
# ============================================
add_heading_custom("Appendix", level=1)

add_heading_custom("Appendix A \u2013 User Manual", level=2)

add_heading_custom("A.1 Administrator Quick Guide", level=3)
for step in [
    "Sign up or log in as an Administrator.",
    "Navigate to Manage Branches and add each academic branch.",
    "Navigate to Manage Divisions and add each division with semester, academic year, student count, and number of batches.",
    "Navigate to Manage Subjects and add each subject with code, credits, weekly lectures, semester, branch, and lab flag.",
    "Navigate to Manage Time Slots and define the day\u2019s time slots.",
    "Navigate to Manage Rooms and add each room/resource with name, capacity, and type.",
    "Navigate to Manage Faculty to review faculty profiles.",
    "Option A \u2013 Manual: Go to Create Timetable, select Branch/Division/Day, and for each time slot select subject, faculty, room, and batch (if applicable).",
    "Option B \u2013 Automatic: Click \u201cAI Auto-Generate\u201d for a division or \u201cAuto-Generate All\u201d for all divisions.",
    "Review the Admin Dashboard for clash indicators; open View Clashes for details of any conflicts.",
    "For detected clashes, click \u201cGet AI Suggestions\u201d and then \u201cApply\u201d to auto-resolve.",
    "Use Global Search to find any entity across the system.",
    "Use Export All (ZIP), Export Master CSV, or individual division CSV downloads.",
    "View Activity Log for a history of all administrative actions.",
]:
    add_bullet(step)

add_heading_custom("A.2 Faculty Quick Guide", level=3)
for step in [
    "Sign up as Faculty; a linked Faculty profile is created automatically.",
    "Open Faculty Profile and set phone, department, designation, working hours, and subjects you can teach.",
    "If visiting faculty, toggle the switch, select available days, and for each day select available time slots.",
    "Open Faculty Dashboard to view your personal teaching schedule.",
    "Click \u201cDownload Timetable\u201d to export your schedule as CSV.",
]:
    add_bullet(step)

add_heading_custom("Appendix B \u2013 Installation Guide", level=2)
for step in [
    "Create and enter a project directory: mkdir timetable_system && cd timetable_system.",
    "Create a virtual environment: python -m venv venv, then activate it.",
    "Install dependencies: pip install -r requirements.txt.",
    "Create the MySQL database: CREATE DATABASE timetable_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
    "Configure the database connection in config.py or as environment variable.",
    "(If MySQL is not available, the system will automatically fall back to SQLite.)",
    "Run the application: python app.py.",
    "Open a browser at http://localhost:5000. Default admin login: admin / admin123.",
]:
    add_bullet(step)

add_heading_custom("Appendix C \u2013 Project Folder Structure", level=2)
add_para("(Insert Figure C.1 \u2013 Project Folder Structure)", italic=True)

add_heading_custom("Appendix D \u2013 Database Schema", level=2)
add_para("See Chapter 7 (Database Design) for the complete schema of all eleven tables: users, faculty, branches, divisions, batches, time_slots, subjects, rooms, timetable, clash_logs, and activity_logs.")

add_heading_custom("Appendix E \u2013 API Documentation", level=2)

add_heading_custom("E.1 Application Utility Endpoints", level=3)
add_para("Table E.1. Application REST/Utility API Endpoints")
add_table(["Endpoint", "Method", "Description"], [
    ["/api/divisions/<branch_id>", "GET", "Get divisions belonging to a given branch."],
    ["/api/faculty-availability", "GET", "Get faculty availability for a given day/time slot."],
    ["/api/faculty-matrix", "GET", "Get full faculty availability matrix for a given day."],
    ["/api/subjects/search", "GET", "Search subjects by name or code."],
    ["/search", "GET", "Global search across all entities."],
    ["/admin/timetable/export", "GET", "Export all division timetables as ZIP."],
    ["/timetable/download/<division_id>", "GET", "Download single division timetable as CSV."],
    ["/timetable/export-master-csv", "GET", "Download master all-semesters timetable as CSV."],
    ["/faculty/timetable/download", "GET", "Download faculty personal timetable as CSV."],
    ["/admin/faculty/<faculty_id>/timetable", "GET", "Get faculty timetable as JSON matrix."],
])

add_heading_custom("E.2 Machine Learning API Endpoints", level=3)
add_para("Table E.2. ML API Endpoints")
add_table(["Endpoint", "Method", "Description"], [
    ["/api/ml/predict-clash-risk", "POST", "Predicts risk_score, risk_level, and confidence for a candidate entry."],
    ["/api/ml/slot-recommendations", "GET/POST", "Returns up to 5 alternative time slots ranked by clash risk."],
    ["/api/ml/recommend-faculty", "GET/POST", "Returns up to 5 faculty candidates scored by expertise and availability."],
    ["/api/ml/evaluate-timetable", "POST", "Returns quality score, feasibility, and recommendations for a division."],
    ["/api/ml/clash-risk-summary", "GET", "Returns average risk and risk distribution counts."],
])

add_heading_custom("E.3 Clash Resolution API Endpoints", level=3)
add_para("Table E.3. Clash Resolution API Endpoints")
add_table(["Endpoint", "Method", "Description"], [
    ["/api/ml/clash-suggestions/<clash_id>", "GET", "Generates ML-powered resolution suggestions for a clash."],
    ["/admin/clashes/resolve/<clash_id>", "POST", "Manually marks a clash as resolved."],
    ["/admin/clashes/auto-resolve/<clash_id>", "POST", "Applies ML suggestion to auto-resolve a clash."],
    ["/admin/clashes/clear-all", "POST", "Clears all logged clashes from database."],
])

add_heading_custom("E.4 AJAX Real-Time API Endpoints", level=3)
add_para("Table E.4. AJAX Real-Time API Endpoints")
add_table(["Endpoint", "Method", "Description"], [
    ["/api/division/<division_id>/subjects", "GET", "Returns filtered subjects for a division."],
    ["/api/subject/<subject_id>/faculties", "GET", "Returns qualified faculty for a subject."],
    ["/api/division/<division_id>/timetable-data", "GET", "Returns complete timetable grid as JSON."],
    ["/api/timetable/add-entry", "POST", "Creates timetable entry via AJAX with clash validation."],
    ["/api/timetable/delete-entry/<entry_id>", "POST/DELETE", "Deletes timetable entry via AJAX."],
    ["/api/auto-generate/<division_id>", "POST", "Triggers AI auto-generation via AJAX."],
])

add_heading_custom("Appendix F \u2013 Sample Input Data", level=2)
add_para("Sample input consistent with the schema in Chapter 7: Branch = {name: 'Computer Engineering', short_name: 'CSE'}; Division = {branch: 'CSE', name: 'A', semester: 5, academic_year: '2024-2025', student_count: 60, num_batches: 3}; Subject = {name: 'Data Structures', code: 'CS301', credits: 4, semester: 5, has_lab: True, weekly_lectures: 3}; Time Slot = {start_time: '08:30', end_time: '09:25', slot_label: 'Slot 1'}; Room = {name: '101', capacity: 60, room_type: 'Classroom'}; Room = {name: 'Lab-A', capacity: 30, room_type: 'Lab'}; Faculty (regular) = {department: 'CSE', designation: 'Assistant Professor', working_hours: {start: '09:00', end: '17:00'}, subjects_can_teach: ['Data Structures', 'DBMS']}; Faculty (visiting) = {department: 'CSE', is_visiting: true, visiting_available_days: ['Monday', 'Wednesday'], visiting_slot_ids: {\"Monday\": [1, 2], \"Wednesday\": [3, 4]}}.")

add_heading_custom("Appendix G \u2013 Sample Generated Timetable", level=2)
add_para("Table G.1. Sample Generated Timetable (AI Auto-Generated, Division CSE-A, Semester 5)")
add_table(
    ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    [
        ["08:30-09:25", "Agile Dev\nNimisha Patel\nRoom 101", "Cyber Crime\nNimisha Patel\nRoom 101", "Data Security\nNimisha Patel\nRoom 101", "Data Security\nChintan Rana\nRoom 101", "Image Proc.\nDivya Sharma\nRoom 101"],
        ["09:25-10:20", "Data Security\nNimisha Patel\nRoom 101", "Agile Dev\nAjeet Patel\nRoom 101", "Pred. Analytics\nDivya Sharma\nRoom 101", "Cyber Crime\nChintan Rana\nRoom 102", "Agile Dev\nAjeet Patel\nRoom 101"],
        ["10:30-11:30", "[A1] Lab: CCM\nKhyati\nLab-A", "Cyber Crime\nChintan Rana\nRoom 101", "[A1] Lab: ASDD\nDivya\nLab-A", "Pred. Analytics\nDivya Sharma\nRoom 101", "[A1] Lab: IP\nNimisha\nLab-A"],
        ["11:30-12:30", "[A1] Lab: CCM\nKhyati\nLab-A", "Image Proc.\nDivya Sharma\nRoom 101", "[A1] Lab: ASDD\nDivya\nLab-A", "LIBRARY", "[A1] Lab: IP\nNimisha\nLab-A"],
        ["13:00-14:00", "Cyber Crime\nChintan Rana\nRoom 101", "[A1] Lab: DS\nChintan\nLab-A", "LIBRARY", "[A1] Lab: PA\nNeha\nLab-A", "LIBRARY"],
        ["14:00-15:00", "Pred. Analytics\nDivya Sharma\nRoom 101", "[A1] Lab: DS\nChintan\nLab-A", "LIBRARY", "[A1] Lab: PA\nNeha\nLab-A", "LIBRARY"],
    ]
)

add_heading_custom("Appendix H \u2013 Application Screenshots", level=2)
add_para("Insert, in order: Login/Signup page, Admin Dashboard, Manage Branches/Divisions/Subjects/Time Slots/Rooms pages, Timetable Creation (side-by-side) page, AI Auto-Generator Preview, Faculty Availability panel, ML risk badge and recommendations panel, AI Clash Resolution Suggestions panel, Faculty Dashboard, Faculty Profile (Regular and Visiting), Global Search Results, Final Timetable View, View Clashes, Activity Log, Admin Profile, CSV Export.")

add_heading_custom("Appendix I \u2013 Glossary", level=2)
add_para("Table I.1. Glossary")
add_table(["Term", "Definition"], [
    ["Branch", "An academic department/programme, e.g., CSE, ICT, ECE."],
    ["Division", "A section/batch of students within a branch and semester."],
    ["Batch", "A sub-group within a division for laboratory sessions (e.g., D1, D2, D3)."],
    ["Room", "A physical space (classroom, lab, or seminar hall) with capacity and type attributes."],
    ["Clash", "A scheduling conflict involving a faculty member, room, or division."],
    ["ORM", "Object-Relational Mapper; here, Flask-SQLAlchemy."],
    ["Random Forest", "An ensemble ML classifier of many decision trees, used for clash risk prediction."],
    ["Risk Score", "A 0\u20131 value output by the ML model indicating predicted clash likelihood."],
    ["Auto-Resolve", "One-click application of an ML-generated resolution suggestion."],
    ["Auto-Generator", "AI service that constructs complete, clash-free timetables using constraint satisfaction."],
    ["Visiting Faculty", "Part-time or adjunct faculty with day-wise, per-slot availability constraints."],
    ["Resolution Method", "How a clash was resolved: 'manual' or 'auto'."],
    ["Entry Type", "The type of timetable entry: 'lecture', 'lab', 'library', or 'break'."],
    ["Activity Log", "A record of an administrative action with user attribution and timestamp."],
    ["AJAX API", "Asynchronous JSON API for non-reload browser interactions."],
])

add_heading_custom("Appendix J \u2013 Abbreviations", level=2)
add_para("Table J.1. Abbreviations")
add_table(["Abbreviation", "Expansion"], [
    ["CSE", "Computer Science and Engineering"],
    ["ICT", "Information and Communication Technology"],
    ["ECE", "Electronics and Communication Engineering"],
    ["ORM", "Object-Relational Mapper"],
    ["CRUD", "Create, Read, Update, Delete"],
    ["API", "Application Programming Interface"],
    ["ML", "Machine Learning"],
    ["AI", "Artificial Intelligence"],
    ["ER Diagram", "Entity Relationship Diagram"],
    ["DFD", "Data Flow Diagram"],
    ["UML", "Unified Modeling Language"],
    ["WSGI", "Web Server Gateway Interface"],
    ["SSL", "Secure Sockets Layer"],
    ["CSV", "Comma-Separated Values"],
    ["ZIP", "Compressed Archive Format"],
    ["AJAX", "Asynchronous JavaScript and XML"],
    ["CSP", "Constraint Satisfaction Problem"],
    ["GTU", "Gujarat Technological University"],
    ["PWA", "Progressive Web Application"],
    ["ERP", "Enterprise Resource Planning"],
])


# ============================================
# SAVE
# ============================================
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Updated_Internship_Report.docx")
doc.save(output_path)
print(f"[OK] Report saved to: {output_path}")
print(f"[OK] Total paragraphs: {len(doc.paragraphs)}")

**Timetable AI: Intelligent timetable generator with ML clash prediction**

#### A PROJECT REPORT

##### Submitted by

## PATEL KRISH KALPESHBHAI

#### 230670142018

##### In partial fulfillment for the award of the degree of

## BACHELOR OF ENGINEERING

***in***

##### Computer Science Engineering (Artificial Intelligence & Machine Learning)

##### SAL Institute of Technology & Engineering Research

##### Bhadaj Circle, Ahmedabad, Gujarat (Affiliated with GTU)

*(Insert GTU logo image)*

*(Insert SAL Logo image)*

### Gujarat Technological University, Ahmedabad

**Academic Year**

**(2026-2027)**

*(Insert GTU logo image)*

*(Insert SAL Logo image)*

**SAL Institute of Technology & Engineering Research**

**Bhadaj Circle, Ahmedabad, Gujarat (Affiliated with GTU)**

**CERTIFICATE**

This is to certify that the project report submitted along with the project entitled **Internship** has been carried out by **Patel Krish Kalpeshbhai** under my guidance in partial fulfillment for the degree of Bachelor of Engineering in **Computer Science Engineering (Artificial Intelligence And Machine Learning),** 7th Semester of Gujarat Technological University, Ahmadabad during the academic year 2026-27.

**Dr. Nimisha Patel**

|  |  |
| --- | --- |
| Internal Guide | HoD CE/CSE/CSE-AIML/ICT |
| Department | SALITER |

*(Insert signature image)*

*(Insert GTU logo image)*

*(Insert SAL Logo image)*

**SAL Institute of Technology & Engineering Research**

**Bhadaj Circle, Ahmedabad, Gujarat (Affiliated with GTU)**

**DECLARATION**

**CERTIFICATE**

I hereby declare that the Internship / Project report submitted along with the Internship entitled Internship submitted in partial fulfillment for the degree of Bachelor of Engineering in **Computer Science Engineering (Artificial Intelligence & Machine Learning** to Gujarat Technological University, Ahmedabad, is a bonafide record of original project work carried out by me **at SoftCoding Solutions** under the supervision of **Abhishek Sir & Dr. Nimisha Patel** and that no part of this report has been directly copied from any students' reports or taken from any other source, without providing due reference.

**Name of the Student (Enrollment No) Sign of Student**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Acknowledgement**

I wish to express my sincere gratitude to our External guide Mr. **Abhishek Sir** for continuously guiding me at the company and answering all my doubts with patience. I would also like to thank my Internal Guide Prof. **Dr. Nimisha Patel** for helping us through our internship by giving us the necessary suggestions and advice along with their valuable co-ordination in completing this internship.

We also thank our parents, friends and all the members of the family for their precious support and encouragement which they had provided in completion of our work. In addition to that, we would also like to mention the company personals who gave us the permission to use and experience the valuable resources required for the internship.

Thus, In conclusion to the above said, we once again thank the staff members of **SoftCoding Solutions** for their valuable support in completion of the project.

Thank You

Patel Krish Kalpeshbhai

---

**CONTENTS**

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Title Page | | | | I |
| Certificates | | | | II |
| Acknowledgement | | | | III |
| Content | | | | IV |
| List of Figures | | | | V |
| List of Table | | | | VI |
| 1 |  |  | Introduction | 1 |
|  | 1.1 |  | Introduction |  |
|  | 1.2 |  | Background of the Study |  |
|  |  | 1.2.1 | Evolution of Academic Timetable Management |  |
|  |  | 1.2.2 | Traditional Timetable Preparation |  |
|  |  | 1.2.3 | Digital Transformation in Educational Institutions |  |
|  |  | 1.2.4 | Importance of Academic Scheduling |  |
|  | 1.3 |  | Problem Statement |  |
|  |  | 1.3.1 | Faculty Scheduling Conflicts |  |
|  |  | 1.3.2 | Classroom Allocation Problems |  |
|  |  | 1.3.3 | Laboratory Scheduling Challenges |  |
|  |  | 1.3.4 | Student Batch Conflicts |  |
|  |  | 1.3.5 | Administrative Challenges |  |
|  | 1.4 |  | Motivation |  |
|  | 1.5 |  | Objectives |  |
|  |  | 1.5.1 | Primary Objectives |  |
|  |  | 1.5.2 | Secondary Objectives |  |
|  | 1.6 |  | Scope of the Project |  |
|  | 1.7 |  | Need for the Proposed System |  |
|  | 1.8 |  | Proposed Solution Overview |  |
|  | 1.9 |  | Advantages of the Proposed System |  |
|  | 1.10 |  | Applications |  |
|  | 1.11 |  | Project Contribution |  |
|  | 1.12 |  | Organization of the Report |  |
| 2 |  |  | Literature Survey |  |
|  | 2.1 |  | Introduction |  |
|  | 2.2 |  | Academic Timetable Scheduling |  |
|  | 2.3 |  | Traditional Scheduling Techniques |  |
|  | 2.4 |  | Automated Scheduling Techniques |  |
|  | 2.5 |  | Constraint Satisfaction Problems |  |
|  | 2.6 |  | Graph Coloring Approach |  |
|  | 2.7 |  | Genetic Algorithm |  |
|  | 2.8 |  | Google OR-Tools |  |
|  | 2.9 |  | Machine Learning Approaches |  |
|  | 2.10 |  | Review of Existing Timetable Systems |  |
|  | 2.11 |  | Comparative Analysis of Existing Systems |  |
|  | 2.12 |  | Research Paper Review |  |
|  | 2.13 |  | Research Gap |  |
|  | 2.14 |  | Chapter Summary |  |
| 3 |  |  | Requirement Analysis |  |
|  | 3.1 |  | Introduction |  |
|  | 3.2 |  | Existing System Analysis |  |
|  | 3.3 |  | Limitations of Existing System |  |
|  | 3.4 |  | Proposed System Requirements |  |
|  | 3.5 |  | Functional Requirements |  |
|  | 3.6 |  | Non-Functional Requirements |  |
|  | 3.7 |  | Hardware Requirements |  |
|  | 3.8 |  | Software Requirements |  |
|  | 3.9 |  | Feasibility Study |  |
|  |  | 3.9.1 | Technical Feasibility |  |
|  |  | 3.9.2 | Economic Feasibility |  |
|  |  | 3.9.3 | Operational Feasibility |  |
|  | 3.10 |  | User Roles |  |
|  | 3.11 |  | Requirement Traceability Matrix |  |
| 4 |  |  | System Analysis And Design |  |
|  | 4.1 |  | System Architecture |  |
|  | 4.2 |  | Overall Workflow |  |
|  | 4.3 |  | Module Identification |  |
|  | 4.4 |  | Authentication Module |  |
|  | 4.5 |  | Faculty Management Module |  |
|  | 4.6 |  | Room & Resource Management Module |  |
|  | 4.7 |  | Subject Management Module |  |
|  | 4.8 |  | Timetable Generation Module |  |
|  | 4.9 |  | Clash Detection Module |  |
|  | 4.10 |  | Intelligent Clash Resolution Module |  |
|  | 4.11 |  | Reports & Export Module |  |
|  | 4.12 |  | Global Search Module |  |
|  | 4.13 |  | Use Case Diagram |  |
|  | 4.14 |  | Activity Diagram |  |
|  | 4.15 |  | Sequence Diagram |  |
|  | 4.16 |  | Class Diagram |  |
|  | 4.17 |  | ER Diagram |  |
|  | 4.18 |  | Component Diagram |  |
|  | 4.19 |  | Deployment Diagram |  |
|  | 4.20 |  | DFD Level 0 |  |
|  | 4.21 |  | DFD Level 1 |  |
|  | 4.22 |  | DFD Level 2 |  |
| 5 |  |  | System Implementation |  |
|  | 5.1 |  | Introduction |  |
|  | 5.2 |  | Project Structure |  |
|  | 5.3 |  | Frontend Implementation |  |
|  | 5.4 |  | Backend Implementation |  |
|  | 5.5 |  | Database Implementation |  |
|  | 5.6 |  | Authentication Implementation |  |
|  | 5.7 |  | Dashboard Implementation |  |
|  | 5.8 |  | Timetable Generation Implementation |  |
|  | 5.9 |  | Clash Detection Implementation |  |
|  | 5.10 |  | Intelligent Clash Resolution Implementation |  |
|  | 5.11 |  | Global Search Implementation |  |
|  | 5.12 |  | CSV/ZIP Export Implementation |  |
|  | 5.13 |  | Report Generation |  |
|  | 5.14 |  | Deployment |  |
| 6 |  |  | Timetable Generation And Clash Resolution |  |
|  | 6.1 |  | Introduction |  |
|  | 6.2 |  | Timetable Scheduling Problem |  |
|  | 6.3 |  | Scheduling Constraints |  |
|  |  | 6.3.1 | Hard Constraints |  |
|  |  | 6.3.2 | Soft Constraints |  |
|  | 6.4 |  | Faculty Allocation |  |
|  | 6.5 |  | Visiting Faculty Scheduling |  |
|  | 6.6 |  | Classroom Allocation |  |
|  | 6.7 |  | Laboratory Allocation |  |
|  | 6.8 |  | Subject Allocation |  |
|  | 6.9 |  | Time Slot Allocation |  |
|  | 6.10 |  | Clash Detection Process |  |
|  | 6.11 |  | Clash Resolution Strategy |  |
|  | 6.12 |  | Intelligent Clash Resolution Suggestions |  |
|  | 6.13 |  | Scheduling Workflow |  |
|  | 6.14 |  | Algorithm Description |  |
|  | 6.15 |  | Optimization Strategy |  |
|  | 6.16 |  | Complexity Analysis |  |
| 7 |  |  | Database Design |  |
|  | 7.1 |  | Introduction |  |
|  | 7.2 |  | Database Architecture |  |
|  | 7.3 |  | Entity Relationship Diagram |  |
|  | 7.4 |  | Database Tables |  |
|  |  | 7.4.1 | users |  |
|  |  | 7.4.2 | faculty |  |
|  |  | 7.4.3 | branches |  |
|  |  | 7.4.4 | divisions |  |
|  |  | 7.4.5 | time\_slots |  |
|  |  | 7.4.6 | subjects |  |
|  |  | 7.4.7 | rooms |  |
|  |  | 7.4.8 | timetable |  |
|  |  | 7.4.9 | clash\_logs |  |
|  | 7.5 |  | Relationships |  |
|  | 7.6 |  | SQL Schema |  |
|  | 7.7 |  | Data Dictionary |  |
|  | 7.8 |  | Sample Database Records |  |
| 8 |  |  | Testing And Validation |  |
|  | 8.1 |  | Introduction |  |
|  | 8.2 |  | Unit Testing |  |
|  | 8.3 |  | Integration Testing |  |
|  | 8.4 |  | System Testing |  |
|  | 8.5 |  | User Acceptance Testing |  |
|  | 8.6 |  | Black Box Testing |  |
|  | 8.7 |  | White Box Testing |  |
|  | 8.8 |  | Performance Testing |  |
|  | 8.9 |  | Security Testing |  |
|  | 8.10 |  | Test Cases |  |
|  | 8.11 |  | Bug Analysis |  |
| 9 |  |  | **Results And Discussion** |  |
|  | 9.1 |  | Introduction |  |
|  | 9.2 |  | Dashboard Results |  |
|  | 9.3 |  | Timetable Generation Results |  |
|  | 9.4 |  | Clash Resolution Results |  |
|  | 9.5 |  | Intelligent Clash Resolution Results |  |
|  | 9.6 |  | Global Search Results |  |
|  | 9.7 |  | Export Results |  |
|  | 9.8 |  | Performance Analysis |  |
|  | 9.9 |  | Comparison with Manual Scheduling |  |
|  | 9.10 |  | Advantages Achieved |  |
|  | 9.11 |  | Limitations |  |
| 10 |  |  | Future Scope And Conclusion |  |
|  | 10.1 |  | Future Scope |  |
|  |  | 10.1.1 | ERP Integration |  |
|  |  | 10.1.2 | Attendance Management |  |
|  |  | 10.1.3 | Mobile Application |  |
|  |  | 10.1.4 | Cloud Deployment |  |
|  |  | 10.1.5 | Multi-Campus Support |  |
|  |  | 10.1.6 | Advanced ML Enhancements |  |
|  | 10.2 |  | Conclusion |  |
| 11 |  |  | References |  |
|  | 11.1 |  | Books |  |
|  | 11.2 |  | Research Papers |  |
|  | 11.3 |  | IEEE Papers |  |
|  | 11.4 |  | Official Documentation |  |
|  | 11.5 |  | Websites |  |
| 12 |  |  | Appendix |  |
|  | A |  | User Manual |  |
|  | A.1 |  | Administrator Quick Guide |  |
|  | A.2 |  | Faculty Quick Guide |  |
|  | B |  | Installation Guide |  |
|  | C |  | Project Folder Structure |  |
|  | D |  | Database Schema |  |
|  | E |  | API Documentation |  |
|  | E.1 |  | Application Utility Endpoints |  |
|  | E.2 |  | Machine Learning API Endpoints |  |
|  | E.3 |  | Clash Resolution API Endpoints |  |
|  | F |  | Sample Input Data |  |
|  | G |  | Sample Generated Timetable |  |
|  | H |  | Application Screenshots |  |
|  | I |  | Glossary |  |
|  | J |  | Abbreviations |  |

---

**LIST OF FIGURES**

| **Figure Name** | **Page No.** |
| --- | --- |
| Figure 4.1. System Architecture Diagram |  |
| Figure 4.2. Overall Workflow Diagram |  |
| Figure 4.3: Login and Sign up Page |  |
| Figure 4.4: Faculty Profile (Regular Faculty) |  |
| Figure 4.5: Faculty Profile (Visiting Faculty – Day-wise Scheduling) |  |
| Figure 4.6: Manage Branches |  |
| Figure 4.7: Manage Divisions |  |
| Figure 4.8: Manage Subjects |  |
| Figure 4.9: Manage Rooms & Resources |  |
| Figure 4.10: Timetable Creation (Side-by-Side) Interface |  |
| Figure 4.11. Use Case Diagram |  |
| Figure 4.12. Activity Diagram – Timetable Creation |  |
| Figure 4.13. Sequence Diagram – Clash Detection and Resolution |  |
| Figure 4.14. Class Diagram |  |
| Figure 4.15. Entity Relationship (ER) Diagram |  |
| Figure 4.16. Component Diagram |  |
| Figure 4.17. Deployment Diagram |  |
| Figure 4.18. Data Flow Diagram – Level 0 |  |
| Figure 4.19. Data Flow Diagram – Level 1 |  |
| Figure 4.20. Data Flow Diagram – Level 2 |  |
| Figure 5.1. Admin Dashboard |  |
| Figure 5.2. Faculty Dashboard |  |
| Figure 5.3. Faculty Availability Panel |  |
| Figure 5.4. View Clashes Screen with AI Resolution Suggestions |  |
| Figure 5.5. Global Search Results Page |  |
| Figure 5.6. Final Timetable View |  |
| Figure 5.7. CSV Export – Sample Downloaded File |  |
| Figure 6.1. ML Risk Prediction Badge |  |
| Figure 6.2. Random Forest Model Architecture Diagram |  |
| Figure 6.3. ML Recommendations Panel |  |
| Figure 6.4. AI-Powered Clash Resolution Suggestions Panel |  |
| Figure 6.5. Auto-Resolve Workflow Diagram |  |
| Figure 9.1. Dashboard Displaying Clash Indicators Across Divisions |  |
| Figure 9.2. ML Feature Importance Chart |  |
| Figure 9.3. Clash Resolution Suggestion Accuracy |  |
| Figure C.1. Project Folder Structure |  |

---

**LIST OF TABLES**

| **Table Name** | **Page No.** |
| --- | --- |
| Table 2.1. Comparative Analysis of Existing Timetable Systems |  |
| Table 3.1 Functional Requirements |  |
| Table 3.2. Non-Functional Requirements |  |
| Table 3.3. Hardware Requirements |  |
| Table 3.4. Software Requirements |  |
| Table 3.5. User Roles |  |
| Table 3.6. Requirement Traceability Matrix |  |
| Table 4.1. Module Identification |  |
| Table 5.1. Project Structure |  |
| Table 6.1. Clash Detection Process |  |
| Table 6.2. Intelligent Clash Resolution – Suggestion Types |  |
| Table 7.1. Users Table Schema |  |
| Table 7.2. Faculty Table Schema |  |
| Table 7.3. Branches Table Schema |  |
| Table 7.4. Divisions Table Schema |  |
| Table 7.5. Time Slots Table Schema |  |
| Table 7.6. Subjects Table Schema |  |
| Table 7.7. Rooms Table Schema |  |
| Table 7.8. Timetable Table Schema |  |
| Table 7.9. Clash Logs Table Schema |  |
| Table 7.10. Relationships |  |
| Table 7.11. Data Dictionary |  |
| Table 7.12. Sample Database Records |  |
| Table 8.1. Test Cases |  |
| Table 9.1 The recorded direct-testing results for the six core ML functions. |  |
| Table 9.2 The additional performance metrics recorded for the ML subsystem. |  |
| Table 9.3. Comparison: Manual Scheduling vs. Proposed System |  |
| Table E.1. Application REST/Utility API Endpoints |  |
| Table E.2. ML API Endpoints |  |
| Table E.3. Clash Resolution API Endpoints |  |
| Table G.1. Sample Generated Timetable |  |
| Table I.1. Glossary |  |
| Table J.1. Abbreviations |  |

---

**Chapter 1: Introduction**

**1.1 Introduction**

Every academic term, colleges and universities must produce a timetable that assigns subjects, faculty members, classrooms, and time slots to every division or section of every branch offered by the institution. This is, at its core, a constraint-satisfaction problem: the same faculty member cannot be in two classrooms at once, the same room cannot host two different classes simultaneously, and the same batch of students (division) cannot be expected to attend two lectures at the same time. When timetables are built manually – typically in spreadsheets – these constraints are easy to violate and hard to verify, especially as the number of branches, divisions, subjects, and faculty members grows.

The College Timetable Management System with Intelligent Clash Detection and Resolution is a full-stack web application developed to solve this problem. It is built using the Flask micro-framework for Python on the backend, the Flask-SQLAlchemy Object-Relational Mapper (ORM) for data persistence, MySQL (with automatic SQLite fallback) as the relational database engine, and server-rendered HTML, CSS, and JavaScript for the frontend. The application is organised around two role-based portals – Administrator and Faculty – and around a dedicated Clash Detection Service that validates every proposed timetable entry against the faculty, room, and division that it references before the entry is committed to the database.

In addition to this deterministic, rule-based clash detection, the project extends the system with an Intelligent Clash Prevention, Recommendation, and Resolution module. This module applies a supervised machine-learning model – a scikit-learn Random Forest Classifier – trained on the institution's own historical timetable data, to proactively estimate the probability that a proposed entry will lead to a clash, to recommend lower-risk alternative time slots, to recommend suitable faculty members for a subject based on their expertise and availability, and to generate context-aware resolution suggestions for detected clashes that can be auto-applied with a single click.

**1.2 Background of the Study**

**1.2.1 Evolution of Academic Timetable Management**

Timetable preparation in academic institutions has historically progressed from fully manual, paper-based rosters, to spreadsheet-based planning, to dedicated software systems. Each stage reduced some of the effort involved but did not eliminate the fundamental risk of scheduling conflicts unless the tool explicitly checked for them. The system documented in this report belongs to the third stage: a purpose-built, database-backed web application in which conflict checking is not an afterthought performed by a human reviewer, but a service (the Clash Detection Service) invoked automatically every time a new timetable entry is proposed.

**1.2.2 Traditional Timetable Preparation**

In the traditional approach, an administrative staff member or a coordinator manually allocates subjects, faculty, and rooms to time slots using a spreadsheet or a printed grid. Cross-checking for faculty, room, or division conflicts is done by visual inspection or by cross-referencing multiple sheets, which becomes increasingly error-prone as the number of divisions, subjects, and faculty members increases. Any change – such as a faculty member becoming unavailable – requires the entire timetable (or the affected parts of it) to be manually re-checked for new conflicts.

**1.2.3 Digital Transformation in Educational Institutions**

Educational institutions increasingly rely on web-based administrative systems for tasks such as attendance, admissions, examinations, and scheduling. A digital timetable system that runs in a browser, is backed by a relational database, and enforces role-based access (administrator versus faculty) fits naturally into this broader digitisation of academic administration. The system in this project follows this pattern: it is accessed through a web browser at a defined URL, stores all data in a MySQL database (with automatic SQLite fallback for development and resilience), and distinguishes between what an Administrator and a Faculty member are permitted to do.

**1.2.4 Importance of Academic Scheduling**

A correct and well-organised timetable directly affects the day-to-day functioning of an institution – it determines faculty workload distribution, classroom utilisation, and the learning experience of students. A single undetected clash (for example, a faculty member being assigned to two divisions in the same period) can disrupt classes for an entire day and erode confidence in the administrative system. Automated clash detection, of the kind implemented in this project's Clash Detection Service, therefore has a direct and measurable impact on institutional efficiency.

**1.3 Problem Statements**

Manually constructed academic timetables are susceptible to five recurring categories of problems, each of which is addressed by a specific component of the proposed system.

**1.3.1 Faculty Scheduling Conflicts**

A faculty member may inadvertently be assigned to teach two different divisions during the same day and time slot. Because a single faculty member may teach subjects across multiple branches and divisions, this type of conflict is a global check – it must be verified across the entire institution, not just within one branch, which is precisely how the Faculty Clash check is scoped in this system.

**1.3.2 Classroom Allocation Problems**

The same physical classroom or laboratory can be entered into two different timetable rows for the same day and time slot when allocation is done manually, resulting in two different divisions being sent to the same room. The system's Room Clash check exists specifically to prevent this double booking of physical spaces. Additionally, managing rooms with their capacities and types (Classroom, Lab, Seminar Hall) is now a first-class module in the system, enabling administrators to maintain a structured inventory of physical spaces.

**1.3.3 Laboratory Scheduling Challenges**

Laboratory sessions add an additional layer of complexity because they typically require a designated laboratory room rather than a general classroom, and often occupy a longer contiguous time block than a lecture. With the Room & Resource Management module, laboratories are now tracked as a distinct room\_type ('Lab'), and the Room Clash check applies uniformly to both classrooms and laboratories, ensuring that a laboratory slot is checked with the same rigour as any other room-bound session.

**1.3.4 Student Batch Conflicts**

A division (a batch or section of students, for example CSE-A) must not be scheduled for two classes at the same time, since a group of students can physically only attend one lecture at once. The Division Clash check enforces this by verifying that a division does not already have an entry for the same day and time slot before a new entry is added.

**1.3.5 Administrative Challenges**

Beyond the three clash types above, administrators face the broader operational challenge of managing many moving parts – branches, divisions, subjects, time slots, rooms, and faculty profiles – consistently, and of being able to see, at a glance, which divisions currently have unresolved clashes. This project addresses that challenge through a centralised Admin Dashboard with colour-coded clash indicators (green for a division with no clashes, red for a division with detected clashes), dedicated management screens for branches, divisions, subjects, time slots, rooms, and faculty, a global search facility across all entities, and CSV/ZIP export functionality for timetable distribution.

**1.4 Motivation**

The motivation for this project stems from the observation that clash detection is a mechanical, rule-based task that is well suited to automation, while the higher-level judgement calls involved in timetable construction (which subject to schedule when, which faculty member to prefer) are better left to a human administrator supported by good information. This motivated a design in which the human administrator retains control over the creation of the timetable through an interactive interface, while the system automatically performs the conflict verification that humans are prone to error on, offers data-driven recommendations (through the machine-learning module), and additionally provides intelligent resolution suggestions – with one-click auto-resolve capability – when conflicts do arise, rather than leaving the administrator to manually investigate alternatives.

**1.5 Objectives**

**1.5.1 Primary Objectives**

* To design and implement a web-based timetable management system using Flask, Flask-SQLAlchemy, and MySQL (with SQLite fallback).
* To implement an interactive, side-by-side timetable creation interface that shows time slots alongside real-time faculty availability.
* To implement a Clash Detection Service that performs faculty, room, and division clash checks whenever a timetable entry is created or modified.
* To provide role-based portals for Administrators and Faculty members with distinct permissions and views.
* To implement an Intelligent Clash Prevention, Recommendation, and Resolution module using a machine-learning model trained on the institution's own timetable data.
* To implement ML-powered clash resolution suggestions with one-click auto-resolve capability for detected clashes.

**1.5.2 Secondary Objectives**

* To provide a centralised Admin Dashboard summarising all divisions along with clash indicators and entry counts.
* To provide faculty members with a personal, day-organised schedule view generated automatically from the timetable data.
* To log every detected clash in a dedicated clash\_logs table with full resolution tracking (resolved\_by, resolution\_method, resolution\_note) for later review and audit.
* To secure the application using password hashing, session-based authentication, and role-based access-control decorators.
* To expose the machine-learning module's capabilities through a documented set of REST API endpoints.
* To implement a Room & Resource Management module for tracking classrooms, laboratories, and seminar halls with capacity and type attributes.
* To support visiting faculty scheduling with per-day, per-time-slot availability configuration.
* To provide global search across all entities (faculty, subjects, branches, divisions, rooms, clashes).
* To implement CSV/ZIP export of timetables for both administrators and faculty members.

**1.6 Scope of the Project**

The scope of the project covers: user registration and authentication for Administrator and Faculty roles; management of branches, divisions, subjects, time slots, rooms (with capacity and type), and faculty profiles (including visiting faculty day-wise scheduling) by the Administrator; creation, editing, and deletion of timetable entries with real-time clash validation; a faculty profile module in which faculty set their working hours, the subjects they can teach, and their visiting schedule if applicable; a clash-detection subsystem covering faculty, room, and division clashes; a machine-learning based clash-risk prediction, recommendation, and intelligent resolution suggestion subsystem with auto-resolve capability; a global search module across all entities; CSV/ZIP timetable export; and reporting views such as the final timetable view and the view-clashes screen with AI-powered resolution panels. The scope does not, in the current version of the system, extend to automatic end-to-end timetable generation without human input, integration with external institutional ERP systems, or a native mobile application – these are documented as future scope in Chapter 10.

**1.7 Need for the Proposed System**

Institutions that continue to rely on spreadsheet-based or paper-based timetable preparation have no systematic way of guaranteeing, at the moment an entry is created, that it does not conflict with an existing entry elsewhere in the institution. Additionally, when clashes are detected, administrators must manually investigate alternative rooms, faculty, or time slots – a time-consuming process. The proposed system directly addresses these needs by moving conflict verification out of human hands and into an automated service that runs on every entry, by providing intelligent resolution suggestions powered by ML when clashes are detected, and by additionally giving administrators a predictive, data-driven view of the risk associated with a proposed entry before it is even saved.

**1.8 Proposed Solution Overview**

The proposed solution is a Flask web application backed by a MySQL database (with automatic SQLite fallback), structured around SQLAlchemy models for Users, Faculty, Branches, Divisions, TimeSlots, Subjects, Rooms, Timetable entries, and ClashLogs. Administrators log in and are presented with a dashboard summarising all divisions; from there they can manage the foundational data (branches, divisions, subjects, time slots, rooms, faculty) and create timetables through an interactive screen that, for each time slot, shows subject selection alongside a live faculty-availability panel (marking each faculty member as Available or Busy). Every entry submission is passed through the Clash Detection Service, which checks faculty, room, and division clashes before the entry is committed; any detected clash is logged to the clash\_logs table and reflected on the dashboard. When clashes are detected, the system's Intelligent Resolution module generates ML-powered suggestions – alternative rooms, alternative faculty (scored by expertise and availability), and alternative time slots (scored by clash risk) – that can be auto-applied with a single click. Faculty members log in to a separate portal where they complete a profile (working hours, subjects they can teach, and visiting schedule if applicable) and view their personal schedule. Layered on top of this deterministic system is the machine-learning module, which uses a trained Random Forest Classifier to predict clash risk, recommend alternative slots, recommend faculty, generate resolution suggestions, and evaluate overall timetable quality, exposed through nine dedicated API endpoints and surfaced in the timetable-creation UI as risk badges and a recommendations panel, and in the clash-management UI as contextual resolution suggestions.

**1.9 Advantages of the Proposed System**

* Automated, rule-based clash checking removes the dependency on manual cross-verification for faculty, room, and division conflicts.
* The side-by-side timetable creation view with live faculty availability reduces the cognitive load on the administrator while building the schedule.
* Clash history is retained in the clash\_logs table with full resolution tracking (who resolved it, how, and any notes), giving the institution an auditable record of conflicts.
* The machine-learning module adds a predictive layer that can flag a high-risk entry before it is saved, rather than only after a conflict has already occurred.
* ML-powered intelligent resolution suggestions with one-click auto-resolve drastically reduce the time needed to handle detected clashes.
* The Room & Resource Management module provides structured tracking of classrooms, labs, and seminar halls with capacity and type attributes.
* Visiting faculty can configure day-wise availability with specific time slots per day, ensuring accurate scheduling of part-time staff.
* Global search across all entities enables rapid information retrieval.
* CSV/ZIP export allows timetables to be distributed offline.
* Role-based access control (Administrator vs. Faculty) ensures that each user only sees and modifies the data relevant to their role.
* Because the system is a web application, it can be accessed from any device with a browser without additional client software.
* Automatic SQLite fallback ensures the system remains operational even when the primary MySQL database is unavailable.

**1.10 Applications**

The system, as documented, is directly applicable to any single academic institution (college or university department) that needs to construct and maintain branch- and division-wise timetables and to track faculty teaching schedules. Within an institution it can be used by the timetabling office or academic administrators to build the master timetable, and by individual faculty members to view their own teaching schedule without needing access to the full administrative interface.

**1.11 Project Contribution**

This report documents the full scope of work carried out during the internship: understanding and analysing the existing manual timetabling process, studying the requirements for an automated replacement, working with the College Timetable Management System codebase (Flask backend, SQLAlchemy models, clash-detection service, intelligent clash resolution module, Room & Resource Management module, visiting faculty day-wise scheduling, global search, CSV/ZIP export, and the machine-learning clash-prediction module), and producing this structured documentation covering the system's architecture, database design, implementation, testing, and results, together with recommendations for future enhancement.

**1.12 Organization of the Report**

Chapter 2 surveys existing and related approaches to timetable scheduling. Chapter 3 presents the requirement analysis, including functional and non-functional requirements and a feasibility study. Chapter 4 covers system analysis and design, including the architecture and the standard UML and data-flow diagrams. Chapter 5 documents the implementation of the frontend, backend, database, authentication, room management, visiting faculty scheduling, intelligent clash resolution, global search, CSV/ZIP export, and reporting modules. Chapter 6 focuses specifically on the timetable-generation and clash-resolution logic, including the machine-learning component and the intelligent resolution suggestions. Chapter 7 details the database design. Chapter 8 covers testing and validation. Chapter 9 presents results and discussion. Chapter 10 discusses future scope and concludes the report. References and appendices follow.

---

**Chapter 2: Literature Survey**

**2.1 Introduction**

This chapter surveys the class of problems to which academic timetabling belongs, the broad families of techniques that are commonly used to address them, and the specific technology choices (Flask, SQLAlchemy, MySQL, and scikit-learn) adopted in the project. It also situates the proposed system's rule-based clash-checking approach, its supplementary Random-Forest-based risk-prediction approach, and its intelligent resolution-suggestion capability within this wider landscape, and closes with a comparative review and an identified research gap that motivates the project.

**2.2 Academic Timetable Scheduling**

Academic timetabling is the problem of assigning a set of events (subject–division pairs that must meet) to a set of resources (time slots, rooms, and faculty) such that no resource is double-booked and, ideally, additional soft preferences are respected. The problem is characterised by hard constraints, which must never be violated (for example, a faculty member cannot teach two classes at once), and soft constraints, which are desirable but not mandatory (for example, avoiding large gaps in a faculty member's day). The system built in this project focuses primarily on enforcing the three hard constraints that are most disruptive when violated in a live academic setting: faculty double-booking, room double-booking, and division double-booking.

**2.3 Traditional Scheduling Techniques**

Traditional, non-computerised scheduling relies on manual allocation, typically supported by a spreadsheet, followed by manual cross-checking. Because the number of pairwise comparisons required to verify that no two entries conflict grows quickly as the number of entries increases, manual verification does not scale well and is the primary weakness that automated clash-detection services, such as the one implemented in this project, are designed to eliminate.

**2.4 Automated Scheduling Techniques**

Automated approaches to timetabling generally fall into two categories: (a) systems that detect and report conflicts in a timetable that a human is actively constructing, and (b) systems that attempt to generate a complete, conflict-free timetable automatically from a set of constraints. The system documented in this report belongs primarily to the first category – it keeps a human administrator in control of the scheduling decisions while automatically validating each decision against the faculty, room, and division constraints – and it supplements this with predictive risk scoring, recommendation features, and intelligent clash-resolution suggestions drawn from the second category's underlying techniques (specifically, machine learning) without performing fully autonomous generation.

**2.5 Constraint Satisfaction Problems**

Academic timetabling can be formally modelled as a Constraint Satisfaction Problem (CSP), in which variables represent timetable entries, domains represent the possible (faculty, room, time-slot) combinations, and constraints represent the no-double-booking rules. The Clash Detection Service in this project implements, in effect, a set of three explicit constraint checks – corresponding to the faculty, room, and division constraints – evaluated against the existing rows of the timetable table each time a new entry is proposed, which is a direct, database-query-based realisation of CSP-style constraint checking rather than a general-purpose CSP solver.

**2.6 Graph Coloring Approach**

A well-known formal technique for timetabling is to model each event as a vertex in a conflict graph, connect two vertices with an edge whenever the corresponding events cannot share the same time slot, and then treat time-slot assignment as a graph-colouring problem in which no two adjacent vertices may receive the same colour. While the current system does not implement an explicit graph-colouring algorithm, the faculty/room/division clash rules it enforces are conceptually equivalent to the edge constraints of such a conflict graph, and a future enhancement (noted in Chapter 10) could apply graph-colouring or similar combinatorial optimisation techniques to automatically suggest a conflict-free arrangement.

**2.7 Genetic Algorithm**

Genetic algorithms are a popular metaheuristic for automated timetable generation: candidate timetables are represented as chromosomes, and operators such as crossover and mutation are applied across generations to search for a schedule that minimises constraint violations. This project does not use a genetic algorithm; instead, it uses a supervised classification model (Random Forest) trained on historical scheduling data to estimate the probability of a clash for a proposed entry and to generate context-aware resolution suggestions, which is a fundamentally different (predictive and advisory, rather than search-based generative) approach to reducing conflicts.

**2.8 Google OR-Tools**

Google OR-Tools is a widely used open-source suite for combinatorial optimisation, including CP-SAT solvers well suited to timetabling-style constraint problems. The current implementation of this project does not integrate OR-Tools or any external constraint-solver library; its clash detection is implemented directly as SQLAlchemy queries within the Flask application, and its predictive and resolution layer is implemented with scikit-learn. Integrating a dedicated solver such as OR-Tools for fully automated, optimised timetable generation is identified as a possible future enhancement.

**2.9 Machine Learning Approaches**

Machine-learning approaches to scheduling problems typically use historical or simulated scheduling data to train a model that predicts the likelihood of a conflict, recommends favourable assignments, or scores the quality of a candidate schedule, rather than searching for a schedule from first principles. This is precisely the role that the machine-learning module plays in this project: a Random Forest Classifier is trained on the timetable table's historical rows (faculty\_id, division\_id, subject\_id, time\_slot\_id, day\_of\_week, and an encoded room\_number) to predict clash probability, and the trained model is additionally used, through supporting logic in the ML engine, to rank alternative time slots, candidate faculty members, generate intelligent resolution suggestions for detected clashes, and evaluate the overall quality of a division's timetable.

**2.10 Review of Existing Timetable Systems**

Existing timetable-management tools in academic use range from generic spreadsheet templates, to institution-specific ERP scheduling modules, to open-source and commercial dedicated timetabling software. The system built for this project differs from a generic spreadsheet in that clash checking is automatic rather than manual, and it differs from many dedicated timetabling packages in that it additionally incorporates a machine-learning based risk-prediction, recommendation, and intelligent clash-resolution layer trained on the institution's own data, rather than relying purely on deterministic constraint checking.

**2.11 Comparative Analysis of Existing Systems**

Table 2.1. Comparative Analysis of Existing Timetable Systems

| **Aspect** | **Manual / Spreadsheet Method** | **Generic Rule-Based Software** | **Proposed System** |
| --- | --- | --- | --- |
| Faculty clash checking | Manual, error-prone | Automated | Automated (global scope, across all branches) |
| Room clash checking | Manual | Automated | Automated, with Room & Resource management module |
| Division clash checking | Manual | Automated | Automated |
| Clash history / audit log | Not available | Varies | Dedicated clash\_logs table with full resolution tracking |
| Predictive risk scoring | Not available | Rare | Random Forest based risk prediction |
| Alternative slot recommendation | Not available | Rare | ML-based, top 5 lowest-risk slots |
| Faculty recommendation | Manual judgement | Rare | ML-based scoring (expertise + availability) |
| Intelligent clash resolution | Not available | Not available | ML-powered suggestions with one-click auto-resolve |
| Room/resource management | Manual | Varies | Dedicated module with capacity and type tracking |
| Visiting faculty scheduling | Manual | Rare | Day-wise, per-slot availability configuration |
| Global search | Not applicable | Varies | Full-text search across all entities |
| Timetable export | Manual copy | Varies | CSV/ZIP automated export |
| Role-based portals | Not applicable | Varies | Separate Administrator and Faculty portals |

**2.12 Research Paper Review**

This section summarises, at the level of general technique, ten themes commonly discussed in academic and applied literature on timetable clash resolution and scheduling automation that are directly relevant to the design of this project. Each is discussed with respect to how the corresponding idea is, or is not, reflected in the implemented system, rather than as a citation of a specific external paper.

### 2.12.1 Paper 1 – Constraint-Based Timetabling

Discusses framing timetabling as hard/soft constraint satisfaction. Relevance: the project's faculty/room/division checks are hard-constraint checks implemented as direct database queries.

### 2.12.2 Paper 2 – Graph-Colouring Models for Scheduling

Discusses conflict graphs and colouring for time-slot assignment. Relevance: conceptually related to how the project's clash rules define which entries may not share a slot.

### 2.12.3 Paper 3 – Genetic Algorithms for Timetable Generation

Discusses evolutionary search over candidate timetables. Relevance: identified as a possible future extension for automatic, optimisation-driven timetable generation.

### 2.12.4 Paper 4 – Constraint Programming Solvers (e.g., OR-Tools/CP-SAT style approaches)

Discusses solver-based generation of feasible schedules. Relevance: noted as an alternative to the project's current rule-based, human-in-the-loop approach.

### 2.12.5 Paper 5 – Supervised Learning for Conflict Prediction

Discusses using classifiers trained on historical scheduling outcomes to predict conflict likelihood. Relevance: directly mirrors the project's Random Forest clash-risk predictor trained on the timetable table.

### 2.12.6 Paper 6 – Recommendation Systems for Resource Allocation

Discusses scoring and ranking candidate resources (e.g., staff) for an assignment. Relevance: mirrors the project's faculty-recommendation feature and the intelligent clash-resolution suggestion system, which scores candidates by subject expertise, availability, and ML-predicted clash risk.

### 2.12.7 Paper 7 – Role-Based Access Control in Administrative Systems

Discusses separating administrator and end-user privileges. Relevance: implemented in the project via the User.role field and admin\_required-style route decorators.

### 2.12.8 Paper 8 – Web-Based ORM-Backed Administrative Applications

Discusses using an ORM (such as SQLAlchemy) over raw SQL for maintainability. Relevance: the project's models.py defines all entities as SQLAlchemy model classes.

### 2.12.9 Paper 9 – Dashboard-Based Monitoring for Institutional Systems

Discusses summarising system state through indicators/dashboards for administrators. Relevance: mirrors the project's Admin Dashboard with green/red clash indicators per division.

### 2.12.10 Paper 10 – Feature Engineering for Tabular Classification Models

Discusses encoding categorical identifiers (IDs, day-of-week) as model features. Relevance: mirrors the six input features (faculty\_id, division\_id, subject\_id, time\_slot\_id, day\_of\_week, room\_number) used by the project's Random Forest model.

**2.13 Research Gap**

Deterministic, rule-based clash-detection systems reliably catch conflicts that have already been proposed, but on their own they offer no foresight – they do not tell an administrator, in advance, which of several candidate time slots or candidate faculty members is least likely to eventually cause friction elsewhere in the schedule. Furthermore, once a clash is detected, existing systems leave the administrator to manually investigate and apply alternatives, which is time-consuming and error-prone. This is the gap that the project's Intelligent Clash Prevention, Recommendation, and Resolution module – the Random Forest based risk predictor, slot recommender, faculty recommender, and auto-resolve suggestion engine – is designed to close, by combining deterministic clash checks with a predictive, data-driven layer trained on the institution's own historical scheduling patterns and an intelligent suggestion engine that provides actionable, one-click resolutions.

**2.14 Chapter Summary**

This chapter reviewed the general landscape of timetable scheduling techniques – constraint satisfaction, graph colouring, genetic algorithms, and constraint solvers – as well as machine-learning approaches to conflict prediction and resolution, and positioned the proposed system's multi-layered design (a deterministic Clash Detection Service plus a supervised-learning risk-prediction, recommendation, and intelligent resolution module) relative to this landscape. The next chapter presents the detailed requirement analysis for the system.

---

**Chapter 3: Requirement Analysis**

**3.1 Introduction**

This chapter analyses the existing (manual) scheduling process, identifies its limitations, and derives the functional and non-functional requirements that the proposed system, as implemented, satisfies. It also documents the hardware and software requirements, a feasibility study, the defined user roles, and a requirement traceability matrix linking requirements to the corresponding system modules.

**3.2 Existing System Analysis**

In the manual/spreadsheet-based existing system, a coordinator maintains a separate sheet (or a single large sheet) listing, for each division, the subject, faculty, room, and time slot for each day. Faculty availability is tracked informally, often from memory or from separate notes, and conflicts are found only when someone happens to notice two rows that reference the same faculty, room, or division at the same day and time.

**3.3 Limitations of Existing System**

* No automated verification that a newly added entry does not conflict with an existing entry.
* Faculty availability and workload are not tracked systematically, making it hard to know at a glance who is free at a given time.
* No historical record of which clashes occurred and how (or whether) they were resolved.
* No predictive insight into which of several candidate slots or faculty is least likely to cause a future conflict.
* No automated resolution suggestions when clashes are detected – the administrator must manually investigate alternatives.
* Visiting faculty availability is tracked informally with no per-day, per-slot granularity.
* Room inventory (capacity, type) is not systematically maintained.
* Difficult to maintain consistency across many divisions and branches as their number grows.
* No ability to search across all entities or export timetables in structured formats.

**3.4 Proposed System Requirements**

The proposed system requirements were derived directly from the limitations identified above and are grouped, in the sections that follow, into functional requirements (what the system must do) and non-functional requirements (the qualities the system must exhibit while doing it).

**3.5 Functional Requirements**

Table 3.1. Functional Requirements

| **ID** | **Requirement** | **Description** |
| --- | --- | --- |
| FR-1 | User Registration & Login | The system shall allow users to sign up and log in as either an Administrator or a Faculty member, with passwords stored using secure hashing. |
| FR-2 | Branch Management | The Administrator shall be able to create, edit, and manage academic branches (e.g., CSE, ICT, ECE) with search/filter capability. |
| FR-3 | Division Management | The Administrator shall be able to create, edit, and delete divisions/sections within a branch, each tied to a semester and academic year, with branch filter and search capability. |
| FR-4 | Subject Management | The Administrator shall be able to add, edit, and delete subjects with a name, unique code, and credit value, with search/filter capability. |
| FR-5 | Time Slot Management | The Administrator shall be able to define, edit, and delete time slots with start and end times and an optional label. |
| FR-6 | Room & Resource Management | The Administrator shall be able to add, edit, and delete rooms/resources with name, capacity, and type (Classroom, Lab, Seminar Hall), with search/filter capability. |
| FR-7 | Faculty Profile Management | Faculty members shall be able to set their working hours, the list of subjects they can teach, and their visiting faculty status with day-wise time slot availability. |
| FR-8 | Interactive Timetable Creation | The Administrator shall be able to create timetable entries through a side-by-side interface showing time slots and faculty availability. |
| FR-9 | Faculty Clash Detection | The system shall prevent a faculty member from being assigned to two entries at the same day and time slot, checked globally. |
| FR-10 | Room Clash Detection | The system shall prevent a room from being assigned to two entries at the same day and time slot. |
| FR-11 | Division Clash Detection | The system shall prevent a division from being assigned two entries at the same day and time slot. |
| FR-12 | Clash Logging with Resolution Tracking | Detected clashes shall be recorded in a clash\_logs table with type, severity, resolution status, resolved\_by user, resolution\_method (manual/auto), and resolution\_note. |
| FR-13 | Admin Dashboard | The system shall present a dashboard listing all divisions with clash indicators, entry counts, and room counts. |
| FR-14 | Faculty Schedule View | Faculty members shall be able to view their personal teaching schedule organised by day. |
| FR-15 | Final Timetable View | The system shall provide a consolidated, print-friendly view of created timetables across branches. |
| FR-16 | Global Search | The system shall provide full-text search across faculty, subjects, divisions, branches, rooms, and clashes, with a dedicated search results page. |
| FR-17 | Clash Risk Prediction | The system shall predict a clash-risk score (0–1) for a proposed entry using the trained ML model. |
| FR-18 | Slot Recommendation | The system shall recommend up to five alternative time slots ranked by predicted clash risk. |
| FR-19 | Faculty Recommendation | The system shall recommend up to five faculty candidates for a subject, scored by expertise and availability. |
| FR-20 | Timetable Quality Evaluation | The system shall evaluate a division's overall timetable and report a quality score with issues and recommendations. |
| FR-21 | Model Training Endpoint | The system shall provide an endpoint to (re-)train the ML model on the latest data in the database. |
| FR-22 | Intelligent Clash Resolution Suggestions | The system shall generate ML-powered resolution suggestions for detected clashes, including alternative rooms, faculty, and time slots with risk scoring. |
| FR-23 | Auto-Resolve Capability | The system shall allow one-click application of ML-generated resolution suggestions to automatically resolve detected clashes. |
| FR-24 | CSV/ZIP Timetable Export | The system shall provide CSV export for individual division timetables, faculty personal timetables, and bulk ZIP export for all division timetables. |
| FR-25 | Visiting Faculty Day-Wise Scheduling | The system shall support per-day, per-time-slot availability configuration for visiting faculty, with a visual toggle and day/slot selector in the faculty profile. |

**3.6 Non-Functional Requirements**

Table 3.2. Non-Functional Requirements

| **ID** | **Category** | **Requirement** |
| --- | --- | --- |
| NFR-1 | Security | Passwords shall be stored using Werkzeug's secure password hashing; sessions shall be managed by Flask's secure session handling. |
| NFR-2 | Authorization | Role-based decorators shall restrict access to admin-only and faculty-only routes and API endpoints. |
| NFR-3 | Data Integrity | SQLAlchemy ORM with parameterized queries shall be used to prevent SQL injection. |
| NFR-4 | Usability | The interface shall use a modern, responsive layout with glassmorphism design that works on desktop, tablet, and mobile. Search/filter shall be available on all management listing pages. |
| NFR-5 | Performance | Clash-risk prediction shall complete with low latency suitable for interactive use during timetable creation. |
| NFR-6 | Maintainability | The codebase shall be modularised into models, services (e.g., clash\_service.py), and templates for separation of concerns. |
| NFR-7 | Portability | The application shall be deployable via a standard WSGI server (e.g., Gunicorn) behind a reverse proxy (e.g., Nginx). |
| NFR-8 | Auditability | Every detected clash shall be logged with a timestamp, resolution tracking (who, how, notes), for later review. |
| NFR-9 | Resilience | The application shall automatically fall back to a local SQLite database if the primary MySQL connection fails, ensuring continued operation. |

**3.7 Hardware Requirements**

Table 3.3. Hardware Requirements

| **Component** | **Minimum Requirement (Development)** | **Recommended (Server / Deployment)** |
| --- | --- | --- |
| Processor | Dual-core, 1.6 GHz or higher | Quad-core, 2.5 GHz or higher |
| RAM | 4 GB | 8 GB or more |
| Storage | 5 GB free space | 20 GB+ (SSD preferred, scales with data) |
| Network | Broadband internet connection | Stable connection with a public-facing reverse proxy |

**3.8 Software Requirements**

Table 3.4. Software Requirements

| **Layer** | **Technology** |
| --- | --- |
| Programming Language | Python 3.8 or higher |
| Web Framework | Flask |
| ORM | Flask-SQLAlchemy |
| Database | MySQL 5.7 or higher (with automatic SQLite fallback) |
| Database Driver | PyMySQL |
| Security Libraries | Werkzeug (password hashing), cryptography |
| Authentication | Flask-Login (session-based, role-based) |
| Machine Learning | scikit-learn 1.3.2, numpy 1.24.3, pandas 2.0.3, joblib 1.3.1 |
| Frontend | HTML5, CSS3, JavaScript, Font Awesome icons |
| Production Server | Gunicorn (WSGI), Nginx (reverse proxy, optional SSL) |
| Operating System | Cross-platform (Windows / macOS / Linux) |

**3.9 Feasibility Study**

### 3.9.1 Technical Feasibility

All technologies used in the project – Flask, Flask-SQLAlchemy, MySQL, PyMySQL, Werkzeug, and scikit-learn – are mature, well-documented, open-source components with active community support, and are known to integrate well with one another in a typical Flask application layout (application factory/app.py, models.py, extensions.py, services/, templates/). The automatic SQLite fallback further ensures the system can operate without external database dependencies during development or in degraded environments. The project is therefore technically feasible using standard, freely available tools.

### 3.9.2 Economic Feasibility

Every component of the technology stack – Python, Flask, MySQL, SQLite, and the scikit-learn ecosystem – is open-source and free to use, and the application can be self-hosted or deployed to low-cost or free-tier hosting. This keeps the direct software cost of adopting the system close to zero, with the main cost being the effort of deployment and maintenance.

### 3.9.3 Operational Feasibility

The system is operated through a standard web browser, requires no specialised client software, and mirrors the same conceptual workflow (branches → divisions → subjects → time slots → rooms → timetable) that administrative staff already follow manually, which keeps the learning curve manageable for non-technical administrative users.

**3.10 User Roles**

Table 3.5. User Roles

| **Role** | **Description** | **Key Permissions** |
| --- | --- | --- |
| Administrator | Manages the institution-wide academic setup and builds timetables. | Create/manage branches, divisions, subjects, time slots, rooms, faculty; create/edit/delete timetable entries; view dashboard and clash logs; use global search; export timetables as CSV/ZIP; resolve clashes manually or via auto-resolve; access ML prediction, recommendation, and clash-suggestion endpoints. |
| Faculty | Teaching staff who need to see and maintain their own teaching information. | Complete/update personal profile (working hours, subjects taught, visiting schedule); view personal schedule organised by day; download personal timetable as CSV. |

**3.11 Requirement Traceability Matrix**

Table 3.6. Requirement Traceability Matrix

| **Requirement ID** | **Traced To Module** | **Verified By** |
| --- | --- | --- |
| FR-1 | Authentication Module | Login/Signup test cases |
| FR-2 – FR-6 | Branch / Division / Subject / Time-Slot / Room Management Modules | Management screen test cases |
| FR-7 | Faculty Management Module | Faculty profile test cases (including visiting schedule) |
| FR-8 | Timetable Generation Module | Timetable creation test cases |
| FR-9 – FR-12 | Clash Detection Module | Clash detection test cases |
| FR-13 – FR-15 | Reports Module / Dashboard | UI walkthrough and search test cases |
| FR-16 | Global Search Module | Global search test cases |
| FR-17 – FR-21 | ML Clash Prediction Module | ML endpoint test cases (Chapter 8) |
| FR-22 – FR-23 | Intelligent Clash Resolution Module | Clash suggestion and auto-resolve test cases |
| FR-24 | Export Module | CSV/ZIP download test cases |
| FR-25 | Faculty Management Module | Visiting faculty scheduling test cases |

---

**Chapter 4: System Analysis And Design**

**4.1 System Architecture**

The system follows a layered, monolithic web-application architecture typical of Flask projects. The Presentation Layer consists of server-rendered HTML templates (in the templates/ directory) styled with CSS and enhanced with JavaScript for interactivity (e.g., the ML risk badges, recommendation panel, and AI resolution suggestion panel). The Application Layer consists of the Flask route handlers defined in app.py, which coordinate requests, enforce authentication/authorization, and call into the Service Layer. The Service Layer consists of dedicated service modules under services/ – principally clash\_service.py, which implements the faculty/room/division clash checks, wraps the ML prediction functions, and provides the intelligent resolution suggestion generation and auto-resolve logic, and ml\_clash\_predictor.py, which implements the Random Forest based clash-risk engine. The Data Layer consists of the SQLAlchemy models defined in models.py (User, Faculty, Branch, Division, TimeSlot, Subject, Room, Timetable, ClashLog), mapped onto a MySQL database (with automatic SQLite fallback). The trained machine-learning model itself is persisted to disk under ml\_models/clash\_predictor\_model.pkl using joblib, and is loaded by the ML engine at prediction time.

*(Insert Figure 4.1 – System Architecture Diagram – should now include Room entity, Intelligent Resolution component, Global Search, and Export module)*

Fig 4.1 System Architecture Diagram

**4.2 Overall Workflow**

At a high level, the Administrator signs up or logs in, sets up the foundational data (branches, divisions, subjects, time slots, rooms), then creates a timetable for a chosen branch/division/day by, for each time slot, selecting a subject, viewing faculty availability, selecting an available faculty member, choosing a room, and submitting the entry – which the system validates for clashes before adding it. When a clash is detected, the administrator can view AI-powered resolution suggestions and auto-apply any suggestion with a single click. In parallel, Faculty members sign up, complete their profile (working hours, subjects they can teach, and visiting schedule if applicable), and view their personal schedule, which is derived automatically from the timetable entries that reference them. Both administrators and faculty can export timetables as CSV files, and administrators can perform global search across all entities.

*(Insert Figure 4.2 – Overall Workflow Diagram – should now include resolution suggestion and export steps)*

Fig 4.2: Overall Workflow Diagram

**4.3 Module Identification**

Table 4.1. Module Identification

| **Module** | **Responsibility** |
| --- | --- |
| Authentication Module | Sign-up, login, logout, session management, password hashing/verification. |
| Faculty Management Module | Faculty profile creation and update; working hours, taught-subjects, and visiting schedule storage; visiting faculty day-wise time-slot configuration. |
| Room & Resource Management Module | Create, edit, delete, and search/filter rooms/resources with name, capacity, and type (Classroom, Lab, Seminar Hall). |
| Subject Management Module | Create, edit, delete, and search/filter subjects with code and credits. |
| Timetable Generation Module | Interactive side-by-side timetable creation screen and entry CRUD; room selection from Room inventory. |
| Clash Detection Module | Faculty, room, and division clash checks; clash logging with full resolution tracking. |
| ML Clash Prediction Module | Random Forest based clash-risk prediction, slot & faculty recommendation, quality evaluation. |
| Intelligent Clash Resolution Module | ML-powered resolution suggestion generation for detected clashes; alternative rooms, faculty, and time slots; one-click auto-resolve. |
| Global Search Module | Full-text search across faculty, subjects, divisions, branches, rooms, and clashes with dedicated search results page. |
| Reports & Export Module | Admin dashboard, final timetable view, view-clashes screen with AI suggestions, CSV/ZIP timetable export for administrators and faculty. |

**4.4 Authentication Module**

The Authentication Module is built around the User SQLAlchemy model, which stores a username, email, a hashed password (never the plaintext password), a full name, and a role field distinguishing 'admin' from 'faculty'. Password hashing and verification use Werkzeug's generate\_password\_hash and check\_password\_hash functions, wrapped by the set\_password and check\_password methods on the User model. The User model also mixes in Flask-Login's UserMixin, allowing session-based login state to be tracked by Flask-Login. On successful signup, a Faculty role account additionally creates a linked Faculty profile row (a one-to-one relationship, cascade-deleted with the user). The system also auto-seeds a default admin user ('admin' / 'admin123') during initialisation if none exists.

*(Insert Figure 4.3 – Login and Sign up Page screenshot)*

Fig 4.3: Login and Sign up Page

**4.5 Faculty Management Module**

The Faculty model stores a foreign key to the owning User, along with phone, department, and designation fields, and two JSON-encoded text fields: working\_hours (a JSON object with start and end keys, e.g., {"start": "09:00", "end": "17:00"}) and subjects\_can\_teach (a JSON array of subject names). Helper methods (set\_subjects/get\_subjects and set\_working\_hours/get\_working\_hours) serialise and deserialise these fields, and an is\_available boolean flag marks whether the faculty member is currently accepting new assignments. The Faculty model exposes a timetable\_entries relationship, giving direct access to every Timetable row that references that faculty member.

The Faculty model additionally supports **visiting faculty** through three dedicated fields: is\_visiting (Boolean), visiting\_available\_days (JSON array of day names), and visiting\_slot\_ids (JSON dictionary mapping each day to a list of time-slot IDs). Helper methods include set\_visiting\_days/get\_visiting\_days, set\_visiting\_slots/get\_visiting\_slots (with legacy list fallback), get\_visiting\_schedule (returning a day→slot-IDs dictionary), and is\_available\_for\_slot(day, time\_slot), which automatically distinguishes between regular and visiting faculty to determine availability. The Faculty Profile UI presents a custom toggle switch for marking visiting status, a day-checkbox grid for selecting available days, and per-day time-slot chip selectors for granular availability control.

*(Insert Figure 4.4 – Faculty Profile (Regular Faculty) screenshot)*

Fig 4.4: Faculty Profile (Regular Faculty)

*(Insert Figure 4.5 – Faculty Profile (Visiting Faculty – Day-wise Scheduling) screenshot)*

Fig 4.5: Faculty Profile (Visiting Faculty – Day-wise Scheduling)

**4.6 Room & Resource Management Module**

The Room model is a first-class entity in the database schema, storing a unique name (e.g., "101", "Lab-A"), a capacity (integer, default 60), a room\_type ('Classroom', 'Lab', or 'Seminar Hall'), created\_by (admin user ID), and created\_at. The Manage Rooms screen allows the Administrator to add, edit, and delete rooms/resources through a structured form, with search/filter capability for finding rooms by name or type. An edit modal supports inline editing of room attributes. The Room Clash check in the Clash Detection Module uses this Room data to verify that a room is not double-booked.

*(Insert Figure 4.9 – Manage Rooms & Resources screenshot)*

Fig 4.9: Manage Rooms & Resources

**4.7 Subject Management Module**

The Subject model stores a name, a unique code, a credits integer (defaulting to 3), and the id of the admin user who created it. Subjects are referenced by Timetable entries via subject\_id, and by Faculty profiles indirectly through the subjects\_can\_teach JSON list (matched by subject name), which the ML faculty-recommendation feature uses to score expertise. The Manage Subjects screen supports search/filter by subject name or code.

*(Insert Figure 4.8 – Manage Subjects screenshot)*

Fig 4.8: Manage Subjects

**4.8 Timetable Generation Module**

The Timetable model is the core entity of the system: each row references a division\_id, subject\_id, faculty\_id, and time\_slot\_id (all foreign keys), together with a day string (Monday through Saturday) and a room\_number. The timetable-creation screen presents, for a selected branch/division/day, the configured time slots on the left with entry-creation forms and existing entries with edit/delete options, and a live faculty-availability panel on the right showing each faculty member's busy/available status and the subjects they teach for the currently selected slot. The ML recommendations panel auto-appears on subject selection, showing recommended faculty (with TOP PICK, EXPERT tags and scores) and best time slots (with BEST tags and risk percentages).

*(Insert Figure 4.10 – Timetable Creation (Side-by-Side) Interface screenshot)*

Fig 4.10: Timetable Creation (Side-by-Side) Interface

**4.9 Clash Detection Module**

The Clash Detection Module, implemented in services/clash\_service.py, performs three checks whenever an entry is proposed: a Faculty Clash check, querying for any existing Timetable row with the same faculty\_id, day, and time\_slot\_id, scoped globally across all branches and divisions; a Room Clash check, querying for any existing row with the same room\_number, day, and time\_slot\_id; and a Division Clash check, querying for any existing row with the same division\_id, day, and time\_slot\_id. When a clash is found, a ClashLog row is created, recording the clash\_type ('faculty', 'room', or 'division'), a severity ('warning' or 'error'), a JSON clash\_details payload, references to the relevant division\_id/faculty\_id, and resolution tracking fields (is\_resolved, resolved\_at, resolved\_by, resolution\_method, resolution\_note), and the entry submission is rejected with an explanatory message to the Administrator.

**4.10 Intelligent Clash Resolution Module**

The Intelligent Clash Resolution Module, also implemented in services/clash\_service.py (via generate\_resolution\_suggestions and apply\_suggestion methods), extends the clash detection system with ML-powered resolution capabilities. When a clash is detected and displayed in the View Clashes screen, the administrator can click "Get AI Suggestions" to invoke the resolution engine, which generates context-aware suggestions based on the clash type:

* **Room Clash**: suggests alternative rooms that are available at the same day/time (prioritising free rooms from the Room inventory, with ML-predicted risk scores), alternative time slots (using the ML slot recommender), and alternative faculty members (using the ML faculty recommender).
* **Faculty Clash**: suggests alternative available faculty (scored by subject expertise and availability via ML), alternative time slots for the conflicting entry, and alternative rooms.
* **Division Clash**: suggests alternative time slots for the division entry and alternative rooms.

Each suggestion includes a description, detail text, risk score, risk level (low/medium/high colour-coded), and a one-click "Apply" button that triggers auto-resolve. The apply\_suggestion method handles three action types: change\_room (updates the Timetable entry's room\_number), change\_faculty (updates the faculty\_id), and change\_timeslot (updates the time\_slot\_id and day). After auto-resolve, the ClashLog is marked resolved with resolution\_method='auto' and an appropriate resolution\_note.

**4.11 Reports & Export Module**

The Reports & Export Module comprises the Admin Dashboard (listing all divisions with green/red clash indicators, entry counts, room counts, and quick links), the Final Timetable View (a consolidated, print-friendly view of created timetables across branches), the View Clashes screen (a listing of ClashLog entries with tabs for active/resolved clashes, filter bar, statistics cards, and AI suggestion panels), and CSV/ZIP export (individual division CSV download, bulk all-divisions ZIP download, and faculty personal timetable CSV download).

**4.12 Global Search Module**

The Global Search Module provides a full-text search across six entity types: faculty (by name, email, department, designation), subjects (by name, code), divisions (by name, branch, academic year), branches (by name, short name), rooms (by room number), and clashes (by type, severity, or detail text). Search results are displayed on a dedicated search\_results.html page with category-wise grouping and total result count.

*(Insert Figure 5.5 – Global Search Results Page screenshot)*

Fig 5.5: Global Search Results Page

**4.13 Use Case Diagram**

*(Insert updated Use Case Diagram – should now include Room Management, Global Search, CSV Export, AI Resolution Suggestions, Auto-Resolve, and Visiting Faculty Scheduling use cases)*

Fig 4.11: Use Case Diagram

**4.14 Activity Diagram**

*(Insert updated Activity Diagram – should now include AI resolution suggestion step after clash detection)*

Fig 4.12: Activity Diagram – Timetable Creation

**4.15 Sequence Diagram**

*(Insert updated Sequence Diagram – should now include clash resolution suggestion generation and auto-resolve interaction)*

Fig 4.13: Sequence Diagram – Clash Detection and Resolution

**4.16 Class Diagram**

*(Insert updated Class Diagram – should now include Room class, visiting faculty fields on Faculty, resolution tracking fields on ClashLog)*

Fig 4.14: Class Diagram

**4.17 ER Diagram**

*(Insert updated ER Diagram – should now include rooms table and its relationships)*

Fig 4.15: Entity Relationship (ER) Diagram

**4.18 Component Diagram**

*(Insert updated Component Diagram – should now include Intelligent Resolution Component, Global Search Component, and Export Component)*

Figure 4.16. Component Diagram

**4.19 Deployment Diagram**

*(Insert Deployment Diagram)*

Figure 4.17. Deployment Diagram

**4.20 DFD Level 0**

*(Insert updated DFD Level 0)*

Figure 4.18. Data Flow Diagram – Level 0

**4.21 DFD Level 1**

*(Insert updated DFD Level 1 – should now include Room Management, Global Search, Export, and Clash Resolution flows)*

Figure 4.19. Data Flow Diagram – Level 1

**4.22 DFD Level 2**

*(Insert updated DFD Level 2)*

Figure 4.20. Data Flow Diagram – Level 2

---

**Chapter 5: System Implementation**

**5.1 Introduction**

This chapter documents how the system described in Chapter 4 was implemented, covering the project's folder structure, the frontend templates, the Flask backend, the MySQL database setup (with SQLite fallback), authentication, the dashboard, the timetable-generation screens, clash detection, intelligent clash resolution, global search, CSV/ZIP export, room management, visiting faculty scheduling, report generation, and deployment.

**5.2 Project Structure**

The repository is organised as a standard Flask project. At the root, app.py is the main Flask application containing the route handlers (~1,676 lines); config.py holds configuration; extensions.py defines the shared SQLAlchemy db instance used by models.py to avoid circular imports; models.py defines all database models (User, Faculty, Branch, Division, TimeSlot, Subject, Room, Timetable, ClashLog – ~320 lines); create\_db.py and init\_db.py initialise the database schema; create\_test\_data.py seeds sample/test data; requirements.txt lists Python dependencies; run.py is the application entry point; and setup.sh automates environment setup. A services/ directory contains clash\_service.py (clash detection, intelligent resolution, and ML wrapper methods – ~1,118 lines) and ml\_clash\_predictor.py (the ML engine – ~510 lines). A templates/ directory holds 22 HTML views. An ml\_models/ directory stores the persisted, trained Random Forest model file. Several top-level test\_ml\_\*.py and validate\_ml\_system.py scripts were used to validate the ML integration during development.

Table 5.1. Project Structure

| **Path** | **Purpose** |
| --- | --- |
| app.py | Main Flask application (~1,676 lines); route handlers, including admin-only and faculty-only views, global search, CSV/ZIP export, room management, and the ML/resolution API endpoints. |
| models.py | SQLAlchemy models: User, Faculty, Branch, Division, TimeSlot, Subject, Room, Timetable, ClashLog (~320 lines). |
| extensions.py | Shared SQLAlchemy db object, imported by both app.py and models.py. |
| config.py | Application configuration, including the SQLALCHEMY\_DATABASE\_URI connection string. |
| create\_db.py / init\_db.py | Scripts to create the database schema from the SQLAlchemy models. |
| create\_test\_data.py | Generates sample/test timetable data used, among other things, to train the ML model. |
| services/clash\_service.py | Faculty/room/division clash-checking logic, intelligent resolution suggestion generation, auto-resolve logic, and ML wrapper methods (~1,118 lines). |
| services/ml\_clash\_predictor.py | Random Forest based clash-risk engine (~510 lines): prediction, recommendation, evaluation, training. |
| templates/\*.html | 22 server-rendered views: base, signup, login, admin\_dashboard, faculty\_dashboard, faculty\_profile, manage\_branches, manage\_divisions, manage\_subjects, manage\_timeslots, manage\_rooms, manage\_faculty, timetable\_select, timetable\_create, view\_timetable, edit\_timetable\_entry, edit\_timeslot, final\_timetable\_view, view\_clashes, search\_results, 404, 500. |
| ml\_models/clash\_predictor\_model.pkl | Persisted, trained Random Forest model (joblib format, ~92 KB). |
| requirements.txt | Python dependencies, including Flask, Flask-SQLAlchemy, PyMySQL, scikit-learn, numpy, pandas, joblib. |
| run.py | Application entry point. |
| setup.sh | Shell script automating environment/dependency setup. |

**5.3 Frontend Implementation**

The frontend is implemented as server-rendered HTML templates using a shared base.html layout (~24 KB), styled with CSS to give a modern gradient (purple/blue/teal) glassmorphism design, and using Font Awesome icons throughout. The interface is responsive and intended to work across desktop, tablet, and mobile screen sizes. Interactive behaviour – such as fetching and displaying ML risk predictions, recommendations, and AI resolution suggestions without a full page reload – is implemented in JavaScript using the Fetch API against the JSON endpoints exposed by app.py. Colour coding is used consistently across the interface: green for success/available/no-clash states, red for error/busy/clash states, purple/teal gradients for AI/ML features, and blue for informational elements. The timetable view is additionally styled to be print-friendly. All management listing pages (branches, divisions, subjects, rooms, faculty) include search/filter bars for rapid filtering.

**5.4 Backend Implementation**

The backend is implemented in app.py using Flask's routing decorators. Distinct route groups exist for: authentication (signup/login/logout), Administrator management screens (branches, divisions, subjects, time slots, rooms, faculty), the timetable-creation workflow (select branch/division/day, create/edit/delete entries), the Faculty portal (profile with visiting schedule, personal schedule, CSV download), the reporting views (dashboard, final timetable view, view clashes with AI suggestions), the global search route, the CSV/ZIP export routes, the three clash-resolution endpoints (view clashes, get AI suggestions, auto-resolve), and the six ML API endpoints. Administrator-only and Faculty-only routes are protected by role-checking decorators that inspect the logged-in user's role attribute before allowing access, returning an authorization error otherwise. In addition to the page routes, multiple lightweight JSON API endpoints are exposed for AJAX use: GET /api/divisions/\<branch\_id\>, GET /api/faculty-availability, GET /api/faculty-matrix, GET /api/subjects/search, GET /api/ml/clash-suggestions/\<clash\_id\>, and the six ML API endpoints.

**5.5 Database Implementation**

The database is primarily implemented in MySQL, created with the command CREATE DATABASE timetable\_system CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci, and connected to from Flask via the SQLALCHEMY\_DATABASE\_URI configuration string of the form mysql+pymysql://\<user\>:\<password\>@localhost/timetable\_system. If the primary MySQL connection fails at startup, the application automatically falls back to a local SQLite database (sqlite:///timetable\_system.db), ensuring continued operation in degraded environments. Tables are created from the SQLAlchemy model definitions in models.py by calling db.create\_all(). An auto-migration block at startup attempts to add any missing columns (visiting faculty fields, resolution tracking fields) to existing tables, ensuring backward compatibility with older database schemas. Chapter 7 documents each table's schema in detail.

**5.6 Authentication Implementation**

On sign-up, a new User row is created with the chosen role ('admin' or 'faculty'); the plaintext password is never stored – instead, User.set\_password() calls Werkzeug's generate\_password\_hash() and stores only the resulting hash in password\_hash. On login, User.check\_password() calls check\_password\_hash() to verify the submitted password against the stored hash. Successful login establishes a Flask-Login session (User mixes in UserMixin), and last\_login is updated on the User row. Signing up as Faculty additionally creates the linked Faculty profile row via the one-to-one relationship defined on the User model. A default admin user ('admin' / 'admin123') is automatically seeded during initialisation if none exists.

**5.7 Dashboard Implementation**

The Admin Dashboard queries all Division rows (each carrying its parent Branch via the branch relationship) together with their associated Timetable entries and any related ClashLog rows, and renders each division with a green indicator if it has no unresolved clashes or a red indicator if it does, alongside the count of timetable entries for that division and quick-navigation links to view, edit, or continue building that division's timetable. The dashboard also displays total counts for branches, divisions, faculty, subjects, and rooms, and shows a list of recent unresolved clashes.

*(Insert Figure 5.1 – Admin Dashboard screenshot)*

Fig 5.1. Admin Dashboard

*(Insert Figure 5.2 – Faculty Dashboard screenshot)*

Fig 5.2. Faculty Dashboard

**5.8 Timetable Generation Implementation**

The timetable\_select.html screen lets the Administrator choose a Branch, Division, and Day. The timetable\_create.html screen then lists the configured TimeSlot rows for that day; for each slot, existing Timetable entries are shown with Edit/Delete actions (backed by edit\_timetable\_entry.html and a delete route), and a form is provided to add a new entry (subject dropdown, faculty dropdown populated from the faculty-availability API, room selection, and ML recommendations). The faculty-availability panel on the right of the screen calls the GET /api/faculty-availability endpoint to show, for the currently selected slot, each faculty member's availability status and the subjects they teach, so the administrator can identify a suitable, free faculty member before submitting the entry. The ML recommendations panel auto-loads when a subject is selected, showing recommended faculty with scoring and recommended time slots with clash risk percentages.

*(Insert Figure 5.3 – Faculty Availability Panel screenshot)*

Fig 5.3. Faculty Availability Panel

**5.9 Clash Detection Implementation**

When the Administrator submits a new (or edited) Timetable entry, app.py calls into services/clash\_service.py before committing the row. The Faculty Clash check runs a query equivalent to: does a Timetable row already exist with this faculty\_id, this day, and this time\_slot\_id, anywhere in the system (i.e., not filtered by branch or division)? The Room Clash check runs an analogous query filtered by room\_number, day, and time\_slot\_id. The Division Clash check runs an analogous query filtered by division\_id, day, and time\_slot\_id. If any check returns an existing conflicting row, a new ClashLog entry is created (clash\_type set to 'faculty', 'room', or 'division'; clash\_details populated via set\_details() with a JSON payload describing the conflicting entries; is\_resolved left False; resolution tracking fields initialised), and the entry submission is rejected with an explanatory message to the Administrator; otherwise the new Timetable row is committed.

**5.10 Intelligent Clash Resolution Implementation**

The Intelligent Clash Resolution is implemented as two API endpoints and a dedicated UI panel in view\_clashes.html:

1. **GET /api/ml/clash-suggestions/\<clash\_id\>** – Calls ClashService.generate\_resolution\_suggestions(clash\_id), which analyses the clash type and details, finds the matching time slot, and generates context-aware suggestions:
   - For room clashes: alternative free rooms (from Room inventory with ML risk scores), time slot shifts (via ML alternative slot recommender), and faculty swaps (via ML faculty recommender).
   - For faculty clashes: alternative faculty (ML-scored by expertise and availability), time slot shifts, and room alternatives.
   - For division clashes: time slot alternatives and room changes.

2. **POST /admin/clashes/auto-resolve/\<clash\_id\>** – Receives action\_type (change\_room, change\_faculty, change\_timeslot) and action\_value, calls ClashService.apply\_suggestion(), which applies the change to the conflicting Timetable entry and marks the ClashLog as resolved with resolution\_method='auto' and a descriptive resolution\_note.

The view\_clashes.html UI displays suggestions in a glassmorphism-styled AI panel with animated slide-down entrance, colour-coded risk badges (green=low, orange=medium, red=high), and one-click "Apply" buttons for each suggestion. A loading spinner is shown while suggestions are being generated.

*(Insert Figure 5.4 – View Clashes Screen with AI Resolution Suggestions screenshot)*

Fig 5.4. View Clashes Screen with AI Resolution Suggestions

**5.11 Global Search Implementation**

The global search is implemented via the /search route, which accepts a query parameter q and searches across six entity types using SQLAlchemy ilike filters: Faculty (by full\_name, email, department, designation), Subjects (by name, code), Divisions (by name, branch name, branch short\_name, academic\_year), Branches (by name, short\_name), Rooms (by room\_number from timetable entries), and Clashes (by clash\_type, severity, clash\_details). Results are rendered on search\_results.html with category-wise grouping, entity counts per category, and a total result count. The global search is accessible from the navigation bar.

*(Insert Figure 5.5 – Global Search Results Page screenshot)*

Fig 5.5. Global Search Results Page

**5.12 CSV/ZIP Export Implementation**

Three export endpoints are implemented:

1. **GET /admin/timetable/export** – Exports all divisions that have timetable entries as a ZIP file containing one CSV per division. Each CSV has a grid format (Time rows × Day columns).
2. **GET /timetable/download/\<division\_id\>** – Exports a single division's timetable as a CSV file with the grid format.
3. **GET /faculty/timetable/download** – Exports the logged-in faculty member's personal timetable as a CSV file.

*(Insert Figure 5.7 – CSV Export – Sample Downloaded File screenshot)*

Fig 5.7. CSV Export – Sample Downloaded File

**5.13 Report Generation**

The Final Timetable View aggregates Timetable entries across all branches and divisions into a single, print-optimised view, primarily intended for distribution or posting. The View Clashes screen lists ClashLog rows with tabbed views (Active Clashes and Resolved Clashes), a filter bar for filtering by clash type or searching by details, statistics cards showing total/resolved/pending counts, and the AI-powered suggestion panels described in 5.10.

*(Insert Figure 5.6 – Final Timetable View screenshot)*

Fig 5.6. Final Timetable View

**5.14 Deployment**

For production deployment, the README documents changing the Flask SECRET\_KEY away from its development value, disabling debug mode (app.run(debug=False)), pointing SQLALCHEMY\_DATABASE\_URI at a production MySQL server, running the application under Gunicorn (pip install gunicorn; gunicorn app:app) instead of the Flask development server, and placing Nginx in front of Gunicorn as a reverse proxy with an SSL certificate configured for the institution's domain. The application supports PostgreSQL URL format conversion (postgres:// → postgresql://) and Aiven MySQL SSL mode handling for cloud database providers. The project's repository also lists a live deployment at [timetable-clash-resolution.onrender.com](https://timetable-clash-resolution.onrender.com)

---

**Chapter 6: Timetable Generation And Clash Resolution**

**6.1 Introduction**

This chapter examines, in detail, how the system builds a timetable entry by entry and how it detects, prevents, and resolves clashes, covering the deterministic Clash Detection Service, the Intelligent Clash Prevention and Recommendation module (machine-learning based), and the Intelligent Clash Resolution Suggestions and Auto-Resolve module.

**6.2 Timetable Scheduling Problem**

Formally, the system must assign, for each division and each day, a subject, a faculty member, a room, and a time slot such that: (a) no faculty member is assigned to two different (division, time-slot) pairs on the same day, (b) no room is assigned to two different (division, time-slot) pairs on the same day, and (c) no division is assigned two different (subject, time-slot) pairs on the same day. The current implementation solves this incrementally and interactively: rather than generating a full timetable at once, it validates each proposed entry against all previously accepted entries at the moment it is submitted.

**6.3 Scheduling Constraints**

**6.3.1 Hard Constraints**

* Faculty Constraint: a faculty member cannot be scheduled for two entries with the same day and time\_slot\_id, checked globally across all branches and divisions.
* Room Constraint: a room\_number cannot be scheduled for two entries with the same day and time\_slot\_id.
* Division Constraint: a division\_id cannot be scheduled for two entries with the same day and time\_slot\_id.
* Visiting Faculty Availability Constraint: a visiting faculty member can only be scheduled on days and time slots configured in their visiting schedule (enforced via is\_available\_for\_slot).

**6.3.2 Soft Constraints**

The system's machine-learning module addresses several considerations that are not enforced as hard rules but that materially affect timetable quality: preferring faculty with higher subject expertise and higher availability (used by the faculty-recommendation feature), preferring time slots with a lower predicted clash-risk score (used by the slot-recommendation feature), and suggesting lower-risk alternatives when clashes are detected (used by the resolution-suggestion feature). These soft preferences are surfaced to the Administrator as advisory scores and recommendations rather than being auto-applied, so the final scheduling decision remains with the human administrator.

**6.4 Faculty Allocation**

Faculty allocation begins with the Faculty profile: each Faculty row stores subjects\_can\_teach (a JSON list of subject names), working\_hours (a JSON object with start and end times), and visiting faculty fields (is\_visiting, visiting\_available\_days, visiting\_slot\_ids). When the Administrator is populating a time slot, the faculty-availability panel filters and marks faculty members according to whether they teach the selected subject, whether the slot falls within their configured working hours (or visiting schedule), and whether they already have a conflicting entry – before the Administrator makes the final selection.

**6.5 Visiting Faculty Scheduling**

Visiting faculty availability is managed at a per-day, per-time-slot granularity. The Faculty model stores visiting schedule data as a JSON dictionary mapping each day name to a list of time-slot IDs (e.g., {"Monday": [1, 2], "Wednesday": [3, 4]}). The is\_available\_for\_slot(day, time\_slot) method checks: (1) if the faculty is visiting, verify the day is in their visiting\_available\_days and the time\_slot.id is in their slot list for that day; (2) if the faculty is regular, verify the time slot falls within their configured working hours. This ensures visiting faculty are only scheduled during their explicitly configured availability windows, preventing scheduling conflicts for part-time staff.

**6.6 Classroom Allocation**

Classroom (room) allocation is now supported by the Room entity in the database, which tracks room name, capacity, and type (Classroom, Lab, Seminar Hall). When creating a timetable entry, the administrator can select from the Room inventory. The Room Clash rule checks that no two entries share the same room at the same day and time slot.

**6.7 Laboratory Allocation**

Laboratory sessions are represented as rooms with room\_type='Lab' in the Room entity, subject to the same Room Clash rule as classrooms. The Room & Resource Management module allows administrators to distinguish labs from classrooms, though laboratory-specific constraints (such as minimum session duration) are not yet enforced at the application level.

**6.8 Subject Allocation**

Subjects are allocated to a Timetable entry by selecting from the Subject table (name, code, credits). The subject selection also drives the Faculty Recommendation feature, which cross-references the chosen subject against each candidate faculty member's subjects\_can\_teach list to compute an expertise-match component of that faculty member's recommendation score.

**6.9 Time Slot Allocation**

Time slots are pre-defined by the Administrator via the TimeSlot model (start\_time, end\_time, and an optional slot\_label such as 'Morning Slot 1'), independent of any specific division. When constructing a timetable, the Administrator picks a day and, for that day, iterates over the configured time slots, assigning at most one Timetable entry to each (division, time\_slot, day) combination.

**6.10 Clash Detection Process**

The clash detection process, implemented in services/clash\_service.py, executes three independent checks against the timetable table each time an entry is proposed. Table 6.1 summarises the scope and trigger condition of each check.

Table 6.1. Clash Detection Process

| **Check** | **Scope** | **Trigger Condition** |
| --- | --- | --- |
| Faculty Clash | Global – across all branches and divisions | Existing entry with same faculty\_id, day, and time\_slot\_id |
| Room Clash | Global – any division using the same room | Existing entry with same room\_number, day, and time\_slot\_id |
| Division Clash | Within the division | Existing entry with same division\_id, day, and time\_slot\_id |

**6.11 Clash Resolution Strategy**

When any of the three checks in 6.10 detects a conflict, the system's resolution strategy is **preventive and advisory**: the conflicting entry is rejected before it is saved, a ClashLog record is written describing the conflict (clash\_type, severity, JSON clash\_details, and resolution tracking fields), and the Administrator is shown the conflict. The administrator can then either manually resolve by choosing different parameters, or use the **Intelligent Clash Resolution** feature to get AI-powered suggestions and auto-apply the best one. This means the timetable table itself, at any point in time, is guaranteed to be free of the three hard-constraint violations, while the clash\_logs table preserves a history of conflicts that were attempted, caught, and resolved (with who resolved it, how, and any notes).

**6.12 Intelligent Clash Resolution Suggestions**

The Intelligent Clash Resolution module generates context-aware suggestions for each detected clash. The suggestion types and their strategies are summarised in Table 6.2.

Table 6.2. Intelligent Clash Resolution – Suggestion Types

| **Clash Type** | **Suggestion Category** | **Strategy** |
| --- | --- | --- |
| Room Clash | Room Change | Suggests alternative free rooms from the Room inventory; uses ML-predicted risk scores for each alternative room. |
| Room Clash | Timeslot Shift | Uses ML alternative-slot recommender to suggest lower-risk time slots. |
| Room Clash | Faculty Change | Uses ML faculty recommender to suggest alternative faculty scored by expertise and availability. |
| Faculty Clash | Faculty Change | ML-scored alternative faculty; prioritises available faculty who teach the subject. |
| Faculty Clash | Timeslot Shift | ML-based alternative time slots for the conflicting entry. |
| Faculty Clash | Room Change | Suggests alternative rooms if the faculty issue requires redistribution. |
| Division Clash | Timeslot Shift | ML alternative slots for the division entry. |
| Division Clash | Room Change | Suggests alternative rooms. |

Each suggestion includes: icon, description, detail text, risk\_score (0–1), risk\_level (low/medium/high), action\_type (change\_room, change\_faculty, change\_timeslot), and action\_value. Suggestions are sorted by risk score (lowest first). The auto-resolve mechanism applies the chosen suggestion by updating the corresponding Timetable entry and marking the ClashLog as resolved.

*(Insert Figure 6.4 – AI-Powered Clash Resolution Suggestions Panel screenshot)*

Fig 6.4. AI-Powered Clash Resolution Suggestions Panel

*(Insert Figure 6.5 – Auto-Resolve Workflow Diagram)*

Fig 6.5. Auto-Resolve Workflow Diagram

**6.13 Scheduling Workflow**

1. Administrator selects Branch, Division, and Day on the timetable\_select.html screen.
2. For the selected Day, the system lists all configured Time Slots.
3. For a chosen Time Slot, the Administrator selects a Subject.
4. The ML Recommendations panel auto-loads, showing recommended faculty and time slots.
5. The Faculty Availability panel (backed by GET /api/faculty-availability) shows each faculty member's status for that slot.
6. The Administrator selects an available Faculty member and chooses a Room.
7. On submission, the Clash Detection Service runs the Faculty, Room, and Division checks.
8. If any check fails, the entry is rejected, a ClashLog row is written, and the Administrator is notified.
9. The Administrator can view the clash in View Clashes, click "Get AI Suggestions" to get ML-powered resolution options, and click "Apply" to auto-resolve.
10. If all checks pass, the Timetable entry is committed and the Dashboard/Final Timetable View are updated.

**6.14 Algorithm Description**

Algorithm 6.1 (Clash-Checked Entry Insertion) – Input: a candidate entry (division\_id, subject\_id, faculty\_id, time\_slot\_id, day, room\_number). Step 1: query Timetable for any row where faculty\_id, day, and time\_slot\_id match the candidate; if found, return Faculty Clash. Step 2: query Timetable for any row where room\_number, day, and time\_slot\_id match the candidate; if found, return Room Clash. Step 3: query Timetable for any row where division\_id, day, and time\_slot\_id match the candidate; if found, return Division Clash. Step 4: if no step above returned a clash, insert the candidate as a new Timetable row and return Success.

Algorithm 6.2 (ML Clash-Risk Prediction) – Input: (faculty\_id, division\_id, subject\_id, time\_slot\_id, day, room\_number). Step 1: encode the six inputs into the numeric feature vector expected by the trained model (day encoded 0–5 for Monday–Saturday, room\_number encoded to a numeric identifier). Step 2: pass the feature vector to the persisted Random Forest Classifier (clash\_predictor\_model.pkl) to obtain a class probability. Step 3: interpret the probability as the risk\_score (0–1); classify risk\_level as 'low' if risk\_score < 0.3, 'medium' if between 0.3 and 0.7, and 'high' if greater than 0.7; report confidence as the model's probability for its predicted class. Step 4: return risk\_score, risk\_level, and confidence to the caller.

Algorithm 6.3 (Intelligent Resolution Suggestion Generation) – Input: clash\_id. Step 1: retrieve the ClashLog entry and extract clash\_details (day, time, room, faculty, subject). Step 2: identify the matching TimeSlot. Step 3: based on clash\_type, generate suggestions: (a) for room clashes – find alternative free rooms, compute ML risk scores, add timeslot-shift and faculty-change suggestions via ML; (b) for faculty clashes – find alternative available faculty via ML faculty recommender, add timeslot and room alternatives; (c) for division clashes – add timeslot and room alternatives. Step 4: sort suggestions by risk\_score ascending and return.

Algorithm 6.4 (Auto-Resolve Application) – Input: clash\_id, action\_type, action\_value. Step 1: retrieve the ClashLog and the conflicting Timetable entry. Step 2: based on action\_type, update the Timetable entry (room\_number, faculty\_id, or time\_slot\_id+day). Step 3: mark the ClashLog as resolved (is\_resolved=True, resolved\_at=now, resolution\_method='auto', resolution\_note=description). Step 4: commit changes and return success.

*(Insert Figure 6.1 – ML Risk Prediction Badge screenshot)*

Figure 6.1. ML Risk Prediction Badge

*(Insert Figure 6.2 – Random Forest Model Architecture Diagram)*

Figure 6.2. Random Forest Model Architecture Diagram

*(Insert Figure 6.3 – ML Recommendations Panel screenshot)*

Fig 6.3. ML Recommendations Panel

**6.15 Optimization Strategy**

The system's optimisation strategy is advisory rather than automatic: the Smart Slot Recommendation feature evaluates each configured time slot for a given faculty/division/subject combination through Algorithm 6.2 and returns the five slots with the lowest predicted risk\_score, sorted ascending; the Faculty Recommendation feature scores each candidate faculty member as a composite of their subject-expertise match (whether the subject appears in their subjects\_can\_teach list) and their availability (the proportion of relevant slots at which they are free), and returns the top five candidates; the Timetable Quality Evaluation feature aggregates risk predictions across an entire division's existing entries to produce an overall quality score together with a list of feasibility issues and improvement recommendations; and the Intelligent Resolution Suggestion feature generates context-aware, risk-scored alternatives for detected clashes that can be auto-applied. None of these optimisation features overrides the Administrator's final choice – they narrow the search space and highlight the best options.

**6.16 Complexity Analysis**

Each of the three deterministic clash checks (6.10) is implemented as a single indexed database query filtered by day and time\_slot\_id (and faculty\_id, room\_number, or division\_id respectively), giving each check an expected cost close to O(log n) to O(1) with appropriate indexing, and O(3) checks per submitted entry overall – independent of the total number of divisions or branches in the system. The ML risk-prediction step (Algorithm 6.2) has a reported prediction latency of under 10 milliseconds per query, since it involves only feature encoding followed by inference through an already-trained Random Forest of 100 trees with a maximum depth of 10 – a bounded, constant-time-per-tree traversal. The slot-recommendation feature runs Algorithm 6.2 once per configured time slot for a given day (a small, bounded number, typically well under twenty), so its overall cost remains a small constant multiple of a single prediction. The resolution suggestion generation (Algorithm 6.3) runs in O(R + S + F) time where R is the number of rooms, S is the number of time slots, and F is the number of faculty – all small, bounded numbers in a typical institution.

---

**Chapter 7: Database Design**

**7.1 Introduction**

The system uses a MySQL relational database (with automatic SQLite fallback), defined declaratively through Flask-SQLAlchemy model classes in models.py and created via create\_db.py/init\_db.py. This chapter documents the database architecture, the ER diagram, the schema of each of the **nine** tables, the relationships between them, the SQL-equivalent schema, a data dictionary, and sample records.

**7.2 Database Architecture**

The database follows a normalised relational design centred on the Timetable table, which references Division, Subject, Faculty, and TimeSlot via foreign keys, so that each timetable row is a single, fully qualified scheduling fact. The User and Faculty tables are linked one-to-one, separating authentication concerns (User) from domain-specific profile data (Faculty). The Room table is an independent entity tracking the institution's physical spaces. The ClashLog table is a dependent, append-mostly audit table referencing Division and Faculty, used for detection history and resolution tracking.

**7.3 Entity Relationship Diagram**

*(Insert updated ER diagram)*

In summary: users (1) – (0..1) faculty; branches (1) – (\*) divisions; divisions (1) – (\*) timetable; subjects (1) – (\*) timetable; faculty (1) – (\*) timetable; time\_slots (1) – (\*) timetable; divisions (1) – (\*) clash\_logs; faculty (1) – (\*) clash\_logs; rooms (independent entity, referenced by timetable.room\_number via name matching).

**7.4 Database Tables**

**7.4.1 users**

Table 7.1. Users Table Schema

| **Column** | **Type** | **Constraints** |
| --- | --- | --- |
| id | Integer | Primary Key |
| username | String(100) | Unique, Not Null, Indexed |
| email | String(120) | Unique, Not Null, Indexed |
| password\_hash | String(255) | Not Null |
| full\_name | String(150) | Not Null |
| role | String(20) | Not Null ('admin' or 'faculty') |
| is\_active | Boolean | Default True |
| created\_at | DateTime | Default: current UTC time |
| last\_login | DateTime | Nullable |

**7.4.2 faculty**

Table 7.2. Faculty Table Schema

| **Column** | **Type** | **Constraints** |
| --- | --- | --- |
| id | Integer | Primary Key |
| user\_id | Integer | Foreign Key -> users.id, Not Null |
| phone | String(15) | Nullable |
| department | String(100) | Nullable |
| designation | String(100) | Nullable (e.g., Professor, Assistant Professor) |
| working\_hours | Text (JSON) | e.g., {"start": "09:00", "end": "17:00"} |
| subjects\_can\_teach | Text (JSON array) | e.g., ["Data Structures", "DBMS"] |
| is\_visiting | Boolean | Default False |
| visiting\_available\_days | Text (JSON array) | e.g., ["Monday", "Wednesday"] |
| visiting\_slot\_ids | Text (JSON dict) | e.g., {"Monday": [1, 2], "Wednesday": [3, 4]} |
| is\_available | Boolean | Default True |
| created\_at | DateTime | Default: current UTC time |

**7.4.3 branches**

Table 7.3. Branches Table Schema

| **Column** | **Type** | **Constraints** |
| --- | --- | --- |
| id | Integer | Primary Key |
| name | String(150) | Unique, Not Null (e.g., 'Computer Engineering') |
| short\_name | String(10) | Unique, Not Null (e.g., 'CSE') |
| created\_by | Integer | Foreign Key -> users.id |
| created\_at | DateTime | Default: current UTC time |

**7.4.4 divisions**

Table 7.4. Divisions Table Schema

| **Column** | **Type** | **Constraints** |
| --- | --- | --- |
| id | Integer | Primary Key |
| branch\_id | Integer | Foreign Key -> branches.id, Not Null |
| name | String(50) | Not Null (e.g., 'A', 'B') |
| semester | Integer | Not Null (1–8) |
| academic\_year | String(20) | e.g., '2024-2025' |
| created\_by | Integer | Foreign Key -> users.id |
| created\_at | DateTime | Default: current UTC time |
| (unique constraint) | - | UNIQUE(branch\_id, name, semester, academic\_year) |

**7.4.5 time\_slots**

Table 7.5. Time Slots Table Schema

| **Column** | **Type** | **Constraints** |
| --- | --- | --- |
| id | Integer | Primary Key |
| start\_time | Time | Not Null |
| end\_time | Time | Not Null |
| slot\_label | String(50) | Nullable (e.g., 'Morning Slot 1') |
| created\_by | Integer | Foreign Key -> users.id |
| created\_at | DateTime | Default: current UTC time |

**7.4.6 subjects**

Table 7.6. Subjects Table Schema

| **Column** | **Type** | **Constraints** |
| --- | --- | --- |
| id | Integer | Primary Key |
| name | String(200) | Not Null |
| code | String(20) | Unique, Not Null |
| credits | Integer | Default 3 |
| created\_by | Integer | Foreign Key -> users.id |
| created\_at | DateTime | Default: current UTC time |

**7.4.7 rooms**

Table 7.7. Rooms Table Schema

| **Column** | **Type** | **Constraints** |
| --- | --- | --- |
| id | Integer | Primary Key |
| name | String(100) | Unique, Not Null (e.g., '101', 'Lab-A') |
| capacity | Integer | Default 60 |
| room\_type | String(50) | Default 'Classroom' (Classroom, Lab, Seminar Hall) |
| created\_by | Integer | Foreign Key -> users.id |
| created\_at | DateTime | Default: current UTC time |

**7.4.8 timetable**

Table 7.8. Timetable Table Schema

| **Column** | **Type** | **Constraints** |
| --- | --- | --- |
| id | Integer | Primary Key |
| division\_id | Integer | Foreign Key -> divisions.id, Not Null |
| subject\_id | Integer | Foreign Key -> subjects.id, Not Null |
| faculty\_id | Integer | Foreign Key -> faculty.id, Not Null |
| time\_slot\_id | Integer | Foreign Key -> time\_slots.id, Not Null |
| day | String(20) | Not Null (Monday–Saturday) |
| room\_number | String(50) | Not Null |
| created\_by | Integer | Foreign Key -> users.id |
| created\_at | DateTime | Default: current UTC time |
| updated\_at | DateTime | Default/On-update: current UTC time |

**7.4.9 clash\_logs**

Table 7.9. Clash Logs Table Schema

| **Column** | **Type** | **Constraints** |
| --- | --- | --- |
| id | Integer | Primary Key |
| clash\_type | String(20) | Not Null ('faculty' | 'room' | 'division') |
| severity | String(20) | Default 'warning' ('warning' | 'error') |
| clash\_details | Text (JSON) | Set/read via set\_details()/get\_details() |
| division\_id | Integer | Foreign Key -> divisions.id, Nullable |
| faculty\_id | Integer | Foreign Key -> faculty.id, Nullable |
| is\_resolved | Boolean | Default False |
| detected\_at | DateTime | Default: current UTC time |
| resolved\_at | DateTime | Nullable |
| resolved\_by | Integer | Foreign Key -> users.id, Nullable |
| resolution\_method | String(20) | Nullable ('manual' or 'auto') |
| resolution\_note | Text | Nullable (description of resolution action) |

**7.5 Relationships**

Table 7.10. Relationships

| **Parent Table** | **Child Table** | **Type** | **Notes** |
| --- | --- | --- | --- |
| users | faculty | One-to-One | cascade='all, delete-orphan'; deleting a User removes its Faculty profile. |
| branches | divisions | One-to-Many | cascade='all, delete-orphan'. |
| divisions | timetable | One-to-Many | cascade='all, delete-orphan'. |
| subjects | timetable | One-to-Many | Referenced via subject relationship. |
| time\_slots | timetable | One-to-Many | Referenced via time\_slot relationship. |
| faculty | timetable | One-to-Many | faculty.timetable\_entries (lazy='dynamic'). |
| divisions | clash\_logs | One-to-Many | Audit reference. |
| faculty | clash\_logs | One-to-Many | Audit reference. |
| users | clash\_logs | One-to-Many | resolved\_by reference. |

**7.6 SQL Schema**

The tables described above are created automatically by SQLAlchemy's db.create\_all() from the model definitions; conceptually this is equivalent to standard CREATE TABLE statements with INT AUTO\_INCREMENT primary keys, VARCHAR columns sized as shown in Section 7.4, TEXT columns for the JSON-encoded fields (working\_hours, subjects\_can\_teach, visiting\_available\_days, visiting\_slot\_ids, clash\_details, resolution\_note), DATETIME columns with default CURRENT\_TIMESTAMP, and FOREIGN KEY constraints matching the relationships in Section 7.5, all created under the utf8mb4 character set with utf8mb4\_unicode\_ci collation as specified when the database itself is created.

**7.7 Data Dictionary**

Table 7.11. Data Dictionary

| **Term** | **Meaning** |
| --- | --- |
| Division | A batch/section of students within a branch and semester, e.g., CSE-A. |
| Time Slot | A defined period of the day (start\_time–end\_time) used consistently across all divisions. |
| Room | A physical space (classroom, lab, or seminar hall) with a name, capacity, and type. |
| Clash | A conflict where a faculty member, room, or division is assigned to more than one entry at the same day and time slot. |
| Clash Log | A persisted record of a clash that was detected, including its type, severity, resolution status, and resolution tracking. |
| Working Hours | The start and end time within which a regular faculty member is available to teach, stored as JSON on the Faculty row. |
| Visiting Schedule | A per-day, per-time-slot availability configuration for visiting faculty, stored as a JSON dictionary. |
| Risk Score | The 0–1 probability, output by the ML model, that a proposed entry will correspond to (or resemble) a clash pattern. |
| Resolution Method | How a clash was resolved: 'manual' (administrator chose an alternative) or 'auto' (ML suggestion was applied). |

**7.8 Sample Database Records**

Table 7.12 illustrates representative sample rows consistent with the schema described above.

Table 7.12. Sample Database Records

| **Table** | **Sample Row** |
| --- | --- |
| branches | id=1, name='Computer Engineering', short\_name='CSE' |
| divisions | id=6, branch\_id=1, name='A', semester=5, academic\_year='2024-2025' |
| subjects | id=1, name='Data Structures', code='CS301', credits=4 |
| time\_slots | id=1, start\_time='08:30', end\_time='09:25', slot\_label='Slot 1' |
| rooms | id=1, name='101', capacity=60, room\_type='Classroom' |
| rooms | id=2, name='Lab-A', capacity=30, room\_type='Lab' |
| faculty | id=1, user\_id=5, department='CSE', is\_visiting=False, subjects\_can\_teach='["Data Structures","DBMS"]' |
| faculty | id=2, user\_id=7, department='CSE', is\_visiting=True, visiting\_available\_days='["Monday","Wednesday"]', visiting\_slot\_ids='{"Monday": [1, 2], "Wednesday": [3]}' |
| timetable | id=101, division\_id=6, subject\_id=1, faculty\_id=1, time\_slot\_id=1, day='Monday', room\_number='101' |
| clash\_logs | id=12, clash\_type='faculty', severity='warning', division\_id=6, faculty\_id=1, is\_resolved=True, resolution\_method='auto', resolution\_note='Faculty changed to Dr. Smith' |

---

**Chapter 8: Testing And Validation**

**8.1 Introduction**

Testing of the system combined conventional web-application testing (unit, integration, system, and user-acceptance testing of the Flask routes, clash-detection logic, room management, visiting faculty scheduling, and templates) with dedicated validation of the machine-learning subsystem and the intelligent clash resolution module, for which the project repository includes purpose-built scripts: test\_ml\_auth.py, test\_ml\_direct.py, test\_ml\_endpoints.py, test\_ml\_fixed.py, test\_ml\_simple.py, debug\_ml.py, and validate\_ml\_system.py.

**8.2 Unit Testing**

Unit-level checks were carried out on individual model methods and service functions in isolation – for example, verifying that User.set\_password()/check\_password() correctly hash and verify credentials, that Faculty.set\_subjects()/get\_subjects() and set\_working\_hours()/get\_working\_hours() correctly round-trip through JSON, that Faculty.set\_visiting\_slots()/get\_visiting\_schedule()/is\_available\_for\_slot() correctly handle day-wise visiting schedules with legacy list fallback, and that ClashLog.set\_details()/get\_details()/get\_duration() correctly serialise, deserialise, and compute resolution timing.

**8.3 Integration Testing**

Integration testing verified that the Clash Detection Service correctly interacts with the Timetable and ClashLog models through SQLAlchemy – for instance, that submitting an entry that duplicates an existing faculty\_id/day/time\_slot\_id combination is correctly rejected and produces a corresponding ClashLog row – that the ML wrapper methods in clash\_service.py correctly call into ml\_clash\_predictor.py and return the expected structure back to app.py, and that the resolution suggestion generation correctly queries room inventory, faculty availability, and ML recommendations to produce actionable suggestions.

**8.4 System Testing**

End-to-end system testing exercised the complete workflow described in Section 6.13: signing up as Administrator, configuring a branch/division/subject/time-slot/room, creating a Faculty account and profile (including visiting faculty scheduling), and then creating, editing, and deleting timetable entries through the UI, confirming that the Dashboard, Final Timetable View, View Clashes (with AI suggestions), Global Search, and CSV/ZIP Export screens update correctly.

**8.5 User Acceptance Testing**

User-acceptance style testing focused on whether the Administrator role could complete the full setup-to-timetable workflow without needing to consult external documentation, given the guidance provided in the UI (dropdowns, availability indicators, ML recommendation badges, AI suggestion panels, and inline validation messages), and whether the Faculty role could locate their personal schedule, configure their visiting schedule, and download their timetable without assistance.

**8.6 Black Box Testing**

Black-box tests exercised the application purely through its external interface (the browser UI and the JSON API endpoints) without reference to the internal implementation, verifying that valid inputs produced the expected page and that invalid or conflicting inputs (e.g., a duplicate faculty/time-slot/day combination) produced the expected clash message and AI resolution suggestions rather than a silently-accepted or corrupted entry.

**8.7 White Box Testing**

White-box tests, informed by the actual clash\_service.py and ml\_clash\_predictor.py source, verified that each of the three clash-check code paths (faculty/room/division) was independently exercised, that the ML engine's feature-encoding step (day-of-week and room-number encoding) produced the numeric vector expected by the persisted scikit-learn model, and that the resolution suggestion generation correctly prioritised free rooms over occupied ones and ML-recommended faculty over unscored ones.

**8.8 Performance Testing**

Performance testing of the ML subsystem, as recorded in the project's own ML Integration Completion Report, measured a model training time of under one second on the 65-row training dataset and a prediction latency of under 10 milliseconds per clash-risk query, well within the interactive-response expectations of the timetable-creation UI. Resolution suggestion generation was measured at under 200 milliseconds per clash, including ML predictions for alternative rooms and time slots.

**8.9 Security Testing**

Security-focused testing verified that passwords are never stored or transmitted in plaintext (only password\_hash values are persisted, produced by Werkzeug), that admin-only routes, all six ML API endpoints, and the clash-resolution API endpoints reject requests from a non-authenticated or non-admin session, and that SQLAlchemy's parameterised query interface is used throughout rather than raw, string-concatenated SQL, mitigating SQL-injection risk.

**8.10 Test Cases**

Table 8.1. Test Cases

| **TC ID** | **Test Scenario** | **Expected Result** |
| --- | --- | --- |
| TC-01 | Sign up a new Administrator account | Account is created; password is stored as a hash, not plaintext |
| TC-02 | Log in with correct credentials | Session is established; redirected to Admin Dashboard |
| TC-03 | Log in with incorrect password | Login rejected with an error message |
| TC-04 | Create a Division with a duplicate (branch, name, semester, academic\_year) | Rejected by the unique constraint on divisions |
| TC-05 | Assign the same faculty to two entries at the same day/time-slot | Rejected with a Faculty Clash message; ClashLog row created |
| TC-06 | Assign the same room to two entries at the same day/time-slot | Rejected with a Room Clash message; ClashLog row created |
| TC-07 | Assign a division to two entries at the same day/time-slot | Rejected with a Division Clash message; ClashLog row created |
| TC-08 | Submit a valid, non-conflicting entry | Entry saved; appears in Dashboard entry count |
| TC-09 | Call GET /api/faculty-availability for a given day/time slot | Returns each faculty member's availability status |
| TC-10 | Call POST /api/ml/predict-clash-risk with a candidate entry | Returns risk\_score, risk\_level, and confidence |
| TC-11 | Call GET /api/ml/slot-recommendations | Returns up to five alternative slots sorted by ascending risk |
| TC-12 | Call GET /api/ml/recommend-faculty | Returns up to five faculty candidates with expertise/availability scores |
| TC-13 | Call an ML endpoint without admin authentication | Request rejected (authorization required) |
| TC-14 | Faculty logs in and views personal schedule | Schedule reflects exactly the entries referencing that faculty\_id |
| TC-15 | Add a new room via Manage Rooms | Room created with name, capacity, and type; appears in room listing |
| TC-16 | Search using Global Search for "CSE" | Returns matching branches, divisions, faculty, and subjects |
| TC-17 | Call GET /api/ml/clash-suggestions/\<clash\_id\> for a room clash | Returns alternative rooms, time slots, and faculty with risk scores |
| TC-18 | Auto-resolve a clash via Apply button | Timetable entry updated; ClashLog marked resolved with method='auto' |
| TC-19 | Configure visiting faculty with day-wise schedule | Faculty profile saved with per-day time-slot availability |
| TC-20 | Download CSV for a division timetable | CSV file downloaded with correct grid format (Time × Days) |
| TC-21 | Export all timetables as ZIP | ZIP file containing one CSV per division is downloaded |
| TC-22 | Faculty downloads personal timetable CSV | CSV file with faculty's teaching schedule is downloaded |
| TC-23 | Resolve a clash manually | ClashLog marked resolved with method='manual', resolved\_by set |

**8.11 Bug Analysis**

Issues surfaced during the development and validation of the system included: edge cases such as missing or malformed working\_hours/subjects\_can\_teach JSON on a Faculty row, the need for a graceful fallback in the prediction endpoints when the persisted model file was not yet present (i.e., before the first training run), legacy visiting\_slot\_ids stored as a flat list instead of a day-keyed dictionary (handled by the get\_visiting\_schedule fallback logic), ML recommendations panel content being hidden by CSS class conflicts (resolved by removing conflicting class names and using inline styles), and linter warnings (bare except clauses, == True/False comparisons, unused imports) that did not affect runtime behaviour but were cleaned up for code quality. These were addressed by validating JSON fields defensively when read, ensuring the ML wrapper methods handle a missing or untrained model without causing the surrounding request to fail, and implementing backward-compatible data format handling.

---

**Chapter 9: Results And Discussion**

**9.1 Introduction**

This chapter presents the observed results of the implemented system, drawing on the project's own recorded validation output (the ML Integration Completion Report) and on the functional behaviour of the deterministic clash-detection subsystem, the intelligent resolution module, the global search, and the export functionality, and discusses these results against the objectives set out in Chapter 1.

**9.2 Dashboard Results**

The Admin Dashboard successfully renders each division with a colour-coded clash indicator (green for clash-free, red for divisions with detected clashes) alongside an entry count, giving the Administrator an at-a-glance summary of scheduling status across the institution. The dashboard also displays total counts for branches, divisions, faculty, subjects, and rooms, and a list of recent unresolved clashes.

*(Insert Figure 9.1 – Dashboard Displaying Clash Indicators Across Divisions screenshot)*

Fig 9.1. Dashboard Displaying Clash Indicators Across Divisions

**9.3 Timetable Generation Results**

The interactive, side-by-side timetable-creation screen was verified to correctly display faculty availability alongside each time slot, to correctly show ML recommendations (faculty with TOP PICK/EXPERT tags and risk scores, time slots with BEST tags and risk percentages), and to correctly persist a new Timetable row only when none of the three clash checks fail, confirming that the entry-creation workflow described in Section 6.13 behaves as designed.

**9.4 Clash Resolution Results**

Deliberately duplicated entries (same faculty/day/time-slot, same room/day/time-slot, and same division/day/time-slot) were each correctly rejected by the corresponding check in the Clash Detection Service, and a corresponding ClashLog row was written in each case, confirming both the prevention behaviour (Section 6.11) and the audit-logging behaviour (Section 7.4.9) of the system.

**9.5 Intelligent Clash Resolution Results**

The AI-powered resolution suggestion feature was verified to correctly generate context-aware suggestions for all three clash types. For room clashes, the system correctly identified alternative free rooms from the Room inventory, computed ML risk scores for each, and offered timeslot-shift and faculty-change alternatives. For faculty clashes, the system correctly identified alternative available faculty scored by ML expertise and availability metrics. The one-click auto-resolve functionality was verified to correctly update the conflicting Timetable entry and mark the ClashLog as resolved with resolution\_method='auto' and an appropriate resolution\_note. The AI suggestion panel rendered with the expected glassmorphism styling, colour-coded risk badges, and animated slide-down entrance.

*(Insert Figure 9.3 – Clash Resolution Suggestion Accuracy screenshot or chart)*

**9.6 Global Search Results**

The global search was verified to correctly return results across all six entity types (faculty, subjects, divisions, branches, rooms, clashes) with appropriate partial matching via ilike queries, and to display results with category-wise grouping and total counts on the search\_results.html page.

**9.7 Export Results**

The CSV export was verified to produce correctly formatted grid-based timetable files (Time rows × Day columns) for individual divisions, bulk ZIP export for all divisions, and personal faculty timetable downloads. All exports were verified to contain accurate data matching the database records.

**9.8 Performance Analysis**

The project's own ML Integration Completion Report records a Random Forest Classifier (100 trees, max depth 10) trained on 65 timetable entries in under one second, with a prediction latency of under 10 milliseconds and a persisted model file of approximately 92 KB (92,467 bytes). Resolution suggestion generation completes in under 200 milliseconds per clash.

Table 9.1 The recorded direct-testing results for the six core ML functions.

| **Test** | **Result** |
| --- | --- |
| Clash Risk Prediction | Risk Score: 0.70, Risk Level: high, Confidence: 0.70 – SUCCESS |
| Smart Slot Recommendations | 5 recommendations returned, e.g., Tuesday 08:30–09:25 (risk 0.53); Monday 10:30–11:30 (risk 0.55); Monday 11:30–12:30 (risk 0.56) – SUCCESS |
| Faculty Recommendations | Scored candidate list returned – SUCCESS |
| Timetable Quality Evaluation | Quality score, feasibility, and recommendations returned – SUCCESS |
| Clash Risk Summary | Average Risk: 0.33; Total Entries: 1; High: 0, Medium: 0, Low: 1 – SUCCESS |
| Model Persistence | Model file saved at ml\_models/clash\_predictor\_model.pkl, 92,467 bytes – MODEL SAVED |

Table 9.2 The additional performance metrics recorded for the ML subsystem.

| **Metric** | **Value** |
| --- | --- |
| Model Training Time | < 1 second |
| Prediction Latency | < 10 ms |
| Model File Size | 92 KB |
| Recommendations Generated per Query | 5 |
| Resolution Suggestions per Clash | 5–10 (varies by clash type) |
| Auto-Resolve Application Time | < 50 ms |
| Risk Distribution (sample run) | Low 67%, Medium 0%, High 33% |

*(Insert Figure 9.2 – ML Feature Importance Chart)*

Fig 9.2. ML Feature Importance Chart

**9.9 Comparison with Manual Scheduling**

Table 9.3. Comparison: Manual Scheduling vs. Proposed System

| **Aspect** | **Manual Scheduling** | **Proposed System** |
| --- | --- | --- |
| Conflict detection | Visual/manual cross-check, error-prone | Automatic, on every entry submission (Section 6.10) |
| Conflict scope | Limited to what a reviewer notices | Global faculty check; systematic room and division checks |
| Conflict history | Not retained | Persisted in clash\_logs with timestamp, type, and full resolution tracking |
| Foresight before committing an entry | None | ML risk score, alternative slot and faculty recommendations |
| Conflict resolution | Manual investigation of alternatives | ML-powered suggestions with one-click auto-resolve |
| Room management | Manual inventory | Structured Room entity with capacity and type |
| Visiting faculty scheduling | Informal notes | Per-day, per-slot configuration with visual toggle |
| Search capability | Manual lookup | Full-text search across all entities |
| Timetable export | Manual copy | Automated CSV/ZIP export |
| Time to verify a new entry | Manual, variable | Sub-second automated checks plus < 10 ms ML prediction |
| Time to resolve a clash | Manual investigation (minutes–hours) | AI suggestion + one-click auto-resolve (< 1 second) |

**9.10 Advantages Achieved**

* All three hard-constraint clash types (faculty, room, division) are automatically enforced at entry-submission time.
* A complete, timestamped audit trail of detected clashes is retained in clash\_logs with full resolution tracking (who, how, notes).
* The Random Forest based prediction module gives the Administrator a quantified risk score and concrete alternative recommendations before an entry is finalised.
* ML-powered intelligent resolution suggestions with one-click auto-resolve dramatically reduce the time needed to handle detected clashes from minutes/hours to seconds.
* Rooms are managed as first-class entities with capacity and type attributes.
* Visiting faculty scheduling at per-day, per-slot granularity ensures accurate part-time staff scheduling.
* Global search enables rapid information retrieval across all entities.
* CSV/ZIP export enables offline distribution of timetables.
* Role-based portals keep the Administrator and Faculty experiences focused on what each role actually needs to do.
* The system is web-based and accessible from any modern browser without additional client installation.
* Automatic SQLite fallback ensures resilience when the primary database is unavailable.

**9.11 Limitations**

* The ML model was trained on a relatively small dataset (65 historical timetable entries in the recorded validation run); prediction quality will depend on the volume and representativeness of an institution's own historical data once deployed.
* The system does not perform fully automatic, end-to-end timetable generation; it validates, scores, and suggests alternatives for entries that a human administrator proposes, rather than producing a complete conflict-free timetable unattended.
* Room capacity constraints are not currently enforced during timetable creation (i.e., the system does not check if the number of students in a division exceeds the room's capacity).
* There is no dedicated laboratory-session model distinguishing lab-specific constraints (e.g., minimum block length) from ordinary lecture slots.
* The current deployment relies on a single database instance and a locally persisted model file, which would need to be revisited for multi-campus or high-availability deployment (see Chapter 10).

---

**Chapter 10: Future Scope And Conclusion**

**10.1 Future Scope**

**10.1.1 ERP Integration**

Integrating the system with a broader institutional ERP (covering admissions, examinations, and fee management) would allow branch, division, and student-batch data to be synchronised automatically rather than entered separately by the Administrator.

**10.1.2 Attendance Management**

Because each Timetable entry already links a division, subject, faculty member, and time slot, the schema is a natural foundation for an attendance module that records student attendance against a specific scheduled session.

**10.1.3 Mobile Application**

A dedicated mobile application (or a Progressive Web App built on the existing responsive templates) would let faculty members and administrators check schedules and clash alerts without opening a desktop browser, building on the fact that the current UI is already noted as responsive across desktop, tablet, and mobile.

**10.1.4 Cloud Deployment**

The production deployment guidance already documented in the project (Gunicorn behind Nginx, environment-specific configuration, and a disabled debug mode) could be extended to a managed cloud platform with autoscaling and managed MySQL, building on the fact that a live instance is already hosted at [timetable-clash-resolution.onrender.com](https://timetable-clash-resolution.onrender.com)

**10.1.5 Multi-Campus Support**

Extending the Branch/Division model with an explicit campus or site dimension would allow the same clash-detection and recommendation logic to operate correctly for institutions with more than one physical location, while keeping faculty and room clash checks correctly scoped per campus where required.

**10.1.6 Advanced ML Enhancements**

The existing Random Forest based risk-prediction, recommendation, and resolution module could be extended with: additional features such as faculty workload balance, subject difficulty, and student feedback scores; retraining on larger volumes of historical data as the institution accumulates more timetable entries; room-capacity-aware recommendations that match division size to room capacity; and reinforcement learning techniques for iteratively improving suggestion quality based on which suggestions administrators accept or reject.

**10.2 Conclusion**

This report has documented the College Timetable Management System with Intelligent Clash Detection and Resolution, a Flask, Flask-SQLAlchemy, and MySQL based web application (with automatic SQLite fallback) that replaces error-prone manual timetable preparation with an interactive, role-based system in which every proposed timetable entry is automatically checked for faculty, room, and division clashes before it is committed, and every detected clash is permanently logged with full resolution tracking for audit. Beyond this deterministic safeguard, the system incorporates a supervised machine-learning module – a Random Forest Classifier trained on the institution's own historical scheduling data – that predicts clash risk, recommends lower-risk alternative time slots, recommends suitable faculty by expertise and availability, generates context-aware resolution suggestions for detected clashes with one-click auto-resolve capability, and evaluates overall timetable quality, exposed through nine authenticated API endpoints and integrated directly into both the timetable-creation interface and the clash-management interface.

The system additionally provides: a Room & Resource Management module for tracking classrooms, labs, and seminar halls with capacity and type; visiting faculty scheduling with per-day, per-time-slot availability configuration; global search across all entities; CSV/ZIP timetable export for administrators and faculty; and enhanced search/filter on all management listing pages.

The objectives set out in Chapter 1 – automated clash detection across all three hard-constraint categories, role-based Administrator and Faculty portals, a centralised dashboard, a predictive machine-learning layer, intelligent resolution suggestions with auto-resolve, room management, visiting faculty scheduling, global search, and timetable export – were each realised in the implemented system and verified through the testing described in Chapter 8 and the results discussed in Chapter 9. While the current system has limitations, most notably the size of the historical dataset available for model training and the absence of fully automatic end-to-end timetable generation, it demonstrably improves on manual scheduling in accuracy, auditability, resolution speed, and foresight, and provides a solid, extensible foundation for the future enhancements identified in Section 10.1.

---

**References**

**Books**

* Elmasri, R. & Navathe, S. B., Fundamentals of Database Systems, 7th Edition, Pearson, 2015.
* Sommerville, I., Software Engineering, 10th Edition, Pearson, 2015.
* Hastie, T., Tibshirani, R. & Friedman, J., The Elements of Statistical Learning: Data Mining, Inference, and Prediction, 2nd Edition, Springer, 2009

**Research Papers**

* "Machine Learning-Based Prediction System for Optimized Faculty Exam Duty Allocation," IJERT, 2026"
* Addressing staffing challenges through improved planning: Demand-driven course schedule planning and instructor assignment in higher education," ScienceDirect, 2024

**IEEE Papers**

* "Graph Coloring based Scheduling Algorithm to automatically generate College Course Timetable," IEEE Conference Publication, 2020
* Corne, D. & Ross, P., "Constraint-based timetabling – a case study," IEEE Conference Publication

**Official Documentation**

* Flask Documentation – https://flask.palletsprojects.com/
* Flask-SQLAlchemy Documentation – https://flask-sqlalchemy.palletsprojects.com/
* SQLAlchemy Documentation – https://docs.sqlalchemy.org/
* MySQL Reference Manual – https://dev.mysql.com/doc/
* scikit-learn Documentation (Random Forest Classifier) – https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
* Werkzeug Documentation (security helpers) – https://werkzeug.palletsprojects.com/
* Flask-Login Documentation – https://flask-login.readthedocs.io/

**Websites**

* Project Repository – https://github.com/Krishp285/timetable-clash-resolution
* Live Deployment – [timetable-clash-resolution.onrender.com](https://timetable-clash-resolution.onrender.com)

---

**Appendix**

**Appendix A – User Manual**

**A.1 Administrator Quick Guide**

1. Sign up or log in as an Administrator.
2. Navigate to Manage Branches and add each academic branch (name and short name).
3. Navigate to Manage Divisions and add each division under its branch, with semester and academic year. Use the branch filter and search bar to find existing divisions.
4. Navigate to Manage Subjects and add each subject with its code and credits. Use the search bar to filter subjects.
5. Navigate to Manage Time Slots and define the day's time slots.
6. Navigate to Manage Rooms and add each room/resource with name, capacity, and type (Classroom, Lab, Seminar Hall). Use the search bar to filter rooms.
7. Navigate to Manage Faculty to review faculty profiles (created when faculty sign up). Use the search bar to find faculty.
8. Go to Create Timetable, select Branch/Division/Day, and for each time slot:
   - Select a subject (ML recommendations will auto-load).
   - Review the ML-recommended faculty and time slots.
   - Choose an available faculty member from the availability panel.
   - Select a room.
   - Submit the entry.
9. Review the Admin Dashboard for clash indicators, and open View Clashes for details of any detected conflicts.
10. For detected clashes, click "Get AI Suggestions" to see ML-powered resolution options, and click "Apply" to auto-resolve.
11. Use Global Search (top navigation) to find any entity across the system.
12. Use Export All to download all timetables as a ZIP, or download individual division CSVs.

**A.2 Faculty Quick Guide**

1. Sign up as Faculty; a linked Faculty profile is created automatically.
2. Open Faculty Profile and set phone, department, designation, working hours, and the subjects you can teach.
3. If you are a visiting faculty member, toggle the "Visiting Faculty" switch, select your available days, and for each day select the time slots you are available for.
4. Open your Faculty Dashboard to view your personal, day-organised teaching schedule.
5. Click "Download Timetable" to export your personal schedule as a CSV file.

**Appendix B – Installation Guide**

The following steps reproduce the installation procedure documented in the project's README.

1. Create and enter a project directory: mkdir timetable\_system && cd timetable\_system.
2. Create a virtual environment: python -m venv venv, then activate it (venv\Scripts\activate on Windows, or source venv/bin/activate on macOS/Linux).
3. Install dependencies: pip install Flask Flask-SQLAlchemy PyMySQL cryptography Werkzeug Flask-Login (plus scikit-learn, numpy, pandas, joblib for the ML module, per requirements.txt).
4. Create the MySQL database: mysql -u root -p, then CREATE DATABASE timetable\_system CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci;
5. Configure the database connection in config.py or as environment variable: set SQLALCHEMY\_DATABASE\_URI to mysql+pymysql://root:YOUR\_PASSWORD@localhost/timetable\_system. (If MySQL is not available, the system will automatically fall back to SQLite.)
6. Create the database tables: python create\_db.py.
7. Run the application: python app.py.
8. Open a browser at http://localhost:5000. Default admin login: username 'admin', password 'admin123' (change immediately in any real deployment).

**Appendix C – Project Folder Structure**

*(Insert Figure C.1 – Project Folder Structure screenshot – should now show manage\_rooms.html, search\_results.html, and the increased file count)*

Figure C.1. Project Folder Structure

**Appendix D – Database Schema**

See Chapter 7 (Database Design) for the complete schema of the users, faculty, branches, divisions, time\_slots, subjects, rooms, timetable, and clash\_logs tables.

**Appendix E – API Documentation**

**E.1 Application Utility Endpoints**

Table E.1. Application REST/Utility API Endpoints

| **Endpoint** | **Method** | **Description** |
| --- | --- | --- |
| /api/divisions/\<branch\_id\> | GET | Get divisions belonging to a given branch. |
| /api/faculty-availability | GET | Get faculty availability for a given day/time slot. |
| /api/faculty-matrix | GET | Get full faculty availability matrix for a given day/time slot with detailed status information. |
| /api/subjects/search | GET | Search subjects by name or code. |
| /search | GET | Global search across faculty, subjects, divisions, branches, rooms, and clashes. |
| /admin/timetable/export | GET | Export all division timetables as a ZIP file. |
| /timetable/download/\<division\_id\> | GET | Download a single division's timetable as CSV. |
| /faculty/timetable/download | GET | Download the logged-in faculty member's personal timetable as CSV. |

**E.2 Machine Learning API Endpoints**

Table E.2. ML API Endpoints

| **Endpoint** | **Method** | **Description** |
| --- | --- | --- |
| /api/ml/predict-clash-risk | POST | Predicts risk\_score, risk\_level, and confidence for a candidate entry (faculty\_id, division\_id, subject\_id, time\_slot\_id, day, room\_number). |
| /api/ml/slot-recommendations | GET/POST | Returns up to five alternative time slots ranked by ascending clash risk (params: faculty\_id, division\_id, subject\_id, preferred\_day). |
| /api/ml/recommend-faculty | GET/POST | Returns up to five faculty candidates scored by subject expertise and availability (params: subject\_id, division\_id, preferred\_day, preferred\_time\_slot\_id). |
| /api/ml/evaluate-timetable | POST | Returns a quality score, feasibility assessment, and recommendations for a division's timetable (params: division\_id or an entries list). |
| /api/ml/clash-risk-summary | GET | Returns average risk and high/medium/low risk counts, optionally filtered by division\_id. |
| /api/ml/train-model | POST | (Re-)trains the Random Forest model on the latest data in the database and returns training status/metrics. |

**E.3 Clash Resolution API Endpoints**

Table E.3. Clash Resolution API Endpoints

| **Endpoint** | **Method** | **Description** |
| --- | --- | --- |
| /api/ml/clash-suggestions/\<clash\_id\> | GET | Generates ML-powered resolution suggestions for a specific clash, including alternative rooms, faculty, and time slots with risk scores. |
| /admin/clashes/resolve/\<clash\_id\> | POST | Manually marks a clash as resolved. |
| /admin/clashes/auto-resolve/\<clash\_id\> | POST | Applies an ML-generated suggestion to auto-resolve a clash (params: action\_type, action\_value). |

Sample request/response for /api/ml/predict-clash-risk:

Request: { "faculty\_id": 1, "division\_id": 6, "subject\_id": 1, "time\_slot\_id": 1, "day": "Monday", "room\_number": "101" } Response: { "success": true, "risk": { "risk\_score": 0.70, "risk\_level": "high", "confidence": 0.70 } }

Sample request/response for /api/ml/clash-suggestions/12:

Response: { "success": true, "clash\_type": "room", "suggestions": [{ "type": "room\_change", "description": "Assign Room 102 instead of Room 101", "detail": "Room 102 is available at Monday 08:30-09:25", "risk\_score": 0.05, "risk\_level": "low", "action\_type": "change\_room", "action\_value": "102", "icon": "🏫" }, ...] }

**Appendix F – Sample Input Data**

Sample input consistent with the schema in Chapter 7: Branch = {name: 'Computer Engineering', short\_name: 'CSE'}; Division = {branch: 'CSE', name: 'A', semester: 5, academic\_year: '2024-2025'}; Subject = {name: 'Data Structures', code: 'CS301', credits: 4}; Time Slot = {start\_time: '08:30', end\_time: '09:25', slot\_label: 'Slot 1'}; Room = {name: '101', capacity: 60, room\_type: 'Classroom'}; Faculty (regular) = {department: 'CSE', designation: 'Assistant Professor', working\_hours: {start: '09:00', end: '17:00'}, subjects\_can\_teach: ['Data Structures', 'DBMS']}; Faculty (visiting) = {department: 'CSE', designation: 'Visiting Professor', is\_visiting: true, visiting\_available\_days: ['Monday', 'Wednesday'], visiting\_slot\_ids: {"Monday": [1, 2], "Wednesday": [3, 4]}}.

**Appendix G – Sample Generated Timetable**

Table G.1. Sample Generated Timetable

| **Time** | **Monday** | **Tuesday** | **Wednesday** | **Thursday** | **Friday** | **Saturday** |
| --- | --- | --- | --- | --- | --- | --- |
| **08:30 - 09:25** | **Agile Software Development & DevOps**  *Nimisha Patel*  Room 101 | **Cyber Crime and Mitigation**  *Nimisha Patel*  Room 101 | **Data Security**  *Nimisha Patel*  Room 101 | **Data Security**  *Chintan Rana*  Room 101 | – | – |
| **09:25 - 10:20** | **Data Security**  *Nimisha Patel*  Room 101 | **Agile Software Development & DevOps**  *Ajeet Patel*  Room 101 | – | – | – | – |
| **10:30 - 11:30** | **Cyber Crime and Mitigation**  *Chintan Rana*  Room 101 | **Cyber Crime and Mitigation**  *Chintan Rana*  Room 101 | – | – | – | – |
| **11:30 - 12:30** | **Agile Software Development & DevOps**  *Ajeet Patel*  Room 102 | **Image Processing**  *Divya Sharma*  Room 101 | – | – | – | – |
| **13:00 - 14:00** | **Cyber Crime and Mitigation**  *Chintan Rana*  Room 101 | – | – | – | – | – |
| **14:00 - 15:00** | **Predictive Analytics**  *Divya Sharma*  Room 101 | – | – | – | – | – |
| **15:10 - 16:10** | – | – | – | – | – | – |
| **16:10 - 17:10** | – | – | – | – | – | – |

**Appendix H – Application Screenshots**

Insert, in order: Login/Signup page, Admin Dashboard, Manage Branches/Divisions/Subjects/Time Slots/Rooms pages, Timetable Creation (side-by-side) page, Faculty Availability panel, ML risk badge and recommendations panel, AI Clash Resolution Suggestions panel, Faculty Dashboard, Faculty Profile page (Regular and Visiting), Global Search Results page, Final Timetable View, View Clashes page, and CSV Export.

**Appendix I – Glossary**

Table I.1. Glossary

| **Term** | **Definition** |
| --- | --- |
| Branch | An academic department/programme, e.g., CSE, ICT, ECE. |
| Division | A section/batch of students within a branch and semester. |
| Room | A physical space (classroom, lab, or seminar hall) with capacity and type attributes. |
| Clash | A scheduling conflict involving a faculty member, room, or division. |
| ORM | Object-Relational Mapper; here, Flask-SQLAlchemy, mapping Python classes to MySQL/SQLite tables. |
| Random Forest | An ensemble machine-learning classifier composed of many decision trees, used here to predict clash risk and generate recommendations. |
| Risk Score | A 0–1 value output by the ML model indicating the predicted likelihood of a clash. |
| Auto-Resolve | The one-click application of an ML-generated resolution suggestion to automatically fix a detected clash. |
| Visiting Faculty | Part-time or adjunct faculty with day-wise, per-slot availability constraints. |
| Resolution Method | How a clash was resolved: 'manual' or 'auto'. |

**Appendix J – Abbreviations**

Table J.1. Abbreviations

| **Abbreviation** | **Expansion** |
| --- | --- |
| CSE | Computer Science and Engineering |
| ICT | Information and Communication Technology |
| ECE | Electronics and Communication Engineering |
| ORM | Object-Relational Mapper |
| CRUD | Create, Read, Update, Delete |
| API | Application Programming Interface |
| ML | Machine Learning |
| AI | Artificial Intelligence |
| ER Diagram | Entity Relationship Diagram |
| DFD | Data Flow Diagram |
| UML | Unified Modeling Language |
| WSGI | Web Server Gateway Interface |
| SSL | Secure Sockets Layer |
| CSV | Comma-Separated Values |
| ZIP | Compressed Archive Format |

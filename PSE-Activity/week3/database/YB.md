# Project Scope – Yoobee College Database

The Yoobee College database will manage core academic and administrative records, focusing on students, lecturers, departments, courses, and classes.  
It will centralize enrollment, teaching assignments, and course offerings to ensure accurate, efficient, and accessible information management for the college.

---

## Entities and Attributes

### i. Student
- `Attributes`: StudentID (PK), Name, Age, Address, Email  
- `Role`: Stores student personal and enrollment details.  

### ii. Lecturer
- `Attributes`: LecturerID (PK), Name, DepartmentID (FK), Email  
- `Role`: Stores lecturer information and teaching assignments.  

### iii. Department
- `Attributes`: DepartmentID (PK), Name  
- `Role`: Groups lecturers and organizes programmes.  

### iv. Programme
- `Attributes`: ProgrammeID (PK), Name, DepartmentID (FK)  
- `Role`: Stores programme information under a department.  

### v. Course
- `Attributes`: CourseID (PK), Name, Credits  
- `Role`: Stores course details offered by programmes.  

### vi. CourseOffering
- `Attributes`: OfferingID (PK), CourseID (FK), SemesterID (FK), RoomID (FK)  
- `Role`: Represents a course offered in a specific semester and classroom.  

### vii. StudentCourse (Enrollment)
- `Attributes`: StudentID (FK), CourseID (FK)  
- `Role`: Links students to the courses they are enrolled in.  

### viii. Assessment
- `Attributes`: AssessmentID (PK), OfferingID (FK), Title, DueDate  
- `Role`: Stores assessment tasks for each course offering.  

### ix. Submission
- `Attributes`: SubmissionID (PK), AssessmentID (FK), StudentID (FK), Grade  
- `Role`: Stores student submissions and grades.  

### x. Attendance
- `Attributes`: AttendanceID (PK), EnrollmentID (FK), Date, Status  
- `Role`: Tracks attendance for enrolled students.  

### xi. Room
- `Attributes`: RoomID (PK), Building, Capacity  
- `Role`: Stores classroom allocation information.  

### xii. Semester
- `Attributes`: SemesterID (PK), Name, Year  
- `Role`: Defines teaching periods.  

---

## Database Diagram

![Database ERD](./db_diagram_2.png)

---

## Notes
- All relationships use **Primary Keys (PK)** and **Foreign Keys (FK)**.  
- Many-to-many (M:N) relationships are resolved using **junction tables** (e.g., StudentCourse, ProgrammeCourse).  
- Diagram was created in *draw.io* and exported as `db_diagram_2.png`.  

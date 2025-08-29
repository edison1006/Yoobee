```mermaid
classDiagram
direction TB

%% ===== Core Users & Roles =====
class User {
  <<abstract>>
  +uuid id
  +string name
  +string email
  +string passwordHash
  +Role role
  +AccountStatus status
  +login(email,pw)
  +updateProfile()
}

class Student {
  +string studentId
  +int year
  +enroll(offering)
  +submitAssignment(assignment,artifact)
}

class Lecturer {
  +string staffId
  +string title
  +createCourse(courseData)
  +grade(submission,score,comment)
}

class Administrator {
  +string adminId
  +approveOffering(offering)
  +generateReport(type,range)
}

User <|-- Student
User <|-- Lecturer
User <|-- Administrator

%% ===== Organisation =====
class Department {
  +uuid id
  +string name
  +string code
}

class Programme {
  +uuid id
  +string name
  +string code
}

Department "1" o-- "0..*" Programme : owns >
Department "1" o-- "0..*" Course : owns >

%% ===== Courses & Delivery =====
class Course {
  +string code
  +string title
  +int credits
  +string description
}

class CourseOffering {
  +uuid id
  +string term      %% e.g., T1/T2/Sem1
  +int year
  +string section   %% e.g., A/B
  +OfferingStatus status
  +publishTimetable()
}

Course "1" o-- "0..*" CourseOffering : offered as >

%% Teaching responsibilities / approvals
Lecturer "1" -- "0..*" CourseOffering : teaches >
Administrator "1" -- "0..*" CourseOffering : approves >

%% ===== Enrolment =====
class Enrollment {
  +uuid id
  +date enrolledAt
  +EnrollmentStatus status
  +withdraw()
}

Student "1" -- "0..*" Enrollment
CourseOffering "1" -- "0..*" Enrollment

%% ===== Learning Materials & Assessments =====
class TeachingMaterial {
  +uuid id
  +MaterialType type   %% slide/pdf/link
  +string url
  +int version
  +date publishedAt
}

class Assignment {
  +uuid id
  +string title
  +datetime dueAt
  +int maxScore
  +string rubricUrl
  +release()
  +close()
}

class Submission {
  +uuid id
  +datetime submittedAt
  +string artifactUrl
  +SubmissionStatus status
}

class Grade {
  +uuid id
  +float score
  +string letter
  +datetime gradedAt
}

class Feedback {
  +uuid id
  +string comments
  +datetime createdAt
}

CourseOffering "1" -- "0..*" TeachingMaterial : includes >
CourseOffering "1" -- "0..*" Assignment : sets >
Assignment "1" -- "0..*" Submission : receives >
Submission "0..1" -- "1" Grade : results in >
Submission "0..*" -- "0..*" Feedback : has >

Lecturer "1" -- "0..*" Grade : grades >
Lecturer "1" -- "0..*" Feedback : comments >
Student  "1" -- "0..*" Submission : makes >

%% ===== Scheduling (Timetable) =====
class ClassSession {
  +uuid id
  +DayOfWeek day
  +time startTime
  +time endTime
  +SessionType type   %% lecture/lab/tutorial
}

class Room {
  +uuid id
  +string code
  +int capacity
  +string building
}

CourseOffering "1" -- "1..*" ClassSession : scheduled as >
ClassSession "1" --> "1" Room : held in >

%% Optional attendance tracking
class AttendanceRecord {
  +uuid id
  +AttendanceStatus status
  +datetime markedAt
}
ClassSession "1" -- "0..*" AttendanceRecord
Student "1" -- "0..*" AttendanceRecord

%% ===== Admin / Reporting / Notifications =====
class Report {
  +uuid id
  +ReportType type   %% enrolment/perf/utilisation
  +date from
  +date to
  +string url
  +generate()
}

class Notification {
  +uuid id
  +NotificationType type
  +string message
  +datetime createdAt
  +bool read
  +markRead()
}

Administrator "1" -- "0..*" Report : generates >
User "1" -- "0..*" Notification : receives >

%% ===== Enumerations (as stereotypes) =====
class Role {
  <<enumeration>>
  STUDENT
  LECTURER
  ADMIN
}

class AccountStatus {
  <<enumeration>>
  ACTIVE
  SUSPENDED
  PENDING
}

class OfferingStatus {
  <<enumeration>>
  DRAFT
  PENDING_APPROVAL
  PUBLISHED
  ARCHIVED
}

class EnrollmentStatus {
  <<enumeration>>
  ENROLLED
  WAITLISTED
  WITHDRAWN
}

class SubmissionStatus {
  <<enumeration>>
  DRAFT
  SUBMITTED
  LATE
  GRADED
  RETURNED
}

class MaterialType {
  <<enumeration>>
  FILE
  LINK
  VIDEO
  READING
}

class SessionType {
  <<enumeration>>
  LECTURE
  LAB
  TUTORIAL
  EXAM
}

class AttendanceStatus {
  <<enumeration>>
  PRESENT
  ABSENT
  LATE
  EXCUSED
}

class ReportType {
  <<enumeration>>
  ENROLMENT
  PERFORMANCE
  UTILISATION
}

class NotificationType {
  <<enumeration>>
  SYSTEM
  DEADLINE
  GRADE_RELEASED
  FEEDBACK_POSTED
}

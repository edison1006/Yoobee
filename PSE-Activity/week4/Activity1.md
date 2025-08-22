# College Academic Management System - Use Case Diagram

```mermaid
flowchart LR
  A[<<actor>> Student]
  B[<<actor>> Lecturer]
  C[<<actor>> Administrator]

  subgraph S[College Academic Management System]
    UC1((Register & Update Profile))
    UC2((Enroll in Courses))
    UC3((View Timetable / Schedule))
    UC4((Submit Assignments))
    UC5((View Grades & Feedback))

    UC6((Create & Update Courses))
    UC7((Schedule & Manage Classes))
    UC8((Upload Teaching Materials))
    UC9((Grade Assignments))
    UC10((Provide Feedback))

    UC11((Manage Student & Lecturer Records))
    UC12((Approve Course Offerings))
    UC13((Allocate Classrooms & Time Slots))
    UC14((Generate Reports))
  end

  A --- UC1
  A --- UC2
  A --- UC3
  A --- UC4
  A --- UC5

  B --- UC6
  B --- UC7
  B --- UC8
  B --- UC9
  B --- UC10

  C --- UC11
  C --- UC12
  C --- UC13
  C --- UC14

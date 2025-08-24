```mermaid
    flowchart TB
  %% Activity Diagram — College AMS (Student / Lecturer / Admin Systems)

  start([Start]):::startend
  endx([End]):::startend

  %% ===== Student System =====
  subgraph STU ["Student System"]
    ST1["Register / Update Profile"]
    ST2["Enroll in Courses"]
    ST3["View Timetable / Materials"]
    ST4["Submit Assignments"]
    ST5["View Grades & Feedback"]
  end

  %% ===== Lecturer System =====
  subgraph LEC ["Lecturer System"]
    L1["Create / Update Courses"]
    L2["Schedule & Manage Classes"]
    L3["Upload Teaching Materials"]
    L4["Grade Assignments"]
    L5["Provide Feedback"]
  end

  %% ===== Admin System =====
  subgraph ADM ["Admin System"]
    A1["Manage Student & Lecturer Records"]
    A2["Approve Course Offerings"]
    A3["Allocate Classrooms & Time Slots"]
    A4["Generate Reports"]
  end

  %% --- Student flow
  start --> ST1 --> ST2 --> ST3 --> ST4 --> ST5 --> endx

  %% --- Lecturer flow
  start --> L1 --> L2 --> L3 --> L4 --> L5 --> endx

  %% --- Admin flow
  start --> A1 --> A2 --> A3 --> A4 --> endx

  %% --- Cross-system interactions
  L3 -->|"Materials available"| ST3
  ST4 -->|"Submission received"| L4
  L5  -->|"Grades & comments"| ST5
  L2  -->|"Timetable published"| ST3
  A2  -->|"Offering approved"| L2
  A3  -->|"Room/time assigned"| L2

  %% ==== Styles ====
  classDef student fill:#dcfce7,stroke:#16a34a,color:#065f46,stroke-width:1.5px;
  classDef lecturer fill:#dbeafe,stroke:#2563eb,color:#1e3a8a,stroke-width:1.5px;
  classDef admin fill:#fef3c7,stroke:#f59e0b,color:#7c2d12,stroke-width:1.5px;
  classDef startend fill:#f3f4f6,stroke:#374151,color:#111827,stroke-width:2px;

  %% Apply classes
  class ST1,ST2,ST3,ST4,ST5 student;
  class L1,L2,L3,L4,L5 lecturer;
  class A1,A2,A3,A4 admin;

```mermaid
    flowchart TB
  %% Activity Diagram — College AMS (Two Main Activities)

  start([Start])

  %% --- Activity A: Student Learning Flow ---
  subgraph A ["Activity A - Student Learning Flow"]
    A1["Register / Update Profile"]
    A2["Enroll in Courses"]
    A3["View Timetable / Schedule"]
    A4["Submit Assignments"]
    A5["View Grades & Feedback"]
  end

  %% --- Activity B: Academic Administration Flow ---
  subgraph B ["Activity B - Academic Administration Flow"]
    B1["Create / Update Courses"]
    B2["Schedule & Manage Classes"]
    B3["Approve Course Offerings"]
    B4["Allocate Classrooms & Time Slots"]
    B5["Upload Teaching Materials"]
    B6["Grade Assignments"]
    B7["Provide Feedback"]
    B8["Generate Reports"]
  end

  endx([End])

  %% --- Main flow wiring ---
  %% Student side
  start --> A1 --> A2 --> A3 --> A4 --> A5 --> endx

  %% Admin/lecturer side
  start --> B1 --> B2 --> B3 --> B4 --> B5 --> B6 --> B7 --> B8 --> endx

  %% --- Cross-lane interactions (key handoffs) ---
  %% Materials published -> student views timetable/materials
  B5 -->|"Materials available"| A3
  %% Student submits -> lecturer grades
  A4 -->|"Submission received"| B6
  %% Lecturer feedback -> student views grades & feedback
  B7 -->|"Grades & comments"| A5

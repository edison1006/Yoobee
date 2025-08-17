-- 1. 部门
CREATE TABLE departments (
  department_id   INTEGER PRIMARY KEY,
  name            VARCHAR(100) NOT NULL UNIQUE
);

-- 2. 讲师
CREATE TABLE lecturers (
  lecturer_id     INTEGER PRIMARY KEY,
  name            VARCHAR(100) NOT NULL,
  email           VARCHAR(120),
  department_id   INTEGER,
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 3. 项目/专业
CREATE TABLE programmes (
  programme_id    INTEGER PRIMARY KEY,
  name            VARCHAR(120) NOT NULL,
  department_id   INTEGER NOT NULL,
  FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 4. 课程
CREATE TABLE courses (
  course_id       INTEGER PRIMARY KEY,
  name            VARCHAR(120) NOT NULL,
  credits         INTEGER NOT NULL CHECK (credits > 0)
);

-- 5. 项目-课程 中间表（一个项目包含多门课；一门课可在多个项目下）
CREATE TABLE programme_course (
  programme_id    INTEGER NOT NULL,
  course_id       INTEGER NOT NULL,
  PRIMARY KEY (programme_id, course_id),
  FOREIGN KEY (programme_id) REFERENCES programmes(programme_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- 6. 课程前置（自引用）
CREATE TABLE course_prerequisite (
  course_id         INTEGER NOT NULL,
  prereq_course_id  INTEGER NOT NULL,
  PRIMARY KEY (course_id, prereq_course_id),
  FOREIGN KEY (course_id)        REFERENCES courses(course_id),
  FOREIGN KEY (prereq_course_id) REFERENCES courses(course_id),
  CHECK (course_id <> prereq_course_id)
);

-- 7. 学期
CREATE TABLE semesters (
  semester_id    INTEGER PRIMARY KEY,
  name           VARCHAR(50) NOT NULL,   -- e.g., "S1", "S2", "Summer"
  year           INTEGER NOT NULL CHECK (year BETWEEN 2000 AND 2100)
);

-- 8. 教室
CREATE TABLE rooms (
  room_id        INTEGER PRIMARY KEY,
  building       VARCHAR(80) NOT NULL,
  room_number    VARCHAR(40),
  capacity       INTEGER CHECK (capacity IS NULL OR capacity > 0)
);

-- 9. 课程开设（某门课程在某学期/教室的一次开设）
CREATE TABLE course_offerings (
  offering_id    INTEGER PRIMARY KEY,
  course_id      INTEGER NOT NULL,
  semester_id    INTEGER NOT NULL,
  room_id        INTEGER,
  -- 如果不做团队授课，也可加 lecturer_id INTEGER NOT NULL
  FOREIGN KEY (course_id)   REFERENCES courses(course_id),
  FOREIGN KEY (semester_id) REFERENCES semesters(semester_id),
  FOREIGN KEY (room_id)     REFERENCES rooms(room_id)
);

-- 10. 团队授课（offering 与 lecturer 的 M–N）
CREATE TABLE offering_lecturer (
  offering_id    INTEGER NOT NULL,
  lecturer_id    INTEGER NOT NULL,
  role           VARCHAR(40),     -- e.g., "Lead", "Co"
  PRIMARY KEY (offering_id, lecturer_id),
  FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id) ON DELETE CASCADE,
  FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id)
);

-- 11. 学生
CREATE TABLE students (
  student_id     INTEGER PRIMARY KEY,
  name           VARCHAR(100) NOT NULL,
  age            INTEGER CHECK (age IS NULL OR age BETWEEN 14 AND 120),
  address        VARCHAR(200),
  email          VARCHAR(120)
);

-- 12. 选课（学生报名到具体的 offering）
CREATE TABLE enrollments (
  enrollment_id  INTEGER PRIMARY KEY,
  student_id     INTEGER NOT NULL,
  offering_id    INTEGER NOT NULL,
  enrolled_at    DATE DEFAULT CURRENT_DATE,
  UNIQUE (student_id, offering_id),
  FOREIGN KEY (student_id)  REFERENCES students(student_id) ON DELETE CASCADE,
  FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id) ON DELETE CASCADE
);

-- 13. 考勤（针对某次报名的某天）
CREATE TABLE attendance (
  attendance_id  INTEGER PRIMARY KEY,
  enrollment_id  INTEGER NOT NULL,
  attended_date  DATE NOT NULL,
  status         VARCHAR(20) NOT NULL,  -- "Present", "Absent", "Late", ...
  notes          VARCHAR(200),
  UNIQUE (enrollment_id, attended_date),
  FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id) ON DELETE CASCADE
);

-- 14. 考核任务（隶属于某个 offering）
CREATE TABLE assessments (
  assessment_id  INTEGER PRIMARY KEY,
  offering_id    INTEGER NOT NULL,
  title          VARCHAR(120) NOT NULL,
  due_at         DATE,
  weight         DECIMAL(5,2) CHECK (weight IS NULL OR (weight >= 0 AND weight <= 100)),
  FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id) ON DELETE CASCADE
);

-- 15. 提交（学生对某个 assessment 的提交与成绩）
CREATE TABLE submissions (
  submission_id  INTEGER PRIMARY KEY,
  assessment_id  INTEGER NOT NULL,
  student_id     INTEGER NOT NULL,
  submitted_at   TIMESTAMP,
  grade          DECIMAL(5,2) CHECK (grade IS NULL OR (grade >= 0 AND grade <= 100)),
  feedback       TEXT,
  UNIQUE (assessment_id, student_id),
  FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE,
  FOREIGN KEY (student_id)    REFERENCES students(student_id)   ON DELETE CASCADE
);

-- 16. 上课时间/排课（可选：一个 offering 在不同时间与教室的 meeting）
CREATE TABLE meetings (
  meeting_id     INTEGER PRIMARY KEY,
  offering_id    INTEGER NOT NULL,
  room_id        INTEGER,
  weekday        INTEGER CHECK (weekday BETWEEN 1 AND 7), -- 1=Mon ... 7=Sun
  start_time     TIME,
  end_time       TIME,
  FOREIGN KEY (offering_id) REFERENCES course_offerings(offering_id) ON DELETE CASCADE,
  FOREIGN KEY (room_id)     REFERENCES rooms(room_id)
);

-- 索引（性能建议）
CREATE INDEX idx_lecturers_dept      ON lecturers(department_id);
CREATE INDEX idx_programmes_dept     ON programmes(department_id);
CREATE INDEX idx_progcourse_course   ON programme_course(course_id);
CREATE INDEX idx_courseoff_course    ON course_offerings(course_id);
CREATE INDEX idx_courseoff_semester  ON course_offerings(semester_id);
CREATE INDEX idx_offlect_lecturer    ON offering_lecturer(lecturer_id);
CREATE INDEX idx_enroll_student      ON enrollments(student_id);
CREATE INDEX idx_enroll_offering     ON enrollments(offering_id);
CREATE INDEX idx_attendance_enroll   ON attendance(enrollment_id);
CREATE INDEX idx_assess_offering     ON assessments(offering_id);
CREATE INDEX idx_submissions_student ON submissions(student_id);

-- schema_min.sql : Yoobee College Database (Minimal DDL)

CREATE TABLE campus (
  campus_id   SERIAL PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  city        VARCHAR(100)
);

CREATE TABLE building (
  building_id SERIAL PRIMARY KEY,
  campus_id   INT NOT NULL REFERENCES campus(campus_id),
  name        VARCHAR(100) NOT NULL
);

CREATE TABLE room (
  room_id     SERIAL PRIMARY KEY,
  building_id INT NOT NULL REFERENCES building(building_id),
  number      VARCHAR(30) NOT NULL,
  capacity    INT CHECK (capacity > 0),
  UNIQUE (building_id, number)
);

CREATE TABLE school (
  school_id   SERIAL PRIMARY KEY,
  name        VARCHAR(150) NOT NULL,
  code        VARCHAR(20)  NOT NULL UNIQUE
);

CREATE TABLE programme (
  programme_id  SERIAL PRIMARY KEY,
  school_id     INT NOT NULL REFERENCES school(school_id),
  code          VARCHAR(30) NOT NULL UNIQUE,
  name          VARCHAR(200) NOT NULL,
  level         VARCHAR(20),
  credits_total INT
);

CREATE TABLE course (
  course_id   SERIAL PRIMARY KEY,
  school_id   INT NOT NULL REFERENCES school(school_id),
  code        VARCHAR(30) NOT NULL UNIQUE,
  title       VARCHAR(200) NOT NULL,
  credits     INT
);

CREATE TABLE programme_course (
  programme_id INT NOT NULL REFERENCES programme(programme_id),
  course_id    INT NOT NULL REFERENCES course(course_id),
  PRIMARY KEY (programme_id, course_id)
);

CREATE TABLE course_prerequisite (
  course_id        INT NOT NULL REFERENCES course(course_id),
  prereq_course_id INT NOT NULL REFERENCES course(course_id),
  PRIMARY KEY (course_id, prereq_course_id),
  CHECK (course_id <> prereq_course_id)
);

CREATE TABLE semester (
  semester_id SERIAL PRIMARY KEY,
  name        VARCHAR(20) NOT NULL UNIQUE,
  start_date  DATE,
  end_date    DATE
);

CREATE TABLE course_offering (
  offering_id   SERIAL PRIMARY KEY,
  course_id     INT NOT NULL REFERENCES course(course_id),
  semester_id   INT NOT NULL REFERENCES semester(semester_id),
  campus_id     INT NOT NULL REFERENCES campus(campus_id),
  section       VARCHAR(10),
  capacity      INT,
  UNIQUE (course_id, semester_id, campus_id, COALESCE(section,''))
);

CREATE TABLE lecturer (
  lecturer_id   SERIAL PRIMARY KEY,
  school_id     INT NOT NULL REFERENCES school(school_id),
  name          VARCHAR(150) NOT NULL,
  email         VARCHAR(254) UNIQUE
);

CREATE TABLE offering_lecturer (
  offering_id INT NOT NULL REFERENCES course_offering(offering_id),
  lecturer_id INT NOT NULL REFERENCES lecturer(lecturer_id),
  PRIMARY KEY (offering_id, lecturer_id)
);

CREATE TABLE student (
  student_id   SERIAL PRIMARY KEY,
  student_no   VARCHAR(30) NOT NULL UNIQUE,
  name         VARCHAR(150) NOT NULL,
  email        VARCHAR(254) UNIQUE,
  dob          DATE
);

CREATE TABLE enrollment (
  enrollment_id SERIAL PRIMARY KEY,
  student_id    INT NOT NULL REFERENCES student(student_id),
  offering_id   INT NOT NULL REFERENCES course_offering(offering_id),
  status        VARCHAR(12) DEFAULT 'Enrolled',
  grade_final   VARCHAR(5),
  UNIQUE (student_id, offering_id)
);

CREATE TABLE meeting (
  meeting_id  SERIAL PRIMARY KEY,
  offering_id INT NOT NULL REFERENCES course_offering(offering_id),
  room_id     INT REFERENCES room(room_id),
  start_time  TIMESTAMP NOT NULL,
  end_time    TIMESTAMP NOT NULL
);

CREATE TABLE attendance (
  attendance_id SERIAL PRIMARY KEY,
  enrollment_id INT NOT NULL REFERENCES enrollment(enrollment_id),
  meeting_id    INT NOT NULL REFERENCES meeting(meeting_id),
  status        VARCHAR(10) DEFAULT 'Present',
  UNIQUE (enrollment_id, meeting_id)
);

CREATE TABLE assessment (
  assessment_id SERIAL PRIMARY KEY,
  offering_id   INT NOT NULL REFERENCES course_offering(offering_id),
  name          VARCHAR(120) NOT NULL,
  weight_pct    NUMERIC(5,2),
  due_at        TIMESTAMP,
  max_score     NUMERIC(6,2)
);

CREATE TABLE submission (
  submission_id SERIAL PRIMARY KEY,
  assessment_id INT NOT NULL REFERENCES assessment(assessment_id),
  student_id    INT NOT NULL REFERENCES student(student_id),
  submitted_at  TIMESTAMP,
  score         NUMERIC(6,2),
  UNIQUE (assessment_id, student_id)
);

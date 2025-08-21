-- Minimal seed to let you run examples fast
INSERT INTO SCHOOL(name) VALUES ('School of Computing') ON CONFLICT(name) DO NOTHING;
INSERT INTO PROGRAMME(school_id, name) VALUES (1, 'MSE') ON CONFLICT(school_id, name) DO NOTHING;
INSERT INTO COURSE(school_id, code, title) VALUES (1, 'COMP601', 'Databases') ON CONFLICT(school_id, code) DO NOTHING;
INSERT INTO LECTURER(school_id, name, email) VALUES (1, 'Dr. Smith', 'smith@example.com');

INSERT INTO STUDENT(name, email) VALUES ('Alice', 'alice@example.com') ON CONFLICT(email) DO NOTHING;

INSERT INTO CAMPUS(name) VALUES ('Albany') ON CONFLICT(name) DO NOTHING;
INSERT INTO BUILDING(campus_id, name) VALUES (1, 'B1') ON CONFLICT(campus_id, name) DO NOTHING;
INSERT INTO ROOM(building_id, name, capacity) VALUES (1, 'B1-101', 40) ON CONFLICT(building_id, name) DO NOTHING;

INSERT INTO SEMESTER(name, start_date, end_date) VALUES ('2025-T1', '2025-02-24', '2025-06-01') ON CONFLICT(name) DO NOTHING;

-- Create an offering and enrollment if not exists (guarded by UNIQUE)
INSERT OR IGNORE INTO COURSE_OFFERING(course_id, semester_id, campus_id, section) VALUES (1, 1, 1, 'A');
INSERT OR IGNORE INTO ENROLLMENT(offering_id, student_id, status) VALUES (1, 1, 'ENROLLED');

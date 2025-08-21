Yoobee Colleges — Week 3, Activity 4 (University ERD)
=====================================================
Command-line application using SQLite (`sqlite3`) implementing the ERD you shared
(CAMPUS, BUILDING, ROOM, SCHOOL, PROGRAMME, COURSE, LECTURER, SEMESTER,
COURSE_OFFERING, ENROLLMENT, etc.).

This CLI supports **init-db**, **seed**, and at least three functions: **add**, **view**, **delete**
across multiple tables.

## Entities covered by CLI commands
- SCHOOL, PROGRAMME, COURSE
- LECTURER, STUDENT
- CAMPUS, BUILDING, ROOM
- SEMESTER, COURSE_OFFERING
- ENROLLMENT (junction table Student↔CourseOffering)

> The schema also defines additional junction tables from the ERD for completeness:
> PROGRAMME_COURSE, COURSE_PREREQUISITE (self-ref), OFFERING_LECTURER,
> MEETING, ASSESSMENT, SUBMISSION, ATTENDANCE.

## Quick Start
```bash
python app.py init-db
python app.py seed

# Add samples
python app.py add school --name "School of Computing"
python app.py add programme --school_id 1 --name "MSE"
python app.py add course --school_id 1 --code "COMP601" --title "Databases"
python app.py add lecturer --school_id 1 --name "Dr. Smith"
python app.py add student --name "Alice" --email "alice@example.com"

python app.py add campus --name "Albany"
python app.py add building --campus_id 1 --name "B1"
python app.py add room --building_id 1 --name "B1-101" --capacity 40

python app.py add semester --name "2025-T1" --start "2025-02-24" --end "2025-06-01"
python app.py add offering --course_id 1 --semester_id 1 --campus_id 1 --section "A"
python app.py add enrollment --offering_id 1 --student_id 1 --status "ENROLLED"

# View
python app.py view schools
python app.py view programmes
python app.py view courses
python app.py view lecturers
python app.py view students
python app.py view campuses
python app.py view buildings
python app.py view rooms
python app.py view semesters
python app.py view offerings
python app.py view enrollments

# Delete (example)
python app.py delete course --id 1
python app.py delete enrollment --offering_id 1 --student_id 1
```

## Tech Notes
- Pure stdlib: `sqlite3`, `argparse`, `pathlib`.
- `schema.sql` mirrors your ERD with foreign keys and junction tables.
- `app.py` contains subcommands and validates minimal required fields.
- Cascade behavior is intentional on some relationships for convenient cleanup
  (e.g., deleting a SCHOOL may delete its PROGRAMMES/COURSES). Adjust as needed.

## Upload to GitHub
```bash
git init
git add .
git commit -m "Week 3 – Activity 4: University ERD SQLite CLI"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

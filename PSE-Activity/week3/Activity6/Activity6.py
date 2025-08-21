import argparse
from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).with_name("university.sqlite3")
ROOT = Path(__file__).parent

def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON;")
    return c

def init_db():
    sql = (ROOT / "schema.sql").read_text(encoding="utf-8")
    with conn() as c:
        c.executescript(sql)
        c.commit()

def seed_db():
    init_db()
    sql = (ROOT / "sample_data.sql").read_text(encoding="utf-8")
    with conn() as c:
        c.executescript(sql)
        c.commit()

def table_print(rows, headers):
    if not rows:
        print("No rows.")
        return
    widths = [len(h) for h in headers]
    for r in rows:
        for i, h in enumerate(headers):
            widths[i] = max(widths[i], len(str(r[h])))
    def line(ch='-'):
        return '+' + '+'.join(ch * (w+2) for w in widths) + '+'
    print(line('-'))
    print('| ' + ' | '.join(h.ljust(widths[i]) for i, h in enumerate(headers)) + ' |')
    print(line('='))
    for r in rows:
        print('| ' + ' | '.join(str(r[h]).ljust(widths[i]) for i, h in enumerate(headers)) + ' |')
        print(line('-'))

# ---------- add commands ----------
def add_school(args):
    with conn() as c:
        cur = c.execute("INSERT INTO SCHOOL(name) VALUES (?)", (args.name,))
        c.commit()
        print("SCHOOL id=", cur.lastrowid)

def add_programme(args):
    with conn() as c:
        cur = c.execute("INSERT INTO PROGRAMME(school_id, name) VALUES (?, ?)", (args.school_id, args.name))
        c.commit()
        print("PROGRAMME id=", cur.lastrowid)

def add_course(args):
    with conn() as c:
        cur = c.execute(
            "INSERT INTO COURSE(school_id, code, title) VALUES (?, ?, ?)",
            (args.school_id, args.code, args.title),
        )
        c.commit()
        print("COURSE id=", cur.lastrowid)

def add_lecturer(args):
    with conn() as c:
        cur = c.execute(
            "INSERT INTO LECTURER(school_id, name, email) VALUES (?, ?, ?)",
            (args.school_id, args.name, args.email),
        )
        c.commit()
        print("LECTURER id=", cur.lastrowid)

def add_student(args):
    with conn() as c:
        cur = c.execute("INSERT INTO STUDENT(name, email) VALUES (?, ?)", (args.name, args.email))
        c.commit()
        print("STUDENT id=", cur.lastrowid)

def add_campus(args):
    with conn() as c:
        cur = c.execute("INSERT INTO CAMPUS(name) VALUES (?)", (args.name,))
        c.commit()
        print("CAMPUS id=", cur.lastrowid)

def add_building(args):
    with conn() as c:
        cur = c.execute("INSERT INTO BUILDING(campus_id, name) VALUES (?, ?)", (args.campus_id, args.name))
        c.commit()
        print("BUILDING id=", cur.lastrowid)

def add_room(args):
    with conn() as c:
        cur = c.execute(
            "INSERT INTO ROOM(building_id, name, capacity) VALUES (?, ?, ?)",
            (args.building_id, args.name, args.capacity),
        )
        c.commit()
        print("ROOM id=", cur.lastrowid)

def add_semester(args):
    with conn() as c:
        cur = c.execute(
            "INSERT INTO SEMESTER(name, start_date, end_date) VALUES (?, ?, ?)",
            (args.name, args.start, args.end),
        )
        c.commit()
        print("SEMESTER id=", cur.lastrowid)

def add_offering(args):
    with conn() as c:
        cur = c.execute(
            "INSERT INTO COURSE_OFFERING(course_id, semester_id, campus_id, section) VALUES (?, ?, ?, ?)",
            (args.course_id, args.semester_id, args.campus_id, args.section),
        )
        c.commit()
        print("OFFERING id=", cur.lastrowid)

def add_enrollment(args):
    with conn() as c:
        cur = c.execute(
            "INSERT INTO ENROLLMENT(offering_id, student_id, status) VALUES (?, ?, ?)",
            (args.offering_id, args.student_id, args.status),
        )
        c.commit()
        print("ENROLLMENT id=", cur.lastrowid)

# ---------- view commands ----------
def view_table(sql, headers):
    with conn() as c:
        rows = c.execute(sql).fetchall()
    table_print(rows, headers)

# ---------- delete commands ----------
def del_by_id(table, id_value):
    with conn() as c:
        cur = c.execute(f"DELETE FROM {table} WHERE id = ?", (id_value,))
        c.commit()
        print(f"Deleted rows: {cur.rowcount}")

def del_enrollment(args):
    with conn() as c:
        cur = c.execute(
            "DELETE FROM ENROLLMENT WHERE offering_id = ? AND student_id = ?",
            (args.offering_id, args.student_id),
        )
        c.commit()
        print(f"Deleted rows: {cur.rowcount}")

def build_parser():
    p = argparse.ArgumentParser(description="Week 3 — Activity 4: University ERD SQLite CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init-db"); sp.set_defaults(func=lambda a: (init_db(), print("DB initialized at", DB_PATH)))
    sp = sub.add_parser("seed");    sp.set_defaults(func=lambda a: (seed_db(), print("Seed done.")))

    # add
    add = sub.add_parser("add"); add_sub = add.add_subparsers(dest="entity", required=True)

    sp = add_sub.add_parser("school");   sp.add_argument("--name", required=True); sp.set_defaults(func=add_school)
    sp = add_sub.add_parser("programme");sp.add_argument("--school_id", type=int, required=True); sp.add_argument("--name", required=True); sp.set_defaults(func=add_programme)
    sp = add_sub.add_parser("course");   sp.add_argument("--school_id", type=int, required=True); sp.add_argument("--code", required=True); sp.add_argument("--title", required=True); sp.set_defaults(func=add_course)
    sp = add_sub.add_parser("lecturer"); sp.add_argument("--school_id", type=int, required=True); sp.add_argument("--name", required=True); sp.add_argument("--email", default=None); sp.set_defaults(func=add_lecturer)
    sp = add_sub.add_parser("student");  sp.add_argument("--name", required=True); sp.add_argument("--email", required=True); sp.set_defaults(func=add_student)
    sp = add_sub.add_parser("campus");   sp.add_argument("--name", required=True); sp.set_defaults(func=add_campus)
    sp = add_sub.add_parser("building"); sp.add_argument("--campus_id", type=int, required=True); sp.add_argument("--name", required=True); sp.set_defaults(func=add_building)
    sp = add_sub.add_parser("room");     sp.add_argument("--building_id", type=int, required=True); sp.add_argument("--name", required=True); sp.add_argument("--capacity", type=int, default=0); sp.set_defaults(func=add_room)
    sp = add_sub.add_parser("semester"); sp.add_argument("--name", required=True); sp.add_argument("--start", required=True); sp.add_argument("--end", required=True); sp.set_defaults(func=add_semester)
    sp = add_sub.add_parser("offering"); sp.add_argument("--course_id", type=int, required=True); sp.add_argument("--semester_id", type=int, required=True); sp.add_argument("--campus_id", type=int, required=True); sp.add_argument("--section", required=True); sp.set_defaults(func=add_offering)
    sp = add_sub.add_parser("enrollment"); sp.add_argument("--offering_id", type=int, required=True); sp.add_argument("--student_id", type=int, required=True); sp.add_argument("--status", default="ENROLLED"); sp.set_defaults(func=add_enrollment)

    # view
    view = sub.add_parser("view"); view_sub = view.add_subparsers(dest="entity", required=True)
    view_sub.add_parser("schools").set_defaults(func=lambda a: view_table("SELECT * FROM SCHOOL ORDER BY id", ["id","name"]))
    view_sub.add_parser("programmes").set_defaults(func=lambda a: view_table("SELECT p.id, s.name AS school, p.name FROM PROGRAMME p JOIN SCHOOL s ON s.id=p.school_id ORDER BY p.id", ["id","school","name"]))
    view_sub.add_parser("courses").set_defaults(func=lambda a: view_table("SELECT c.id, s.name AS school, c.code, c.title FROM COURSE c JOIN SCHOOL s ON s.id=c.school_id ORDER BY c.id", ["id","school","code","title"]))
    view_sub.add_parser("lecturers").set_defaults(func=lambda a: view_table("SELECT l.id, s.name AS school, l.name, l.email FROM LECTURER l JOIN SCHOOL s ON s.id=l.school_id ORDER BY l.id", ["id","school","name","email"]))
    view_sub.add_parser("students").set_defaults(func=lambda a: view_table("SELECT * FROM STUDENT ORDER BY id", ["id","name","email"]))
    view_sub.add_parser("campuses").set_defaults(func=lambda a: view_table("SELECT * FROM CAMPUS ORDER BY id", ["id","name"]))
    view_sub.add_parser("buildings").set_defaults(func=lambda a: view_table("SELECT b.id, c.name AS campus, b.name FROM BUILDING b JOIN CAMPUS c ON c.id=b.campus_id ORDER BY b.id", ["id","campus","name"]))
    view_sub.add_parser("rooms").set_defaults(func=lambda a: view_table("SELECT r.id, b.name AS building, r.name, r.capacity FROM ROOM r JOIN BUILDING b ON b.id=r.building_id ORDER BY r.id", ["id","building","name","capacity"]))
    view_sub.add_parser("semesters").set_defaults(func=lambda a: view_table("SELECT * FROM SEMESTER ORDER BY id", ["id","name","start_date","end_date"]))
    view_sub.add_parser("offerings").set_defaults(func=lambda a: view_table("SELECT o.id, c.code AS course, s.name AS semester, cp.name AS campus, o.section FROM COURSE_OFFERING o JOIN COURSE c ON c.id=o.course_id JOIN SEMESTER s ON s.id=o.semester_id JOIN CAMPUS cp ON cp.id=o.campus_id ORDER BY o.id", ["id","course","semester","campus","section"]))
    view_sub.add_parser("enrollments").set_defaults(func=lambda a: view_table("SELECT e.id, st.name AS student, c.code AS course, se.name AS semester, e.status FROM ENROLLMENT e JOIN STUDENT st ON st.id=e.student_id JOIN COURSE_OFFERING o ON o.id=e.offering_id JOIN COURSE c ON c.id=o.course_id JOIN SEMESTER se ON se.id=o.semester_id ORDER BY e.id", ["id","student","course","semester","status"]))

    # delete
    delete = sub.add_parser("delete"); del_sub = delete.add_subparsers(dest="entity", required=True)
    for tab in ["school","programme","course","lecturer","student","campus","building","room","semester","offering"]:
        sp = del_sub.add_parser(tab); sp.add_argument("--id", type=int, required=True); sp.set_defaults(func=lambda a, t=tab.upper(): del_by_id(t, a.id))
    sp = del_sub.add_parser("enrollment"); sp.add_argument("--offering_id", type=int, required=True); sp.add_argument("--student_id", type=int, required=True); sp.set_defaults(func=del_enrollment)

    return p

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()

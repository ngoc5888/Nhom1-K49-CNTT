import sqlite3
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lms.db")
print("path", p)
print("exists", os.path.exists(p), "size", os.path.getsize(p) if os.path.exists(p) else 0)
conn = sqlite3.connect(p)
conn.row_factory = sqlite3.Row
c = conn.cursor()
print("users", c.execute("select count(*) from users").fetchone()[0])
print("students", c.execute("select count(*) from students").fetchone()[0])
rows = c.execute(
    """
    select u.id, u.email, u.full_name, u.role, u.is_active, s.student_code
    from users u
    left join students s on s.user_id = u.id
    where u.role = 'student'
    order by u.id
    limit 12
    """
).fetchall()
for r in rows:
    d = dict(r)
    d["full_name"] = (d.get("full_name") or "").encode("ascii", "replace").decode()
    print(d)
r = c.execute("select id, email, role, is_active from users where email = 'student@example.com'").fetchone()
print("demo", dict(r) if r else "MISSING")
orphans = c.execute(
    """
    select u.id, u.email from users u
    where u.role = 'student'
      and not exists (select 1 from students s where s.user_id = u.id)
    """
).fetchall()
print("orphan students", [dict(x) for x in orphans])
from werkzeug.security import check_password_hash
for email, pw in [
    ("student@example.com", "student123"),
    ("student@example.com", "demo123"),
    ("teacher@example.com", "teacher123"),
    ("teacher@example.com", "demo123"),
    ("admin@example.com", "admin123"),
    ("admin@example.com", "demo123"),
]:
    row = c.execute("select password_hash from users where email = ?", (email,)).fetchone()
    print(email, pw, check_password_hash(row[0], pw) if row else "MISSING")

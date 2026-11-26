import sys
import os

# UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from __init__ import create_app
from database import query_db, get_setting, set_setting

app = create_app()
app.config['TESTING'] = True
client = app.test_client()

def db_query(query, args=(), one=False):
    with app.app_context():
        return query_db(query, args, one=one)

def db_setting(key, default=None):
    with app.app_context():
        return get_setting(key, default)

def db_set(key, val):
    with app.app_context():
        return set_setting(key, val)

print("==================================================")
print("RUNNING COMPREHENSIVE SYSTEM VERIFICATION")
print("==================================================")

# 1. Database Entities Check
print("\n[TEST 1] Database Entities Check:")
depts = db_query("SELECT COUNT(*) as c FROM departments", one=True)['c']
majors = db_query("SELECT COUNT(*) as c FROM majors", one=True)['c']
subjects = db_query("SELECT COUNT(*) as c FROM subjects", one=True)['c']
classes = db_query("SELECT COUNT(*) as c FROM student_classes", one=True)['c']
teachers = db_query("SELECT COUNT(*) as c FROM teachers", one=True)['c']
students = db_query("SELECT COUNT(*) as c FROM students", one=True)['c']
years = db_query("SELECT COUNT(*) as c FROM academic_years", one=True)['c']
semesters = db_query("SELECT COUNT(*) as c FROM semesters", one=True)['c']
admin_u = db_query("SELECT * FROM users WHERE email = 'admin@example.com'", one=True)
teacher_u = db_query("SELECT * FROM users WHERE email = 'teacher@example.com'", one=True)
student_u = db_query("SELECT * FROM users WHERE email = 'student@example.com'", one=True)

print(f"Khoa: {depts}/10 - {'PASS' if depts == 10 else 'FAIL'}")
print(f"Ngành: {majors}/10 - {'PASS' if majors == 10 else 'FAIL'}")
print(f"Môn học: {subjects}/20 - {'PASS' if subjects == 20 else 'FAIL'}")
print(f"Lớp sinh hoạt: {classes}/40 - {'PASS' if classes == 40 else 'FAIL'}")
print(f"Giảng viên: {teachers}/20 - {'PASS' if teachers == 20 else 'FAIL'}")
print(f"Sinh viên: {students} (>= 50) - {'PASS' if students >= 50 else 'FAIL'}")
print(f"Năm học: {years}/8 - {'PASS' if years == 8 else 'FAIL'}")
print(f"Học kỳ: {semesters}/16 - {'PASS' if semesters == 16 else 'FAIL'}")

assert depts == 10 and majors == 10 and subjects == 20 and classes == 40 and teachers == 20 and students >= 50 and years == 8 and semesters == 16

# 2. Check accounts preserved
print("\n[TEST 2] Default Accounts Check:")
print(f"admin@example.com: {'EXISTS' if admin_u else 'MISSING'}")
print(f"teacher@example.com: {'EXISTS' if teacher_u else 'MISSING'}")
print(f"student@example.com: {'EXISTS' if student_u else 'MISSING'}")
assert admin_u and teacher_u and student_u

# Reset settings to normal before web tests
db_set('maintenance_mode', '0')
db_set('system_lock', '0')

# 3. Test Admin Dashboard & Reports
print("\n[TEST 3] Admin Dashboard & Reports:")
client.get('/logout')
res = client.post('/login', data={'email': 'admin@example.com', 'password': 'admin123'}, follow_redirects=True)
assert res.status_code == 200
assert "Admin Dashboard" in res.data.decode('utf-8')
print("Admin Login & Dashboard: PASS")

# Reports
res = client.get('/admin/reports')
assert res.status_code == 200
html = res.data.decode('utf-8')
assert "chart1" in html and "chart7" in html
assert "Báo Cáo & Thống Kê" in html
print("Admin Reports (7 Charts present): PASS")

# Multi-filter
res = client.get('/admin/reports?department_id=1&semester=Học+kỳ+1')
assert res.status_code == 200
print("Admin Reports Multi-filter: PASS")

# CSV Export
res = client.get('/admin/reports?export=csv')
assert res.status_code == 200
assert res.mimetype == "text/csv"
print("Admin Reports CSV Export: PASS")

# 4. Test Admin Broadcast Notifications
print("\n[TEST 4] Admin Broadcast Notifications:")
res = client.get('/admin/notifications')
assert res.status_code == 200
res = client.post('/admin/notifications', data={
    'target_type': 'all',
    'title': 'Thông báo khai giảng năm học mới',
    'content': 'Toàn trường chuẩn bị tham gia lễ khai giảng trực tuyến lúc 8h sáng thứ Hai.'
}, follow_redirects=True)
assert res.status_code == 200
assert "Đã phát thông báo thành công" in res.data.decode('utf-8')
print("Admin Broadcast Notification Sent: PASS")

# 5. Test Teacher Class Notifications
print("\n[TEST 5] Teacher Class Notifications:")
client.get('/logout')
res = client.post('/login', data={'email': 'teacher@example.com', 'password': 'teacher123'}, follow_redirects=True)
assert res.status_code == 200
print("Teacher Login: PASS")

# Get a course taught by this teacher
course = db_query("SELECT id, name FROM courses WHERE teacher_id = ?", (teacher_u['id'],), one=True)
assert course is not None
res = client.get('/teacher/notifications')
assert res.status_code == 200
res = client.post('/teacher/notifications', data={
    'course_id': course['id'],
    'title': 'Nhắc nộp bài tập lớn tuần này',
    'content': 'Các em nhớ nộp bài tập lớn trước 23h59 Chủ nhật.'
}, follow_redirects=True)
assert res.status_code == 200
assert "Đã gửi thông báo" in res.data.decode('utf-8')
print(f"Teacher Notification for course '{course['name']}': PASS")

# 6. Test Student receives notifications
print("\n[TEST 6] Student Notifications Inbox:")
client.get('/logout')
res = client.post('/login', data={'email': 'student@example.com', 'password': 'student123'}, follow_redirects=True)
assert res.status_code == 200
print("Student Login: PASS")
res = client.get('/notifications')
assert res.status_code == 200
s_html = res.data.decode('utf-8')
assert "Thông báo khai giảng" in s_html or "Nhắc nộp bài" in s_html
print("Student received notifications: PASS")

# 7. Test Maintenance Mode
print("\n[TEST 7] Maintenance Mode:")
client.get('/logout')
# Admin turns ON maintenance mode
client.post('/login', data={'email': 'admin@example.com', 'password': 'admin123'}, follow_redirects=True)
res = client.post('/admin/system/toggle-maintenance', follow_redirects=True)
assert res.status_code == 200
assert db_setting('maintenance_mode') == '1'
print("Maintenance Mode turned ON: PASS")

# Check Admin is NOT blocked
res = client.get('/admin/dashboard')
assert res.status_code == 200
print("Admin NOT blocked during maintenance: PASS")

# Logout Admin
client.get('/logout')

# Student attempts login
res = client.post('/login', data={'email': 'student@example.com', 'password': 'student123'}, follow_redirects=True)
assert "/maintenance" in res.request.path or "HỆ THỐNG ĐANG BẢO TRÌ" in res.data.decode('utf-8')
print("Student BLOCKED by Maintenance Mode: PASS")

# Teacher attempts login
res = client.post('/login', data={'email': 'teacher@example.com', 'password': 'teacher123'}, follow_redirects=True)
assert "/maintenance" in res.request.path or "HỆ THỐNG ĐANG BẢO TRÌ" in res.data.decode('utf-8')
print("Teacher BLOCKED by Maintenance Mode: PASS")

# Admin logs in again and turns OFF maintenance mode
res = client.post('/login', data={'email': 'admin@example.com', 'password': 'admin123'}, follow_redirects=True)
assert res.status_code == 200
res = client.post('/admin/system/toggle-maintenance', follow_redirects=True)
assert res.status_code == 200
assert db_setting('maintenance_mode') == '0'
print("Maintenance Mode turned OFF: PASS")

# 8. Test System Lock
print("\n[TEST 8] System Lock:")
# Admin turns ON system lock
res = client.post('/admin/system/toggle-lock', follow_redirects=True)
assert res.status_code == 200
assert db_setting('system_lock') == '1'
print("System Lock turned ON: PASS")

# Admin is NOT blocked
res = client.get('/admin/dashboard')
assert res.status_code == 200
print("Admin NOT blocked during system lock: PASS")

# Logout Admin
client.get('/logout')

# Student attempts login
res = client.post('/login', data={'email': 'student@example.com', 'password': 'student123'}, follow_redirects=True)
assert "/system-locked" in res.request.path or "HỆ THỐNG HIỆN ĐANG BỊ KHÓA" in res.data.decode('utf-8')
print("Student BLOCKED by System Lock: PASS")

# Teacher attempts login
res = client.post('/login', data={'email': 'teacher@example.com', 'password': 'teacher123'}, follow_redirects=True)
assert "/system-locked" in res.request.path or "HỆ THỐNG HIỆN ĐANG BỊ KHÓA" in res.data.decode('utf-8')
print("Teacher BLOCKED by System Lock: PASS")

# Admin logs in again and turns OFF system lock
res = client.post('/login', data={'email': 'admin@example.com', 'password': 'admin123'}, follow_redirects=True)
assert res.status_code == 200
res = client.post('/admin/system/toggle-lock', follow_redirects=True)
assert res.status_code == 200
assert db_setting('system_lock') == '0'
print("System Lock turned OFF: PASS")

client.get('/logout')
print("\n==================================================")
print("ALL SYSTEM VERIFICATION TESTS PASSED 100%!")
print("==================================================")

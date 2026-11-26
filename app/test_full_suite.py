import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from __init__ import create_app

app = create_app()
app.config['TESTING'] = True
client = app.test_client()

print("Testing Student Routes...")
client.get('/logout')
res = client.post('/login', data={'email': 'student@example.com', 'password': 'student123'}, follow_redirects=True)
assert res.status_code == 200

student_routes = [
    '/student/dashboard',
    '/student/classes',
    '/student/class/1',
    '/student/materials',
    '/student/assignments',
    '/student/exams',
    '/student/academic-results',
    '/notifications',
    '/profile'
]
for route in student_routes:
    res = client.get(route)
    assert res.status_code == 200, f"Route {route} returned {res.status_code}"
    print(f"  {route}: OK (200)")

print("\nTesting Teacher Routes...")
client.get('/logout')
res = client.post('/login', data={'email': 'teacher@example.com', 'password': 'teacher123'}, follow_redirects=True)
assert res.status_code == 200

teacher_routes = [
    '/teacher/dashboard',
    '/teacher/classes',
    '/teacher/materials',
    '/teacher/assignments',
    '/teacher/exams',
    '/teacher/grades',
    '/teacher/notifications',
    '/notifications',
    '/profile'
]
for route in teacher_routes:
    res = client.get(route)
    assert res.status_code == 200, f"Route {route} returned {res.status_code}"
    print(f"  {route}: OK (200)")

print("\nTesting Admin Routes...")
client.get('/logout')
res = client.post('/login', data={'email': 'admin@example.com', 'password': 'admin123'}, follow_redirects=True)
assert res.status_code == 200

admin_routes = [
    '/admin/dashboard',
    '/admin/users',
    '/admin/education',
    '/admin/reports',
    '/admin/notifications',
    '/notifications',
    '/profile'
]
for route in admin_routes:
    res = client.get(route)
    assert res.status_code == 200, f"Route {route} returned {res.status_code}"
    print(f"  {route}: OK (200)")

print("\nTesting Public Maintenance & System Lock Pages...")
client.get('/logout')
for route in ['/maintenance', '/system-locked', '/login', '/forgot-password']:
    res = client.get(route)
    assert res.status_code == 200, f"Route {route} returned {res.status_code}"
    print(f"  {route}: OK (200)")

print("\nALL 27 APPLICATION ROUTES TESTED AND RETURNED 200 OK!")

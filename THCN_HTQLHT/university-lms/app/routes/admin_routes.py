from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from werkzeug.security import generate_password_hash
from database import query_db, execute_db
from auth import login_required, role_required

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    total_students = query_db("SELECT COUNT(*) as count FROM users WHERE role = 'student'", one=True)['count']
    total_teachers = query_db("SELECT COUNT(*) as count FROM users WHERE role = 'teacher'", one=True)['count']
    total_courses = query_db("SELECT COUNT(*) as count FROM courses", one=True)['count']
    total_subjects = query_db("SELECT COUNT(*) as count FROM subjects", one=True)['count']
    total_materials = query_db("SELECT COUNT(*) as count FROM materials", one=True)['count']
    total_assignments = query_db("SELECT COUNT(*) as count FROM assignments", one=True)['count']

    # Chart data 1: Students by Major
    major_stats = query_db("""
        SELECT m.name as major_name, COUNT(s.user_id) as student_count
        FROM majors m
        LEFT JOIN students s ON m.id = s.major_id
        GROUP BY m.id
    """)

    # Chart data 2: Courses by Department
    dept_stats = query_db("""
        SELECT d.name as dept_name, COUNT(c.id) as course_count
        FROM departments d
        LEFT JOIN subjects sub ON d.id = sub.department_id
        LEFT JOIN courses c ON sub.id = c.subject_id
        GROUP BY d.id
    """)

    recent_users = query_db("SELECT * FROM users ORDER BY created_at DESC LIMIT 6")

    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_teachers=total_teachers,
        total_courses=total_courses,
        total_subjects=total_subjects,
        total_materials=total_materials,
        total_assignments=total_assignments,
        major_stats=major_stats,
        dept_stats=dept_stats,
        recent_users=recent_users
    )

@admin_bp.route('/users')
@login_required
@role_required('admin')
def users():
    role_filter = request.args.get('role', '')
    search = request.args.get('search', '').strip()

    query = """
        SELECT u.*,
               s.student_code, t.teacher_code,
               sc.name as class_name, d.name as dept_name
        FROM users u
        LEFT JOIN students s ON u.id = s.user_id
        LEFT JOIN student_classes sc ON s.student_class_id = sc.id
        LEFT JOIN teachers t ON u.id = t.user_id
        LEFT JOIN departments d ON s.department_id = d.id OR t.department_id = d.id
        WHERE 1=1
    """
    params = []

    if role_filter:
        query += " AND u.role = ?"
        params.append(role_filter)
    if search:
        query += " AND (u.full_name LIKE ? OR u.email LIKE ? OR s.student_code LIKE ? OR t.teacher_code LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"])

    query += " ORDER BY u.id DESC"
    users_list = query_db(query, params)

    departments = query_db("SELECT * FROM departments ORDER BY name ASC")
    student_classes = query_db("SELECT * FROM student_classes ORDER BY name ASC")

    return render_template(
        'admin/users.html',
        users=users_list,
        departments=departments,
        student_classes=student_classes,
        selected_role=role_filter,
        search=search
    )

@admin_bp.route('/user/create', methods=['POST'])
@login_required
@role_required('admin')
def create_user():
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    role = request.form.get('role', 'student')
    password = request.form.get('password', '123456')
    dept_id = request.form.get('department_id')
    class_id = request.form.get('student_class_id')

    if not full_name or not email:
        flash("Vui lòng điền Họ tên và Email.", "danger")
        return redirect(url_for('admin_bp.users'))

    existing = query_db("SELECT id FROM users WHERE email = ?", (email,), one=True)
    if existing:
        flash(f"Email {email} đã tồn tại trong hệ thống.", "danger")
        return redirect(url_for('admin_bp.users'))

    pass_hash = generate_password_hash(password)
    user_id = execute_db("""
        INSERT INTO users (email, password_hash, full_name, role, phone)
        VALUES (?, ?, ?, ?, ?)
    """, (email, pass_hash, full_name, role, phone))

    if role == 'student':
        code = f"SV2024{user_id:04d}"
        execute_db("INSERT INTO students (user_id, student_code, department_id, student_class_id) VALUES (?, ?, ?, ?)",
                   (user_id, code, dept_id if dept_id else None, class_id if class_id else None))
    elif role == 'teacher':
        code = f"GV2024{user_id:03d}"
        execute_db("INSERT INTO teachers (user_id, teacher_code, department_id) VALUES (?, ?, ?)",
                   (user_id, code, dept_id if dept_id else None))

    flash(f"Tạo người dùng {full_name} ({role}) thành công!", "success")
    return redirect(url_for('admin_bp.users'))

@admin_bp.route('/user/<int:user_id>/toggle-status')
@login_required
@role_required('admin')
def toggle_user_status(user_id):
    user = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
    if user:
        new_status = 0 if user['is_active'] else 1
        execute_db("UPDATE users SET is_active = ? WHERE id = ?", (new_status, user_id))
        status_str = "Mở khóa" if new_status else "Khóa"
        flash(f"Đã {status_str} tài khoản {user['email']}.", "info")
    return redirect(url_for('admin_bp.users'))

@admin_bp.route('/user/<int:user_id>/delete')
@login_required
@role_required('admin')
def delete_user(user_id):
    execute_db("DELETE FROM users WHERE id = ?", (user_id,))
    flash("Đã xóa người dùng khỏi hệ thống.", "success")
    return redirect(url_for('admin_bp.users'))

@admin_bp.route('/education')
@login_required
@role_required('admin')
def education():
    departments = query_db("SELECT d.*, (SELECT COUNT(*) FROM majors WHERE department_id = d.id) as major_count FROM departments d ORDER BY d.id DESC")
    majors = query_db("SELECT m.*, d.name as dept_name FROM majors m JOIN departments d ON m.department_id = d.id ORDER BY m.id DESC")
    student_classes = query_db("SELECT c.*, m.name as major_name FROM student_classes c JOIN majors m ON c.major_id = m.id ORDER BY c.id DESC")
    subjects = query_db("SELECT s.*, d.name as dept_name FROM subjects s LEFT JOIN departments d ON s.department_id = d.id ORDER BY s.id DESC")
    courses = query_db("""
        SELECT c.*, sub.name as subject_name, u.full_name as teacher_name,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as student_count
        FROM courses c
        JOIN subjects sub ON c.subject_id = sub.id
        JOIN users u ON c.teacher_id = u.id
        ORDER BY c.id DESC
    """)

    teachers = query_db("SELECT id, full_name FROM users WHERE role = 'teacher'")

    return render_template(
        'admin/education.html',
        departments=departments,
        majors=majors,
        student_classes=student_classes,
        subjects=subjects,
        courses=courses,
        teachers=teachers
    )

@admin_bp.route('/department/create', methods=['POST'])
@login_required
@role_required('admin')
def create_department():
    code = request.form.get('code', '').strip()
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    if code and name:
        execute_db("INSERT INTO departments (code, name, description) VALUES (?, ?, ?)", (code, name, description))
        flash(f"Thêm Khoa {name} thành công!", "success")
    return redirect(url_for('admin_bp.education'))

@admin_bp.route('/major/create', methods=['POST'])
@login_required
@role_required('admin')
def create_major():
    dept_id = request.form.get('department_id')
    code = request.form.get('code', '').strip()
    name = request.form.get('name', '').strip()
    if dept_id and code and name:
        execute_db("INSERT INTO majors (department_id, code, name) VALUES (?, ?, ?)", (dept_id, code, name))
        flash(f"Thêm Ngành {name} thành công!", "success")
    return redirect(url_for('admin_bp.education'))

@admin_bp.route('/subject/create', methods=['POST'])
@login_required
@role_required('admin')
def create_subject():
    dept_id = request.form.get('department_id')
    code = request.form.get('code', '').strip()
    name = request.form.get('name', '').strip()
    credits = int(request.form.get('credits', 3))
    description = request.form.get('description', '').strip()
    if code and name:
        execute_db("INSERT INTO subjects (department_id, code, name, credits, description) VALUES (?, ?, ?, ?, ?)",
                   (dept_id if dept_id else None, code, name, credits, description))
        flash(f"Thêm Môn học {name} thành công!", "success")
    return redirect(url_for('admin_bp.education'))

@admin_bp.route('/reports')
@login_required
@role_required('admin')
def reports():
    export_format = request.args.get('export')

    grade_summary = query_db("""
        SELECT u.full_name, st.student_code, c.name as course_name, g.total_score, g.letter_grade
        FROM grades g
        JOIN users u ON g.student_id = u.id
        LEFT JOIN students st ON u.id = st.user_id
        JOIN courses c ON g.course_id = c.id
        ORDER BY g.total_score DESC
    """)

    if export_format == 'csv':
        csv_data = "Mã Sinh Viên,Họ và Tên,Lớp Học Phần,Điểm Tổng Kết,Xếp Loại\n"
        for row in grade_summary:
            csv_data += f"{row['student_code']},{row['full_name']},{row['course_name']},{row['total_score']},{row['letter_grade']}\n"
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=bao_cao_bang_diem.csv"}
        )

    return render_template('admin/reports.html', grade_summary=grade_summary)

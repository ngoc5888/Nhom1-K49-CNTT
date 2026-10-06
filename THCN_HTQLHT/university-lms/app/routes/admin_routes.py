from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, jsonify
from werkzeug.security import generate_password_hash
from database import query_db, execute_db, get_setting, set_setting
from auth import login_required, role_required, get_current_user

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    total_students = query_db("SELECT COUNT(*) as count FROM users WHERE role = 'student'", one=True)['count']
    total_teachers = query_db("SELECT COUNT(*) as count FROM users WHERE role = 'teacher'", one=True)['count']
    total_departments = query_db("SELECT COUNT(*) as count FROM departments", one=True)['count']
    total_majors = query_db("SELECT COUNT(*) as count FROM majors", one=True)['count']
    total_subjects = query_db("SELECT COUNT(*) as count FROM subjects", one=True)['count']
    total_student_classes = query_db("SELECT COUNT(*) as count FROM student_classes", one=True)['count']
    total_courses = query_db("SELECT COUNT(*) as count FROM courses", one=True)['count']
    total_active_users = query_db("SELECT COUNT(*) as count FROM users WHERE is_active = 1", one=True)['count']
    total_locked_users = query_db("SELECT COUNT(*) as count FROM users WHERE is_active = 0", one=True)['count']
    total_notifications = query_db("SELECT COUNT(*) as count FROM notifications", one=True)['count']
    total_academic_years = query_db("SELECT COUNT(*) as count FROM academic_years", one=True)['count']
    total_semesters = query_db("SELECT COUNT(*) as count FROM semesters", one=True)['count']
    total_materials = query_db("SELECT COUNT(*) as count FROM materials", one=True)['count']
    total_assignments = query_db("SELECT COUNT(*) as count FROM assignments", one=True)['count']

    maintenance_mode = get_setting('maintenance_mode', '0')
    system_lock = get_setting('system_lock', '0')

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
        total_departments=total_departments,
        total_majors=total_majors,
        total_subjects=total_subjects,
        total_student_classes=total_student_classes,
        total_courses=total_courses,
        total_active_users=total_active_users,
        total_locked_users=total_locked_users,
        total_notifications=total_notifications,
        total_academic_years=total_academic_years,
        total_semesters=total_semesters,
        total_materials=total_materials,
        total_assignments=total_assignments,
        maintenance_mode=maintenance_mode,
        system_lock=system_lock,
        major_stats=major_stats,
        dept_stats=dept_stats,
        recent_users=recent_users
    )

@admin_bp.route('/system/toggle-maintenance', methods=['POST'])
@login_required
@role_required('admin')
def toggle_maintenance():
    current_val = get_setting('maintenance_mode', '0')
    new_val = '0' if current_val == '1' else '1'
    set_setting('maintenance_mode', new_val)
    admin = get_current_user()

    now_str = datetime.now().strftime('%H:%M %d/%m/%Y')
    if new_val == '1':
        title = "HỆ THỐNG ĐANG BẢO TRÌ"
        msg = f"Hệ thống sẽ bảo trì từ {now_str}. Vui lòng lưu lại công việc của bạn."
        execute_db(
            "INSERT INTO announcements (sender_id, title, content, target_type) VALUES (?, ?, ?, 'all')",
            (admin['id'], title, msg)
        )
        users = query_db("SELECT id FROM users")
        for u in users:
            execute_db(
                "INSERT INTO notifications (user_id, title, message, category, link) VALUES (?, ?, ?, 'system', '#')",
                (u['id'], title, msg)
            )
        flash("Đã BẬT chế độ bảo trì hệ thống và tự động phát thông báo đến toàn bộ người dùng!", "warning")
    else:
        title = "Hệ thống LMS đã hoàn tất bảo trì"
        msg = f"Hệ thống LMS đã hoàn tất bảo trì vào lúc {now_str} và hoạt động bình thường trở lại."
        execute_db(
            "INSERT INTO announcements (sender_id, title, content, target_type) VALUES (?, ?, ?, 'all')",
            (admin['id'], title, msg)
        )
        users = query_db("SELECT id FROM users")
        for u in users:
            execute_db(
                "INSERT INTO notifications (user_id, title, message, category, link) VALUES (?, ?, ?, 'system', '#')",
                (u['id'], title, msg)
            )
        flash("Đã TẮT chế độ bảo trì. Hệ thống mở lại bình thường cho toàn bộ người dùng!", "success")

    return redirect(request.referrer or url_for('admin_bp.dashboard'))

@admin_bp.route('/system/toggle-lock', methods=['POST'])
@login_required
@role_required('admin')
def toggle_system_lock():
    current_val = get_setting('system_lock', '0')
    new_val = '0' if current_val == '1' else '1'
    set_setting('system_lock', new_val)
    admin = get_current_user()

    if new_val == '1':
        title = "HỆ THỐNG HIỆN ĐANG BỊ KHÓA"
        msg = "Hệ thống tạm thời bị khóa để kiểm tra kỹ thuật."
        execute_db(
            "INSERT INTO announcements (sender_id, title, content, target_type) VALUES (?, ?, ?, 'all')",
            (admin['id'], title, msg)
        )
        users = query_db("SELECT id FROM users")
        for u in users:
            execute_db(
                "INSERT INTO notifications (user_id, title, message, category, link) VALUES (?, ?, ?, 'system', '#')",
                (u['id'], title, msg)
            )
        flash("Đã KHÓA toàn bộ hệ thống và tự động gửi thông báo kiểm tra kỹ thuật đến toàn bộ người dùng!", "danger")
    else:
        title = "Hệ thống LMS đã được mở khóa"
        msg = "Hệ thống LMS đã được mở khóa và có thể truy cập bình thường."
        execute_db(
            "INSERT INTO announcements (sender_id, title, content, target_type) VALUES (?, ?, ?, 'all')",
            (admin['id'], title, msg)
        )
        users = query_db("SELECT id FROM users")
        for u in users:
            execute_db(
                "INSERT INTO notifications (user_id, title, message, category, link) VALUES (?, ?, ?, 'system', '#')",
                (u['id'], title, msg)
            )
        flash("Đã MỞ KHÓA hệ thống. Mọi người dùng đã có thể truy cập lại bình thường!", "success")

    return redirect(request.referrer or url_for('admin_bp.dashboard'))

@admin_bp.route('/notifications', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def broadcast_notifications():
    admin = get_current_user()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        target_type = request.form.get('target_type', 'all').strip()

        if not title or not content:
            flash("Vui lòng nhập đầy đủ tiêu đề và nội dung thông báo.", "danger")
            return redirect(url_for('admin_bp.broadcast_notifications'))

        # Insert announcement
        execute_db(
            "INSERT INTO announcements (sender_id, title, content, target_type) VALUES (?, ?, ?, ?)",
            (admin['id'], title, content, target_type)
        )

        # Deliver to target users
        if target_type == 'student':
            recipients = query_db("SELECT id FROM users WHERE role = 'student'")
            target_label = "toàn bộ sinh viên"
        elif target_type == 'teacher':
            recipients = query_db("SELECT id FROM users WHERE role = 'teacher'")
            target_label = "toàn bộ giảng viên"
        else:
            recipients = query_db("SELECT id FROM users")
            target_label = "toàn bộ người dùng"

        for u in recipients:
            execute_db(
                "INSERT INTO notifications (user_id, title, message, category, link) VALUES (?, ?, ?, 'system', '#')",
                (u['id'], title, content)
            )

        flash(f"Đã phát thông báo thành công đến {target_label} ({len(recipients)} người dùng)!", "success")
        return redirect(url_for('admin_bp.broadcast_notifications'))

    # GET
    broadcasts = query_db("""
        SELECT a.*, u.full_name as sender_name
        FROM announcements a
        JOIN users u ON a.sender_id = u.id
        WHERE a.target_type IN ('all', 'student', 'teacher')
        ORDER BY a.created_at DESC
    """)
    total_users_count = query_db("SELECT COUNT(*) as c FROM users", one=True)['c']
    total_students_count = query_db("SELECT COUNT(*) as c FROM users WHERE role = 'student'", one=True)['c']
    total_teachers_count = query_db("SELECT COUNT(*) as c FROM users WHERE role = 'teacher'", one=True)['c']

    return render_template(
        'admin/broadcast_notifications.html',
        broadcasts=broadcasts,
        total_users_count=total_users_count,
        total_students_count=total_students_count,
        total_teachers_count=total_teachers_count
    )

@admin_bp.route('/notification/<int:announcement_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_broadcast(announcement_id):
    execute_db("DELETE FROM announcements WHERE id = ?", (announcement_id,))
    flash("Đã xóa bản ghi thông báo toàn trường.", "info")
    return redirect(url_for('admin_bp.broadcast_notifications'))

@admin_bp.route('/users')
@login_required
@role_required('admin')
def users():
    role_filter = request.args.get('role', '').strip()
    status_filter = request.args.get('status', '').strip()
    dept_filter = request.args.get('dept_id', '').strip()
    search = request.args.get('search', '').strip()

    query = """
        SELECT u.*,
               s.student_code, s.department_id as student_dept_id, s.major_id as student_major_id, s.student_class_id,
               t.teacher_code, t.department_id as teacher_dept_id, t.title as teacher_title,
               sc.name as class_name, sc.code as class_code,
               m.name as major_name, m.code as major_code,
               COALESCE(d_s.name, d_t.name) as dept_name,
               COALESCE(d_s.code, d_t.code) as dept_code,
               COALESCE(s.department_id, t.department_id) as dept_id
        FROM users u
        LEFT JOIN students s ON u.id = s.user_id
        LEFT JOIN student_classes sc ON s.student_class_id = sc.id
        LEFT JOIN majors m ON s.major_id = m.id
        LEFT JOIN departments d_s ON s.department_id = d_s.id
        LEFT JOIN teachers t ON u.id = t.user_id
        LEFT JOIN departments d_t ON t.department_id = d_t.id
        WHERE 1=1
    """
    params = []

    if role_filter in ['student', 'teacher', 'admin']:
        query += " AND u.role = ?"
        params.append(role_filter)
    if status_filter in ['0', '1']:
        query += " AND u.is_active = ?"
        params.append(int(status_filter))
    if dept_filter and dept_filter.isdigit():
        query += " AND (s.department_id = ? OR t.department_id = ?)"
        params.extend([int(dept_filter), int(dept_filter)])
    if search:
        query += """ AND (
            u.full_name LIKE ? OR 
            u.email LIKE ? OR 
            u.phone LIKE ? OR 
            s.student_code LIKE ? OR 
            t.teacher_code LIKE ? OR 
            sc.name LIKE ?
        )"""
        p = f"%{search}%"
        params.extend([p, p, p, p, p, p])

    query += " ORDER BY u.id DESC"
    users_list = query_db(query, params)

    # Statistical summaries
    stats = {
        'total': query_db("SELECT COUNT(*) as c FROM users", one=True)['c'],
        'student': query_db("SELECT COUNT(*) as c FROM users WHERE role = 'student'", one=True)['c'],
        'teacher': query_db("SELECT COUNT(*) as c FROM users WHERE role = 'teacher'", one=True)['c'],
        'admin': query_db("SELECT COUNT(*) as c FROM users WHERE role = 'admin'", one=True)['c'],
        'active': query_db("SELECT COUNT(*) as c FROM users WHERE is_active = 1", one=True)['c'],
        'locked': query_db("SELECT COUNT(*) as c FROM users WHERE is_active = 0", one=True)['c'],
    }

    departments = query_db("SELECT * FROM departments ORDER BY name ASC")
    majors = query_db("SELECT * FROM majors ORDER BY name ASC")
    student_classes = query_db("SELECT * FROM student_classes ORDER BY name ASC")

    return render_template(
        'admin/users.html',
        users=users_list,
        stats=stats,
        departments=departments,
        majors=majors,
        student_classes=student_classes,
        selected_role=role_filter,
        selected_status=status_filter,
        selected_dept=dept_filter,
        search=search
    )

@admin_bp.route('/user/create', methods=['POST'])
@login_required
@role_required('admin')
def create_user():
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    role = request.form.get('role', 'student').strip()
    password = request.form.get('password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()
    is_active = int(request.form.get('is_active', 1))

    dept_id = request.form.get('department_id')
    major_id = request.form.get('major_id')
    class_id = request.form.get('student_class_id')

    if not full_name or not email:
        flash("Vui lòng điền Họ tên và Email.", "danger")
        return redirect(url_for('admin_bp.users'))

    if not password:
        flash("Vui lòng nhập mật khẩu khởi tạo.", "danger")
        return redirect(url_for('admin_bp.users'))

    if password != confirm_password:
        flash("Mật khẩu xác nhận không trùng khớp.", "danger")
        return redirect(url_for('admin_bp.users'))

    existing = query_db("SELECT id FROM users WHERE email = ?", (email,), one=True)
    if existing:
        flash(f"Email {email} đã tồn tại trong hệ thống.", "danger")
        return redirect(url_for('admin_bp.users'))

    pass_hash = generate_password_hash(password)
    user_id = execute_db("""
        INSERT INTO users (email, password_hash, full_name, role, phone, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (email, pass_hash, full_name, role, phone, is_active))

    if role == 'student':
        code = f"SV2024{user_id:04d}"
        execute_db("""
            INSERT INTO students (user_id, student_code, department_id, major_id, student_class_id)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, code, int(dept_id) if dept_id else None, int(major_id) if major_id else None, int(class_id) if class_id else None))
    elif role == 'teacher':
        code = f"GV2024{user_id:03d}"
        execute_db("""
            INSERT INTO teachers (user_id, teacher_code, department_id, title)
            VALUES (?, ?, ?, ?)
        """, (user_id, code, int(dept_id) if dept_id else None, 'Giảng viên'))

    flash("Đã tạo tài khoản thành công.", "success")
    return redirect(url_for('admin_bp.users'))

@admin_bp.route('/user/<int:user_id>/edit', methods=['POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    current_admin = get_current_user()
    target_user = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
    if not target_user:
        flash("Tài khoản không tồn tại.", "danger")
        return redirect(url_for('admin_bp.users'))

    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    role = request.form.get('role', target_user['role']).strip()
    is_active = int(request.form.get('is_active', 1))

    dept_id = request.form.get('department_id')
    major_id = request.form.get('major_id')
    class_id = request.form.get('student_class_id')

    new_password = request.form.get('new_password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()

    if not full_name or not email:
        flash("Vui lòng điền Họ tên và Email.", "danger")
        return redirect(url_for('admin_bp.users'))

    # Check email uniqueness against other users
    existing = query_db("SELECT id FROM users WHERE email = ? AND id != ?", (email, user_id), one=True)
    if existing:
        flash(f"Email {email} đã được sử dụng bởi người dùng khác.", "danger")
        return redirect(url_for('admin_bp.users'))

    # Rule: Admin cannot lock or demote themselves
    if current_admin and current_admin['id'] == user_id:
        if is_active == 0:
            flash("Bạn không thể khóa hoặc xóa tài khoản đang đăng nhập.", "danger")
            is_active = 1
        if role != 'admin':
            flash("Bạn không thể thay đổi vai trò tài khoản đang đăng nhập.", "danger")
            role = 'admin'

    # Handle password change if requested
    if new_password:
        if new_password != confirm_password:
            flash("Mật khẩu mới không trùng khớp.", "danger")
            return redirect(url_for('admin_bp.users'))
        if len(new_password) < 6:
            flash("Mật khẩu mới phải có ít nhất 6 ký tự.", "danger")
            return redirect(url_for('admin_bp.users'))
        new_hash = generate_password_hash(new_password)
        execute_db("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))

    # Update basic user record
    execute_db("""
        UPDATE users
        SET full_name = ?, email = ?, phone = ?, role = ?, is_active = ?
        WHERE id = ?
    """, (full_name, email, phone, role, is_active, user_id))

    # Update role-specific records
    if role == 'student':
        st = query_db("SELECT user_id FROM students WHERE user_id = ?", (user_id,), one=True)
        if st:
            execute_db("""
                UPDATE students
                SET department_id = ?, major_id = ?, student_class_id = ?
                WHERE user_id = ?
            """, (int(dept_id) if dept_id else None, int(major_id) if major_id else None, int(class_id) if class_id else None, user_id))
        else:
            code = f"SV2024{user_id:04d}"
            execute_db("""
                INSERT INTO students (user_id, student_code, department_id, major_id, student_class_id)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, code, int(dept_id) if dept_id else None, int(major_id) if major_id else None, int(class_id) if class_id else None))
    elif role == 'teacher':
        tc = query_db("SELECT user_id FROM teachers WHERE user_id = ?", (user_id,), one=True)
        if tc:
            execute_db("""
                UPDATE teachers
                SET department_id = ?
                WHERE user_id = ?
            """, (int(dept_id) if dept_id else None, user_id))
        else:
            code = f"GV2024{user_id:03d}"
            execute_db("""
                INSERT INTO teachers (user_id, teacher_code, department_id, title)
                VALUES (?, ?, ?, ?)
            """, (user_id, code, int(dept_id) if dept_id else None, 'Giảng viên'))

    flash("Đã cập nhật tài khoản thành công.", "success")
    return redirect(url_for('admin_bp.users'))

@admin_bp.route('/user/<int:user_id>/json')
@login_required
@role_required('admin')
def get_user_json(user_id):
    query = """
        SELECT u.id, u.email, u.full_name, u.role, u.phone, u.avatar, u.is_active, u.created_at,
               s.student_code, s.department_id as student_dept_id, s.major_id as student_major_id, s.student_class_id,
               t.teacher_code, t.department_id as teacher_dept_id, t.title as teacher_title,
               sc.name as class_name, sc.code as class_code,
               m.name as major_name, m.code as major_code,
               COALESCE(d_s.name, d_t.name) as dept_name,
               COALESCE(d_s.code, d_t.code) as dept_code,
               COALESCE(s.department_id, t.department_id) as dept_id
        FROM users u
        LEFT JOIN students s ON u.id = s.user_id
        LEFT JOIN student_classes sc ON s.student_class_id = sc.id
        LEFT JOIN majors m ON s.major_id = m.id
        LEFT JOIN departments d_s ON s.department_id = d_s.id
        LEFT JOIN teachers t ON u.id = t.user_id
        LEFT JOIN departments d_t ON t.department_id = d_t.id
        WHERE u.id = ?
    """
    row = query_db(query, (user_id,), one=True)
    if not row:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(row))

@admin_bp.route('/user/<int:user_id>/toggle-status')
@login_required
@role_required('admin')
def toggle_user_status(user_id):
    current_admin = get_current_user()
    if current_admin and current_admin['id'] == user_id:
        flash("Bạn không thể khóa hoặc xóa tài khoản đang đăng nhập.", "danger")
        return redirect(url_for('admin_bp.users'))

    user = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
    if user:
        new_status = 0 if user['is_active'] else 1
        execute_db("UPDATE users SET is_active = ? WHERE id = ?", (new_status, user_id))
        status_str = "Mở khóa" if new_status else "Khóa"
        flash(f"Đã {status_str} tài khoản {user['email']}.", "success" if new_status else "info")
    return redirect(url_for('admin_bp.users'))

@admin_bp.route('/user/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    current_admin = get_current_user()
    if current_admin and current_admin['id'] == user_id:
        flash("Bạn không thể khóa hoặc xóa tài khoản đang đăng nhập.", "danger")
        return redirect(url_for('admin_bp.users'))

    user = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
    if not user:
        flash("Tài khoản không tồn tại.", "danger")
        return redirect(url_for('admin_bp.users'))

    # If teacher has active courses, avoid breaking courses and student records
    if user['role'] == 'teacher':
        course_count = query_db("SELECT COUNT(*) as c FROM courses WHERE teacher_id = ?", (user_id,), one=True)['c']
        if course_count > 0:
            execute_db("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
            flash(f"Giảng viên {user['full_name']} đang phụ trách {course_count} lớp học phần. Để bảo toàn dữ liệu lớp học và điểm của sinh viên, tài khoản đã được chuyển sang trạng thái Đã khóa.", "warning")
            return redirect(url_for('admin_bp.users'))

    # Clean up student/teacher dependencies safely
    if user['role'] == 'student':
        execute_db("DELETE FROM enrollments WHERE student_id = ?", (user_id,))
        execute_db("DELETE FROM submissions WHERE student_id = ?", (user_id,))
        execute_db("DELETE FROM exam_results WHERE student_id = ?", (user_id,))
        execute_db("DELETE FROM grades WHERE student_id = ?", (user_id,))
        execute_db("DELETE FROM students WHERE user_id = ?", (user_id,))
    elif user['role'] == 'teacher':
        execute_db("DELETE FROM teachers WHERE user_id = ?", (user_id,))

    execute_db("DELETE FROM notifications WHERE user_id = ?", (user_id,))
    execute_db("DELETE FROM users WHERE id = ?", (user_id,))
    flash(f"Đã xóa tài khoản {user['full_name']} thành công.", "success")
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
    academic_year = request.args.get('academic_year', '').strip()
    semester = request.args.get('semester', '').strip()
    dept_id = request.args.get('department_id', '').strip()
    major_id = request.args.get('major_id', '').strip()
    export_format = request.args.get('export', '').strip()

    # Dropdown filters
    academic_years = query_db("SELECT * FROM academic_years ORDER BY start_year ASC")
    semesters = query_db("SELECT * FROM semesters ORDER BY id ASC")
    departments = query_db("SELECT * FROM departments ORDER BY id ASC")
    majors = query_db("SELECT * FROM majors ORDER BY id ASC")

    # Base Grade Query with Filters
    grade_query = """
        SELECT g.*, u.full_name, st.student_code,
               d.name as dept_name, m.name as major_name,
               c.name as course_name, c.code as course_code, c.academic_year, c.semester
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        JOIN subjects sub ON c.subject_id = sub.id
        JOIN users u ON g.student_id = u.id
        LEFT JOIN students st ON u.id = st.user_id
        LEFT JOIN departments d ON st.department_id = d.id
        LEFT JOIN majors m ON st.major_id = m.id
        WHERE 1=1
    """
    params = []
    if academic_year:
        grade_query += " AND c.academic_year = ?"
        params.append(academic_year)
    if semester:
        grade_query += " AND c.semester LIKE ?"
        params.append(f"%{semester}%")
    if dept_id and dept_id.isdigit():
        grade_query += " AND (st.department_id = ? OR sub.department_id = ?)"
        params.extend([int(dept_id), int(dept_id)])
    if major_id and major_id.isdigit():
        grade_query += " AND st.major_id = ?"
        params.append(int(major_id))

    grade_query += " ORDER BY g.total_score DESC"
    filtered_grades = query_db(grade_query, params)

    # Export CSV if requested
    if export_format == 'csv':
        csv_data = "\ufeffMã Sinh Viên,Họ và Tên,Khoa,Ngành,Năm Học,Học Kỳ,Lớp Học Phần,Điểm Tổng Kết,Xếp Loại\n"
        for row in filtered_grades:
            sc_code = row['student_code'] or ''
            name = (row['full_name'] or '').replace(',', ' ')
            dept = (row['dept_name'] or '').replace(',', ' ')
            maj = (row['major_name'] or '').replace(',', ' ')
            ay = row['academic_year'] or ''
            sem = (row['semester'] or '').replace(',', ' ')
            course = (row['course_name'] or '').replace(',', ' ')
            score = row['total_score'] if row['total_score'] is not None else ''
            letter = row['letter_grade'] or ''
            csv_data += f"{sc_code},{name},{dept},{maj},{ay},{sem},{course},{score},{letter}\n"
        return Response(
            csv_data,
            mimetype="text/csv; charset=utf-8",
            headers={"Content-disposition": "attachment; filename=bao_cao_ket_qua_hoc_tap.csv"}
        )

    # Detailed Statistics
    # A. Sinh viên
    sv_sql = """
        SELECT s.*, u.full_name, d.name as dept_name, m.name as major_name, sc.name as class_name
        FROM students s
        JOIN users u ON s.user_id = u.id
        LEFT JOIN departments d ON s.department_id = d.id
        LEFT JOIN majors m ON s.major_id = m.id
        LEFT JOIN student_classes sc ON s.student_class_id = sc.id
        WHERE 1=1
    """
    sv_params = []
    if dept_id and dept_id.isdigit():
        sv_sql += " AND s.department_id = ?"
        sv_params.append(int(dept_id))
    if major_id and major_id.isdigit():
        sv_sql += " AND s.major_id = ?"
        sv_params.append(int(major_id))
    students_list = query_db(sv_sql, sv_params)
    total_students_count = len(students_list)

    # B. Giảng viên
    gv_sql = """
        SELECT t.*, u.full_name, d.name as dept_name
        FROM teachers t
        JOIN users u ON t.user_id = u.id
        LEFT JOIN departments d ON t.department_id = d.id
        WHERE 1=1
    """
    gv_params = []
    if dept_id and dept_id.isdigit():
        gv_sql += " AND t.department_id = ?"
        gv_params.append(int(dept_id))
    teachers_list = query_db(gv_sql, gv_params)
    total_teachers_count = len(teachers_list)

    # C. Môn học
    sub_sql = "SELECT sub.*, d.name as dept_name FROM subjects sub LEFT JOIN departments d ON sub.department_id = d.id WHERE 1=1"
    sub_params = []
    if dept_id and dept_id.isdigit():
        sub_sql += " AND sub.department_id = ?"
        sub_params.append(int(dept_id))
    subjects_list = query_db(sub_sql, sub_params)
    total_subjects_count = len(subjects_list)
    avg_credits = round(sum(s['credits'] for s in subjects_list) / len(subjects_list), 1) if subjects_list else 0.0

    # D. Lớp học
    sc_sql = "SELECT sc.*, m.name as major_name FROM student_classes sc JOIN majors m ON sc.major_id = m.id WHERE 1=1"
    sc_params = []
    if dept_id and dept_id.isdigit():
        sc_sql += " AND m.department_id = ?"
        sc_params.append(int(dept_id))
    if major_id and major_id.isdigit():
        sc_sql += " AND sc.major_id = ?"
        sc_params.append(int(major_id))
    classes_list = query_db(sc_sql, sc_params)
    total_classes_count = len(classes_list)

    # Lớp học phần
    cr_sql = "SELECT c.* FROM courses c JOIN subjects sub ON c.subject_id = sub.id WHERE 1=1"
    cr_params = []
    if academic_year:
        cr_sql += " AND c.academic_year = ?"
        cr_params.append(academic_year)
    if semester:
        cr_sql += " AND c.semester LIKE ?"
        cr_params.append(f"%{semester}%")
    if dept_id and dept_id.isdigit():
        cr_sql += " AND sub.department_id = ?"
        cr_params.append(int(dept_id))
    courses_list = query_db(cr_sql, cr_params)
    total_courses_count = len(courses_list)

    # E. Kết quả học tập
    total_grades_count = len(filtered_grades)
    if total_grades_count > 0:
        valid_scores = [g['total_score'] for g in filtered_grades if g['total_score'] is not None]
        avg_gpa = round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else 0.0
        passed_count = sum(1 for g in filtered_grades if g['total_score'] is not None and g['total_score'] >= 5.0)
        failed_count = sum(1 for g in filtered_grades if g['total_score'] is not None and g['total_score'] < 5.0)
        pass_rate = round((passed_count / total_grades_count) * 100, 1)
        fail_rate = round((failed_count / total_grades_count) * 100, 1)

        rank_excellent = sum(1 for g in filtered_grades if g['total_score'] is not None and g['total_score'] >= 8.5)
        rank_good = sum(1 for g in filtered_grades if g['total_score'] is not None and 7.0 <= g['total_score'] < 8.5)
        rank_fair = sum(1 for g in filtered_grades if g['total_score'] is not None and 5.5 <= g['total_score'] < 7.0)
        rank_average = sum(1 for g in filtered_grades if g['total_score'] is not None and 4.0 <= g['total_score'] < 5.5)
        rank_poor = sum(1 for g in filtered_grades if g['total_score'] is not None and g['total_score'] < 4.0)
    else:
        avg_gpa = 0.0
        passed_count = 0
        failed_count = 0
        pass_rate = 0.0
        fail_rate = 0.0
        rank_excellent = 0
        rank_good = 0
        rank_fair = 0
        rank_average = 0
        rank_poor = 0

    # 7 Datasets for Chart.js
    # 1. SV theo khoa (Bar)
    chart1_labels = [d['name'] for d in departments]
    chart1_data = [query_db("SELECT COUNT(*) as c FROM students WHERE department_id = ?", (d['id'],), one=True)['c'] for d in departments]

    # 2. SV theo ngành (Bar)
    chart2_labels = [m['name'] for m in majors]
    chart2_data = [query_db("SELECT COUNT(*) as c FROM students WHERE major_id = ?", (m['id'],), one=True)['c'] for m in majors]

    # 3. SV theo từng năm học (Bar / Line)
    chart3_labels = [y['code'] for y in academic_years]
    chart3_data = [query_db("SELECT COUNT(DISTINCT e.student_id) as c FROM enrollments e JOIN courses c ON e.course_id = c.id WHERE c.academic_year = ?", (y['code'],), one=True)['c'] for y in academic_years]

    # 4. GV theo từng khoa (Bar)
    chart4_labels = [d['name'] for d in departments]
    chart4_data = [query_db("SELECT COUNT(*) as c FROM teachers WHERE department_id = ?", (d['id'],), one=True)['c'] for d in departments]

    # 5. Phân bố SV theo khoa (Doughnut)
    chart5_labels = [d['name'] for d in departments]
    chart5_data = chart1_data

    # 6. Số lượng lớp học theo từng khoa (Bar)
    chart6_labels = [d['name'] for d in departments]
    chart6_data = [query_db("SELECT COUNT(*) as c FROM student_classes sc JOIN majors m ON sc.major_id = m.id WHERE m.department_id = ?", (d['id'],), one=True)['c'] for d in departments]

    # 7. Thống kê SV theo học kỳ (Bar)
    chart7_labels = [s['name'] for s in semesters]
    chart7_data = [query_db("SELECT COUNT(DISTINCT e.student_id) as c FROM enrollments e JOIN courses c ON e.course_id = c.id WHERE c.semester LIKE ?", (f"%{s['name']}%",), one=True)['c'] for s in semesters]

    return render_template(
        'admin/reports.html',
        academic_years=academic_years,
        semesters=semesters,
        departments=departments,
        majors=majors,
        current_year=academic_year,
        current_semester=semester,
        current_dept=dept_id,
        current_major=major_id,
        filtered_grades=filtered_grades,
        total_students_count=total_students_count,
        total_teachers_count=total_teachers_count,
        total_subjects_count=total_subjects_count,
        avg_credits=avg_credits,
        total_classes_count=total_classes_count,
        total_courses_count=total_courses_count,
        total_grades_count=total_grades_count,
        avg_gpa=avg_gpa,
        passed_count=passed_count,
        failed_count=failed_count,
        pass_rate=pass_rate,
        fail_rate=fail_rate,
        rank_excellent=rank_excellent,
        rank_good=rank_good,
        rank_fair=rank_fair,
        rank_average=rank_average,
        rank_poor=rank_poor,
        chart1_labels=chart1_labels,
        chart1_data=chart1_data,
        chart2_labels=chart2_labels,
        chart2_data=chart2_data,
        chart3_labels=chart3_labels,
        chart3_data=chart3_data,
        chart4_labels=chart4_labels,
        chart4_data=chart4_data,
        chart5_labels=chart5_labels,
        chart5_data=chart5_data,
        chart6_labels=chart6_labels,
        chart6_data=chart6_data,
        chart7_labels=chart7_labels,
        chart7_data=chart7_data
    )

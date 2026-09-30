import os
import json
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import query_db, execute_db
from auth import login_user, logout_user, get_current_user

auth_bp = Blueprint('auth_bp', __name__)

DEBUG_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'debug-45cb16.log')

DEMO_PASSWORDS = {
    'student@example.com': 'student123',
    'teacher@example.com': 'teacher123',
    'admin@example.com': 'admin123',
}


def _auth_dbg(hypothesis_id, location, message, data):
    # #region agent log
    try:
        with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                'sessionId': '45cb16',
                'runId': 'post-fix',
                'hypothesisId': hypothesis_id,
                'location': location,
                'message': message,
                'data': data,
                'timestamp': int(time.time() * 1000),
            }) + '\n')
    except Exception:
        pass
    # #endregion

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    current_user = get_current_user()
    if current_user:
        # #region agent log
        _auth_dbg('H5', 'auth_routes.py:login', 'already authenticated redirect', {
            'role': current_user['role'],
            'email': current_user['email'],
        })
        # #endregion
        if current_user['role'] == 'admin':
            return redirect(url_for('admin_bp.dashboard'))
        elif current_user['role'] == 'teacher':
            return redirect(url_for('teacher_bp.dashboard'))
        else:
            return redirect(url_for('student_bp.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash("Vui lòng điền đầy đủ Email và Mật khẩu.", "danger")
            return render_template('auth/login.html', email=email)

        user = query_db("SELECT * FROM users WHERE email = ?", (email,), one=True)
        password_ok = bool(user and check_password_hash(user['password_hash'], password))
        # #region agent log
        _auth_dbg('H1', 'auth_routes.py:login', 'login attempt', {
            'email': email,
            'user_found': bool(user),
            'role': user['role'] if user else None,
            'is_active': user['is_active'] if user else None,
            'password_ok': password_ok,
        })
        # #endregion

        if password_ok:
            if not user['is_active']:
                flash("Tài khoản của bạn đã bị khóa. Vui lòng liên hệ Admin.", "danger")
                return render_template('auth/login.html', email=email)

            login_user(user)
            flash(f"Đăng nhập thành công! Xin chào {user['full_name']}.", "success")

            next_url = request.args.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)

            if user['role'] == 'admin':
                return redirect(url_for('admin_bp.dashboard'))
            elif user['role'] == 'teacher':
                return redirect(url_for('teacher_bp.dashboard'))
            else:
                return redirect(url_for('student_bp.dashboard'))
        else:
            flash("Email hoặc Mật khẩu không chính xác.", "danger")

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        role = request.form.get('role', 'student').strip()

        if not full_name or not email or not password:
            flash("Vui lòng nhập đầy đủ thông tin bắt buộc.", "danger")
            return render_template('auth/register.html')

        if password != confirm_password:
            flash("Mật khẩu xác nhận không trùng khớp.", "danger")
            return render_template('auth/register.html')

        existing_user = query_db("SELECT id FROM users WHERE email = ?", (email,), one=True)
        if existing_user:
            flash("Email này đã được đăng ký sử dụng trong hệ thống.", "danger")
            return render_template('auth/register.html')

        password_hash = generate_password_hash(password)
        user_id = execute_db("""
            INSERT INTO users (email, password_hash, full_name, role, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (email, password_hash, full_name, role, phone))

        # Create student or teacher record
        if role == 'student':
            student_code = f"SV{user_id:06d}"
            execute_db("INSERT INTO students (user_id, student_code) VALUES (?, ?)", (user_id, student_code))
        elif role == 'teacher':
            teacher_code = f"GV{user_id:04d}"
            execute_db("INSERT INTO teachers (user_id, teacher_code) VALUES (?, ?)", (user_id, teacher_code))

        flash("Đăng ký tài khoản thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for('auth_bp.login'))

    return render_template('auth/register.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = query_db("SELECT * FROM users WHERE email = ?", (email,), one=True)
        if user:
            flash(f"Yêu cầu cấp lại mật khẩu cho {email} đã được gửi. Mật khẩu tạm thời mặc định là: demo123", "info")
            new_hash = generate_password_hash("demo123")
            execute_db("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user['id']))
        else:
            flash("Email không tồn tại trong hệ thống.", "danger")
    return render_template('auth/forgot_password.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("Bạn đã đăng xuất khỏi hệ thống thành công.", "info")
    return redirect(url_for('auth_bp.login'))

import os
import json
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import query_db, execute_db, get_setting
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
        if current_user['role'] != 'admin':
            if get_setting('system_lock', '0') == '1':
                return redirect(url_for('common_bp.system_locked'))
            if get_setting('maintenance_mode', '0') == '1':
                return redirect(url_for('common_bp.maintenance'))

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

            if user['role'] != 'admin':
                if get_setting('system_lock', '0') == '1':
                    flash("HỆ THỐNG HIỆN ĐANG BỊ KHÓA. Hệ thống hiện đang tạm thời bị khóa theo quyết định của Quản trị viên. Vui lòng liên hệ quản trị viên để biết thêm thông tin.", "danger")
                    return redirect(url_for('common_bp.system_locked'))
                if get_setting('maintenance_mode', '0') == '1':
                    flash("HỆ THỐNG ĐANG BẢO TRÌ. Hệ thống LMS hiện đang được bảo trì để nâng cấp và đảm bảo chất lượng dịch vụ. Vui lòng quay lại sau.", "warning")
                    return redirect(url_for('common_bp.maintenance'))

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
    flash("Chức năng đăng ký tài khoản công khai đã đóng. Vui lòng liên hệ Quản trị viên để được cấp tài khoản.", "info")
    return redirect(url_for('auth_bp.login'))

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

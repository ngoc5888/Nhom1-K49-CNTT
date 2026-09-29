from functools import wraps
from flask import session, redirect, url_for, flash, g, request
from database import query_db

def get_current_user():
    if 'user_id' not in session:
        return None
    if 'current_user' not in g:
        g.current_user = query_db(
            "SELECT * FROM users WHERE id = ? AND is_active = 1",
            (session['user_id'],),
            one=True
        )
    return g.current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if user is None:
            flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
            return redirect(url_for('auth_bp.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if user is None:
                flash("Vui lòng đăng nhập để thực hiện thao tác này.", "warning")
                return redirect(url_for('auth_bp.login'))
            if user['role'] not in roles:
                flash("Bạn không có quyền truy cập vào chức năng này!", "danger")
                # Redirect user to their matching dashboard
                if user['role'] == 'admin':
                    return redirect(url_for('admin_bp.dashboard'))
                elif user['role'] == 'teacher':
                    return redirect(url_for('teacher_bp.dashboard'))
                else:
                    return redirect(url_for('student_bp.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_user(user):
    session.clear()
    session['user_id'] = user['id']
    session['user_name'] = user['full_name']
    session['user_role'] = user['role']
    session['user_email'] = user['email']

def logout_user():
    session.clear()

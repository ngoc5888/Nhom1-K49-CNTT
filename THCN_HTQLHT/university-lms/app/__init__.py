import os
from flask import Flask, g
from database import close_db, query_db, init_db
from auth import get_current_user

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'lms-university-secret-key-2026-secure'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize DB schema if file doesn't exist
    init_db()

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    from routes.teacher_routes import teacher_bp
    from routes.admin_routes import admin_bp
    from routes.common_routes import common_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(common_bp)

    @app.teardown_appcontext
    def teardown_db(exception):
        close_db(exception)

    @app.template_filter('safe_str')
    def safe_str(val):
        if val is None:
            return ''
        return str(val)

    @app.before_request
    def check_system_status():
        from flask import request, redirect, url_for
        from database import get_setting

        # Allow static files
        if request.path.startswith('/static'):
            return None

        # Exempt endpoints
        exempt_endpoints = {
            'common_bp.maintenance',
            'common_bp.system_locked',
            'auth_bp.login',
            'auth_bp.logout'
        }
        if request.endpoint in exempt_endpoints:
            return None

        # Admin is NEVER blocked
        user = get_current_user()
        if user and user['role'] == 'admin':
            return None

        is_locked = get_setting('system_lock', '0') == '1'
        if is_locked:
            return redirect(url_for('common_bp.system_locked'))

        is_maintenance = get_setting('maintenance_mode', '0') == '1'
        if is_maintenance:
            return redirect(url_for('common_bp.maintenance'))

        return None

    @app.context_processor
    def inject_user_context():
        user = get_current_user()
        unread_count = 0
        if user:
            res = query_db("SELECT COUNT(*) as count FROM notifications WHERE user_id = ? AND is_read = 0", (user['id'],), one=True)
            if res:
                unread_count = res['count']
        return dict(current_user=user, unread_notifications_count=unread_count)

    @app.route('/')
    def index():
        from flask import redirect, url_for
        user = get_current_user()
        if user:
            if user['role'] == 'admin':
                return redirect(url_for('admin_bp.dashboard'))
            elif user['role'] == 'teacher':
                return redirect(url_for('teacher_bp.dashboard'))
            else:
                return redirect(url_for('student_bp.dashboard'))
        return redirect(url_for('auth_bp.login'))

    return app

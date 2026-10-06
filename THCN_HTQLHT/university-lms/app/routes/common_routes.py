from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import query_db, execute_db
from auth import login_required, get_current_user

common_bp = Blueprint('common_bp', __name__)

@common_bp.route('/notifications')
@login_required
def notifications():
    user = get_current_user()

    # Mark all read if requested
    action = request.args.get('action')
    if action == 'mark_all_read':
        execute_db("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (user['id'],))
        flash("Đã đánh dấu tất cả thông báo là đã đọc.", "success")
        return redirect(url_for('common_bp.notifications'))

    all_notifs = query_db("SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC", (user['id'],))

    return render_template('common/notifications.html', notifications=all_notifs)

@common_bp.route('/notification/<int:notif_id>/read')
@login_required
def read_notification(notif_id):
    user = get_current_user()
    notif = query_db("SELECT * FROM notifications WHERE id = ? AND user_id = ?", (notif_id, user['id']), one=True)
    if notif:
        execute_db("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
        if notif['link'] and notif['link'] != '#':
            return redirect(notif['link'])
    return redirect(url_for('common_bp.notifications'))

@common_bp.route('/notification/<int:notif_id>/delete')
@login_required
def delete_notification(notif_id):
    user = get_current_user()
    execute_db("DELETE FROM notifications WHERE id = ? AND user_id = ?", (notif_id, user['id']))
    flash("Đã xóa thông báo.", "info")
    return redirect(url_for('common_bp.notifications'))

@common_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = get_current_user()

    # Get specific role details
    student_details = None
    teacher_details = None

    if user['role'] == 'student':
        student_details = query_db("""
            SELECT s.*, c.name as class_name, m.name as major_name, d.name as dept_name
            FROM students s
            LEFT JOIN student_classes c ON s.student_class_id = c.id
            LEFT JOIN majors m ON s.major_id = m.id
            LEFT JOIN departments d ON s.department_id = d.id
            WHERE s.user_id = ?
        """, (user['id'],), one=True)
    elif user['role'] == 'teacher':
        teacher_details = query_db("""
            SELECT t.*, d.name as dept_name
            FROM teachers t
            LEFT JOIN departments d ON t.department_id = d.id
            WHERE t.user_id = ?
        """, (user['id'],), one=True)

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_info':
            full_name = request.form.get('full_name', '').strip()
            phone = request.form.get('phone', '').strip()

            execute_db("UPDATE users SET full_name = ?, phone = ? WHERE id = ?", (full_name, phone, user['id']))
            flash("Cập nhật thông tin cá nhân thành công!", "success")
            return redirect(url_for('common_bp.profile'))

        elif action == 'change_password':
            old_pass = request.form.get('old_password', '').strip()
            new_pass = request.form.get('new_password', '').strip()
            confirm_pass = request.form.get('confirm_password', '').strip()

            if not check_password_hash(user['password_hash'], old_pass):
                flash("Mật khẩu hiện tại không chính xác.", "danger")
            elif new_pass != confirm_pass:
                flash("Mật khẩu mới không trùng khớp.", "danger")
            elif len(new_pass) < 6:
                flash("Mật khẩu mới phải có ít nhất 6 ký tự.", "danger")
            else:
                new_hash = generate_password_hash(new_pass)
                execute_db("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user['id']))
                flash("Đổi mật khẩu thành công!", "success")

            return redirect(url_for('common_bp.profile'))

    return render_template(
        'common/profile.html',
        user=user,
        student_details=student_details,
        teacher_details=teacher_details
    )

@common_bp.route('/maintenance')
def maintenance():
    return render_template('common/maintenance.html')

@common_bp.route('/system-locked')
def system_locked():
    return render_template('common/system_locked.html')


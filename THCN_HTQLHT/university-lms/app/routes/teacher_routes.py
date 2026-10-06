import os
import json
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from database import query_db, execute_db
from auth import login_required, role_required, get_current_user

teacher_bp = Blueprint('teacher_bp', __name__, url_prefix='/teacher')

DEBUG_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'debug-45cb16.log')


def _teacher_dbg(hypothesis_id, location, message, data):
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


def letter_from_total(total):
    return "A+" if total >= 9.0 else ("A" if total >= 8.5 else ("B+" if total >= 8.0 else ("B" if total >= 7.0 else ("C+" if total >= 6.5 else ("C" if total >= 5.5 else ("D" if total >= 4.0 else "F"))))))


def a1_from_parts(assignment_score, quiz_score):
    assignment = float(assignment_score or 0)
    quiz = float(quiz_score or 0)
    if quiz == 0 or assignment == quiz:
        return round(assignment, 2)
    return round((assignment + quiz) / 2.0, 2)

@teacher_bp.route('/dashboard')
@login_required
@role_required('teacher')
def dashboard():
    user = get_current_user()

    # 1. Total teaching classes
    classes_count = query_db("SELECT COUNT(*) as count FROM courses WHERE teacher_id = ?", (user['id'],), one=True)['count']

    # 2. Total students across classes
    total_students = query_db("""
        SELECT COUNT(DISTINCT e.student_id) as count
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        WHERE c.teacher_id = ?
    """, (user['id'],), one=True)['count']

    # 3. Total assignments created
    assignments_count = query_db("SELECT COUNT(*) as count FROM assignments WHERE created_by = ?", (user['id'],), one=True)['count']

    # 4. Ungraded submissions count
    ungraded_count = query_db("""
        SELECT COUNT(s.id) as count
        FROM submissions s
        JOIN assignments a ON s.assignment_id = a.id
        WHERE a.created_by = ? AND s.score IS NULL
    """, (user['id'],), one=True)['count']

    # 5. Recent teaching classes
    recent_classes = query_db("""
        SELECT c.*, sub.name as subject_name,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as student_count
        FROM courses c
        JOIN subjects sub ON c.subject_id = sub.id
        WHERE c.teacher_id = ?
        ORDER BY c.id DESC LIMIT 4
    """, (user['id'],))

    # 6. Ungraded submission list preview
    pending_submissions = query_db("""
        SELECT s.*, u.full_name as student_name, a.title as assignment_title, c.name as course_name
        FROM submissions s
        JOIN users u ON s.student_id = u.id
        JOIN assignments a ON s.assignment_id = a.id
        JOIN courses c ON a.course_id = c.id
        WHERE a.created_by = ? AND s.score IS NULL
        ORDER BY s.submitted_at DESC LIMIT 5
    """, (user['id'],))

    return render_template(
        'teacher/dashboard.html',
        classes_count=classes_count,
        total_students=total_students,
        assignments_count=assignments_count,
        ungraded_count=ungraded_count,
        recent_classes=recent_classes,
        pending_submissions=pending_submissions
    )

@teacher_bp.route('/classes')
@login_required
@role_required('teacher')
def classes():
    user = get_current_user()

    courses = query_db("""
        SELECT c.*, sub.name as subject_name, sub.code as subject_code, sub.credits,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as student_count
        FROM courses c
        JOIN subjects sub ON c.subject_id = sub.id
        WHERE c.teacher_id = ?
        ORDER BY c.id DESC
    """, (user['id'],))

    subjects = query_db("SELECT * FROM subjects ORDER BY name ASC")

    return render_template('teacher/classes.html', courses=courses, subjects=subjects)

@teacher_bp.route('/class/create', methods=['POST'])
@login_required
@role_required('teacher')
def create_class():
    user = get_current_user()
    subject_id = request.form.get('subject_id')
    code = request.form.get('code', '').strip()
    name = request.form.get('name', '').strip()
    semester = request.form.get('semester', 'HK1 (2024-2025)').strip()
    room = request.form.get('room', 'Phòng A.101').strip()
    schedule_info = request.form.get('schedule_info', 'Thứ 2 (08:00 - 11:30)').strip()
    description = request.form.get('description', '').strip()

    if not subject_id or not code or not name:
        flash("Vui lòng điền các trường bắt buộc.", "danger")
        return redirect(url_for('teacher_bp.classes'))

    try:
        course_id = execute_db("""
            INSERT INTO courses (subject_id, teacher_id, code, name, semester, room, schedule_info, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (subject_id, user['id'], code, name, semester, room, schedule_info, description))
        flash(f"Tạo lớp học phần {name} ({code}) thành công!", "success")
    except Exception as e:
        flash(f"Lỗi tạo lớp học: Mã lớp {code} đã tồn tại hoặc dữ liệu không hợp lệ.", "danger")

    return redirect(url_for('teacher_bp.classes'))

@teacher_bp.route('/materials')
@login_required
@role_required('teacher')
def materials():
    user = get_current_user()

    materials_list = query_db("""
        SELECT m.*, c.name as course_name
        FROM materials m
        JOIN courses c ON m.course_id = c.id
        WHERE c.teacher_id = ?
        ORDER BY m.created_at DESC
    """, (user['id'],))

    my_courses = query_db("SELECT id, name, code FROM courses WHERE teacher_id = ?", (user['id'],))

    return render_template('teacher/materials.html', materials=materials_list, courses=my_courses)

@teacher_bp.route('/material/upload', methods=['POST'])
@login_required
@role_required('teacher')
def upload_material():
    user = get_current_user()
    course_id = request.form.get('course_id')
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    file_type = request.form.get('file_type', 'PDF')
    file = request.files.get('material_file')

    if not course_id or not title:
        flash("Vui lòng nhập tên tài liệu và chọn lớp học.", "danger")
        return redirect(url_for('teacher_bp.materials'))

    file_path = "/static/uploads/sample_material.pdf"
    file_size = "2.4 MB"

    if file and file.filename != '':
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"mat_{user['id']}_{file.filename}"
        save_path = os.path.join(upload_folder, filename)
        file.save(save_path)
        file_path = f"/static/uploads/{filename}"
        size_bytes = os.path.getsize(save_path)
        file_size = f"{round(size_bytes / (1024*1024), 1)} MB" if size_bytes >= 1024*1024 else f"{round(size_bytes / 1024, 1)} KB"

    execute_db("""
        INSERT INTO materials (course_id, title, description, file_path, file_type, file_size, uploaded_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (course_id, title, description, file_path, file_type, file_size, user['id']))

    flash(f"Đã tải lên tài liệu '{title}' thành công!", "success")
    return redirect(url_for('teacher_bp.materials'))

@teacher_bp.route('/assignments')
@login_required
@role_required('teacher')
def assignments():
    user = get_current_user()

    assignments_list = query_db("""
        SELECT a.*, c.name as course_name,
               (SELECT COUNT(*) FROM submissions WHERE assignment_id = a.id) as submitted_count,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = a.course_id) as total_students
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        WHERE a.created_by = ?
        ORDER BY a.created_at DESC
    """, (user['id'],))

    my_courses = query_db("SELECT id, name FROM courses WHERE teacher_id = ?", (user['id'],))

    return render_template('teacher/assignments.html', assignments=assignments_list, courses=my_courses)

@teacher_bp.route('/assignment/create', methods=['POST'])
@login_required
@role_required('teacher')
def create_assignment():
    user = get_current_user()
    course_id = request.form.get('course_id')
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    due_date = request.form.get('due_date', '').strip()
    max_points = float(request.form.get('max_points', 10.0))

    if not course_id or not title or not due_date:
        flash("Vui lòng điền các thông tin bài tập bắt buộc.", "danger")
        return redirect(url_for('teacher_bp.assignments'))

    file_path = ""
    file = request.files.get('assignment_file')
    if file and file.filename != '':
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"assign_{user['id']}_{file.filename}"
        file.save(os.path.join(upload_folder, filename))
        file_path = f"/static/uploads/{filename}"

    # Standardize HTML datetime format T to space
    due_date_str = due_date.replace('T', ' ') + ':00' if 'T' in due_date else due_date

    execute_db("""
        INSERT INTO assignments (course_id, title, description, file_path, due_date, max_points, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (course_id, title, description, file_path, due_date_str, max_points, user['id']))

    flash(f"Tạo bài tập '{title}' thành công!", "success")
    return redirect(url_for('teacher_bp.assignments'))

@teacher_bp.route('/assignment/<int:assignment_id>/submissions')
@login_required
@role_required('teacher')
def assignment_submissions(assignment_id):
    assignment = query_db("""
        SELECT a.*, c.name as course_name FROM assignments a JOIN courses c ON a.course_id = c.id WHERE a.id = ?
    """, (assignment_id,), one=True)

    submissions_list = query_db("""
        SELECT s.*, u.full_name as student_name, st.student_code
        FROM submissions s
        JOIN users u ON s.student_id = u.id
        LEFT JOIN students st ON u.id = st.user_id
        WHERE s.assignment_id = ?
        ORDER BY s.submitted_at DESC
    """, (assignment_id,))

    return render_template('teacher/submissions.html', assignment=assignment, submissions=submissions_list)

@teacher_bp.route('/submission/<int:submission_id>/grade', methods=['POST'])
@login_required
@role_required('teacher')
def grade_submission(submission_id):
    score = float(request.form.get('score', 0.0))
    feedback = request.form.get('feedback', '').strip()
    assignment_id = request.form.get('assignment_id')

    execute_db("""
        UPDATE submissions
        SET score = ?, feedback = ?, graded_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (score, feedback, submission_id))

    flash("Đã lưu điểm và nhận xét thành công!", "success")
    return redirect(url_for('teacher_bp.assignment_submissions', assignment_id=assignment_id))

@teacher_bp.route('/exams')
@login_required
@role_required('teacher')
def exams():
    user = get_current_user()

    exams_list = query_db("""
        SELECT ex.*, c.name as course_name,
               (SELECT COUNT(*) FROM questions WHERE exam_id = ex.id) as question_count,
               (SELECT COUNT(*) FROM exam_results WHERE exam_id = ex.id) as result_count
        FROM exams ex
        JOIN courses c ON ex.course_id = c.id
        WHERE ex.created_by = ?
        ORDER BY ex.created_at DESC
    """, (user['id'],))

    my_courses = query_db("SELECT id, name FROM courses WHERE teacher_id = ?", (user['id'],))

    return render_template('teacher/exams.html', exams=exams_list, courses=my_courses)

@teacher_bp.route('/exam/create', methods=['POST'])
@login_required
@role_required('teacher')
def create_exam():
    user = get_current_user()
    course_id = request.form.get('course_id')
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    duration_minutes = int(request.form.get('duration_minutes', 45))

    if not course_id or not title:
        flash("Vui lòng điền tiêu đề bài kiểm tra và chọn lớp học.", "danger")
        return redirect(url_for('teacher_bp.exams'))

    exam_id = execute_db("""
        INSERT INTO exams (course_id, title, description, duration_minutes, created_by)
        VALUES (?, ?, ?, ?, ?)
    """, (course_id, title, description, duration_minutes, user['id']))

    flash(f"Tạo bài kiểm tra '{title}' thành công. Hãy thêm các câu hỏi trắc nghiệm!", "success")
    return redirect(url_for('teacher_bp.exam_questions', exam_id=exam_id))

@teacher_bp.route('/exam/<int:exam_id>/questions')
@login_required
@role_required('teacher')
def exam_questions(exam_id):
    exam = query_db("SELECT ex.*, c.name as course_name FROM exams ex JOIN courses c ON ex.course_id = c.id WHERE ex.id = ?", (exam_id,), one=True)
    questions = query_db("SELECT * FROM questions WHERE exam_id = ?", (exam_id,))

    formatted_questions = []
    for q in questions:
        q_dict = dict(q)
        q_dict['options'] = json.loads(q['options_json'])
        q_dict['correct_indices'] = json.loads(q['correct_answers_json'])
        formatted_questions.append(q_dict)

    return render_template('teacher/exam_questions.html', exam=exam, questions=formatted_questions)

@teacher_bp.route('/exam/<int:exam_id>/question/add', methods=['POST'])
@login_required
@role_required('teacher')
def add_question(exam_id):
    question_text = request.form.get('question_text', '').strip()
    q_type = request.form.get('question_type', 'single')
    points = float(request.form.get('points', 2.0))

    opt_a = request.form.get('opt_a', '').strip()
    opt_b = request.form.get('opt_b', '').strip()
    opt_c = request.form.get('opt_c', '').strip()
    opt_d = request.form.get('opt_d', '').strip()

    options = [opt_a, opt_b, opt_c, opt_d]
    correct_idx = int(request.form.get('correct_option', 0))

    execute_db("""
        INSERT INTO questions (exam_id, question_text, question_type, options_json, correct_answers_json, points)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (exam_id, question_text, q_type, json.dumps(options), json.dumps([correct_idx]), points))

    flash("Đã thêm câu hỏi mới thành công!", "success")
    return redirect(url_for('teacher_bp.exam_questions', exam_id=exam_id))

@teacher_bp.route('/grades')
@login_required
@role_required('teacher')
def grades():
    user = get_current_user()
    course_id = request.args.get('course_id', '')

    my_courses = query_db("SELECT id, name, code FROM courses WHERE teacher_id = ?", (user['id'],))

    students_grades = []
    selected_course_info = None

    if course_id:
        selected_course_info = query_db("SELECT * FROM courses WHERE id = ?", (course_id,), one=True)
        students_grades = query_db("""
            SELECT u.id as student_id, u.full_name, st.student_code,
                   g.assignment_score, g.quiz_score, g.midterm_score, g.final_score, g.total_score, g.letter_grade
            FROM enrollments e
            JOIN users u ON e.student_id = u.id
            LEFT JOIN students st ON u.id = st.user_id
            LEFT JOIN grades g ON g.course_id = e.course_id AND g.student_id = e.student_id
            WHERE e.course_id = ?
            ORDER BY u.full_name ASC
        """, (course_id,))
        formatted = []
        for sg in students_grades:
            item = dict(sg)
            item['a1'] = a1_from_parts(item.get('assignment_score'), item.get('quiz_score'))
            item['a2'] = round(float(item['midterm_score'] or 0), 2)
            item['a3'] = round(float(item['final_score'] or 0), 2)
            item['total_score'] = round(item['a1'] * 0.2 + item['a2'] * 0.3 + item['a3'] * 0.5, 2)
            formatted.append(item)
        students_grades = formatted
        # #region agent log
        _teacher_dbg('H6', 'teacher_routes.py:grades', 'teacher gradebook A1 A2 A3', {
            'course_id': course_id,
            'rows': [{'a1': r['a1'], 'a2': r['a2'], 'a3': r['a3']} for r in students_grades[:5]],
        })
        # #endregion

    return render_template('teacher/grades.html', courses=my_courses, students_grades=students_grades, selected_course=course_id, selected_course_info=selected_course_info)

@teacher_bp.route('/grades/update', methods=['POST'])
@login_required
@role_required('teacher')
def update_grade():
    course_id = request.form.get('course_id')
    student_id = request.form.get('student_id')

    a1 = float(request.form.get('a1_score', request.form.get('assignment_score', 0.0)))
    a2 = float(request.form.get('a2_score', request.form.get('midterm_score', 0.0)))
    a3 = float(request.form.get('a3_score', request.form.get('final_score', 0.0)))

    assignment_score = a1
    quiz_score = a1
    midterm_score = a2
    final_score = a3
    total = round(a1 * 0.2 + a2 * 0.3 + a3 * 0.5, 2)
    letter = letter_from_total(total)
    # #region agent log
    _teacher_dbg('H6', 'teacher_routes.py:update_grade', 'saved A1 A2 A3', {
        'a1': a1, 'a2': a2, 'a3': a3, 'total': total, 'letter': letter, 'weights': [0.2, 0.3, 0.5],
    })
    # #endregion

    existing = query_db("SELECT id FROM grades WHERE course_id = ? AND student_id = ?", (course_id, student_id), one=True)
    if existing:
        execute_db("""
            UPDATE grades
            SET assignment_score = ?, quiz_score = ?, midterm_score = ?, final_score = ?, total_score = ?, letter_grade = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (assignment_score, quiz_score, midterm_score, final_score, total, letter, existing['id']))
    else:
        execute_db("""
            INSERT INTO grades (course_id, student_id, assignment_score, quiz_score, midterm_score, final_score, total_score, letter_grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (course_id, student_id, assignment_score, quiz_score, midterm_score, final_score, total, letter))

    flash("Cập nhật điểm thành công!", "success")
    return redirect(url_for('teacher_bp.grades', course_id=course_id))

@teacher_bp.route('/notifications', methods=['GET', 'POST'])
@login_required
@role_required('teacher')
def class_notifications():
    user = get_current_user()

    if request.method == 'POST':
        course_id = request.form.get('course_id')
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not course_id or not title or not content:
            flash("Vui lòng chọn lớp học phần và điền đầy đủ tiêu đề, nội dung.", "danger")
            return redirect(url_for('teacher_bp.class_notifications'))

        # Verify teacher owns this course
        course = query_db("SELECT * FROM courses WHERE id = ? AND teacher_id = ?", (course_id, user['id']), one=True)
        if not course:
            flash("Bạn không có quyền gửi thông báo cho lớp học phần này.", "danger")
            return redirect(url_for('teacher_bp.class_notifications'))

        # Insert into announcements
        execute_db(
            "INSERT INTO announcements (sender_id, title, content, target_type, course_id) VALUES (?, ?, ?, 'course', ?)",
            (user['id'], title, content, course['id'])
        )

        # Deliver notification to each enrolled student
        enrolled_students = query_db("SELECT student_id FROM enrollments WHERE course_id = ?", (course['id'],))
        for s in enrolled_students:
            execute_db(
                "INSERT INTO notifications (user_id, title, message, category, link) VALUES (?, ?, ?, 'teacher', ?)",
                (s['student_id'], f"[{course['name']}] {title}", content, f"/student/class/{course['id']}")
            )

        flash(f"Đã gửi thông báo đến {len(enrolled_students)} sinh viên của lớp học phần {course['name']} thành công!", "success")
        return redirect(url_for('teacher_bp.class_notifications'))

    # GET
    courses = query_db("""
        SELECT c.*, sub.name as subject_name,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as student_count
        FROM courses c
        JOIN subjects sub ON c.subject_id = sub.id
        WHERE c.teacher_id = ?
        ORDER BY c.id DESC
    """, (user['id'],))

    announcements = query_db("""
        SELECT a.*, c.name as course_name, c.code as course_code
        FROM announcements a
        JOIN courses c ON a.course_id = c.id
        WHERE a.sender_id = ? AND a.target_type = 'course'
        ORDER BY a.created_at DESC
    """, (user['id'],))

    return render_template(
        'teacher/class_notifications.html',
        courses=courses,
        announcements=announcements
    )

@teacher_bp.route('/notification/<int:announcement_id>/delete', methods=['POST'])
@login_required
@role_required('teacher')
def delete_class_notification(announcement_id):
    user = get_current_user()
    execute_db("DELETE FROM announcements WHERE id = ? AND sender_id = ?", (announcement_id, user['id']))
    flash("Đã xóa bản ghi thông báo lớp học phần.", "info")
    return redirect(url_for('teacher_bp.class_notifications'))


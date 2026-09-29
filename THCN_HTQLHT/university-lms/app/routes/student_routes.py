import os
import json
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from database import query_db, execute_db
from auth import login_required, role_required, get_current_user

student_bp = Blueprint('student_bp', __name__, url_prefix='/student')

DEBUG_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'debug-45cb16.log')


def score10_to_gpa4(score):
    if score is None:
        return 0.0
    s = float(score)
    if s >= 9.0:
        return 4.0
    if s >= 8.5:
        return 3.7
    if s >= 8.0:
        return 3.5
    if s >= 7.0:
        return 3.0
    if s >= 6.5:
        return 2.5
    if s >= 5.5:
        return 2.0
    if s >= 4.0:
        return 1.0
    return 0.0


def classify_gpa4(gpa):
    if gpa >= 3.6:
        return "Xuất sắc"
    if gpa >= 3.2:
        return "Giỏi"
    if gpa >= 2.5:
        return "Khá"
    if gpa >= 2.0:
        return "Trung bình"
    return "Yếu"


def compute_gpa4(grade_rows):
    total_credits = 0
    weighted = 0.0
    for row in grade_rows or []:
        credits = row['credits'] or 0
        total_credits += credits
        weighted += score10_to_gpa4(row['total_score']) * credits
    if total_credits <= 0:
        return 0.0
    return round(weighted / total_credits, 2)


def grade_components(row):
    """A1 chuyên cần (bài tập + kiểm tra, thang 10); A2 giữa kỳ; A3 cuối kỳ."""
    assignment = float(row['assignment_score'] or 0)
    quiz = float(row['quiz_score'] or 0)
    if quiz == 0 or assignment == quiz:
        a1 = round(assignment, 2)
    else:
        a1 = round((assignment + quiz) / 2.0, 2)
    a2 = round(float(row['midterm_score'] or 0), 2)
    a3 = round(float(row['final_score'] or 0), 2)
    return a1, a2, a3


def compute_total10(a1, a2, a3):
    return round(float(a1) * 0.2 + float(a2) * 0.3 + float(a3) * 0.5, 2)


def _dbg(hypothesis_id, location, message, data, run_id='post-fix'):
    # #region agent log
    try:
        with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                'sessionId': '45cb16',
                'runId': run_id,
                'hypothesisId': hypothesis_id,
                'location': location,
                'message': message,
                'data': data,
                'timestamp': int(time.time() * 1000),
            }) + '\n')
    except Exception:
        pass
    # #endregion

@student_bp.route('/dashboard')
@login_required
@role_required('student')
def dashboard():
    user = get_current_user()
    user_id = user['id']

    # Get student info
    student_info = query_db("""
        SELECT s.*, c.name as class_name, m.name as major_name, d.name as dept_name
        FROM students s
        LEFT JOIN student_classes c ON s.student_class_id = c.id
        LEFT JOIN majors m ON s.major_id = m.id
        LEFT JOIN departments d ON s.department_id = d.id
        WHERE s.user_id = ?
    """, (user_id,), one=True)

    # 1. Class count
    classes_count = query_db("""
        SELECT COUNT(*) as count FROM enrollments WHERE student_id = ? AND status = 'active'
    """, (user_id,), one=True)['count']

    # 2. Materials count across student courses
    materials_count = query_db("""
        SELECT COUNT(m.id) as count
        FROM materials m
        JOIN enrollments e ON m.course_id = e.course_id
        WHERE e.student_id = ?
    """, (user_id,), one=True)['count']

    # 3. Assignments count
    assignments_count = query_db("""
        SELECT COUNT(a.id) as count
        FROM assignments a
        JOIN enrollments e ON a.course_id = e.course_id
        WHERE e.student_id = ?
    """, (user_id,), one=True)['count']

    # 4. Exams count
    exams_count = query_db("""
        SELECT COUNT(ex.id) as count
        FROM exams ex
        JOIN enrollments e ON ex.course_id = e.course_id
        WHERE e.student_id = ?
    """, (user_id,), one=True)['count']

    # 5. Cumulative GPA (4.0 scale, credit-weighted)
    grade_rows = query_db("""
        SELECT g.total_score, g.assignment_score, g.quiz_score, g.midterm_score, g.final_score, sub.credits
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        JOIN subjects sub ON c.subject_id = sub.id
        WHERE g.student_id = ?
    """, (user_id,))
    recomputed = []
    for r in grade_rows:
        item = dict(r)
        a1, a2, a3 = grade_components(item)
        item['total_score'] = compute_total10(a1, a2, a3)
        recomputed.append(item)
    avg_score_10 = round(sum((r['total_score'] or 0) for r in recomputed) / len(recomputed), 2) if recomputed else 0.0
    avg_grade = compute_gpa4(recomputed)
    gpa_classification = classify_gpa4(avg_grade)
    # #region agent log
    _dbg('H1', 'student_routes.py:dashboard', 'dashboard GPA scales', {
        'avg_score_10': avg_score_10,
        'gpa4': avg_grade,
        'gpa_classification': gpa_classification,
        'grade_count': len(recomputed),
        'display_denominator': 4,
        'weights': 'A1 20 A2 30 A3 50',
    })
    # #endregion

    # 6. Overall progress percentage
    submitted_count = query_db("SELECT COUNT(*) as count FROM submissions WHERE student_id = ?", (user_id,), one=True)['count']
    progress_pct = round((submitted_count / assignments_count * 100), 1) if assignments_count > 0 else 0

    # 7. Upcoming assignments
    upcoming_assignments = query_db("""
        SELECT a.*, c.name as course_name, s.score, s.submitted_at
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        JOIN enrollments e ON a.course_id = e.course_id
        LEFT JOIN submissions s ON a.id = s.assignment_id AND s.student_id = e.student_id
        WHERE e.student_id = ?
        ORDER BY a.due_date ASC
        LIMIT 5
    """, (user_id,))

    # 8. Recent notifications
    recent_notifs = query_db("""
        SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 5
    """, (user_id,))

    # 9. Enrolled classes preview
    recent_classes = query_db("""
        SELECT c.*, u.full_name as teacher_name, sub.name as subject_name,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as student_count
        FROM courses c
        JOIN enrollments e ON c.id = e.course_id
        JOIN users u ON c.teacher_id = u.id
        JOIN subjects sub ON c.subject_id = sub.id
        WHERE e.student_id = ?
        LIMIT 4
    """, (user_id,))

    return render_template(
        'student/dashboard.html',
        user=user,
        student_info=student_info,
        classes_count=classes_count,
        materials_count=materials_count,
        assignments_count=assignments_count,
        exams_count=exams_count,
        avg_grade=avg_grade,
        gpa_classification=gpa_classification,
        progress_pct=progress_pct,
        upcoming_assignments=upcoming_assignments,
        recent_notifs=recent_notifs,
        recent_classes=recent_classes
    )

@student_bp.route('/classes')
@login_required
@role_required('student')
def classes():
    user = get_current_user()
    search = request.args.get('search', '').strip()
    subject_id = request.args.get('subject_id', '')

    query = """
        SELECT c.*, u.full_name as teacher_name, sub.name as subject_name, sub.credits,
               (SELECT COUNT(*) FROM enrollments WHERE course_id = c.id) as student_count
        FROM courses c
        JOIN enrollments e ON c.id = e.course_id
        JOIN users u ON c.teacher_id = u.id
        JOIN subjects sub ON c.subject_id = sub.id
        WHERE e.student_id = ?
    """
    params = [user['id']]

    if search:
        query += " AND (c.name LIKE ? OR c.code LIKE ? OR sub.name LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])
    if subject_id:
        query += " AND c.subject_id = ?"
        params.append(subject_id)

    query += " ORDER BY c.id DESC"
    enrolled_courses = query_db(query, params)
    all_subjects = query_db("SELECT * FROM subjects ORDER BY name ASC")

    return render_template('student/classes.html', courses=enrolled_courses, subjects=all_subjects, search=search, selected_subject=subject_id)

@student_bp.route('/class/<int:course_id>')
@login_required
@role_required('student')
def class_detail(course_id):
    user = get_current_user()

    # Check enrollment
    enrollment = query_db("SELECT * FROM enrollments WHERE course_id = ? AND student_id = ?", (course_id, user['id']), one=True)
    if not enrollment:
        flash("Bạn chưa đăng ký tham gia lớp học này.", "danger")
        return redirect(url_for('student_bp.classes'))

    course = query_db("""
        SELECT c.*, u.full_name as teacher_name, u.email as teacher_email, u.phone as teacher_phone,
               sub.name as subject_name, sub.code as subject_code, sub.credits, sub.description as subject_desc
        FROM courses c
        JOIN users u ON c.teacher_id = u.id
        JOIN subjects sub ON c.subject_id = sub.id
        WHERE c.id = ?
    """, (course_id,), one=True)

    materials = query_db("SELECT m.*, u.full_name as uploader FROM materials m JOIN users u ON m.uploaded_by = u.id WHERE m.course_id = ? ORDER BY m.created_at DESC", (course_id,))
    assignments = query_db("""
        SELECT a.*, s.submitted_at, s.score
        FROM assignments a
        LEFT JOIN submissions s ON a.id = s.assignment_id AND s.student_id = ?
        WHERE a.course_id = ?
        ORDER BY a.due_date ASC
    """, (user['id'], course_id))

    exams = query_db("""
        SELECT ex.*, er.score as my_score, er.submitted_at as exam_submitted_at
        FROM exams ex
        LEFT JOIN exam_results er ON ex.id = er.exam_id AND er.student_id = ?
        WHERE ex.course_id = ?
        ORDER BY ex.created_at DESC
    """, (user['id'], course_id))

    members = query_db("""
        SELECT u.full_name, u.email, u.avatar, st.student_code
        FROM enrollments e
        JOIN users u ON e.student_id = u.id
        LEFT JOIN students st ON u.id = st.user_id
        WHERE e.course_id = ?
        ORDER BY u.full_name ASC
    """, (course_id,))

    return render_template(
        'student/class_detail.html',
        course=course,
        materials=materials,
        assignments=assignments,
        exams=exams,
        members=members
    )

@student_bp.route('/materials')
@login_required
@role_required('student')
def materials():
    user = get_current_user()
    search = request.args.get('search', '').strip()
    course_id = request.args.get('course_id', '')
    file_type = request.args.get('file_type', '')

    query = """
        SELECT m.*, c.name as course_name, u.full_name as uploader_name
        FROM materials m
        JOIN courses c ON m.course_id = c.id
        JOIN enrollments e ON c.id = e.course_id
        JOIN users u ON m.uploaded_by = u.id
        WHERE e.student_id = ?
    """
    params = [user['id']]

    if search:
        query += " AND (m.title LIKE ? OR m.description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if course_id:
        query += " AND m.course_id = ?"
        params.append(course_id)
    if file_type:
        query += " AND m.file_type = ?"
        params.append(file_type)

    query += " ORDER BY m.created_at DESC"
    materials_list = query_db(query, params)

    enrolled_courses = query_db("""
        SELECT c.id, c.name FROM courses c JOIN enrollments e ON c.id = e.course_id WHERE e.student_id = ?
    """, (user['id'],))

    return render_template(
        'student/materials.html',
        materials=materials_list,
        courses=enrolled_courses,
        search=search,
        selected_course=course_id,
        selected_type=file_type
    )

@student_bp.route('/assignments')
@login_required
@role_required('student')
def assignments():
    user = get_current_user()
    search = request.args.get('search', '').strip()
    course_id = request.args.get('course_id', '')
    status = request.args.get('status', '')

    query = """
        SELECT a.*, c.name as course_name, s.file_path as sub_file, s.submitted_at, s.score, s.feedback
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        JOIN enrollments e ON c.id = e.course_id
        LEFT JOIN submissions s ON a.id = s.assignment_id AND s.student_id = ?
        WHERE e.student_id = ?
    """
    params = [user['id'], user['id']]

    if search:
        query += " AND (a.title LIKE ? OR a.description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if course_id:
        query += " AND a.course_id = ?"
        params.append(course_id)

    query += " ORDER BY a.due_date ASC"
    all_assignments = query_db(query, params)

    # Filter by status post query for accuracy
    filtered_assignments = []
    for item in all_assignments:
        item_status = "Chưa làm"
        if item['score'] is not None:
            item_status = "Đã chấm"
        elif item['submitted_at'] is not None:
            item_status = "Đã nộp"

        if status:
            if status == item_status:
                filtered_assignments.append(item)
        else:
            filtered_assignments.append(item)

    enrolled_courses = query_db("""
        SELECT c.id, c.name FROM courses c JOIN enrollments e ON c.id = e.course_id WHERE e.student_id = ?
    """, (user['id'],))

    return render_template(
        'student/assignments.html',
        assignments=filtered_assignments,
        courses=enrolled_courses,
        search=search,
        selected_course=course_id,
        selected_status=status
    )

@student_bp.route('/assignment/<int:assignment_id>')
@login_required
@role_required('student')
def assignment_detail(assignment_id):
    user = get_current_user()

    assignment = query_db("""
        SELECT a.*, c.name as course_name, u.full_name as teacher_name
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        JOIN users u ON a.created_by = u.id
        WHERE a.id = ?
    """, (assignment_id,), one=True)

    if not assignment:
        flash("Bài tập không tồn tại.", "danger")
        return redirect(url_for('student_bp.assignments'))

    submission = query_db("""
        SELECT * FROM submissions WHERE assignment_id = ? AND student_id = ?
    """, (assignment_id, user['id']), one=True)

    return render_template('student/assignment_detail.html', assignment=assignment, submission=submission)

@student_bp.route('/assignment/<int:assignment_id>/submit', methods=['POST'])
@login_required
@role_required('student')
def submit_assignment(assignment_id):
    user = get_current_user()
    notes = request.form.get('notes', '').strip()
    file = request.files.get('submission_file')

    file_path = "/static/uploads/default_submission.zip"
    if file and file.filename != '':
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"sub_{user['id']}_{assignment_id}_{file.filename}"
        file.save(os.path.join(upload_folder, filename))
        file_path = f"/static/uploads/{filename}"

    existing = query_db("SELECT id FROM submissions WHERE assignment_id = ? AND student_id = ?", (assignment_id, user['id']), one=True)
    if existing:
        execute_db("""
            UPDATE submissions
            SET file_path = ?, notes = ?, submitted_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (file_path, notes, existing['id']))
        flash("Cập nhật bài nộp thành công!", "success")
    else:
        execute_db("""
            INSERT INTO submissions (assignment_id, student_id, file_path, notes)
            VALUES (?, ?, ?, ?)
        """, (assignment_id, user['id'], file_path, notes))
        flash("Nộp bài tập thành công!", "success")

    return redirect(url_for('student_bp.assignment_detail', assignment_id=assignment_id))

@student_bp.route('/exams')
@login_required
@role_required('student')
def exams():
    user = get_current_user()

    exams_list = query_db("""
        SELECT ex.*, c.name as course_name, er.score as student_score, er.submitted_at as exam_submitted_at,
               (SELECT COUNT(*) FROM questions WHERE exam_id = ex.id) as question_count
        FROM exams ex
        JOIN courses c ON ex.course_id = c.id
        JOIN enrollments e ON c.id = e.course_id
        LEFT JOIN exam_results er ON ex.id = er.exam_id AND er.student_id = ?
        WHERE e.student_id = ?
        ORDER BY ex.created_at DESC
    """, (user['id'], user['id']))

    return render_template('student/exams.html', exams=exams_list)

@student_bp.route('/exam/<int:exam_id>/take')
@login_required
@role_required('student')
def take_exam(exam_id):
    user = get_current_user()

    # Check if already submitted
    existing_result = query_db("SELECT * FROM exam_results WHERE exam_id = ? AND student_id = ?", (exam_id, user['id']), one=True)
    if existing_result:
        flash("Bạn đã hoàn thành bài kiểm tra này trước đó.", "info")
        return redirect(url_for('student_bp.exam_result', exam_id=exam_id))

    exam = query_db("""
        SELECT ex.*, c.name as course_name FROM exams ex JOIN courses c ON ex.course_id = c.id WHERE ex.id = ?
    """, (exam_id,), one=True)

    if not exam:
        flash("Bài kiểm tra không tồn tại.", "danger")
        return redirect(url_for('student_bp.exams'))

    questions = query_db("SELECT * FROM questions WHERE exam_id = ?", (exam_id,))

    # Format JSON options
    formatted_questions = []
    for q in questions:
        q_dict = dict(q)
        q_dict['options'] = json.loads(q['options_json'])
        formatted_questions.append(q_dict)

    return render_template('student/take_exam.html', exam=exam, questions=formatted_questions)

@student_bp.route('/exam/<int:exam_id>/submit', methods=['POST'])
@login_required
@role_required('student')
def submit_exam(exam_id):
    user = get_current_user()

    existing_result = query_db("SELECT id FROM exam_results WHERE exam_id = ? AND student_id = ?", (exam_id, user['id']), one=True)
    if existing_result:
        return redirect(url_for('student_bp.exam_result', exam_id=exam_id))

    questions = query_db("SELECT * FROM questions WHERE exam_id = ?", (exam_id,))
    total_questions = len(questions)
    correct_count = 0
    total_points_earned = 0.0
    total_possible_points = sum(q['points'] for q in questions) if questions else 10.0

    student_answers = {}

    for q in questions:
        q_id = str(q['id'])
        correct_indices = json.loads(q['correct_answers_json'])

        # Selected options from form
        selected = request.form.getlist(f"question_{q_id}")
        selected_indices = [int(x) for x in selected if x.isdigit()]
        student_answers[q_id] = selected_indices

        if sorted(selected_indices) == sorted(correct_indices):
            correct_count += 1
            total_points_earned += q['points']

    final_score = round((total_points_earned / total_possible_points) * 10.0, 1) if total_possible_points > 0 else 0.0

    execute_db("""
        INSERT INTO exam_results (exam_id, student_id, score, total_questions, correct_count, answers_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (exam_id, user['id'], final_score, total_questions, correct_count, json.dumps(student_answers)))

    flash(f"Nộp bài kiểm tra thành công! Điểm của bạn: {final_score}/10", "success")
    return redirect(url_for('student_bp.exam_result', exam_id=exam_id))

@student_bp.route('/exam/<int:exam_id>/result')
@login_required
@role_required('student')
def exam_result(exam_id):
    user = get_current_user()

    result = query_db("SELECT * FROM exam_results WHERE exam_id = ? AND student_id = ?", (exam_id, user['id']), one=True)
    if not result:
        flash("Chưa tìm thấy kết quả làm bài.", "danger")
        return redirect(url_for('student_bp.exams'))

    exam = query_db("SELECT ex.*, c.name as course_name FROM exams ex JOIN courses c ON ex.course_id = c.id WHERE ex.id = ?", (exam_id,), one=True)
    questions = query_db("SELECT * FROM questions WHERE exam_id = ?", (exam_id,))

    answers_given = json.loads(result['answers_json']) if result['answers_json'] else {}

    formatted_questions = []
    for q in questions:
        q_dict = dict(q)
        q_dict['options'] = json.loads(q['options_json'])
        q_dict['correct_indices'] = json.loads(q['correct_answers_json'])
        q_dict['student_selected'] = answers_given.get(str(q['id']), [])
        formatted_questions.append(q_dict)

    return render_template('student/exam_result.html', exam=exam, result=result, questions=formatted_questions)

@student_bp.route('/academic-results')
@login_required
@role_required('student')
def academic_results():
    user = get_current_user()

    grades_list = query_db("""
        SELECT g.*, c.name as course_name, c.code as course_code, c.semester, c.academic_year, sub.credits
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        JOIN subjects sub ON c.subject_id = sub.id
        WHERE g.student_id = ?
    """, (user['id'],))

    latest_term = query_db("""
        SELECT c.semester, c.academic_year
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        WHERE g.student_id = ?
        ORDER BY c.academic_year DESC, c.semester DESC
        LIMIT 1
    """, (user['id'],), one=True)

    semester_grades = grades_list
    current_semester_label = ''
    if latest_term:
        current_semester_label = f"{latest_term['semester']}"
        semester_grades = [
            g for g in grades_list
            if g['semester'] == latest_term['semester'] and g['academic_year'] == latest_term['academic_year']
        ]

    formatted_grades = []
    for g in grades_list:
        item = dict(g)
        item['a1'], item['a2'], item['a3'] = grade_components(item)
        item['total_score'] = compute_total10(item['a1'], item['a2'], item['a3'])
        formatted_grades.append(item)

    semester_formatted = formatted_grades
    if latest_term:
        semester_formatted = [
            g for g in formatted_grades
            if g['semester'] == latest_term['semester'] and g['academic_year'] == latest_term['academic_year']
        ]

    avg_score = (
        round(sum((g['total_score'] or 0) for g in semester_formatted) / len(semester_formatted), 2)
        if semester_formatted else 0.0
    )
    gpa4 = compute_gpa4(formatted_grades)
    total_courses = len(formatted_grades)
    completed_courses = len([g for g in formatted_grades if g['total_score'] >= 5.0])
    classification = classify_gpa4(gpa4)

    # #region agent log
    _dbg('H2', 'student_routes.py:academic_results', 'academic results scales', {
        'semester_avg_10': avg_score,
        'gpa4': gpa4,
        'current_semester': current_semester_label,
        'semester_grade_count': len(semester_grades),
        'all_grade_count': total_courses,
        'course_totals_10': [g['total_score'] for g in formatted_grades],
        'classification': classification,
    })
    _dbg('H6', 'student_routes.py:academic_results', 'A1 A2 A3 components', {
        'components': [
            {'code': g.get('course_code'), 'a1': g['a1'], 'a2': g['a2'], 'a3': g['a3'], 'assignment': g['assignment_score'], 'quiz': g['quiz_score']}
            for g in formatted_grades
        ],
        'column_count': 3,
    })
    # #endregion

    return render_template(
        'student/academic_results.html',
        grades=formatted_grades,
        avg_score=avg_score,
        gpa4=gpa4,
        current_semester_label=current_semester_label,
        total_courses=total_courses,
        completed_courses=completed_courses,
        classification=classification
    )

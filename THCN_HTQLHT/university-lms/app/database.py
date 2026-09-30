import sqlite3
import os
from flask import g

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lms.db")

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DB_PATH
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(db_path=None):
    target_path = db_path or DB_PATH
    conn = sqlite3.connect(target_path)
    cursor = conn.cursor()

    # Foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'teacher', 'student')),
        avatar TEXT DEFAULT '/static/images/default_avatar.png',
        phone TEXT DEFAULT '',
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Departments (Khoa)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        description TEXT DEFAULT ''
    );
    """)

    # 3. Majors (Ngành)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS majors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_id INTEGER NOT NULL,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (department_id) REFERENCES departments (id) ON DELETE CASCADE
    );
    """)

    # 4. Student Classes (Lớp sinh hoạt)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        major_id INTEGER NOT NULL,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        year TEXT DEFAULT '2024-2028',
        FOREIGN KEY (major_id) REFERENCES majors (id) ON DELETE CASCADE
    );
    """)

    # 5. Students
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        user_id INTEGER PRIMARY KEY,
        student_code TEXT UNIQUE NOT NULL,
        department_id INTEGER,
        major_id INTEGER,
        student_class_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (department_id) REFERENCES departments (id) ON DELETE SET NULL,
        FOREIGN KEY (major_id) REFERENCES majors (id) ON DELETE SET NULL,
        FOREIGN KEY (student_class_id) REFERENCES student_classes (id) ON DELETE SET NULL
    );
    """)

    # 6. Teachers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        user_id INTEGER PRIMARY KEY,
        teacher_code TEXT UNIQUE NOT NULL,
        department_id INTEGER,
        title TEXT DEFAULT 'Giảng viên',
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (department_id) REFERENCES departments (id) ON DELETE SET NULL
    );
    """)

    # 7. Subjects (Môn học)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_id INTEGER,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        credits INTEGER NOT NULL DEFAULT 3,
        description TEXT DEFAULT '',
        FOREIGN KEY (department_id) REFERENCES departments (id) ON DELETE SET NULL
    );
    """)

    # 8. Courses (Lớp học phần)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        semester TEXT DEFAULT 'HK1 (2024-2025)',
        academic_year TEXT DEFAULT '2024-2025',
        room TEXT DEFAULT 'A101',
        schedule_info TEXT DEFAULT 'Thứ 2 (08:00 - 11:30)',
        description TEXT DEFAULT '',
        FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE,
        FOREIGN KEY (teacher_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # 9. Enrollments (Đăng ký môn học)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active',
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE,
        UNIQUE(course_id, student_id)
    );
    """)

    # 10. Materials (Tài liệu học tập)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT DEFAULT '',
        file_path TEXT NOT NULL,
        file_type TEXT NOT NULL, -- PDF, Word, PowerPoint, Video, Image, Zip
        file_size TEXT DEFAULT '1.2 MB',
        uploaded_by INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
        FOREIGN KEY (uploaded_by) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # 11. Assignments (Bài tập)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        file_path TEXT DEFAULT '',
        due_date TIMESTAMP NOT NULL,
        max_points REAL DEFAULT 10.0,
        created_by INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
        FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # 12. Submissions (Bài nộp của sinh viên)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        file_path TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        score REAL DEFAULT NULL,
        feedback TEXT DEFAULT '',
        graded_at TIMESTAMP DEFAULT NULL,
        FOREIGN KEY (assignment_id) REFERENCES assignments (id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE,
        UNIQUE(assignment_id, student_id)
    );
    """)

    # 13. Exams (Bài kiểm tra / Thi trực tuyến)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT DEFAULT '',
        duration_minutes INTEGER NOT NULL DEFAULT 45,
        max_score REAL DEFAULT 10.0,
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        created_by INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
        FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # 14. Questions (Câu hỏi kiểm tra)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        question_type TEXT DEFAULT 'single', -- single, multiple, true_false
        options_json TEXT NOT NULL, -- JSON string array of options ["Đáp án A", "Đáp án B", ...]
        correct_answers_json TEXT NOT NULL, -- JSON string array of correct indices [0] or [0, 2]
        points REAL DEFAULT 1.0,
        FOREIGN KEY (exam_id) REFERENCES exams (id) ON DELETE CASCADE
    );
    """)

    # 15. Exam Results (Kết quả kiểm tra sinh viên)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        score REAL NOT NULL,
        total_questions INTEGER NOT NULL,
        correct_count INTEGER NOT NULL,
        answers_json TEXT DEFAULT '{}', -- JSON student selected answers
        FOREIGN KEY (exam_id) REFERENCES exams (id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # 16. Grades (Bảng điểm tổng hợp)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        assignment_score REAL DEFAULT 0.0,
        quiz_score REAL DEFAULT 0.0,
        midterm_score REAL DEFAULT 0.0,
        final_score REAL DEFAULT 0.0,
        total_score REAL DEFAULT 0.0,
        letter_grade TEXT DEFAULT 'F',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE,
        UNIQUE(course_id, student_id)
    );
    """)

    # 17. Notifications (Thông báo)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        category TEXT DEFAULT 'system', -- assignment, exam, material, grade, teacher, system
        link TEXT DEFAULT '#',
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id

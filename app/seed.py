import sqlite3
import json
import os
from werkzeug.security import generate_password_hash
from database import DB_PATH, init_db

def seed_database():
    init_db(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing data
    tables = [
        "notifications", "grades", "exam_results", "questions", "exams",
        "submissions", "assignments", "materials", "enrollments", "courses",
        "subjects", "teachers", "students", "student_classes", "majors",
        "departments", "users"
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")

    hashed_admin_pass = generate_password_hash("admin123")
    hashed_teacher_pass = generate_password_hash("teacher123")
    hashed_student_pass = generate_password_hash("student123")

    # 1. Insert Users
    # Admin
    cursor.execute("""
        INSERT INTO users (email, password_hash, full_name, role, phone)
        VALUES (?, ?, ?, ?, ?)
    """, ("admin@example.com", hashed_admin_pass, "Nguyễn Văn Quản Trị", "admin", "0901234567"))
    admin_id = cursor.lastrowid

    # Primary Teacher (teacher@example.com)
    cursor.execute("""
        INSERT INTO users (email, password_hash, full_name, role, phone)
        VALUES (?, ?, ?, ?, ?)
    """, ("teacher@example.com", hashed_teacher_pass, "TS. Nguyễn Văn Giảng", "teacher", "0912345678"))
    main_teacher_id = cursor.lastrowid

    # 9 Additional Teachers
    teacher_names = [
        "PGS.TS. Lê Thị Thảo", "ThS. Trần Đức Minh", "TS. Phạm Hoàng Nam",
        "ThS. Vũ Thị Ngọc", "TS. Đặng Quốc Bảo", "ThS. Nguyễn Thị Huệ",
        "TS. Bùi Anh Tuấn", "ThS. Hoàng Trọng Hiếu", "TS. Đỗ Thị Thu"
    ]
    teacher_ids = [main_teacher_id]
    for i, name in enumerate(teacher_names, start=2):
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, role, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (f"teacher{i}@example.com", hashed_teacher_pass, name, "teacher", f"091234567{i}"))
        teacher_ids.append(cursor.lastrowid)

    # Primary Student (student@example.com)
    cursor.execute("""
        INSERT INTO users (email, password_hash, full_name, role, phone)
        VALUES (?, ?, ?, ?, ?)
    """, ("student@example.com", hashed_student_pass, "Trần Thị Sinh Viên", "student", "0987654321"))
    main_student_id = cursor.lastrowid

    # 49 Additional Students
    student_names = [
        "Nguyễn An", "Trần Bình", "Lê Cường", "Phạm Dũng", "Hoàng Giang",
        "Vũ Hương", "Đặng Khánh", "Bùi Lan", "Đỗ Minh", "Hồ Nam",
        "Ngô Phương", "Dương Quân", "Lý Sơn", "Võ Trang", "Phan Uyên",
        "Đinh Vinh", "Nguyễn Yến", "Trần Bảo", "Lê Chi", "Phạm Đức",
        "Hoàng Hà", "Vũ Huy", "Đặng Kiên", "Bùi Linh", "Đỗ Mai",
        "Hồ Nguyên", "Ngô Phong", "Dương Quỳnh", "Lý Tâm", "Võ Tuấn",
        "Phan Vân", "Đinh Xuân", "Nguyễn Hải", "Trần Hằng", "Lê Khôi",
        "Phạm Lâm", "Hoàng Nghĩa", "Vũ Oanh", "Đặng Phúc", "Bùi Quyên",
        "Đỗ Thảo", "Hồ Trí", "Ngô Uyên", "Dương Việt", "Lý Vũ",
        "Võ Ý", "Phan Anh", "Đinh Bách", "Nguyễn Cúc"
    ]
    student_ids = [main_student_id]
    for i, name in enumerate(student_names, start=2):
        cursor.execute("""
            INSERT INTO users (email, password_hash, full_name, role, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (f"student{i}@example.com", hashed_student_pass, name, "student", f"09876543{i:02d}"))
        student_ids.append(cursor.lastrowid)

    # 2. Departments
    cursor.execute("INSERT INTO departments (code, name, description) VALUES ('CNTT', 'Khoa Công nghệ thông tin', 'Đào tạo kỹ sư phần mềm, AI và khoa học máy tính');")
    dept_cntt = cursor.lastrowid
    cursor.execute("INSERT INTO departments (code, name, description) VALUES ('KT', 'Khoa Kinh tế & Quản trị', 'Đào tạo cử nhân kinh tế, tài chính và quản trị kinh doanh');")
    dept_kt = cursor.lastrowid
    cursor.execute("INSERT INTO departments (code, name, description) VALUES ('NN', 'Khoa Ngoại ngữ', 'Đào tạo cử nhân Tiếng Anh chuyên ngành và ngôn ngữ học');")
    dept_nn = cursor.lastrowid

    # 3. Majors
    cursor.execute("INSERT INTO majors (department_id, code, name) VALUES (?, 'KTPM', 'Kỹ thuật phần mềm');", (dept_cntt,))
    major_ktpm = cursor.lastrowid
    cursor.execute("INSERT INTO majors (department_id, code, name) VALUES (?, 'TTNT', 'Trí tuệ nhân tạo');", (dept_cntt,))
    major_ttnt = cursor.lastrowid
    cursor.execute("INSERT INTO majors (department_id, code, name) VALUES (?, 'QTKD', 'Quản trị kinh doanh');", (dept_kt,))
    major_qtkd = cursor.lastrowid
    cursor.execute("INSERT INTO majors (department_id, code, name) VALUES (?, 'TCNH', 'Tài chính ngân hàng');", (dept_kt,))
    major_tcnh = cursor.lastrowid
    cursor.execute("INSERT INTO majors (department_id, code, name) VALUES (?, 'NNA', 'Ngôn ngữ Anh');", (dept_nn,))
    major_nna = cursor.lastrowid

    # 4. Student Classes
    cursor.execute("INSERT INTO student_classes (major_id, code, name, year) VALUES (?, 'SE1801', 'Lớp KTPM K18 - 01', '2024-2028');", (major_ktpm,))
    class_se1 = cursor.lastrowid
    cursor.execute("INSERT INTO student_classes (major_id, code, name, year) VALUES (?, 'SE1802', 'Lớp KTPM K18 - 02', '2024-2028');", (major_ktpm,))
    class_se2 = cursor.lastrowid
    cursor.execute("INSERT INTO student_classes (major_id, code, name, year) VALUES (?, 'AI1801', 'Lớp TTNT K18 - 01', '2024-2028');", (major_ttnt,))
    class_ai1 = cursor.lastrowid
    cursor.execute("INSERT INTO student_classes (major_id, code, name, year) VALUES (?, 'BA1801', 'Lớp QTKD K18 - 01', '2024-2028');", (major_qtkd,))
    class_ba1 = cursor.lastrowid
    cursor.execute("INSERT INTO student_classes (major_id, code, name, year) VALUES (?, 'EN1801', 'Lớp NNA K18 - 01', '2024-2028');", (major_nna,))
    class_en1 = cursor.lastrowid

    # Link Students to Details
    for idx, sid in enumerate(student_ids):
        code = f"SV2024{idx+1:04d}"
        if idx == 0:
            code = "SV20240001" # Demo student
        c_id = class_se1 if idx < 10 else (class_se2 if idx < 20 else (class_ai1 if idx < 30 else (class_ba1 if idx < 40 else class_en1)))
        m_id = major_ktpm if idx < 20 else (major_ttnt if idx < 30 else (major_qtkd if idx < 40 else major_nna))
        d_id = dept_cntt if idx < 30 else (dept_kt if idx < 40 else dept_nn)
        cursor.execute("INSERT INTO students (user_id, student_code, department_id, major_id, student_class_id) VALUES (?, ?, ?, ?, ?);",
                       (sid, code, d_id, m_id, c_id))

    # Link Teachers to Details
    for idx, tid in enumerate(teacher_ids):
        code = f"GV2024{idx+1:03d}"
        d_id = dept_cntt if idx < 4 else (dept_kt if idx < 7 else dept_nn)
        cursor.execute("INSERT INTO teachers (user_id, teacher_code, department_id, title) VALUES (?, ?, ?, ?);",
                       (tid, code, d_id, "Giảng viên chính" if idx == 0 else "Giảng viên"))

    # 5. Subjects
    subjects_data = [
        (dept_cntt, "WEB201", "Lập trình Web nâng cao", 3, "Học kiến thức HTML5, CSS3, JavaScript, Flask và RESTful API"),
        (dept_cntt, "CSDL101", "Cơ sở dữ liệu quan hệ", 3, "Thiết kế CSDL, SQL, Chuẩn hóa dữ liệu và Tối ưu truy vấn"),
        (dept_cntt, "CTDL202", "Cấu trúc dữ liệu & Giải thuật", 4, "Mảng, Danh sách liên kết, Cây, Đồ thị, Thuật toán sắp xếp"),
        (dept_cntt, "AI301", "Nhập môn Trí tuệ nhân tạo", 3, "Học máy, Mạng Nơ-ron và Thị giác máy tính"),
        (dept_cntt, "ATTT401", "An toàn & Bảo mật thông tin", 3, "Mã hóa dữ liệu, Xác thực OAuth2, OWASP Top 10 và Firewall"),
        (dept_kt, "QTKD101", "Quản trị học đại cương", 3, "Các nguyên lý quản trị hiện đại trong doanh nghiệp"),
        (dept_kt, "TCNH201", "Tài chính doanh nghiệp", 3, "Phân tích báo cáo tài chính, quản lý dòng tiền và đầu tư"),
        (dept_nn, "ENG101", "Tiếng Anh chuyên ngành IT", 3, "Thuật ngữ tiếng Anh chuyên ngành công nghệ thông tin"),
        (dept_cntt, "PTTK201", "Phân tích & Thiết kế hệ thống", 3, "UML, Sơ đồ Use Case, Sequence Diagram và Kiến trúc phần mềm"),
        (dept_cntt, "ML302", "Học máy ứng dụng (Machine Learning)", 4, "Scikit-Learn, Regression, Classification, Clustering")
    ]

    subject_ids = []
    for s in subjects_data:
        cursor.execute("INSERT INTO subjects (department_id, code, name, credits, description) VALUES (?, ?, ?, ?, ?);", s)
        subject_ids.append(cursor.lastrowid)

    # 6. Courses (Lớp học phần)
    courses_data = [
        (subject_ids[0], main_teacher_id, "LHP_WEB201_01", "Lập trình Web - Nhóm 01", "HK1 (2024-2025)", "2024-2025", "Phòng A.201", "Thứ 2 (08:00 - 11:30)", "Lớp học phần Lập trình Web dành cho sinh viên CNTT"),
        (subject_ids[1], main_teacher_id, "LHP_CSDL101_01", "Cơ sở dữ liệu - Nhóm 01", "HK1 (2024-2025)", "2024-2025", "Phòng B.105", "Thứ 3 (13:00 - 16:30)", "Lớp học phần CSDL nâng cao"),
        (subject_ids[2], teacher_ids[1], "LHP_CTDL202_01", "Cấu trúc dữ liệu - Nhóm 01", "HK1 (2024-2025)", "2024-2025", "Phòng C.302", "Thứ 4 (08:00 - 11:30)", "Cấu trúc dữ liệu và giải thuật"),
        (subject_ids[3], teacher_ids[2], "LHP_AI301_01", "Trí tuệ nhân tạo - Nhóm 01", "HK1 (2024-2025)", "2024-2025", "Lab AI.01", "Thứ 5 (13:00 - 16:30)", "Nhập môn AI & Deep Learning"),
        (subject_ids[4], teacher_ids[3], "LHP_ATTT401_01", "An toàn thông tin - Nhóm 01", "HK1 (2024-2025)", "2024-2025", "Phòng A.404", "Thứ 6 (08:00 - 11:30)", "Bảo mật ứng dụng Web & Mạng"),
        (subject_ids[5], teacher_ids[4], "LHP_QTKD101_01", "Quản trị học - Nhóm 01", "HK1 (2024-2025)", "2024-2025", "Phòng D.101", "Thứ 2 (13:00 - 16:30)", "Quản trị doanh nghiệp 4.0"),
        (subject_ids[6], teacher_ids[5], "LHP_TCNH201_01", "Tài chính doanh nghiệp - Nhóm 01", "HK1 (2024-2025)", "2024-2025", "Phòng D.202", "Thứ 3 (08:00 - 11:30)", "Phân tích tài chính và đầu tư"),
        (subject_ids[7], teacher_ids[6], "LHP_ENG101_01", "Tiếng Anh IT - Nhóm 01", "HK1 (2024-2025)", "2024-2025", "Phòng E.101", "Thứ 4 (13:00 - 16:30)", "Kỹ năng đọc viết tài liệu kỹ thuật"),
        (subject_ids[8], teacher_ids[7], "LHP_PTTK201_01", "Phân tích thiết kế hệ thống - Nhóm 01", "HK1 (2024-2025)", "2024-2025", "Phòng A.303", "Thứ 5 (08:00 - 11:30)", "Thiết kế kiến trúc phần mềm"),
        (subject_ids[9], teacher_ids[8], "LHP_ML302_01", "Học máy ứng dụng - Nhóm 01", "HK1 (2024-2025)", "2024-2025", "Lab AI.02", "Thứ 6 (13:00 - 16:30)", "Thực hành Machine Learning với Python")
    ]

    course_ids = []
    for c in courses_data:
        cursor.execute("""
            INSERT INTO courses (subject_id, teacher_id, code, name, semester, academic_year, room, schedule_info, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, c)
        course_ids.append(cursor.lastrowid)

    # 7. Enrollments (Enroll main student in 5 courses, other students randomly)
    for cid in course_ids[:5]:
        cursor.execute("INSERT INTO enrollments (course_id, student_id) VALUES (?, ?);", (cid, main_student_id))

    for idx, sid in enumerate(student_ids[1:], start=1):
        # enroll in 3 to 4 courses
        assigned_courses = course_ids[idx % len(course_ids): idx % len(course_ids) + 4]
        for cid in assigned_courses:
            cursor.execute("INSERT OR IGNORE INTO enrollments (course_id, student_id) VALUES (?, ?);", (cid, sid))

    # 8. Materials
    materials_data = [
        (course_ids[0], "Giáo trình Lập trình Web đầy đủ", "Tài liệu tổng hợp kiến thức từ cơ bản đến nâng cao", "/static/uploads/giao_trinh_web.pdf", "PDF", "4.5 MB", main_teacher_id),
        (course_ids[0], "Slide Bài giảng Chương 1 - HTML5 & CSS3", "Bộ slide thuyết trình tuần 1", "/static/uploads/chuong1_html_css.pptx", "PowerPoint", "8.2 MB", main_teacher_id),
        (course_ids[0], "Slide Bài giảng Chương 2 - JavaScript ES6+", "Cú pháp hiện đại và lập trình bất đồng bộ Async/Await", "/static/uploads/chuong2_js_es6.pptx", "PowerPoint", "6.1 MB", main_teacher_id),
        (course_ids[0], "Mẫu dự án Thực hành Flask & SQLite", "Mã nguồn mẫu thực hành CRUD web ứng dụng", "/static/uploads/flask_demo_project.zip", "Zip", "12.4 MB", main_teacher_id),
        (course_ids[1], "Giáo trình Cơ sở dữ liệu chuẩn ISO", "Kiến thức thiết kế ERD và chuẩn hóa 1NF 2NF 3NF BCNF", "/static/uploads/giao_trinh_csdl.pdf", "PDF", "5.8 MB", main_teacher_id),
        (course_ids[1], "Hướng dẫn Cài đặt & Sử dụng SQLite Studio", "Tài liệu hướng dẫn trực quan", "/static/uploads/huong_dan_sqlite.docx", "Word", "2.1 MB", main_teacher_id),
        (course_ids[2], "Tài liệu Cấu trúc dữ liệu & Giải thuật", "Các bài toán kinh điển và cách tối ưu độ phức tạp Big-O", "/static/uploads/ctdl_gt_full.pdf", "PDF", "7.3 MB", teacher_ids[1]),
        (course_ids[3], "Slide Giới thiệu Trí tuệ nhân tạo", "Tổng quan về mạng Neural và Deep Learning", "/static/uploads/intro_ai.pptx", "PowerPoint", "14.2 MB", teacher_ids[2]),
        (course_ids[4], "Tài liệu OWASP Top 10 Bảo mật Web", "Danh sách 10 lỗ hổng bảo mật phổ biến nhất", "/static/uploads/owasp_top10.pdf", "PDF", "3.9 MB", teacher_ids[3]),
        (course_ids[0], "Video Hướng dẫn Deploy ứng dụng Web", "Video bài giảng thực hành đưa web lên server", "https://youtube.com/watch?v=demo", "Video", "Online", main_teacher_id)
    ]
    for m in materials_data:
        cursor.execute("""
            INSERT INTO materials (course_id, title, description, file_path, file_type, file_size, uploaded_by)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, m)

    # 9. Assignments
    assignments_data = [
        (course_ids[0], "Bài tập 1: Thiết kế Giao diện Responsive HTML/CSS", "Yêu cầu xây dựng trang web cá nhân sử dụng Flexbox & Grid, hiển thị mượt mà trên Mobile và Desktop.", "/static/uploads/de_bai_1.pdf", "2026-09-25 23:59:00", 10.0, main_teacher_id),
        (course_ids[0], "Bài tập 2: Lập trình Đăng nhập & Đăng ký với Flask", "Sử dụng Flask và SQLite để hoàn thiện chức năng Login/Register có mã hóa mật khẩu.", "/static/uploads/de_bai_2.pdf", "2026-10-05 23:59:00", 10.0, main_teacher_id),
        (course_ids[0], "Bài tập lớn: Xây dựng Website Bán hàng / LMS", "Làm theo nhóm hoặc cá nhân, có đầy đủ chức năng CRUD và nộp báo cáo kèm source code.", "/static/uploads/de_bai_lon.pdf", "2026-10-30 23:59:00", 10.0, main_teacher_id),
        (course_ids[1], "Bài tập 1: Vẽ Sơ đồ Thực thể Liên kết (ERD)", "Phân tích yêu cầu bài toán quản lý thư viện và vẽ sơ đồ ERD chuẩn.", "/static/uploads/de_bai_erd.pdf", "2026-09-28 23:59:00", 10.0, main_teacher_id),
        (course_ids[1], "Bài tập 2: Viết các Truy vấn SQL Nâng cao", "Thực hành các câu lệnh JOIN, GROUP BY, HAVING và Subquery trên cơ sở dữ liệu mẫu.", "/static/uploads/de_bai_sql.pdf", "2026-10-10 23:59:00", 10.0, main_teacher_id),
        (course_ids[2], "Bài tập Cài đặt Cây Nhị phân Tìm kiếm (BST)", "Cài đặt bằng C++ hoặc Python các thao tác Thêm, Xóa, Tìm kiếm trên cây BST.", "", "2026-10-02 23:59:00", 10.0, teacher_ids[1])
    ]

    assignment_ids = []
    for a in assignments_data:
        cursor.execute("""
            INSERT INTO assignments (course_id, title, description, file_path, due_date, max_points, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, a)
        assignment_ids.append(cursor.lastrowid)

    # 10. Submissions (Demo student submission for assignment 1)
    cursor.execute("""
        INSERT INTO submissions (assignment_id, student_id, file_path, notes, score, feedback, graded_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
    """, (assignment_ids[0], main_student_id, "/static/uploads/bai_lam_sv1.zip", "Em đã hoàn thành đủ yêu cầu và test trên cả Chrome lẫn Safari.", 9.5, "Giao diện rất đẹp, code sạch sẽ và responsive chuẩn! Tốt lắm."))

    cursor.execute("""
        INSERT INTO submissions (assignment_id, student_id, file_path, notes)
        VALUES (?, ?, ?, ?);
    """, (assignment_ids[1], main_student_id, "/static/uploads/bai_lam_sv1_bt2.zip", "Em đã thêm chức năng mã hóa Werkzeug."))

    # 11. Exams & Questions
    cursor.execute("""
        INSERT INTO exams (course_id, title, description, duration_minutes, max_score, start_time, end_time, created_by)
        VALUES (?, ?, ?, ?, ?, '2026-09-01 00:00:00', '2026-12-31 23:59:00', ?);
    """, (course_ids[0], "Kiểm tra Giữa kỳ: Lập trình Web", "Bài kiểm tra trắc nghiệm 15 phút đánh giá kiến thức HTML/CSS, JS và Flask.", 15, 10.0, main_teacher_id))
    exam_id_1 = cursor.lastrowid

    cursor.execute("""
        INSERT INTO exams (course_id, title, description, duration_minutes, max_score, start_time, end_time, created_by)
        VALUES (?, ?, ?, ?, ?, '2026-09-01 00:00:00', '2026-12-31 23:59:00', ?);
    """, (course_ids[1], "Kiểm tra 15 Phút: Kiến thức CSDL SQL", "Trắc nghiệm các câu lệnh SQL cơ bản và thiết kế ERD.", 15, 10.0, main_teacher_id))
    exam_id_2 = cursor.lastrowid

    # Questions for Exam 1
    questions_exam1 = [
        (exam_id_1, "Thẻ HTML nào được sử dụng để tạo đường dẫn liên kết (hyperlink)?", "single",
         json.dumps(["<link>", "<a>", "<href>", "<url>"]), json.dumps([1]), 2.0),
        (exam_id_1, "Trong CSS, thuộc tính nào được sử dụng để thay đổi màu nền của một phần tử?", "single",
         json.dumps(["color", "background-color", "bgcolor", "canvas-color"]), json.dumps([1]), 2.0),
        (exam_id_1, "Phương thức HTTP nào thường được dùng để gửi dữ liệu form tạo mới tài nguyên lên Server?", "single",
         json.dumps(["GET", "POST", "PUT", "DELETE"]), json.dumps([1]), 2.0),
        (exam_id_1, "Trong Flask framework, decorator nào dùng để định nghĩa một đường dẫn route?", "single",
         json.dumps(["@app.route()", "@app.url()", "@app.path()", "@app.get()"]), json.dumps([0]), 2.0),
        (exam_id_1, "SQLite có phải là một Hệ quản trị Cơ sở dữ liệu quan hệ dạng Server-Client không?", "true_false",
         json.dumps(["Đúng (Có Server riêng)", "Sai (Là tệp tin nhúng - Embedded DB)"]), json.dumps([1]), 2.0)
    ]

    for q in questions_exam1:
        cursor.execute("""
            INSERT INTO questions (exam_id, question_text, question_type, options_json, correct_answers_json, points)
            VALUES (?, ?, ?, ?, ?, ?);
        """, q)

    # Exam Result for Demo Student
    cursor.execute("""
        INSERT INTO exam_results (exam_id, student_id, score, total_questions, correct_count, answers_json)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (exam_id_1, main_student_id, 10.0, 5, 5, json.dumps({"1": [1], "2": [1], "3": [1], "4": [0], "5": [1]})))

    # 12. Grades (Bảng điểm)
    for cid in course_ids[:5]:
        b_score = 9.5 if cid == course_ids[0] else (8.5 if cid == course_ids[1] else 8.0)
        q_score = 10.0 if cid == course_ids[0] else 9.0
        m_score = 9.0 if cid == course_ids[0] else 8.0
        f_score = 9.5 if cid == course_ids[0] else 8.5
        a1 = round((b_score + q_score) / 2.0, 2)
        total = round(a1 * 0.2 + m_score * 0.3 + f_score * 0.5, 2)
        letter = "A+" if total >= 9.0 else ("A" if total >= 8.5 else "B+")
        cursor.execute("""
            INSERT INTO grades (course_id, student_id, assignment_score, quiz_score, midterm_score, final_score, total_score, letter_grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (cid, main_student_id, b_score, q_score, m_score, f_score, total, letter))

    # 13. Notifications
    notifs = [
        (main_student_id, "Bài tập mới", "Giảng viên đã giao Bài tập 2: Lập trình Đăng nhập & Đăng ký với Flask trong môn Lập trình Web.", "assignment", "/student/assignments", 0),
        (main_student_id, "Đã chấm điểm", "Bài tập 1: Thiết kế Giao diện Responsive đã được chấm 9.5/10 điểm.", "grade", "/student/academic-results", 0),
        (main_student_id, "Tài liệu mới", "Giảng viên đã đăng tải 'Mẫu dự án Thực hành Flask & SQLite'.", "material", "/student/materials", 1),
        (main_student_id, "Bài kiểm tra sắp diễn ra", "Bài kiểm tra 15 Phút CSDL sẽ mở vào tuần sau.", "exam", "/student/exams", 1),
        (main_teacher_id, "Bài nộp mới", "Sinh viên Trần Thị Sinh Viên vừa nộp bài cho 'Bài tập 2: Lập trình Đăng nhập'.", "assignment", "/teacher/assignments", 0),
        (main_teacher_id, "Thành viên lớp mới", "Đã có 50 sinh viên đăng ký tham gia lớp Lập trình Web - Nhóm 01.", "system", "/teacher/classes", 1)
    ]
    for n in notifs:
        cursor.execute("""
            INSERT INTO notifications (user_id, title, message, category, link, is_read)
            VALUES (?, ?, ?, ?, ?, ?);
        """, n)

    conn.commit()
    conn.close()
    print("Seeded database successfully!")

if __name__ == "__main__":
    seed_database()

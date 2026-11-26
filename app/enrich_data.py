import sqlite3
import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lms.db")

def enrich_database():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    print("--- 1. Bổ sung Khoa (Departments) để đạt 10 Khoa ---")
    current_depts = c.execute("SELECT code, name FROM departments").fetchall()
    existing_dept_codes = {r['code'] for r in current_depts}
    
    new_depts = [
        ('TOAN', 'Khoa Toán học & Thống kê', 'Đào tạo Toán ứng dụng, Xác suất thống kê và Khoa học dữ liệu'),
        ('VL', 'Khoa Vật lý & Công nghệ bán dẫn', 'Nghiên cứu và đào tạo Vật lý kỹ thuật, Vi mạch bán dẫn'),
        ('HOA', 'Khoa Hóa học & Môi trường', 'Đào tạo Hóa dược, Công nghệ vật liệu mới và Môi trường'),
        ('SH', 'Khoa Sinh học & Công nghệ sinh học', 'Đào tạo Công nghệ sinh học, Y sinh và Di truyền'),
        ('QTKD', 'Khoa Quản trị kinh doanh', 'Đào tạo Quản trị kinh doanh, Marketing số và Khởi nghiệp'),
        ('KHXH', 'Khoa Khoa học Xã hội & Nhân văn', 'Đào tạo Xã hội học, Tâm lý ứng dụng và Quan hệ công chúng'),
    ]
    for code, name, desc in new_depts:
        if code not in existing_dept_codes:
            c.execute("INSERT INTO departments (code, name, description) VALUES (?, ?, ?)", (code, name, desc))
            print(f"  + Thêm Khoa: {name} ({code})")
    
    dept_map = {r['code']: r['id'] for r in c.execute("SELECT id, code FROM departments").fetchall()}
    print(f"Tổng số Khoa hiện tại: {len(dept_map)}")

    print("\n--- 2. Bổ sung Ngành (Majors) để đạt 10 Ngành ---")
    current_majors = c.execute("SELECT code, name FROM majors").fetchall()
    existing_major_codes = {r['code'] for r in current_majors}

    new_majors = [
        (dept_map.get('SPTH', 4), 'GDTH', 'Giáo dục Tiểu học'),
        (dept_map.get('TOAN', 5), 'TOANUD', 'Toán ứng dụng & Khoa học dữ liệu'),
        (dept_map.get('VL', 6), 'VLUD', 'Vật lý kỹ thuật & Bán dẫn'),
        (dept_map.get('HOA', 7), 'HOADH', 'Hóa dược & Công nghệ vật liệu'),
        (dept_map.get('SH', 8), 'CNSH', 'Công nghệ sinh học'),
    ]
    for dept_id, code, name in new_majors:
        if code not in existing_major_codes:
            c.execute("INSERT INTO majors (department_id, code, name) VALUES (?, ?, ?)", (dept_id, code, name))
            print(f"  + Thêm Ngành: {name} ({code})")

    major_map = {r['code']: r['id'] for r in c.execute("SELECT id, code FROM majors").fetchall()}
    print(f"Tổng số Ngành hiện tại: {len(major_map)}")

    print("\n--- 3. Bổ sung Môn học (Subjects) để đạt 20 Môn học ---")
    current_subs = c.execute("SELECT code, name FROM subjects").fetchall()
    existing_sub_codes = {r['code'] for r in current_subs}

    new_subjects = [
        (dept_map.get('TOAN', 5), 'MATH101', 'Giải tích & Đại số tuyến tính', 3, 'Kiến thức toán cao cấp nền tảng'),
        (dept_map.get('TOAN', 5), 'XSTK102', 'Xác suất thống kê & Khoa học dữ liệu', 3, 'Ứng dụng thống kê trong phân tích dữ liệu'),
        (dept_map.get('VL', 6), 'PHY101', 'Vật lý đại cương & Bán dẫn', 3, 'Nguyên lý vật lý và công nghệ vật liệu bán dẫn'),
        (dept_map.get('HOA', 7), 'CHEM101', 'Hóa học đại cương & Vật liệu mới', 3, 'Hóa học ứng dụng trong sản xuất'),
        (dept_map.get('SH', 8), 'BIO101', 'Sinh học phân tử & Công nghệ vi sinh', 3, 'Kỹ thuật gen và vi sinh vật'),
        (dept_map.get('KT', 2), 'KTVI101', 'Kinh tế vi mô & vĩ mô', 3, 'Nguyên lý kinh tế ứng dụng'),
        (dept_map.get('QTKD', 9) or dept_map.get('KT', 2), 'MKT201', 'Marketing căn bản & Kỹ thuật số', 3, 'Chiến lược truyền thông và tiếp thị số'),
        (dept_map.get('SPTH', 4), 'GDH101', 'Tâm lý học & Giáo dục học đại cương', 3, 'Phương pháp sư phạm và tâm lý người học'),
        (dept_map.get('KHXH', 10), 'SOC101', 'Xã hội học đại cương & Kỹ năng mềm', 3, 'Phát triển kỹ năng giao tiếp và làm việc nhóm'),
        (dept_map.get('CNTT', 1), 'NET201', 'Mạng máy tính & Truyền thông dữ liệu', 3, 'Kiến trúc mạng TCP/IP và bảo mật kết nối'),
    ]
    for dept_id, code, name, creds, desc in new_subjects:
        if code not in existing_sub_codes:
            c.execute("INSERT INTO subjects (department_id, code, name, credits, description) VALUES (?, ?, ?, ?, ?)",
                      (dept_id, code, name, creds, desc))
            print(f"  + Thêm Môn học: {name} ({code})")

    subject_count = c.execute("SELECT COUNT(*) FROM subjects").fetchone()[0]
    print(f"Tổng số Môn học hiện tại: {subject_count}")

    print("\n--- 4. Bổ sung Lớp học sinh hoạt (Student Classes) để đạt 40 Lớp ---")
    current_classes = c.execute("SELECT code, name FROM student_classes").fetchall()
    existing_class_codes = {r['code'] for r in current_classes}

    # Generate classes across majors and years 2020-2027 (K20 - K27)
    majors_list = c.execute("SELECT id, code, name FROM majors").fetchall()
    
    # Target 40 classes total
    classes_to_add = []
    cohorts = [
        ('K20', '2020-2024'),
        ('K21', '2121-2025'),
        ('K22', '2022-2026'),
        ('K23', '2023-2027'),
        ('K24', '2024-2028'),
    ]
    
    for m in majors_list:
        m_code = m['code']
        m_id = m['id']
        for k_label, y_range in cohorts:
            c_code = f"{m_code}_{k_label}"
            c_name = f"Lớp {m_code} {k_label} - 01"
            if c_code not in existing_class_codes and len(existing_class_codes) + len(classes_to_add) < 40:
                classes_to_add.append((m_id, c_code, c_name, y_range))

    # If still need more to hit 40
    extra_idx = 2
    while len(existing_class_codes) + len(classes_to_add) < 40:
        for m in majors_list:
            if len(existing_class_codes) + len(classes_to_add) >= 40:
                break
            c_code = f"{m['code']}_K24_0{extra_idx}"
            c_name = f"Lớp {m['code']} K24 - 0{extra_idx}"
            if c_code not in existing_class_codes:
                classes_to_add.append((m['id'], c_code, c_name, '2024-2028'))
        extra_idx += 1

    for m_id, code, name, year in classes_to_add:
        c.execute("INSERT INTO student_classes (major_id, code, name, year) VALUES (?, ?, ?, ?)", (m_id, code, name, year))
        print(f"  + Thêm Lớp: {name} ({code})")

    class_count = c.execute("SELECT COUNT(*) FROM student_classes").fetchone()[0]
    print(f"Tổng số Lớp học sinh hoạt hiện tại: {class_count}")

    print("\n--- 5. Bổ sung Giảng viên để đạt 20 Giảng viên ---")
    current_teachers = c.execute("SELECT u.email FROM users u JOIN teachers t ON u.id = t.user_id").fetchall()
    existing_t_emails = {r['email'] for r in current_teachers}
    current_t_count = len(existing_t_emails)
    print(f"Giảng viên hiện có: {current_t_count}")

    hashed_pw = generate_password_hash("Teacher@123")
    hashed_legacy_pw = generate_password_hash("teacher123")

    new_teachers_info = [
        ('teacher11@example.com', 'TS. Nguyễn Hải Nam', '0913000011', dept_map.get('SPTH', 4), 'Trưởng bộ môn GDTH'),
        ('teacher12@example.com', 'ThS. Lê Thị Mai Hoa', '0913000012', dept_map.get('SPTH', 4), 'Giảng viên Sư phạm'),
        ('teacher13@example.com', 'PGS.TS. Trần Quốc Hùng', '0913000013', dept_map.get('TOAN', 5), 'Trưởng khoa Toán'),
        ('teacher14@example.com', 'TS. Phạm Văn Dũng', '0913000014', dept_map.get('TOAN', 5), 'Phó khoa Toán'),
        ('teacher15@example.com', 'TS. Nguyễn Thị Hồng', '0913000015', dept_map.get('VL', 6), 'Trưởng khoa Vật lý'),
        ('teacher16@example.com', 'ThS. Đỗ Minh Quân', '0913000016', dept_map.get('VL', 6), 'Giảng viên Vật lý'),
        ('teacher17@example.com', 'TS. Vũ Hoàng Anh', '0913000017', dept_map.get('HOA', 7), 'Trưởng khoa Hóa học'),
        ('teacher18@example.com', 'ThS. Lê Cẩm Tú', '0913000018', dept_map.get('HOA', 7), 'Giảng viên Hóa học'),
        ('teacher19@example.com', 'PGS.TS. Trịnh Bá Toàn', '0913000019', dept_map.get('SH', 8), 'Trưởng khoa Sinh học'),
        ('teacher20@example.com', 'TS. Ngô Thùy Trang', '0913000020', dept_map.get('SH', 8), 'Giảng viên Sinh học'),
    ]

    for email, full_name, phone, dept_id, title in new_teachers_info:
        if email not in existing_t_emails:
            c.execute("""
                INSERT INTO users (email, password_hash, full_name, role, phone, is_active)
                VALUES (?, ?, ?, 'teacher', ?, 1)
            """, (email, hashed_pw, full_name, phone))
            uid = c.lastrowid
            t_code = f"GV2024{uid:03d}"
            c.execute("""
                INSERT INTO teachers (user_id, teacher_code, department_id, title)
                VALUES (?, ?, ?, ?)
            """, (uid, t_code, dept_id, title))
            print(f"  + Thêm Giảng viên: {full_name} ({email}) - {t_code}")

    total_teachers = c.execute("SELECT COUNT(*) FROM teachers").fetchone()[0]
    print(f"Tổng số Giảng viên hiện tại: {total_teachers}")

    print("\n--- 6. Khởi tạo Năm học (2020-2027: 8 năm) và Học kỳ (16 học kỳ) ---")
    academic_years_data = [
        ('2020-2021', 'Năm học 2020 - 2021', 2020, 2021),
        ('2021-2022', 'Năm học 2021 - 2022', 2021, 2022),
        ('2022-2023', 'Năm học 2022 - 2023', 2022, 2023),
        ('2023-2024', 'Năm học 2023 - 2024', 2023, 2024),
        ('2024-2025', 'Năm học 2024 - 2025', 2024, 2025),
        ('2025-2026', 'Năm học 2025 - 2026', 2025, 2026),
        ('2026-2027', 'Năm học 2026 - 2027', 2026, 2027),
        ('2027-2028', 'Năm học 2027 - 2028', 2027, 2028),
    ]

    for code, name, s_yr, e_yr in academic_years_data:
        c.execute("""
            INSERT INTO academic_years (code, name, start_year, end_year)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(code) DO UPDATE SET name=excluded.name
        """, (code, name, s_yr, e_yr))

    ay_rows = c.execute("SELECT id, code, name FROM academic_years").fetchall()
    print(f"Đã cập nhật {len(ay_rows)} Năm học (2020 - 2027).")

    # 16 Semesters
    for ay in ay_rows:
        ay_id = ay['id']
        ay_code = ay['code']
        # Term 1
        s1_code = f"HK1_{ay_code.replace('-', '_')}"
        s1_name = f"Học kỳ 1 ({ay_code})"
        c.execute("""
            INSERT INTO semesters (academic_year_id, code, name, term)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(code) DO UPDATE SET name=excluded.name
        """, (ay_id, s1_code, s1_name))
        # Term 2
        s2_code = f"HK2_{ay_code.replace('-', '_')}"
        s2_name = f"Học kỳ 2 ({ay_code})"
        c.execute("""
            INSERT INTO semesters (academic_year_id, code, name, term)
            VALUES (?, ?, ?, 2)
            ON CONFLICT(code) DO UPDATE SET name=excluded.name
        """, (ay_id, s2_code, s2_name))

    sem_count = c.execute("SELECT COUNT(*) FROM semesters").fetchone()[0]
    print(f"Đã cập nhật {sem_count} Học kỳ (16 học kỳ).")

    print("\n--- 7. Cấu hình Mặc định Hệ thống (Bảo trì & Khóa) ---")
    default_settings = [
        ('maintenance_mode', '0'),
        ('system_lock', '0'),
        ('maintenance_message', 'Hệ thống LMS hiện đang được bảo trì để nâng cấp và đảm bảo chất lượng dịch vụ. Vui lòng quay lại sau.'),
        ('lock_message', 'Hệ thống LMS hiện đang bị khóa. Vui lòng liên hệ quản trị viên để biết thêm thông tin.'),
    ]
    for k, v in default_settings:
        c.execute("""
            INSERT INTO system_settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO NOTHING
        """, (k, v))
    print("Khởi tạo cấu hình hệ thống hoàn tất.")

    print("\n--- 8. Phân bổ Sinh viên đều qua 10 Khoa, 10 Ngành và 40 Lớp ---")
    students = c.execute("SELECT user_id FROM students ORDER BY user_id ASC").fetchall()
    print(f"Tổng sinh viên hiện có: {len(students)}")
    
    all_classes = c.execute("SELECT c.id, c.major_id, m.department_id FROM student_classes c JOIN majors m ON c.major_id = m.id ORDER BY c.id ASC").fetchall()
    
    # Keep primary student (student@example.com - user_id 12) in SE1801, major 1, dept 1
    # Distribute the rest across classes evenly
    for idx, st in enumerate(students):
        uid = st['user_id']
        if uid == 12:
            c.execute("""
                UPDATE students SET department_id = 1, major_id = 1, student_class_id = 1
                WHERE user_id = ?
            """, (uid,))
        else:
            cls = all_classes[idx % len(all_classes)]
            c.execute("""
                UPDATE students SET department_id = ?, major_id = ?, student_class_id = ?
                WHERE user_id = ?
            """, (cls['department_id'], cls['major_id'], cls['id'], uid))

    print("Phân bổ sinh viên hoàn tất.")

    print("\n--- 9. Bổ sung Lớp học phần (Courses) trải rộng qua các Năm học & Học kỳ ---")
    current_courses = c.execute("SELECT code FROM courses").fetchall()
    existing_course_codes = {r['code'] for r in current_courses}

    # Distribute courses across all 20 teachers, 20 subjects, and semesters
    all_subjects = c.execute("SELECT id, code, name, department_id FROM subjects ORDER BY id ASC").fetchall()
    all_teachers = c.execute("SELECT user_id, department_id FROM teachers ORDER BY user_id ASC").fetchall()
    all_semesters = c.execute("SELECT s.name as sem_name, a.code as ay_code FROM semesters s JOIN academic_years a ON s.academic_year_id = a.id ORDER BY s.id ASC").fetchall()

    new_courses_to_add = []
    # Create courses for each semester
    for s_idx, sem in enumerate(all_semesters):
        sem_name = sem['sem_name']
        ay_code = sem['ay_code']
        # 2 courses per semester
        sub1 = all_subjects[(s_idx * 2) % len(all_subjects)]
        sub2 = all_subjects[(s_idx * 2 + 1) % len(all_subjects)]

        t1 = all_teachers[(s_idx * 2) % len(all_teachers)]
        t2 = all_teachers[(s_idx * 2 + 1) % len(all_teachers)]

        c1_code = f"LHP_{sub1['code']}_{ay_code.replace('-', '_')}_{s_idx+1}_01"
        c2_code = f"LHP_{sub2['code']}_{ay_code.replace('-', '_')}_{s_idx+1}_02"

        if c1_code not in existing_course_codes:
            new_courses_to_add.append((sub1['id'], t1['user_id'], c1_code, f"{sub1['name']} - {ay_code}", sem_name, ay_code, 'A201', 'Thứ 2 (07:30 - 11:00)'))
        if c2_code not in existing_course_codes:
            new_courses_to_add.append((sub2['id'], t2['user_id'], c2_code, f"{sub2['name']} - {ay_code}", sem_name, ay_code, 'B302', 'Thứ 4 (13:30 - 17:00)'))

    for s_id, t_id, c_code, c_name, sem_n, ay_c, room, sched in new_courses_to_add:
        c.execute("""
            INSERT INTO courses (subject_id, teacher_id, code, name, semester, academic_year, room, schedule_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (s_id, t_id, c_code, c_name, sem_n, ay_c, room, sched))
        new_cid = c.lastrowid

        # Enroll 5-10 students into this course
        enrolled_students = students[(new_cid * 3) % len(students): (new_cid * 3 + 8) % len(students) + 1]
        for st in enrolled_students:
            uid = st['user_id']
            try:
                c.execute("""
                    INSERT INTO enrollments (course_id, student_id, status)
                    VALUES (?, ?, 'active')
                """, (new_cid, uid))
                
                # Add sample grade for rich reporting
                score = round(6.0 + (new_cid % 4) * 0.9 + (uid % 3) * 0.4, 1)
                letter = "A+" if score >= 9.0 else ("A" if score >= 8.5 else ("B+" if score >= 8.0 else ("B" if score >= 7.0 else ("C+" if score >= 6.5 else ("C" if score >= 5.5 else ("D" if score >= 4.0 else "F"))))))
                c.execute("""
                    INSERT INTO grades (course_id, student_id, assignment_score, quiz_score, midterm_score, final_score, total_score, letter_grade)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (new_cid, uid, score, score, score, score, score, letter))
            except sqlite3.IntegrityError:
                pass

    total_courses = c.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    print(f"Tổng số Lớp học phần hiện tại: {total_courses}")

    conn.commit()
    conn.close()
    print("\n>>> HOÀN THÀNH BỔ SUNG DỮ LIỆU TOÀN DIỆN! <<<")

if __name__ == '__main__':
    enrich_database()

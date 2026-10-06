import sqlite3
import os
import sys

# Configure UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'lms.db')
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("Balancing LMS distribution across 10 departments...")

# 1. Departments (10)
depts_data = [
    (1, 'CNTT', 'Khoa Công nghệ thông tin', 'Đào tạo kỹ sư phần mềm, khoa học máy tính và AI.'),
    (2, 'KT', 'Khoa Kinh tế & Tài chính', 'Đào tạo chuyên gia kinh tế, ngân hàng và tài chính doanh nghiệp.'),
    (3, 'NN', 'Khoa Ngoại ngữ', 'Đào tạo cử nhân Ngôn ngữ Anh và giao tiếp quốc tế.'),
    (4, 'SPTH', 'Khoa Sư phạm & Giáo dục', 'Đào tạo giáo viên tiểu học và cán bộ nghiên cứu giáo dục.'),
    (5, 'TOAN', 'Khoa Toán học & Thống kê', 'Đào tạo chuyên gia Toán ứng dụng và Khoa học dữ liệu.'),
    (6, 'VL', 'Khoa Vật lý & Bán dẫn', 'Đào tạo kỹ sư Vật lý kỹ thuật và Công nghệ vi mạch bán dẫn.'),
    (7, 'HOA', 'Khoa Hóa học & Môi trường', 'Đào tạo kỹ sư Hóa dược, Hóa phân tích và Quản lý môi trường.'),
    (8, 'SH', 'Khoa Sinh học & CNSH', 'Đào tạo chuyên gia Công nghệ sinh học và Sinh học phân tử.'),
    (9, 'QTKD', 'Khoa Quản trị kinh doanh', 'Đào tạo nhà quản trị, Marketing kỹ thuật số và Khởi nghiệp.'),
    (10, 'KHXH', 'Khoa Khoa học Xã hội & Nhân văn', 'Đào tạo cử nhân Xã hội học, Tâm lý và Truyền thông.')
]
for d in depts_data:
    cursor.execute("""
        UPDATE departments SET code = ?, name = ?, description = ? WHERE id = ?
    """, (d[1], d[2], d[3], d[0]))

# 2. Majors (10 - exactly 1 per department)
majors_data = [
    (1, 1, 'KTPM', 'Kỹ thuật phần mềm'),
    (2, 2, 'TCNH', 'Tài chính – Ngân hàng'),
    (3, 3, 'NNA', 'Ngôn ngữ Anh'),
    (4, 4, 'GDTH', 'Giáo dục Tiểu học'),
    (5, 5, 'TOANUD', 'Toán ứng dụng & Khoa học dữ liệu'),
    (6, 6, 'VLUD', 'Vật lý kỹ thuật & Bán dẫn'),
    (7, 7, 'HOADH', 'Hóa dược & Công nghệ vật liệu'),
    (8, 8, 'CNSH', 'Công nghệ sinh học'),
    (9, 9, 'QTKD', 'Quản trị kinh doanh'),
    (10, 10, 'KHXH', 'Xã hội học & Tâm lý ứng dụng')
]
cursor.execute("UPDATE majors SET code = 'TMP_' || id")
for m in majors_data:
    cursor.execute("""
        UPDATE majors SET department_id = ?, code = ?, name = ? WHERE id = ?
    """, (m[1], m[2], m[3], m[0]))

# 3. Teachers (20 - exactly 2 per department)
teacher_users = cursor.execute("SELECT u.id, u.email FROM users u WHERE u.role = 'teacher' ORDER BY u.id").fetchall()
print(f"Total teachers: {len(teacher_users)}")
for idx, tu in enumerate(teacher_users):
    dept_id = (idx // 2) + 1
    if dept_id > 10:
        dept_id = 10
    cursor.execute("UPDATE teachers SET department_id = ? WHERE user_id = ?", (dept_id, tu['id']))

# 4. Subjects (20 - exactly 2 per department)
subjects_data = [
    # Dept 1 - CNTT
    (1, 1, 'WEB201', 'Lập trình Web nâng cao', 3, 'HTML, CSS, JS, Flask, REST API'),
    (2, 1, 'CSDL101', 'Cơ sở dữ liệu quan hệ', 4, 'SQL, ERD, Chuẩn hóa dữ liệu'),
    # Dept 2 - KT
    (3, 2, 'TCNH201', 'Tài chính doanh nghiệp', 3, 'Quản lý tài chính, phân tích dòng tiền'),
    (4, 2, 'KTVI101', 'Kinh tế vi mô & vĩ mô', 3, 'Nguyên lý kinh tế học, cung cầu và thị trường'),
    # Dept 3 - NN
    (5, 3, 'ENG101', 'Tiếng Anh chuyên ngành', 3, 'Từ vựng học thuật, viết bài báo cáo'),
    (6, 3, 'ENG102', 'Tiếng Anh giao tiếp & Biên dịch', 3, 'Kỹ năng thuyết trình và phiên dịch'),
    # Dept 4 - SPTH
    (7, 4, 'GDH101', 'Tâm lý học & Giáo dục học', 3, 'Phương pháp sư phạm, tâm lý lứa tuổi'),
    (8, 4, 'PPGD102', 'Phương pháp giảng dạy tiểu học', 3, 'Thiết kế bài giảng và phương pháp sư phạm'),
    # Dept 5 - TOAN
    (9, 5, 'MATH101', 'Giải tích & Đại số tuyến tính', 4, 'Ma trận, không gian vector, tích phân'),
    (10, 5, 'XSTK102', 'Xác suất thống kê & Khoa học DL', 3, 'Phân phối xác suất, kiểm định giả thuyết'),
    # Dept 6 - VL
    (11, 6, 'PHY101', 'Vật lý đại cương & Bán dẫn', 4, 'Quang học, điện từ học, vật liệu bán dẫn'),
    (12, 6, 'VLBD102', 'Vật lý bán dẫn & Vi điện tử', 3, 'Cấu trúc tinh thể bán dẫn, linh kiện vi mạch'),
    # Dept 7 - HOA
    (13, 7, 'CHEM101', 'Hóa học đại cương & Vật liệu mới', 3, 'Cấu tạo phân tử, liên kết hóa học'),
    (14, 7, 'HOAMT102', 'Hóa môi trường & Xử lý chất thải', 3, 'Công nghệ xử lý nước và khí thải'),
    # Dept 8 - SH
    (15, 8, 'BIO101', 'Sinh học phân tử & Vi sinh', 4, 'DNA/RNA, công nghệ gen và vi sinh vật'),
    (16, 8, 'CNSH102', 'Công nghệ gen & Ứng dụng', 3, 'Ứng dụng sinh học trong y học và nông nghiệp'),
    # Dept 9 - QTKD
    (17, 9, 'QTKD101', 'Quản trị học đại cương', 3, 'Kỹ năng quản trị, lập kế hoạch kinh doanh'),
    (18, 9, 'MKT201', 'Marketing căn bản & Kỹ thuật số', 3, 'Nghiên cứu thị trường và Digital Marketing'),
    # Dept 10 - KHXH
    (19, 10, 'SOC101', 'Xã hội học đại cương & Kỹ năng mềm', 3, 'Cơ cấu xã hội, kỹ năng giao tiếp'),
    (20, 10, 'TLH102', 'Tâm lý học xã hội & Hành vi', 3, 'Tâm lý đám đông, hành vi xã hội')
]
cursor.execute("UPDATE subjects SET code = 'TMP_' || id")
for s in subjects_data:
    cursor.execute("""
        UPDATE subjects SET department_id = ?, code = ?, name = ?, credits = ?, description = ? WHERE id = ?
    """, (s[1], s[2], s[3], s[4], s[5], s[0]))

# 5. Student classes (40 - exactly 4 per major)
all_classes = cursor.execute("SELECT id FROM student_classes ORDER BY id").fetchall()
print(f"Total student classes: {len(all_classes)}")
cursor.execute("UPDATE student_classes SET code = 'TMP_' || id")
major_codes = ['KTPM', 'TCNH', 'NNA', 'GDTH', 'TOANUD', 'VLUD', 'HOADH', 'CNSH', 'QTKD', 'KHXH']
years_cycle = ['2020-2024', '2021-2025', '2022-2026', '2023-2027']

for idx, c in enumerate(all_classes):
    m_idx = idx // 4
    if m_idx >= 10:
        m_idx = 9
    major_id = m_idx + 1
    m_code = major_codes[m_idx]
    y_idx = idx % 4
    y_str = years_cycle[y_idx]
    c_code = f"LH-{m_code}-{idx+1:02d}"
    c_name = f"Lớp {m_code} ({y_str}) - 01"
    cursor.execute("""
        UPDATE student_classes SET major_id = ?, code = ?, name = ?, year = ? WHERE id = ?
    """, (major_id, c_code, c_name, y_str, c['id']))

# 6. Students (53 students - distributed across all 10 majors and 10 departments)
student_rows = cursor.execute("SELECT s.user_id, u.email FROM students s JOIN users u ON s.user_id = u.id ORDER BY s.user_id").fetchall()
print(f"Total students: {len(student_rows)}")

# Preserve student@example.com in major 1 (KTPM), dept 1, class 1
for idx, st in enumerate(student_rows):
    if st['email'] == 'student@example.com':
        major_id = 1
        dept_id = 1
        # find class 1
        class_id = all_classes[0]['id']
    else:
        # distribute evenly across majors 1..10
        m_idx = (idx % 10)
        major_id = m_idx + 1
        dept_id = major_id # 1-to-1 mapping
        # pick a class for this major
        class_offset = m_idx * 4 + (idx % 4)
        if class_offset >= len(all_classes):
            class_offset = len(all_classes) - 1
        class_id = all_classes[class_offset]['id']

    cursor.execute("""
        UPDATE students SET department_id = ?, major_id = ?, student_class_id = ? WHERE user_id = ?
    """, (dept_id, major_id, class_id, st['user_id']))

# 7. Courses (Lớp học phần) - update teacher_id and subject_id to align with departments
courses = cursor.execute("SELECT id, subject_id, teacher_id FROM courses ORDER BY id").fetchall()
for idx, cr in enumerate(courses):
    # subject from 1 to 20
    sub_id = (idx % 20) + 1
    # find department of this subject
    sub = cursor.execute("SELECT department_id FROM subjects WHERE id = ?", (sub_id,)).fetchone()
    dept_id = sub['department_id'] if sub else 1
    # find teacher in this department
    t_row = cursor.execute("SELECT user_id FROM teachers WHERE department_id = ? LIMIT 1", (dept_id,)).fetchone()
    t_id = t_row['user_id'] if t_row else teacher_users[0]['id']
    cursor.execute("UPDATE courses SET subject_id = ?, teacher_id = ? WHERE id = ?", (sub_id, t_id, cr['id']))

conn.commit()
conn.close()
print("Successfully balanced data across all 10 departments, 10 majors, 20 subjects, 40 classes, 20 teachers, and 53 students!")

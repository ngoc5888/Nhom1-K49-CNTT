-- ====================================================================
-- PHÂN HỆ TRUY VẤN NÂNG CAO & THỐNG KÊ BÁO CÁO (LMS ANALYTICS)
-- ====================================================================

-- 1. VIEW: Bảng điểm tổng hợp chi tiết của sinh viên kèm thông tin môn học & lớp
CREATE VIEW IF NOT EXISTS view_student_academic_transcript AS
SELECT 
    u.id AS student_id,
    s.student_code,
    u.full_name AS student_name,
    c.code AS course_code,
    c.name AS course_name,
    sub.credits,
    g.assignment_score,
    g.quiz_score,
    g.midterm_score,
    g.final_score,
    g.total_score,
    g.letter_grade
FROM grades g
JOIN users u ON g.student_id = u.id
JOIN students s ON s.user_id = u.id
JOIN courses c ON g.course_id = c.id
JOIN subjects sub ON c.subject_id = sub.id;

-- 2. TRUY VẤN: Tính điểm GPA tích lũy hệ 4 và phân loại học lực toàn khóa
SELECT 
    student_code,
    student_name,
    COUNT(course_code) AS total_courses,
    SUM(credits) AS total_credits,
    ROUND(SUM(
        CASE letter_grade
            WHEN 'A+' THEN 4.0
            WHEN 'A'  THEN 3.7
            WHEN 'B+' THEN 3.5
            WHEN 'B'  THEN 3.0
            WHEN 'C+' THEN 2.5
            WHEN 'C'  THEN 2.0
            WHEN 'D+' THEN 1.5
            WHEN 'D'  THEN 1.0
            ELSE 0.0
        END * credits
    ) / SUM(credits), 2) AS gpa_4_0,
    CASE 
        WHEN (SUM(CASE letter_grade WHEN 'A+' THEN 4.0 WHEN 'A' THEN 3.7 WHEN 'B+' THEN 3.5 WHEN 'B' THEN 3.0 WHEN 'C+' THEN 2.5 WHEN 'C' THEN 2.0 WHEN 'D+' THEN 1.5 WHEN 'D' THEN 1.0 ELSE 0.0 END * credits) / SUM(credits)) >= 3.6 THEN 'Xuất sắc'
        WHEN (SUM(CASE letter_grade WHEN 'A+' THEN 4.0 WHEN 'A' THEN 3.7 WHEN 'B+' THEN 3.5 WHEN 'B' THEN 3.0 WHEN 'C+' THEN 2.5 WHEN 'C' THEN 2.0 WHEN 'D+' THEN 1.5 WHEN 'D' THEN 1.0 ELSE 0.0 END * credits) / SUM(credits)) >= 3.2 THEN 'Giỏi'
        WHEN (SUM(CASE letter_grade WHEN 'A+' THEN 4.0 WHEN 'A' THEN 3.7 WHEN 'B+' THEN 3.5 WHEN 'B' THEN 3.0 WHEN 'C+' THEN 2.5 WHEN 'C' THEN 2.0 WHEN 'D+' THEN 1.5 WHEN 'D' THEN 1.0 ELSE 0.0 END * credits) / SUM(credits)) >= 2.5 THEN 'Khá'
        ELSE 'Trung bình'
    END AS academic_rank
FROM view_student_academic_transcript
GROUP BY student_id;

-- 3. TRUY VẤN: Thống kê tỷ lệ nộp bài tập theo từng lớp học phần
SELECT 
    c.code AS class_code,
    c.name AS course_name,
    a.title AS assignment_title,
    COUNT(DISTINCT e.student_id) AS total_students,
    COUNT(DISTINCT sub.student_id) AS submitted_count,
    ROUND((COUNT(DISTINCT sub.student_id) * 100.0 / COUNT(DISTINCT e.student_id)), 1) AS submission_rate_percent
FROM assignments a
JOIN courses c ON a.course_id = c.id
JOIN enrollments e ON e.course_id = c.id
LEFT JOIN submissions sub ON sub.assignment_id = a.id AND sub.student_id = e.student_id
GROUP BY a.id;

-- 4. TRUY VẤN: Top sinh viên đạt điểm thi trắc nghiệm cao nhất môn Lập trình Web
SELECT 
    s.student_code,
    u.full_name AS student_name,
    e.title AS exam_title,
    er.score,
    er.correct_count,
    er.total_questions,
    er.submitted_at
FROM exam_results er
JOIN exams e ON er.exam_id = e.id
JOIN users u ON er.student_id = u.id
JOIN students s ON s.user_id = u.id
WHERE e.title LIKE '%Lập trình Web%'
ORDER BY er.score DESC, er.submitted_at ASC
LIMIT 10;
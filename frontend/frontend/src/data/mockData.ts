// ===== Mock Data for LMS Dashboard =====

// Students
export const mockStudents = [
  { id: 'SV001', name: 'Nguyễn Văn An', email: 'an.nv@sv.edu.vn', class: 'CNTT-K22A', gpa: 3.65, status: 'active' },
  { id: 'SV002', name: 'Trần Thị Bình', email: 'binh.tt@sv.edu.vn', class: 'CNTT-K22A', gpa: 3.20, status: 'active' },
  { id: 'SV003', name: 'Lê Hoàng Cường', email: 'cuong.lh@sv.edu.vn', class: 'CNTT-K22B', gpa: 2.90, status: 'active' },
  { id: 'SV004', name: 'Phạm Thị Diệu', email: 'dieu.pt@sv.edu.vn', class: 'CNTT-K22B', gpa: 3.80, status: 'active' },
  { id: 'SV005', name: 'Hoàng Văn Em', email: 'em.hv@sv.edu.vn', class: 'KTMT-K22A', gpa: 2.50, status: 'inactive' },
  { id: 'SV006', name: 'Ngô Thị Phương', email: 'phuong.nt@sv.edu.vn', class: 'KTMT-K22A', gpa: 3.45, status: 'active' },
  { id: 'SV007', name: 'Vũ Đức Giang', email: 'giang.vd@sv.edu.vn', class: 'HTTT-K22A', gpa: 3.10, status: 'active' },
  { id: 'SV008', name: 'Đặng Thị Hà', email: 'ha.dt@sv.edu.vn', class: 'HTTT-K22A', gpa: 3.55, status: 'active' },
  { id: 'SV009', name: 'Bùi Trọng Inh', email: 'inh.bt@sv.edu.vn', class: 'CNTT-K22A', gpa: 2.75, status: 'active' },
  { id: 'SV010', name: 'Trịnh Thị Kim', email: 'kim.tt@sv.edu.vn', class: 'CNTT-K22B', gpa: 3.90, status: 'active' },
]

// Teachers
export const mockTeachers = [
  { id: 'GV001', name: 'PGS.TS. Nguyễn Văn Hùng', email: 'hung.nv@gv.edu.vn', department: 'Khoa CNTT', subject: 'Lập trình Web', classes: 3, students: 120 },
  { id: 'GV002', name: 'TS. Trần Thị Lan', email: 'lan.tt@gv.edu.vn', department: 'Khoa CNTT', subject: 'Cơ sở Dữ liệu', classes: 2, students: 85 },
  { id: 'GV003', name: 'ThS. Lê Văn Minh', email: 'minh.lv@gv.edu.vn', department: 'Khoa KTMT', subject: 'Kiến trúc Máy tính', classes: 4, students: 160 },
  { id: 'GV004', name: 'TS. Phạm Thị Nga', email: 'nga.pt@gv.edu.vn', department: 'Khoa HTTT', subject: 'Hệ thống Thông tin', classes: 3, students: 95 },
  { id: 'GV005', name: 'ThS. Hoàng Văn Oanh', email: 'oanh.hv@gv.edu.vn', department: 'Khoa CNTT', subject: 'Thuật toán', classes: 2, students: 75 },
]

// Classes
export const mockClasses = [
  { id: 'LH001', name: 'Lập trình Web Nâng cao', code: 'IT4023', teacher: 'Nguyễn Văn Hùng', students: 42, schedule: 'T2, T4 - 7:30', room: 'A204', credits: 3, status: 'active' },
  { id: 'LH002', name: 'Cơ sở Dữ liệu', code: 'IT3012', teacher: 'Trần Thị Lan', students: 38, schedule: 'T3, T5 - 9:15', room: 'B301', credits: 3, status: 'active' },
  { id: 'LH003', name: 'Kiến trúc Máy tính', code: 'CE2011', teacher: 'Lê Văn Minh', students: 45, schedule: 'T2, T5 - 13:00', room: 'C102', credits: 4, status: 'active' },
  { id: 'LH004', name: 'Nhập môn Trí tuệ Nhân tạo', code: 'AI3001', teacher: 'Phạm Thị Nga', students: 50, schedule: 'T4, T6 - 7:30', room: 'D401', credits: 3, status: 'active' },
  { id: 'LH005', name: 'Mạng Máy tính', code: 'NET2001', teacher: 'Hoàng Văn Oanh', students: 35, schedule: 'T3, T6 - 13:00', room: 'A305', credits: 3, status: 'inactive' },
]

// Assignments
export const mockAssignments = [
  { id: 'BT001', title: 'Bài tập lớn - Xây dựng Website E-commerce', course: 'Lập trình Web Nâng cao', dueDate: '2026-10-05', status: 'pending', score: null, maxScore: 100 },
  { id: 'BT002', title: 'Thiết kế CSDL cho hệ thống thư viện', course: 'Cơ sở Dữ liệu', dueDate: '2026-09-28', status: 'submitted', score: 85, maxScore: 100 },
  { id: 'BT003', title: 'Bài tập tuần 5 - Bộ nhớ ảo', course: 'Kiến trúc Máy tính', dueDate: '2026-09-20', status: 'overdue', score: null, maxScore: 10 },
  { id: 'BT004', title: 'Cài đặt thuật toán A*', course: 'Nhập môn Trí tuệ Nhân tạo', dueDate: '2026-10-10', status: 'pending', score: null, maxScore: 100 },
  { id: 'BT005', title: 'Báo cáo phân tích mạng LAN', course: 'Mạng Máy tính', dueDate: '2026-09-30', status: 'submitted', score: 92, maxScore: 100 },
]

// Exams
export const mockExams = [
  { id: 'KT001', title: 'Kiểm tra giữa kỳ - Lập trình Web', course: 'Lập trình Web Nâng cao', date: '2026-10-15', duration: 90, type: 'midterm', status: 'upcoming' },
  { id: 'KT002', title: 'Quiz chương 3 - CSDL Quan hệ', course: 'Cơ sở Dữ liệu', date: '2026-09-29', duration: 30, type: 'quiz', status: 'upcoming' },
  { id: 'KT003', title: 'Kiểm tra cuối kỳ - Kiến trúc MT', course: 'Kiến trúc Máy tính', date: '2026-12-10', duration: 120, type: 'final', status: 'upcoming' },
  { id: 'KT004', title: 'Quiz AI cơ bản', course: 'Nhập môn Trí tuệ Nhân tạo', date: '2026-09-25', duration: 45, type: 'quiz', status: 'completed', score: 88 },
]

// Grades / Results
export const mockGrades = [
  { course: 'Lập trình Web Nâng cao', code: 'IT4023', credits: 3, midterm: 8.5, final: null, average: null, grade: null },
  { course: 'Cơ sở Dữ liệu', code: 'IT3012', credits: 3, midterm: 7.0, final: 8.0, average: 7.6, grade: 'B+' },
  { course: 'Kiến trúc Máy tính', code: 'CE2011', credits: 4, midterm: 6.5, final: 7.5, average: 7.1, grade: 'B' },
  { course: 'Nhập môn Trí tuệ Nhân tạo', code: 'AI3001', credits: 3, midterm: 9.0, final: 9.2, average: 9.1, grade: 'A' },
  { course: 'Mạng Máy tính', code: 'NET2001', credits: 3, midterm: 8.0, final: 8.5, average: 8.3, grade: 'A-' },
]

// Notifications
export const mockNotifications = [
  { id: 'TB001', title: 'Nhắc nhở nộp bài tập', message: 'Bài tập "Xây dựng Website E-commerce" còn 9 ngày nữa hết hạn.', time: '2 giờ trước', read: false, type: 'warning' },
  { id: 'TB002', title: 'Điểm kiểm tra đã được cập nhật', message: 'Bài Quiz AI cơ bản đã có điểm: 8.8/10', time: '5 giờ trước', read: false, type: 'success' },
  { id: 'TB003', title: 'Thông báo từ nhà trường', message: 'Lịch thi học kỳ I năm 2026-2027 đã được công bố trên cổng thông tin.', time: '1 ngày trước', read: true, type: 'info' },
  { id: 'TB004', title: 'Tài liệu mới được đăng tải', message: 'Giảng viên Nguyễn Văn Hùng vừa tải lên slide bài giảng tuần 7.', time: '2 ngày trước', read: true, type: 'info' },
  { id: 'TB005', title: 'Bài tập quá hạn', message: 'Bài tập "Bộ nhớ ảo" đã quá hạn nộp. Liên hệ giảng viên để biết thêm.', time: '6 ngày trước', read: true, type: 'error' },
]

// Materials
export const mockMaterials = [
  { id: 'TL001', title: 'Slide bài giảng tuần 7 - React Hooks', course: 'Lập trình Web Nâng cao', type: 'pdf', size: '4.2 MB', uploadedAt: '2026-09-24', teacher: 'Nguyễn Văn Hùng' },
  { id: 'TL002', title: 'Lab 3 - SQL Nâng cao', course: 'Cơ sở Dữ liệu', type: 'docx', size: '1.8 MB', uploadedAt: '2026-09-22', teacher: 'Trần Thị Lan' },
  { id: 'TL003', title: 'Chương 5 - Kiến trúc bộ nhớ', course: 'Kiến trúc Máy tính', type: 'pdf', size: '6.7 MB', uploadedAt: '2026-09-20', teacher: 'Lê Văn Minh' },
  { id: 'TL004', title: 'Tài liệu thuật toán tìm kiếm', course: 'Nhập môn Trí tuệ Nhân tạo', type: 'pdf', size: '3.1 MB', uploadedAt: '2026-09-18', teacher: 'Phạm Thị Nga' },
  { id: 'TL005', title: 'Video hướng dẫn cấu hình Router', course: 'Mạng Máy tính', type: 'mp4', size: '245 MB', uploadedAt: '2026-09-15', teacher: 'Hoàng Văn Oanh' },
]

// Dashboard stats
export const adminDashboardStats = {
  totalStudents: 1247,
  totalTeachers: 68,
  totalCourses: 142,
  totalClasses: 215,
  activeClasses: 189,
  newStudentsThisMonth: 42,
}

export const teacherDashboardStats = {
  totalClasses: 3,
  totalStudents: 125,
  pendingGrading: 18,
  upcomingExams: 2,
}

export const studentDashboardStats = {
  enrolledClasses: 5,
  pendingAssignments: 2,
  completionRate: 72,
  gpa: 8.02,
}

// Chart data
export const gpaChartData = [
  { semester: 'HK1 2024', gpa: 7.2 },
  { semester: 'HK2 2024', gpa: 7.8 },
  { semester: 'HK1 2025', gpa: 8.1 },
  { semester: 'HK2 2025', gpa: 7.9 },
  { semester: 'HK1 2026', gpa: 8.4 },
]

export const adminUserGrowthData = [
  { month: 'T1', students: 980, teachers: 60 },
  { month: 'T2', students: 1010, teachers: 62 },
  { month: 'T3', students: 1050, teachers: 63 },
  { month: 'T4', students: 1090, teachers: 64 },
  { month: 'T5', students: 1110, teachers: 65 },
  { month: 'T6', students: 1130, teachers: 66 },
  { month: 'T7', students: 1150, teachers: 66 },
  { month: 'T8', students: 1180, teachers: 67 },
  { month: 'T9', students: 1247, teachers: 68 },
]

export const classDistributionData = [
  { name: 'Khoa CNTT', value: 85 },
  { name: 'Khoa KTMT', value: 52 },
  { name: 'Khoa HTTT', value: 48 },
  { name: 'Khoa MMT', value: 30 },
]

export const teacherAssignmentData = [
  { week: 'Tuần 1', submitted: 15, graded: 12 },
  { week: 'Tuần 2', submitted: 22, graded: 18 },
  { week: 'Tuần 3', submitted: 19, graded: 19 },
  { week: 'Tuần 4', submitted: 28, graded: 21 },
  { week: 'Tuần 5', submitted: 24, graded: 20 },
  { week: 'Tuần 6', submitted: 30, graded: 18 },
]

export const scheduleData = [
  { day: 'Thứ 2', subject: 'Lập trình Web Nâng cao', room: 'A204', time: '7:30 - 9:10', class: 'CNTT-K22A' },
  { day: 'Thứ 3', subject: 'Cơ sở Dữ liệu', room: 'B301', time: '9:15 - 11:00', class: 'CNTT-K22B' },
  { day: 'Thứ 4', subject: 'Lập trình Web Nâng cao', room: 'A204', time: '7:30 - 9:10', class: 'CNTT-K22B' },
  { day: 'Thứ 5', subject: 'Cơ sở Dữ liệu', room: 'B301', time: '9:15 - 11:00', class: 'KTMT-K22A' },
  { day: 'Thứ 6', subject: 'Kiểm tra Định kỳ', room: 'D401', time: '13:00 - 14:40', class: 'HTTT-K22A' },
]

export const faculties = [
  { id: 'F001', name: 'Khoa Công nghệ Thông tin', code: 'CNTT', dean: 'PGS.TS. Nguyễn Minh Tuấn', teachers: 25, students: 480 },
  { id: 'F002', name: 'Khoa Kỹ thuật Máy tính', code: 'KTMT', dean: 'TS. Trần Văn Hải', teachers: 18, students: 320 },
  { id: 'F003', name: 'Khoa Hệ thống Thông tin', code: 'HTTT', dean: 'TS. Lê Thị Hoa', teachers: 15, students: 280 },
  { id: 'F004', name: 'Khoa Mạng Máy tính', code: 'MMT', dean: 'ThS. Phạm Văn Lam', teachers: 10, students: 167 },
]

export const courses = [
  { id: 'M001', name: 'Lập trình Web Nâng cao', code: 'IT4023', faculty: 'CNTT', credits: 3, prerequisite: 'IT2001', status: 'active' },
  { id: 'M002', name: 'Cơ sở Dữ liệu', code: 'IT3012', faculty: 'CNTT', credits: 3, prerequisite: null, status: 'active' },
  { id: 'M003', name: 'Kiến trúc Máy tính', code: 'CE2011', faculty: 'KTMT', credits: 4, prerequisite: 'CE1001', status: 'active' },
  { id: 'M004', name: 'Nhập môn Trí tuệ Nhân tạo', code: 'AI3001', faculty: 'CNTT', credits: 3, prerequisite: 'IT2010', status: 'active' },
  { id: 'M005', name: 'Mạng Máy tính', code: 'NET2001', faculty: 'MMT', credits: 3, prerequisite: null, status: 'inactive' },
]

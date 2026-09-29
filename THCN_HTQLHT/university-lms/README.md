# 🎓 University Learning Management System (LMS)
> **Hệ thống Quản lý Học tập Trực tuyến Đầy đủ dành cho Trường Đại học**

Hệ thống LMS được xây dựng hoàn chỉnh với giao diện hiện đại (Sidebar màu xanh Navy đậm `#0F172A`, Menu đang chọn có nền tím và dải màu hồng `#EC4899`, bo góc hiện đại, responsive trên máy tính, tablet và điện thoại). Phân quyền 3 vai trò: **Sinh viên**, **Giảng viên**, và **Quản trị viên (Admin)** với cơ sở dữ liệu SQLite thực tế và dữ liệu mẫu phong phú.

---

## 🔑 Tài khoản Demo Kiểm thử

Hệ thống đã được khởi tạo sẵn dữ liệu mẫu thực tế. Bạn có thể sử dụng các tài khoản sau để đăng nhập:

| Vai trò | Email | Mật khẩu | Chức năng chính |
| :--- | :--- | :--- | :--- |
| **🎓 Sinh viên** | `student@example.com` | `student123` | Xem lớp học, tải tài liệu, nộp bài tập, làm bài thi trắc nghiệm trực tuyến có đếm giờ, xem bảng điểm & tiến độ. |
| **👨‍🏫 Giảng viên** | `teacher@example.com` | `teacher123` | Quản lý lớp học phần, tải lên giáo trình/bài giảng, tạo bài tập & chấm điểm, tạo đề thi trắc nghiệm, quản lý sổ điểm. |
| **🛡️ Admin** | `admin@example.com` | `admin123` | Bảng điều khiển quản trị toàn trường, quản lý tài khoản người dùng, quản lý danh mục đào tạo (Khoa, Ngành, Lớp, Môn học), báo cáo & xuất Excel/PDF. |

---

## 🚀 Hướng dẫn Cài đặt & Chạy ứng dụng

### Yêu cầu hệ thống:
- **Python 3.10+** (Khuyến nghị Python 3.11 - 3.13)
- Hỗ trợ tất cả các hệ điều hành: Windows, macOS, Linux.

### Các bước khởi chạy:

1. **Điều hướng vào thư mục dự án**:
   ```bash
   cd C:\Users\ADMIN\.gemini\antigravity\scratch\university-lms
   ```

2. **Chạy ứng dụng (Tự động khởi tạo CSDL & Dữ liệu mẫu nếu chưa có)**:
   ```bash
   python run.py
   ```

3. **Mở trình duyệt Web**:
   Truy cập vào địa chỉ: [http://127.0.0.1:5000](http://127.0.0.1:5000)

*(Nếu muốn nạp lại dữ liệu demo mẫu bất cứ lúc nào, chỉ cần chạy: `python app/seed.py`)*

---

## 📁 Cấu trúc Thư mục Dự án

```text
university-lms/
├── app/
│   ├── routes/
│   │   ├── admin_routes.py      # Tuyến đường dành cho Quản trị viên (Admin)
│   │   ├── auth_routes.py       # Tuyến đường Xử lý Đăng nhập, Đăng ký, Đăng xuất, Quên mật khẩu
│   │   ├── common_routes.py     # Tuyến đường Thông báo & Hồ sơ cá nhân
│   │   ├── student_routes.py    # Tuyến đường dành cho Sinh viên (Lớp, Tài liệu, Bài tập, Thi online, Điểm)
│   │   └── teacher_routes.py    # Tuyến đường dành cho Giảng viên (Quản lý Lớp, Đồ án, Đề thi, Sổ điểm)
│   ├── static/
│   │   ├── uploads/             # Thư mục lưu trữ tệp bài làm và tài liệu đính kèm
│   │   └── images/              # Hình ảnh mặc định
│   ├── templates/
│   │   ├── admin/               # Templates Giao diện Admin
│   │   ├── auth/                # Templates Đăng nhập, Đăng ký
│   │   ├── common/              # Templates Thông báo & Profile
│   │   ├── student/             # Templates Giao diện Sinh viên
│   │   ├── teacher/             # Templates Giao diện Giảng viên
│   │   └── base.html            # Layout chung có Sidebar Navy, Menu tím viền hồng & Header
│   ├── auth.py                  # Module Phân quyền & Quản lý Session (RBAC)
│   ├── database.py              # Xử lý kết nối SQLite3 & Định nghĩa Tables
│   └── seed.py                  # Script sinh dữ liệu demo thực tế (3 Khoa, 5 Ngành, 50 SV, 10 GV...)
├── lms.db                       # Cơ sở dữ liệu SQLite3 (Tự động khởi tạo)
├── run.py                       # File khởi chạy server Flask chính
└── README.md                    # Hướng dẫn sử dụng & Kiến trúc hệ thống
```

---

## 🌟 Danh sách Các Tính năng Chính

### 1. Giao diện Tổng thể (UI/UX):
- Sidebar cố định màu xanh Navy đậm (`#0F172A`).
- Hiệu ứng Menu active màu tím với thanh viền hồng nổi bật (`#EC4899`).
- Responsive 100% (Mobile Drawer sidebar, co giãn linh hoạt trên Tablet & Desktop).
- Top Header chứa thanh tìm kiếm nhanh, nút thông báo có Badge số dư, và User Profile Avatar dropdown.

### 2. Mô-đun Sinh viên (Student):
- **Dashboard Sinh viên**: Card thống kê số lớp, tài liệu, bài tập, bài thi, tiến độ % và GPA trung bình.
- **Lớp học**: Danh sách lớp học phần đang tham gia, xem chi tiết môn học, giáo trình, bài giảng, danh sách bạn học.
- **Tài liệu**: Tìm kiếm & lọc tài liệu theo môn học và định dạng file (PDF, Word, PPTX, Video, Code Zip).
- **Bài tập**: Nộp bài làm qua file đính kèm + ghi chú, theo dõi trạng thái bài nộp, xem điểm và nhận xét của giảng viên.
- **Kiểm tra Trực tuyến**: Hệ thống thi trắc nghiệm online với đồng hồ đếm ngược JS, tự động nộp bài khi hết giờ, bảng câu hỏi tương tác và xem kết quả tự động chấm ngay lập tức.
- **Kết quả học tập**: Bảng điểm tổng hợp các môn, xếp loại học lực, và biểu đồ trực quan hóa điểm số Chart.js.

### 3. Mô-đun Giảng viên (Teacher):
- **Teacher Dashboard**: Bảng tổng quan bài tập chưa chấm, danh sách lớp giảng dạy và các hoạt động gần đây.
- **Quản lý Lớp học**: Tạo lớp học phần mới, quản lý thông tin phòng học và lịch học.
- **Quản lý Tài liệu**: Upload giáo trình/bài giảng theo môn học.
- **Quản lý Bài tập**: Đăng bài tập mới, đặt hạn nộp, duyệt và chấm bài làm của sinh viên kèm lời nhận xét.
- **Ngân hàng Đề thi**: Tạo đề thi trắc nghiệm, thêm/sửa câu hỏi và đáp án A/B/C/D.
- **Quản lý Sổ điểm**: Bảng nhập điểm tương tác (Bài tập, Kiểm tra, Giữa kỳ, Cuối kỳ) tự động tính toán tổng điểm và xếp loại A+/A/B/C/D/F.

### 4. Mô-đun Quản trị viên (Admin):
- **Admin Dashboard**: Biểu đồ phân bố sinh viên theo ngành, biểu đồ lớp học theo khoa, thống kê tổng quát toàn trường.
- **Quản lý Người dùng**: Tạo mới, sửa, xóa, khóa/mở khóa tài khoản Sinh viên, Giảng viên và Admin.
- **Quản lý Đào tạo**: CRUD danh mục Khoa, Ngành học, Môn học, Lớp sinh hoạt và Lớp học phần.
- **Báo cáo & Thống kê**: Xuất báo cáo bảng điểm toàn trường dạng **Excel CSV** hoặc in ấn trực tiếp (PDF).

---

## 🔐 Bảo mật Hệ thống
- Tất cả mật khẩu được mã hóa băm bằng thuật toán bảo mật của `werkzeug.security`.
- Bảo vệ các đường dẫn trang web bằng Decorators kiểm tra Session và Phân quyền vai trò nghiêm ngặt (Ngăn sinh viên truy cập đường dẫn của Giảng viên hoặc Admin).

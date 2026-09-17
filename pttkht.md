## Phần 3: THIẾT KẾ GIAO DIỆN
BƯỚC 4: THIẾT KẾ GIAO DIỆN
1. Mục tiêu:
Thiết kế giao diện hệ thống quản lý học tập đơn giản, dễ sử dụng và phù hợp với từng loại người dùng.
Hệ thống gồm 3 giao diện chính:

👨‍🎓 Sinh viên

👨‍🏫 Giảng viên

👨‍💼 Quản trị viên

2. Giao diện đăng nhập
Người dùng nhập:
Tên đăng nhập
Mật khẩu
Chức năng:
Đăng nhập
Quên mật khẩu

┌─────────────────────────────────┐
│       🎓 QUẢN LÝ HỌC TẬP        │
│                                 │
│  Tên đăng nhập: [____________]  │
│  Mật khẩu:      [____________]  │
│                                 │
│          [  ĐĂNG NHẬP  ]        │
│                                 │
│          Quên mật khẩu?         │
└─────────────────────────────────┘

3. Giao diện sinh viên
Trang chủ
Hiển thị:
Thông tin sinh viên
Môn học
Thời khóa biểu
Điểm
Tài liệu

┌──────────────────────────────────────────────┐
│ 🎓 HỆ THỐNG QUẢN LÝ HỌC TẬP       👤 SV     │
├──────────────┬───────────────────────────────┤
│ 🏠 Trang chủ │                               │
│ 📚 Môn học   │       Xin chào, Sinh viên!   │
│ 📝 Đăng ký   │                               │
│ 📅 Lịch học  │   📚 Môn học: 6              │
│ 📊 Điểm      │   📝 Đã đăng ký: 5            │
│ 📖 Tài liệu  │   📊 GPA: 3.25                │
│ 🚪 Đăng xuất │                               │
└──────────────┴───────────────────────────────┘

4. Giao diện đăng ký môn học

Sinh viên có thể xem danh sách môn học và đăng ký.

Mã môn	Tên môn	Tín chỉ	Giảng viên	Sĩ số	Thao tác
CNTT01	Lập trình Web	3	Nguyễn Văn A	35/50	Đăng ký
CNTT02	Cơ sở dữ liệu	3	Trần Văn B	40/50	Đăng ký
CNTT03	Phân tích hệ thống	3	Lê Văn C	45/50	Đăng ký
5. Giao diện xem điểm
┌──────────────────────────────────────────────┐
│              📊 KẾT QUẢ HỌC TẬP              │
├────────┬─────────────────────┬───────────────┤
│ Mã môn │ Tên môn             │ Điểm          │
├────────┼─────────────────────┼───────────────┤
│ CNTT01 │ Lập trình Web       │ 8.5           │
│ CNTT02 │ Cơ sở dữ liệu       │ 7.8           │
│ CNTT03 │ Phân tích hệ thống  │ 9.0           │
└────────┴─────────────────────┴───────────────┘

              Điểm trung bình: 8.43

6. Giao diện giảng viên

Các chức năng chính:

🏠 Trang chủ

🏫 Lớp học

👥 Sinh viên

📖 Tài liệu

📊 Nhập điểm

👤 Thông tin cá nhân

🚪 Đăng xuất

┌──────────────────────────────────────────────┐
│ 🎓 QUẢN LÝ HỌC TẬP              👨‍🏫 GV      │
├──────────────┬───────────────────────────────┤
│ 🏠 Trang chủ │                               │
│ 🏫 Lớp học   │       Lớp học phần            │
│ 👥 Sinh viên  │                               │
│ 📖 Tài liệu  │  CNTT01 - Lập trình Web      │
│ 📊 Nhập điểm │  CNTT02 - Cơ sở dữ liệu      │
│ 🚪 Đăng xuất │                               │
└──────────────┴───────────────────────────────┘

7. Giao diện nhập điểm
Mã SV	Họ tên	Chuyên cần	Giữa kỳ	Cuối kỳ	Tổng
SV001	Nguyễn Văn A	9	8	9	8.7
SV002	Trần Văn B	8	7	8	7.7
SV003	Lê Văn C	10	9	9	9.3

Nút chức năng:

[ LƯU ĐIỂM ]    [ HỦY ]

8. Giao diện quản trị viên

Quản trị viên có quyền quản lý toàn bộ hệ thống.

┌──────────────────────────────────────────────┐
│ 🎓 QUẢN TRỊ HỆ THỐNG              👨‍💼 ADMIN │
├────────────────┬─────────────────────────────┤
│ 🏠 Trang chủ   │                             │
│ 👤 Tài khoản   │      Tổng quan hệ thống    │
│ 👨‍🎓 Sinh viên  │                             │
│ 👨‍🏫 Giảng viên │   Sinh viên: 500           │
│ 📚 Môn học     │   Giảng viên: 50            │
│ 🏫 Lớp học     │   Môn học: 80               │
│ 📊 Báo cáo     │   Lớp học phần: 120         │
│ 🚪 Đăng xuất   │                             │
└────────────────┴─────────────────────────────┘

9. Nguyên tắc thiết kế

Giao diện đơn giản, dễ sử dụng.

Thiết kế Responsive cho máy tính và điện thoại.

Màu sắc thống nhất.

Các chức năng được phân quyền rõ ràng.

Thông tin quan trọng được hiển thị dễ nhìn.

Có thông báo khi thêm, sửa, xóa hoặc đăng ký dữ liệu.

Hạn chế thao tác dư thừa.

10. Màu sắc chủ đạo
Primary:   #2563EB  🔵
Success:   #16A34A  🟢
Warning:   #F59E0B  🟡
Danger:    #DC2626  🔴
Background:#F8FAFC  ⚪
Text:      #1E293B  ⚫

11. Cấu trúc giao diện
                HỆ THỐNG QUẢN LÝ HỌC TẬP
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Sinh viên     Giảng viên     Admin
              │            │            │
              ▼            ▼            ▼
          Trang chủ     Trang chủ    Dashboard
          Môn học       Lớp học      Người dùng
          Đăng ký       Tài liệu     Sinh viên
          Lịch học      Nhập điểm    Giảng viên
          Điểm          Sinh viên    Môn học
          Tài liệu                    Lớp học

12. Kết quả

Giao diện được thiết kế theo từng nhóm người dùng, giúp:

Sinh viên dễ dàng theo dõi quá trình học tập.

Giảng viên quản lý lớp và điểm.

Quản trị viên quản lý toàn bộ hệ thống.

Thiết kế giao diện là cơ sở để triển khai Frontend của hệ thống.

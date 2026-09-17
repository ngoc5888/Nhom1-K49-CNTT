## Phần 1: Khảo sát và xác định yêu cầu
Bảng mô tả bài toán
### Bảng mô tả bài toán
| Tiêu chí | Nội dung mô tả |
| :--- | :--- |
| **Bối cảnh** | Nhu cầu tổ chức và tham gia học tập trên môi trường trực tuyến cho nhà trường, giảng viên và sinh viên. |
| **Thực trạng giải quyết** | Khắc phục tình trạng quản lý phân tán thông tin người dùng, môn học, tài liệu giảng dạy, bài tập và theo dõi điểm. |
| **Giải pháp** | Xây dựng Hệ thống Quản lý Học tập Trực tuyến để quản trị toàn bộ hoạt động dạy và học. |                      |

Mục tiêu dự án
* Xây dựng nền tảng hỗ trợ học tập trực tuyến.
* Quản lý tập trung thông tin sinh viên, giảng viên và tài khoản toàn hệ thống.
* Quản lý môn học và khóa học có hệ thống.
* Cho phép giảng viên đăng tải bài giảng, tài liệu môn học, tạo bài tập, bài kiểm tra và chấm điểm.
* Cho phép sinh viên xem, tham gia khóa học, xem bài giảng, tải tài liệu, làm bài tập, làm bài kiểm tra và tra cứu điểm số.
* Theo dõi kết quả học tập của sinh viên và hỗ trợ quản trị viên quản lý toàn bộ hệ thống.

Phạm vi hệ thống
* Xây dựng hệ thống web hỗ trợ 3 đối tượng (Admin, Giảng viên, Sinh viên) thực hiện các chức năng: quản lý tài khoản, quản lý môn học và khóa học; đăng tải/xem bài giảng và tài liệu; tạo, làm và chấm điểm bài tập/bài kiểm tra; theo dõi kết quả học tập.

Danh sách tác nhân:
* Quản trị viên(Admin):Quản lý toàn bộ hệ thống, gồm tài khoản, giảng viên, sinh viên, môn học và khóa học.
* Giảng viên (Teacher): Phụ trách tạo và quản lý khóa học, đăng bài giảng, đăng tài liệu, tạo bài tập/kiểm tra, chấm điểm và theo dõi kết quả của sinh viên.
* Sinh viên (Student): Người học đăng ký/đăng nhập, xem và tham gia khóa học, học bài, tải tài liệu, làm bài tập/kiểm tra và xem kết quả.

## Phần 2: Phân tích hệ thống
### 1. Sơ đồ Luồng Đăng nhập và Phân quyền

```mermaid
graph TD
    A[Nhập Tài khoản / Mật khẩu] --> B(ĐĂNG NHẬP)
    B --> C{Kiểm tra tài khoản}
    
    C -->|Quyền Admin| D[Admin UI]
    C -->|Quyền Giảng viên| E[Teacher UI]
    C -->|Quyền Sinh viên| F[Student UI]
```
### 2. Phân rã chức năng - Quản trị viên (Admin)

```mermaid
graph TD
    Admin[Admin UI] --> TQ[TỔNG QUAN]
    TQ --> DB1[Dashboard]

    Admin --> QLND[QUẢN LÝ NGƯỜI DÚNG]
    QLND --> SV[Sinh viên]
    QLND --> GV[Giảng viên]
    QLND --> TK[Tài khoản]

    Admin --> QLDT[QUẢN LÝ ĐÀO TẠO]
    QLDT --> K[Khoa]
    QLDT --> N[Ngành]
    QLDT --> L[Lớp]
    QLDT --> MH[Môn học]

    Admin --> QLHT[QUẢN LÝ HỆ THỐNG]
    QLHT --> ND[Nội dung học tập]
    QLHT --> TB1[Thông báo]
    QLHT --> BC[Báo cáo]
    QLHT --> CD1[Cài đặt]
    
    Admin --> DX1(Đăng xuất)
```
### 3. Phân rã chức năng - Giảng viên

```mermaid
graph TD
    Teacher[Teacher UI] --> TQ[TỔNG QUAN]
    TQ --> DB2[Dashboard]

    Teacher --> QLGD[QUẢN LÝ GIẢNG DẠY]
    QLGD --> LH[Lớp học]
    QLGD --> SV2[Sinh viên]
    QLGD --> TL[Tài liệu]
    QLGD --> BT[Bài tập]
    QLGD --> KT[Kiểm tra]
    QLGD --> D[Điểm]

    Teacher --> QL[QUẢN LÝ]
    QL --> TB2[Thông báo]
    QL --> LICH[Lịch học]

    Teacher --> CN1[CÁ NHÂN]
    CN1 --> HS1[Hồ sơ]
    CN1 --> CD2[Cài đặt]
    
    Teacher --> DX2(Đăng xuất)
```
### 4. Phân rã chức năng - Sinh viên

```mermaid
graph TD
    Student[Student UI] --> ST[SỔ TAY]
    ST --> TQ2[Tổng quan]

    Student --> HT[HỌC TẬP]
    HT --> LCM[Lớp của tôi]
    HT --> GT[Giáo trình]
    HT --> HL[Học liệu]
    HT --> BT2[Bài tập]
    HT --> KT2[Kiểm tra]
    HT --> KQ[Kết quả]

    Student --> CN2[CÁ NHÂN]
    CN2 --> HS2[Hồ sơ]
    CN2 --> TD[Tiến độ]
    CN2 --> TB3[Thông báo]
    CN2 --> CD3[Cài đặt]
    
    Student --> DX3(Đăng xuất)
```
## Phần 4: Triển khai và Kiểm thử

### 4.1. Môi trường triển khai
* **Mã nguồn & Quản lý phiên bản:** Git, GitHub.
* **Công cụ lập trình:** Visual Studio Code.
* **Kiểm thử API:** Postman.

### 4.2. Kết quả đạt được
* Xây dựng thành công hệ thống với 3 phân quyền hoạt động độc lập: **Admin**, **Giảng viên**, và **Sinh viên**.
* Hoàn thiện các luồng nghiệp vụ cốt lõi: Quản lý danh mục đào tạo, Đăng tải học liệu (Video, PDF), Quản lý bài tập/đề thi và Theo dõi kết quả học tập.

### 4.3. Kiểm thử hệ thống (Testing)
Quá trình kiểm thử được thực hiện để đảm bảo tính ổn định của hệ thống:
* **Kiểm thử giao diện (UI/UX):** Đảm bảo tính Responsive và các luồng thao tác (nhấp chuột, điền form) hoạt động đúng như thiết kế.
* **Kiểm thử API (Backend):** Sử dụng Postman để xác thực các endpoint, đảm bảo dữ liệu trả về chính xác (đặc biệt là API Đăng nhập và Nộp bài).
* **Kiểm thử luồng nghiệp vụ:**
  * Hệ thống tự động chặn truy cập (báo lỗi 403) khi sinh viên cố tình vào trang của giảng viên.
  * Tự động khóa thao tác và thu bài thi khi hết thời gian đếm ngược.

### 4.4. Hướng phát triển
* Nâng cấp hệ thống lưu trữ đám mây (Cloud Storage) để tối ưu băng thông tải video bài giảng.
* Tích hợp tính năng phòng học trực tuyến (Video Call) để tăng tính tương tác.
3. THIẾT KẾ GIAO DIỆN
3.1. Mục tiêu

Thiết kế giao diện hệ thống quản lý học tập đơn giản, dễ sử dụng và phù hợp với từng nhóm người dùng.

Hệ thống gồm 3 nhóm người dùng:

👨‍🎓 Sinh viên

👨‍🏫 Giảng viên

👨‍💼 Quản trị viên

3.2. Giao diện đăng nhập

Người dùng nhập tên đăng nhập và mật khẩu.

Các chức năng:

Đăng nhập

Quên mật khẩu

+---------------------------------+
|       🎓 QUẢN LÝ HỌC TẬP       |
|                                 |
| Tên đăng nhập: [____________]   |
| Mật khẩu:      [____________]   |
|                                 |
|          [ ĐĂNG NHẬP ]          |
|                                 |
|          Quên mật khẩu?         |
+---------------------------------+

3.3. Giao diện sinh viên
Trang chủ

Sinh viên có thể xem:

Thông tin cá nhân

Danh sách môn học

Đăng ký môn học

Thời khóa biểu

Kết quả học tập

Tài liệu học tập

+-----------------------------------------------+
| 🎓 HỆ THỐNG QUẢN LÝ HỌC TẬP          👤 SV   |
+----------------+------------------------------+
| 🏠 Trang chủ   |      Xin chào, Sinh viên!   |
| 📚 Môn học     |      Môn học: 6             |
| 📝 Đăng ký     |      Đã đăng ký: 5          |
| 📅 Lịch học    |      GPA: 3.25              |
| 📊 Điểm        |                              |
| 📖 Tài liệu    |                              |
| 🚪 Đăng xuất   |                              |
+----------------+------------------------------+

Đăng ký môn học

Sinh viên chọn môn học muốn đăng ký. Hệ thống hiển thị mã môn, tên môn, số tín chỉ, giảng viên và sĩ số lớp.

Ví dụ:

CNTT01 - Lập trình Web
3 tín chỉ - GV: Nguyễn Văn A
Sĩ số: 35/50
[ ĐĂNG KÝ ]

CNTT02 - Cơ sở dữ liệu
3 tín chỉ - GV: Trần Văn B
Sĩ số: 40/50
[ ĐĂNG KÝ ]

Xem điểm

Sinh viên xem điểm của từng môn học và điểm trung bình.

CNTT01 - Lập trình Web       : 8.5
CNTT02 - Cơ sở dữ liệu       : 7.8
CNTT03 - Phân tích hệ thống  : 9.0

Điểm trung bình: 8.43

3.4. Giao diện giảng viên

Giảng viên có các chức năng:

🏠 Trang chủ

🏫 Quản lý lớp học

👥 Xem danh sách sinh viên

📖 Quản lý tài liệu

📊 Nhập và cập nhật điểm

👤 Quản lý thông tin cá nhân

🚪 Đăng xuất

+-----------------------------------------------+
| 🎓 QUẢN LÝ HỌC TẬP                 👨‍🏫 GV    |
+----------------+------------------------------+
| 🏠 Trang chủ   |       Lớp học phần           |
| 🏫 Lớp học     |                              |
| 👥 Sinh viên   |  CNTT01 - Lập trình Web     |
| 📖 Tài liệu    |  CNTT02 - Cơ sở dữ liệu     |
| 📊 Nhập điểm   |                              |
| 🚪 Đăng xuất   |                              |
+----------------+------------------------------+

Nhập điểm

Giảng viên chọn lớp học phần, chọn sinh viên và nhập điểm.

SV001 - Nguyễn Văn A
Chuyên cần: 9 | Giữa kỳ: 8 | Cuối kỳ: 9
Điểm tổng: 8.7

SV002 - Trần Văn B
Chuyên cần: 8 | Giữa kỳ: 7 | Cuối kỳ: 8
Điểm tổng: 7.7

[ LƯU ĐIỂM ]    [ HỦY ]

3.5. Giao diện quản trị viên

Quản trị viên có quyền quản lý toàn bộ hệ thống.

Các chức năng:

👤 Quản lý tài khoản

👨‍🎓 Quản lý sinh viên

👨‍🏫 Quản lý giảng viên

📚 Quản lý môn học

🏫 Quản lý lớp học

📊 Xem báo cáo

🚪 Đăng xuất

+-----------------------------------------------+
| 🎓 QUẢN TRỊ HỆ THỐNG              👨‍💼 ADMIN |
+----------------+------------------------------+
| 🏠 Trang chủ   |      Tổng quan hệ thống     |
| 👤 Tài khoản   |                              |
| 👨‍🎓 Sinh viên  |      Sinh viên: 500          |
| 👨‍🏫 Giảng viên |      Giảng viên: 50           |
| 📚 Môn học     |      Môn học: 80              |
| 🏫 Lớp học     |      Lớp học phần: 120        |
| 📊 Báo cáo     |                              |
| 🚪 Đăng xuất   |                              |
+----------------+------------------------------+

3.6. Nguyên tắc thiết kế

Giao diện đơn giản, dễ sử dụng.

Bố cục rõ ràng.

Phân quyền theo từng nhóm người dùng.

Responsive trên máy tính và điện thoại.

Màu sắc thống nhất.

Có thông báo khi thực hiện thao tác.

Hạn chế các thao tác không cần thiết.

Màu sắc chủ đạo
Primary    : #2563EB
Success    : #16A34A
Warning    : #F59E0B
Danger     : #DC2626
Background : #F8FAFC
Text       : #1E293B

3.7. Cấu trúc giao diện
              HỆ THỐNG QUẢN LÝ HỌC TẬP
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      Sinh viên      Giảng viên       Admin
          |              |              |
          v              v              v
       Môn học        Lớp học       Tài khoản
       Đăng ký        Tài liệu      Sinh viên
       Lịch học       Nhập điểm     Giảng viên
       Điểm           Sinh viên     Môn học
       Tài liệu                     Lớp học

3.8. Kết quả

Giao diện được thiết kế theo từng nhóm người dùng:

👨‍🎓 Sinh viên: Theo dõi và quản lý quá trình học tập.

👨‍🏫 Giảng viên: Quản lý lớp học, tài liệu và điểm.

👨‍💼 Quản trị viên: Quản lý toàn bộ hệ thống.

Thiết kế giao diện là cơ sở để triển khai Frontend của hệ thống.

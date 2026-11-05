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

## Phần 4: Triển khai và Kiểm thử

### 4.1. Môi trường triển khai
* **Ngôn ngữ & Framework:** Python, Flask
* **Môi trường phát triển:** Visual Studio Code
* **Quản lý mã nguồn:** Git, GitHub
* **Công cụ kiểm thử:** Python `unittest` (Flask Test Client), Postman

### 4.2. Kết quả đạt được
* Xây dựng hệ thống web phân quyền 3 nhóm người dùng: Quản trị viên (Admin), Giảng viên và Sinh viên.
* Hoàn thiện các luồng chức năng cốt lõi:
  * Quản lý tài khoản và phân quyền truy cập.
  * Đăng tải học liệu (tệp PDF, liên kết video bài giảng).
  * Giao bài tập, nộp bài và chấm điểm trực tiếp.
  * Theo dõi kết quả và tiến độ học tập.

### 4.3. Kiểm thử hệ thống (Testing)

#### Kiểm thử tự động (Unit Test với `unittest`)
Sử dụng `Flask Test Client` để kiểm tra phản hồi từ các endpoint:
* `test_home_redirect`: Gửi yêu cầu `GET /` khi chưa đăng nhập $\rightarrow$ Trả về mã HTTP `302` (chuyển hướng về `/login`).
* `test_login_page`: Gửi yêu cầu `GET /login` $\rightarrow$ Trả về mã HTTP `200` (trang đăng nhập hiển thị bình thường).

#### Kiểm thử chức năng & API (Manual & Postman)
* **Xác thực và phân quyền:** Kiểm tra luồng đăng nhập; chặn quyền truy cập trái phép của sinh viên vào các trang quản lý của giảng viên (trả về lỗi `403` hoặc điều hướng lại).
* **Nghiệp vụ bài tập:** Kiểm tra tính hợp lệ của dữ liệu form đầu vào, định dạng tệp tải lên và xử lý khi nộp bài.
* **Giao diện:** Kiểm tra khả năng hiển thị trên trình duyệt máy tính và thiết bị di động.

### 4.4. Hạn chế và Hướng phát triển
* Mở rộng thêm các kịch bản kiểm thử tự động cho phương thức `POST` (đăng nhập sai thông tin, nộp bài quá hạn).
* Tối ưu hóa lưu trữ tệp bài tập và nâng cấp cơ chế thông báo điểm số cho sinh viên theo thời gian thực.
#### 3. THIẾT KẾ GIAO DIỆN

Hệ thống quản lý học tập
1. Giới thiệu
Hệ thống quản lý học tập (LMS) được xây dựng nhằm hỗ trợ sinh viên, giảng viên và quản trị viên trong việc quản lý quá trình học tập.
2. Đối tượng sử dụng
Sinh viên: Xem khóa học, học bài, làm bài tập, xem điểm và theo dõi tiến độ.
Giảng viên: Quản lý khóa học, tạo bài tập, chấm điểm và theo dõi sinh viên.
Quản trị viên: Quản lý tài khoản, khóa học và các chức năng của hệ thống.
3. Thiết kế giao diện
Giao diện được thiết kế theo hướng đơn giản, dễ sử dụng và dễ mở rộng.
Dashboard
Hiển thị các thông tin chính:
Khóa học đang tham gia
Tiến độ học tập
Bài tập sắp đến hạn
Lịch học
Thông báo
Quản lý khóa học
Sinh viên có thể xem nội dung bài học, tài liệu và tiến độ.
Giảng viên có thể tạo, chỉnh sửa và quản lý nội dung khóa học.
Bài tập và kiểm tra
Sinh viên làm và nộp bài.
Giảng viên chấm điểm và nhận xét.
Hệ thống hiển thị kết quả sau khi hoàn thành.
Quản lý điểm
Hiển thị:
Điểm từng bài tập
Điểm kiểm tra
Điểm trung bình
Kết quả học tập
Quản lý người dùng
Quản trị viên có thể:
Quản lý sinh viên
Quản lý giảng viên
Quản lý tài khoản
Phân quyền người dùng
4. Điều hướng giao diện
Dashboard
├── Khóa học
├── Bài tập
├── Điểm số
├── Lịch học
├── Thông báo
└── Cài đặt
5. Nguyên tắc UI/UX
Giao diện đơn giản, trực quan.
Bố cục rõ ràng và nhất quán.
Màu sắc và font chữ dễ đọc.
Responsive trên máy tính và điện thoại.
Các chức năng được phân quyền theo từng loại người dùng.
6. Mục tiêu
Hệ thống hướng tới việc tạo ra một môi trường học tập trực tuyến thuận tiện, giúp người dùng dễ dàng quản lý khóa học, bài tập, điểm số và tiến độ học tập.

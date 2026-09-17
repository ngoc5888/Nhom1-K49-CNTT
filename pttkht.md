## 1. Khảo sát và xác định yêu cầu
Bảng mô tả bài toán
|Tiêu chí               |    Nội dung mô tả                                                                                                   |
|Bối cảnh               |    Nhu cầu tổ chức và tham gia học tập trên môi trường trực tuyến cho nhà trường, giảng viên và sinh viên.          |
|Thực trạng giải quyết  |    Khắc phục tình trạng quản lý phân tán thông tin người dùng,môn học, tài liệu giảng dạy, bài tập và theo dõi điểm |
|Giải pháp              |    Xây dựng Hệ thống Quản lý Học tập Trực tuyến để quản trị toàn bộ hoạt động dạy và học.                           |
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

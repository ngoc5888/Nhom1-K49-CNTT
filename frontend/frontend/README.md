# LMS Dashboard

Giao diện Front-End cho **Hệ thống Quản lý Học tập** (Learning Management System) — SPA xây dựng bằng React + TypeScript + Tailwind CSS.

![Preview](https://img.shields.io/badge/React-19-blue?logo=react) ![TypeScript](https://img.shields.io/badge/TypeScript-6-blue?logo=typescript) ![TailwindCSS](https://img.shields.io/badge/Tailwind-3-38bdf8?logo=tailwindcss) ![Vite](https://img.shields.io/badge/Vite-8-646cff?logo=vite)

---

## Tech Stack

| Lớp | Công nghệ |
|---|---|
| Build tool | Vite 8 + TypeScript 6 |
| UI Framework | React 19 |
| Styling | Tailwind CSS 3 |
| Routing | React Router DOM v7 |
| State Management | Zustand v5 (persist) |
| Form & Validation | React Hook Form + Zod |
| Charts | Recharts v3 |
| Icons | Lucide React |
| UI Primitives | Radix UI |

---

## Cài đặt & Chạy

```bash
# Clone repo
git clone <your-repo-url>
cd lms-dashboard

# Cài dependencies
npm install

# Chạy dev server
npm run dev
```

Mở trình duyệt tại `http://localhost:5173`

```bash
# Build production
npm run build

# Preview bản build
npm run preview
```

---

## Tài khoản Demo

| Tài khoản | Mật khẩu | Role |
|---|---|---|
| `admin` | `123456` | Quản trị viên |
| `teacher` | `123456` | Giảng viên |
| `student` | `123456` | Sinh viên |

Hoặc bấm thẳng vào 3 nút **Đăng nhập nhanh** ở trang Login.

---

## Cấu trúc thư mục

```
src/
├── App.tsx                   # Router chính (3 roles)
├── main.tsx                  # React entry point
├── index.css                 # Tailwind + global styles
├── types/index.ts            # TypeScript types
├── store/authStore.ts        # Zustand auth store
├── data/mockData.ts          # Mock data
├── lib/utils.ts              # Utilities (cn, formatDate...)
├── components/
│   ├── auth/                 # ProtectedRoute, PublicRoute
│   ├── layout/               # DashboardLayout, Header, Sidebar
│   └── ui/                   # Button, Badge, Avatar, Card, Input, Modal, Table
└── pages/
    ├── auth/                 # LoginPage
    ├── admin/                # 12 trang Admin
    ├── teacher/              # 11 trang Giảng viên
    └── student/              # 9 trang Sinh viên
```

---

## Tính năng theo Role

### Quản trị viên (Admin)
- Dashboard thống kê toàn hệ thống (biểu đồ người dùng, phân bổ lớp học)
- CRUD Sinh viên, Giảng viên, Tài khoản
- Quản lý Khoa, Ngành, Lớp học, Môn học
- Quản lý khung chương trình đào tạo
- Phát thông báo toàn trường
- Báo cáo thống kê đào tạo
- Cài đặt niên khóa, bảo mật hệ thống

### Giảng viên (Teacher)
- Dashboard thống kê lớp phụ trách
- Quản lý lớp học, danh sách sinh viên
- Upload tài liệu bài giảng
- Tạo bài tập, chấm điểm inline
- Nhập điểm (GK/Lab/CK) với tính tự động
- Tạo đề kiểm tra
- Lịch dạy theo tuần
- Gửi thông báo cho sinh viên

### Sinh viên (Student)
- Dashboard cá nhân (GPA chart, lịch thi, bài tập)
- Xem lớp học, tài liệu, bài tập, kiểm tra
- Bảng kết quả học tập (RadarChart, BarChart)
- Chỉnh sửa hồ sơ cá nhân
- Thông báo từ nhà trường

---

## Ghi chú

- Toàn bộ data là **mock** — không có API thực
- Auth được lưu vào `localStorage` qua Zustand persist
- UI text hoàn toàn bằng **tiếng Việt**

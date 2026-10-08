// Admin supplementary pages
import { useState } from 'react'
import {
  Plus, Edit2, Trash2, Search, Shield, Key, Settings, BookOpen,
  Building2, Briefcase, Layers, Bell, FileBarChart, BarChart2,
  Users, GraduationCap, TrendingUp, Download, Calendar,
  CheckCircle, AlertTriangle, Info, Megaphone, Database,
} from 'lucide-react'
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend, PieChart, Pie, Cell,
} from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Avatar } from '../../components/ui/Avatar'
import { Table, Td, Tr } from '../../components/ui/Table'
import { Button } from '../../components/ui/Button'
import { Modal } from '../../components/ui/Modal'
import { mockTeachers, mockStudents, faculties, courses, mockClasses, mockNotifications } from '../../data/mockData'

// ===== Teachers =====
export function AdminTeachers() {
  const [showModal, setShowModal] = useState(false)
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Giảng viên</h1>
          <p className="text-slate-500 text-sm mt-1">Thêm, sửa, phân công khoa giảng viên</p>
        </div>
        <Button onClick={() => setShowModal(true)}><Plus size={15} />Thêm giảng viên</Button>
      </div>
      <Card>
        <Table headers={['Giảng viên', 'Mã GV', 'Khoa', 'Môn phụ trách', 'Số lớp', 'Số SV', 'Hành động']}>
          {mockTeachers.map((t) => (
            <Tr key={t.id}>
              <Td>
                <div className="flex items-center gap-3">
                  <Avatar name={t.name} size="sm" />
                  <div>
                    <p className="font-medium text-slate-800">{t.name}</p>
                    <p className="text-xs text-slate-400">{t.email}</p>
                  </div>
                </div>
              </Td>
              <Td className="font-mono text-xs text-slate-500">{t.id}</Td>
              <Td><Badge variant="purple">{t.department}</Badge></Td>
              <Td className="text-slate-600">{t.subject}</Td>
              <Td className="text-slate-700 font-semibold">{t.classes}</Td>
              <Td className="text-slate-700">{t.students}</Td>
              <Td>
                <div className="flex items-center gap-1.5">
                  <button className="p-1.5 hover:bg-blue-50 rounded text-blue-500 transition-colors"><Edit2 size={13} /></button>
                  <button className="p-1.5 hover:bg-red-50 rounded text-red-500 transition-colors"><Trash2 size={13} /></button>
                </div>
              </Td>
            </Tr>
          ))}
        </Table>
      </Card>

      <Modal open={showModal} onClose={() => setShowModal(false)} title="Thêm Giảng viên mới"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowModal(false)}>Hủy</Button>
            <Button onClick={() => setShowModal(false)}>Thêm giảng viên</Button>
          </>
        }
      >
        <div className="space-y-4">
          {['Họ và tên', 'Mã giảng viên', 'Email', 'Học hàm / Học vị'].map((label) => (
            <div key={label} className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-700">{label}</label>
              <input type="text" placeholder={`Nhập ${label.toLowerCase()}...`}
                className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary" />
            </div>
          ))}
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Khoa công tác</label>
            <select className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
              {faculties.map((f) => <option key={f.id}>{f.name}</option>)}
            </select>
          </div>
        </div>
      </Modal>
    </div>
  )
}

// ===== Accounts =====
export function AdminAccounts() {
  const accounts = [
    { id: '1', name: 'Nguyễn Quản Trị', username: 'admin', role: 'ADMIN', status: 'active', lastLogin: '26/09/2026' },
    { id: '2', name: 'Trần Văn Giảng', username: 'teacher', role: 'TEACHER', status: 'active', lastLogin: '25/09/2026' },
    { id: '3', name: 'Lê Thị Sinh Viên', username: 'student', role: 'STUDENT', status: 'active', lastLogin: '26/09/2026' },
    ...mockStudents.slice(0, 5).map((s, i) => ({
      id: `sv-${i}`, name: s.name, username: s.id.toLowerCase(), role: 'STUDENT',
      status: s.status, lastLogin: '24/09/2026',
    })),
  ]
  const roleVariant: Record<string, 'red' | 'blue' | 'green'> = { ADMIN: 'red', TEACHER: 'blue', STUDENT: 'green' }
  const roleLabel: Record<string, string> = { ADMIN: 'Quản trị viên', TEACHER: 'Giảng viên', STUDENT: 'Sinh viên' }

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Tài khoản</h1>
          <p className="text-slate-500 text-sm mt-1">Cấp phát, reset mật khẩu và phân quyền hệ thống</p>
        </div>
        <Button><Plus size={15} />Tạo tài khoản</Button>
      </div>

      {/* Action Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {[
          { label: 'Cấp phát tài khoản mới', icon: Shield, color: 'bg-blue-500', desc: 'Tạo tài khoản sinh viên hoặc giảng viên mới vào hệ thống' },
          { label: 'Reset mật khẩu', icon: Key, color: 'bg-amber-500', desc: 'Đặt lại mật khẩu cho tài khoản bị quên hoặc mất quyền truy cập' },
          { label: 'Phân quyền hệ thống', icon: Settings, color: 'bg-violet-500', desc: 'Cấu hình quyền truy cập theo vai trò (Admin, Giảng viên, Sinh viên)' },
        ].map((item) => {
          const Icon = item.icon
          return (
            <div key={item.label} className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm hover:shadow-md transition-all cursor-pointer group">
              <div className={`w-12 h-12 ${item.color} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                <Icon size={22} className="text-white" />
              </div>
              <h3 className="font-semibold text-slate-800">{item.label}</h3>
              <p className="text-sm text-slate-500 mt-1 leading-relaxed">{item.desc}</p>
            </div>
          )
        })}
      </div>

      {/* Account Table */}
      <Card>
        <CardHeader><CardTitle>Danh sách tài khoản ({accounts.length})</CardTitle></CardHeader>
        <Table headers={['Người dùng', 'Tài khoản', 'Vai trò', 'Trạng thái', 'Đăng nhập cuối', 'Hành động']}>
          {accounts.map((acc) => (
            <Tr key={acc.id}>
              <Td>
                <div className="flex items-center gap-3">
                  <Avatar name={acc.name} size="sm" />
                  <span className="font-medium text-slate-800">{acc.name}</span>
                </div>
              </Td>
              <Td className="font-mono text-xs text-slate-500">{acc.username}</Td>
              <Td><Badge variant={roleVariant[acc.role] ?? 'gray'}>{roleLabel[acc.role] ?? acc.role}</Badge></Td>
              <Td><Badge variant={acc.status === 'active' ? 'green' : 'gray'}>{acc.status === 'active' ? 'Hoạt động' : 'Bị khóa'}</Badge></Td>
              <Td className="text-slate-500">{acc.lastLogin}</Td>
              <Td>
                <div className="flex items-center gap-1.5">
                  <button className="p-1.5 hover:bg-amber-50 rounded text-amber-500 transition-colors" title="Reset mật khẩu"><Key size={13} /></button>
                  <button className="p-1.5 hover:bg-blue-50 rounded text-blue-500 transition-colors" title="Chỉnh sửa"><Edit2 size={13} /></button>
                  <button className="p-1.5 hover:bg-red-50 rounded text-red-500 transition-colors" title="Xóa"><Trash2 size={13} /></button>
                </div>
              </Td>
            </Tr>
          ))}
        </Table>
      </Card>
    </div>
  )
}

// ===== Faculties =====
export function AdminFaculties() {
  const [showModal, setShowModal] = useState(false)
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Khoa</h1>
          <p className="text-slate-500 text-sm mt-1">Danh mục các khoa đào tạo</p>
        </div>
        <Button onClick={() => setShowModal(true)}><Plus size={15} />Thêm khoa mới</Button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {faculties.map((f) => (
          <Card key={f.id} className="hover:shadow-md transition-shadow">
            <CardContent className="p-5">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-blue-100 rounded-xl flex-shrink-0">
                  <Building2 size={22} className="text-blue-600" />
                </div>
                <div className="flex-1">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-semibold text-slate-800">{f.name}</p>
                      <p className="text-xs text-slate-500 mt-0.5">Mã: <strong>{f.code}</strong></p>
                    </div>
                    <div className="flex gap-1.5">
                      <button className="p-1.5 hover:bg-blue-50 rounded text-blue-500 transition-colors"><Edit2 size={13} /></button>
                      <button className="p-1.5 hover:bg-red-50 rounded text-red-500 transition-colors"><Trash2 size={13} /></button>
                    </div>
                  </div>
                  <p className="text-sm text-slate-600 mt-2">Trưởng khoa: <strong>{f.dean}</strong></p>
                  <div className="mt-3 grid grid-cols-2 gap-3 text-center text-xs">
                    <div className="bg-slate-50 rounded-lg py-2">
                      <p className="font-bold text-slate-800 text-lg">{f.teachers}</p>
                      <p className="text-slate-500">Giảng viên</p>
                    </div>
                    <div className="bg-slate-50 rounded-lg py-2">
                      <p className="font-bold text-slate-800 text-lg">{f.students}</p>
                      <p className="text-slate-500">Sinh viên</p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Modal open={showModal} onClose={() => setShowModal(false)} title="Thêm Khoa mới"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowModal(false)}>Hủy</Button>
            <Button onClick={() => setShowModal(false)}>Thêm khoa</Button>
          </>
        }
      >
        <div className="space-y-4">
          {['Tên khoa', 'Mã khoa', 'Trưởng khoa'].map((label) => (
            <div key={label} className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-700">{label}</label>
              <input type="text" placeholder={`Nhập ${label.toLowerCase()}...`}
                className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
            </div>
          ))}
        </div>
      </Modal>
    </div>
  )
}

// ===== Majors =====
export function AdminMajors() {
  const majors = [
    { id: 'NG001', name: 'Kỹ thuật Phần mềm', code: 'SE', faculty: 'CNTT', duration: 4, students: 180 },
    { id: 'NG002', name: 'Khoa học Máy tính', code: 'CS', faculty: 'CNTT', duration: 4, students: 150 },
    { id: 'NG003', name: 'Trí tuệ Nhân tạo', code: 'AI', faculty: 'CNTT', duration: 4, students: 120 },
    { id: 'NG004', name: 'Kỹ thuật Máy tính', code: 'CE', faculty: 'KTMT', duration: 4.5, students: 95 },
    { id: 'NG005', name: 'Hệ thống Thông tin', code: 'IS', faculty: 'HTTT', duration: 4, students: 110 },
    { id: 'NG006', name: 'Mạng & Truyền thông', code: 'NET', faculty: 'MMT', duration: 4, students: 85 },
  ]
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Ngành học</h1>
          <p className="text-slate-500 text-sm mt-1">Các chuyên ngành đào tạo</p>
        </div>
        <Button><Plus size={15} />Thêm ngành</Button>
      </div>
      <Card>
        <Table headers={['Tên ngành', 'Mã ngành', 'Khoa', 'Thời gian đào tạo', 'Số sinh viên', 'Hành động']}>
          {majors.map((m) => (
            <Tr key={m.id}>
              <Td className="font-medium text-slate-800">{m.name}</Td>
              <Td><Badge variant="blue">{m.code}</Badge></Td>
              <Td className="text-slate-600">{m.faculty}</Td>
              <Td className="text-slate-600">{m.duration} năm</Td>
              <Td className="text-slate-700 font-semibold">{m.students}</Td>
              <Td>
                <div className="flex items-center gap-1.5">
                  <button className="p-1.5 hover:bg-blue-50 rounded text-blue-500"><Edit2 size={13} /></button>
                  <button className="p-1.5 hover:bg-red-50 rounded text-red-500"><Trash2 size={13} /></button>
                </div>
              </Td>
            </Tr>
          ))}
        </Table>
      </Card>
    </div>
  )
}

// ===== Classes =====
export function AdminClasses() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Lớp học</h1>
          <p className="text-slate-500 text-sm mt-1">Tạo lớp niên chế, phân công giảng viên</p>
        </div>
        <Button><Plus size={15} />Tạo lớp mới</Button>
      </div>
      <Card>
        <Table headers={['Tên lớp', 'Mã HP', 'Giảng viên', 'Sĩ số', 'Lịch học', 'Phòng', 'TC', 'Trạng thái', 'Hành động']}>
          {mockClasses.map((c) => (
            <Tr key={c.id}>
              <Td className="font-medium text-slate-800">{c.name}</Td>
              <Td className="font-mono text-xs text-slate-500">{c.code}</Td>
              <Td className="text-slate-600">{c.teacher}</Td>
              <Td className="text-slate-700 font-semibold">{c.students}</Td>
              <Td className="text-slate-500 text-xs">{c.schedule}</Td>
              <Td className="text-slate-500">{c.room}</Td>
              <Td className="text-slate-600">{c.credits}</Td>
              <Td><Badge variant={c.status === 'active' ? 'green' : 'gray'}>{c.status === 'active' ? 'Đang học' : 'Kết thúc'}</Badge></Td>
              <Td>
                <div className="flex items-center gap-1.5">
                  <button className="p-1.5 hover:bg-blue-50 rounded text-blue-500"><Edit2 size={13} /></button>
                  <button className="p-1.5 hover:bg-red-50 rounded text-red-500"><Trash2 size={13} /></button>
                </div>
              </Td>
            </Tr>
          ))}
        </Table>
      </Card>
    </div>
  )
}

// ===== Courses =====
export function AdminCourses() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Môn học</h1>
          <p className="text-slate-500 text-sm mt-1">Học phần, tín chỉ và môn tiên quyết</p>
        </div>
        <Button><Plus size={15} />Thêm môn học</Button>
      </div>
      <Card>
        <Table headers={['Tên môn học', 'Mã môn', 'Khoa', 'Tín chỉ', 'Môn tiên quyết', 'Trạng thái', 'Hành động']}>
          {courses.map((c) => (
            <Tr key={c.id}>
              <Td className="font-medium text-slate-800">{c.name}</Td>
              <Td className="font-mono text-xs text-slate-500">{c.code}</Td>
              <Td><Badge variant="purple">{c.faculty}</Badge></Td>
              <Td className="text-slate-700 font-semibold">{c.credits}</Td>
              <Td className="text-slate-500 text-xs">{c.prerequisite ?? '—'}</Td>
              <Td><Badge variant={c.status === 'active' ? 'green' : 'gray'}>{c.status === 'active' ? 'Hoạt động' : 'Ngừng'}</Badge></Td>
              <Td>
                <div className="flex items-center gap-1.5">
                  <button className="p-1.5 hover:bg-blue-50 rounded text-blue-500"><Edit2 size={13} /></button>
                  <button className="p-1.5 hover:bg-red-50 rounded text-red-500"><Trash2 size={13} /></button>
                </div>
              </Td>
            </Tr>
          ))}
        </Table>
      </Card>
    </div>
  )
}

// ===== Curriculum =====
export function AdminCurriculum() {
  const programs = [
    { code: 'CTDT-SE', name: 'Kỹ thuật Phần mềm', totalCredits: 140, mandatory: 90, elective: 50, updated: '01/09/2026' },
    { code: 'CTDT-CS', name: 'Khoa học Máy tính', totalCredits: 138, mandatory: 88, elective: 50, updated: '01/09/2026' },
    { code: 'CTDT-AI', name: 'Trí tuệ Nhân tạo', totalCredits: 142, mandatory: 92, elective: 50, updated: '15/08/2026' },
    { code: 'CTDT-CE', name: 'Kỹ thuật Máy tính', totalCredits: 145, mandatory: 95, elective: 50, updated: '01/09/2026' },
  ]
  const semesters = [
    { sem: 'HK1', courses: ['Nhập môn CNTT', 'Giải tích 1', 'Vật lý đại cương', 'Tiếng Anh 1'], credits: 18 },
    { sem: 'HK2', courses: ['Lập trình cơ bản', 'Giải tích 2', 'Đại số tuyến tính', 'Tiếng Anh 2'], credits: 20 },
    { sem: 'HK3', courses: ['Cấu trúc dữ liệu', 'Lập trình hướng đối tượng', 'Xác suất thống kê', 'Kinh tế vi mô'], credits: 21 },
    { sem: 'HK4', courses: ['Cơ sở dữ liệu', 'Hệ điều hành', 'Mạng máy tính', 'Công nghệ phần mềm'], credits: 20 },
  ]
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Nội dung học tập</h1>
          <p className="text-slate-500 text-sm mt-1">Quản lý cấu trúc khung chương trình đào tạo</p>
        </div>
        <Button><Plus size={15} />Tạo chương trình</Button>
      </div>

      {/* Program cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {programs.map((p) => (
          <Card key={p.code} className="hover:shadow-md transition-shadow">
            <CardContent className="p-5">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <Badge variant="blue" className="mb-1.5">{p.code}</Badge>
                  <p className="font-semibold text-slate-800">{p.name}</p>
                  <p className="text-xs text-slate-500 mt-0.5">Cập nhật: {p.updated}</p>
                </div>
                <div className="flex gap-1.5">
                  <button className="p-1.5 hover:bg-blue-50 rounded text-blue-500"><Edit2 size={13} /></button>
                  <button className="p-1.5 hover:bg-red-50 rounded text-red-500"><Trash2 size={13} /></button>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-3 text-center text-xs mt-4">
                <div className="bg-slate-50 rounded-lg py-2">
                  <p className="font-bold text-slate-800 text-base">{p.totalCredits}</p>
                  <p className="text-slate-500">Tổng TC</p>
                </div>
                <div className="bg-blue-50 rounded-lg py-2">
                  <p className="font-bold text-blue-700 text-base">{p.mandatory}</p>
                  <p className="text-blue-500">Bắt buộc</p>
                </div>
                <div className="bg-emerald-50 rounded-lg py-2">
                  <p className="font-bold text-emerald-700 text-base">{p.elective}</p>
                  <p className="text-emerald-500">Tự chọn</p>
                </div>
              </div>
              {/* Credit progress bar */}
              <div className="mt-3">
                <div className="flex justify-between text-xs text-slate-500 mb-1">
                  <span>Tiến độ khung chương trình</span>
                  <span>{Math.round((p.mandatory / p.totalCredits) * 100)}% bắt buộc</span>
                </div>
                <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full"
                    style={{ width: `${(p.mandatory / p.totalCredits) * 100}%` }}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Semester structure */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Cấu trúc theo học kỳ — Kỹ thuật Phần mềm</CardTitle>
            <Badge variant="blue">4 HK đầu</Badge>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-slate-50">
            {semesters.map((s) => (
              <div key={s.sem} className="px-5 py-4 hover:bg-slate-50/50 transition-colors">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-slate-700 bg-blue-100 text-blue-700 px-2.5 py-0.5 rounded-md">{s.sem}</span>
                  <Badge variant="gray">{s.credits} tín chỉ</Badge>
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {s.courses.map((c) => (
                    <span key={c} className="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-full">{c}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// ===== Notifications (Admin) =====
export function AdminNotifications() {
  const [showModal, setShowModal] = useState(false)
  const notifTypes = [
    { value: 'info', label: 'Thông tin', icon: Info, color: 'text-blue-500' },
    { value: 'warning', label: 'Cảnh báo', icon: AlertTriangle, color: 'text-amber-500' },
    { value: 'success', label: 'Thành công', icon: CheckCircle, color: 'text-emerald-500' },
  ]
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Thông báo toàn trường</h1>
          <p className="text-slate-500 text-sm mt-1">Phát thông báo hệ thống đến tất cả người dùng</p>
        </div>
        <Button onClick={() => setShowModal(true)}><Megaphone size={15} />Đăng thông báo mới</Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Tổng thông báo', value: 24, icon: Bell, color: 'bg-blue-500' },
          { label: 'Chưa đọc', value: 8, icon: AlertTriangle, color: 'bg-amber-500' },
          { label: 'Đã phát hôm nay', value: 3, icon: CheckCircle, color: 'bg-emerald-500' },
        ].map((s) => {
          const Icon = s.icon
          return (
            <div key={s.label} className="bg-white rounded-xl p-4 border border-slate-100 shadow-sm flex items-center gap-4">
              <div className={`p-3 rounded-xl ${s.color}`}><Icon size={20} className="text-white" /></div>
              <div>
                <p className="text-2xl font-bold text-slate-800">{s.value}</p>
                <p className="text-xs text-slate-500">{s.label}</p>
              </div>
            </div>
          )
        })}
      </div>

      {/* Notification list */}
      <Card>
        <CardHeader><CardTitle>Lịch sử thông báo</CardTitle></CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-slate-50">
            {mockNotifications.map((n) => {
              const typeConfig = {
                info: { icon: Info, color: 'text-blue-500 bg-blue-50', badge: 'blue' as const },
                warning: { icon: AlertTriangle, color: 'text-amber-500 bg-amber-50', badge: 'yellow' as const },
                success: { icon: CheckCircle, color: 'text-emerald-500 bg-emerald-50', badge: 'green' as const },
                error: { icon: AlertTriangle, color: 'text-red-500 bg-red-50', badge: 'red' as const },
              }
              const cfg = typeConfig[n.type as keyof typeof typeConfig] ?? typeConfig.info
              const Icon = cfg.icon
              return (
                <div key={n.id} className="flex items-start gap-4 px-5 py-4 hover:bg-slate-50/50 transition-colors">
                  <div className={`p-2 rounded-lg ${cfg.color} flex-shrink-0 mt-0.5`}>
                    <Icon size={14} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2">
                      <p className="text-sm font-medium text-slate-800">{n.title}</p>
                      <Badge variant={cfg.badge}>{n.type}</Badge>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{n.message}</p>
                    <p className="text-xs text-slate-400 mt-1.5">{n.time}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Modal */}
      <Modal open={showModal} onClose={() => setShowModal(false)} title="Đăng thông báo toàn trường" size="lg"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowModal(false)}>Hủy</Button>
            <Button onClick={() => setShowModal(false)}><Megaphone size={14} />Phát thông báo</Button>
          </>
        }
      >
        <div className="space-y-4">
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Tiêu đề thông báo</label>
            <input type="text" placeholder="Nhập tiêu đề..."
              className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary" />
          </div>
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Loại thông báo</label>
            <select className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
              {notifTypes.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
            </select>
          </div>
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Gửi đến</label>
            <select className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
              <option>Tất cả người dùng</option>
              <option>Tất cả sinh viên</option>
              <option>Tất cả giảng viên</option>
              <option>Theo khoa cụ thể</option>
            </select>
          </div>
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Nội dung</label>
            <textarea rows={5} placeholder="Nhập nội dung thông báo..."
              className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary resize-none" />
          </div>
        </div>
      </Modal>
    </div>
  )
}

// ===== Reports =====
const PIE_COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']

export function AdminReports() {
  const enrollmentData = [
    { month: 'T7', newStudents: 120, dropouts: 5 },
    { month: 'T8', newStudents: 145, dropouts: 3 },
    { month: 'T9', newStudents: 210, dropouts: 8 },
    { month: 'T10', newStudents: 80, dropouts: 4 },
    { month: 'T11', newStudents: 60, dropouts: 6 },
    { month: 'T12', newStudents: 30, dropouts: 2 },
  ]
  const gpaDistribution = [
    { range: 'Xuất sắc (≥9)', value: 125 },
    { range: 'Giỏi (8-9)', value: 380 },
    { range: 'Khá (7-8)', value: 450 },
    { range: 'Trung bình (5-7)', value: 250 },
  ]
  const reportCards = [
    { label: 'Tổng sinh viên đang học', value: '1,247', growth: '+3.5%', icon: GraduationCap, color: 'bg-blue-500' },
    { label: 'Tỷ lệ tốt nghiệp đúng hạn', value: '87.4%', growth: '+2.1%', icon: CheckCircle, color: 'bg-emerald-500' },
    { label: 'GPA trung bình toàn trường', value: '7.82', growth: '+0.3', icon: TrendingUp, color: 'bg-violet-500' },
    { label: 'Lớp học đang hoạt động', value: '189', growth: '+12', icon: Layers, color: 'bg-amber-500' },
  ]

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Báo cáo Thống kê</h1>
          <p className="text-slate-500 text-sm mt-1">Báo cáo định kỳ về hoạt động đào tạo</p>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary"><Calendar size={15} />Chọn kỳ học</Button>
          <Button><Download size={15} />Xuất báo cáo</Button>
        </div>
      </div>

      {/* KPI cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {reportCards.map((r) => {
          const Icon = r.icon
          return (
            <div key={r.label} className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm hover:shadow-md transition-all">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-slate-500 font-medium">{r.label}</p>
                  <p className="text-2xl font-bold text-slate-800 mt-1">{r.value}</p>
                  <p className="text-xs text-emerald-600 font-medium mt-1">↑ {r.growth}</p>
                </div>
                <div className={`p-3 rounded-xl ${r.color}`}><Icon size={20} className="text-white" /></div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <Card className="lg:col-span-2">
          <CardHeader><CardTitle>Biến động tuyển sinh 6 tháng gần đây</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={230}>
              <BarChart data={enrollmentData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ borderRadius: 8, border: 'none', fontSize: 12 }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="newStudents" name="Tuyển mới" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="dropouts" name="Thôi học" fill="#f87171" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Phân bổ GPA sinh viên</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={230}>
              <PieChart>
                <Pie data={gpaDistribution} cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={4} dataKey="value" nameKey="range">
                  {gpaDistribution.map((_, i) => <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />)}
                </Pie>
                <Tooltip contentStyle={{ borderRadius: 8, border: 'none', fontSize: 12 }} />
                <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 11 }} />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Report table */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Tổng kết theo Khoa - HK1 2026-2027</CardTitle>
            <Button variant="secondary" size="sm"><Download size={13} />Tải Excel</Button>
          </div>
        </CardHeader>
        <Table headers={['Khoa', 'Tổng SV', 'SV Xuất sắc', 'SV Giỏi', 'SV Khá', 'GPA TB', 'Tỷ lệ đạt']}>
          {faculties.map((f) => (
            <Tr key={f.id}>
              <Td className="font-medium text-slate-800">{f.name}</Td>
              <Td className="font-semibold text-slate-700">{f.students}</Td>
              <Td className="text-emerald-600 font-semibold">{Math.round(f.students * 0.1)}</Td>
              <Td className="text-blue-600 font-semibold">{Math.round(f.students * 0.31)}</Td>
              <Td className="text-amber-600 font-semibold">{Math.round(f.students * 0.36)}</Td>
              <Td className="font-semibold text-slate-800">7.8{Math.round(Math.random() * 5)}</Td>
              <Td><Badge variant="green">94.{Math.round(Math.random() * 9)}%</Badge></Td>
            </Tr>
          ))}
        </Table>
      </Card>
    </div>
  )
}

// ===== Settings =====
export function AdminSettings() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Cài đặt Hệ thống</h1>
        <p className="text-slate-500 text-sm mt-1">Cấu hình niên khóa, kỳ học và bảo mật hệ thống</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Academic year */}
        <Card>
          <CardHeader><CardTitle>Niên khóa & Kỳ học</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-700">Niên khóa hiện tại</label>
              <select className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
                <option>2026 - 2027</option>
                <option>2025 - 2026</option>
              </select>
            </div>
            <div className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-700">Học kỳ đang hoạt động</label>
              <select className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
                <option>Học kỳ 1 (2026-2027)</option>
                <option>Học kỳ 2 (2025-2026)</option>
              </select>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <label className="block text-sm font-medium text-slate-700">Ngày bắt đầu HK</label>
                <input type="date" defaultValue="2026-09-01"
                  className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
              </div>
              <div className="space-y-1.5">
                <label className="block text-sm font-medium text-slate-700">Ngày kết thúc HK</label>
                <input type="date" defaultValue="2027-01-15"
                  className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
              </div>
            </div>
            <Button className="w-full">Lưu cấu hình học vụ</Button>
          </CardContent>
        </Card>

        {/* Security */}
        <Card>
          <CardHeader><CardTitle>Bảo mật hệ thống</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            {[
              { label: 'Yêu cầu xác thực 2 bước (2FA)', enabled: false },
              { label: 'Giới hạn đăng nhập sai (5 lần)', enabled: true },
              { label: 'Tự động đăng xuất sau 30 phút', enabled: true },
              { label: 'Ghi log hoạt động người dùng', enabled: true },
            ].map((setting) => (
              <div key={setting.label} className="flex items-center justify-between py-2">
                <span className="text-sm text-slate-700">{setting.label}</span>
                <div className={`relative w-10 h-5 rounded-full transition-colors cursor-pointer ${setting.enabled ? 'bg-blue-500' : 'bg-slate-200'}`}>
                  <div className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${setting.enabled ? 'left-5' : 'left-0.5'}`} />
                </div>
              </div>
            ))}
            <div className="pt-2 border-t border-slate-100">
              <div className="space-y-1.5">
                <label className="block text-sm font-medium text-slate-700">Mật khẩu mặc định sinh viên mới</label>
                <input type="text" defaultValue="123456"
                  className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
              </div>
            </div>
            <Button className="w-full">Cập nhật bảo mật</Button>
          </CardContent>
        </Card>

        {/* System info */}
        <Card className="lg:col-span-2">
          <CardHeader><CardTitle>Thông tin hệ thống</CardTitle></CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { label: 'Phiên bản', value: 'LMS v2.4.1' },
                { label: 'Môi trường', value: 'Production' },
                { label: 'Cập nhật lần cuối', value: '01/09/2026' },
                { label: 'Database', value: 'PostgreSQL 15' },
              ].map((info) => (
                <div key={info.label} className="bg-slate-50 rounded-xl p-4">
                  <p className="text-xs text-slate-500">{info.label}</p>
                  <p className="text-sm font-semibold text-slate-800 mt-1">{info.value}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

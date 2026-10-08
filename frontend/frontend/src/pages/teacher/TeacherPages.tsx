// Teacher supplementary pages
import { useState } from 'react'
import {
  Plus, Upload, Save, Edit2, Mail, Phone, User,
  BookOpenCheck, Clock, Calendar, Bell, CheckCircle, MapPin,
} from 'lucide-react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Table, Td, Tr } from '../../components/ui/Table'
import { Button } from '../../components/ui/Button'
import { Modal } from '../../components/ui/Modal'
import { mockClasses, mockExams, mockMaterials, mockNotifications } from '../../data/mockData'
import { useAuthStore } from '../../store/authStore'

// ===== TeacherClasses =====
export function TeacherClasses() {
  const colors = [
    'from-blue-500 to-indigo-600',
    'from-violet-500 to-purple-600',
    'from-emerald-500 to-teal-600',
    'from-amber-500 to-orange-600',
    'from-rose-500 to-pink-600',
  ]
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Lớp học của tôi</h1>
          <p className="text-slate-500 text-sm mt-1">Quản lý các lớp được phân công giảng dạy</p>
        </div>
        <Badge variant="blue">{mockClasses.filter((c) => c.status === 'active').length} lớp đang dạy</Badge>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        {mockClasses.map((cls, i) => (
          <div key={cls.id} className="bg-white rounded-xl border border-slate-100 shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden">
            <div className={`h-2 bg-gradient-to-r ${colors[i % colors.length]}`} />
            <div className="p-5">
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-semibold text-slate-800">{cls.name}</p>
                  <p className="text-xs text-slate-500 mt-0.5">{cls.code} • {cls.credits} tín chỉ</p>
                </div>
                <Badge variant={cls.status === 'active' ? 'green' : 'gray'}>
                  {cls.status === 'active' ? 'Đang dạy' : 'Kết thúc'}
                </Badge>
              </div>
              <div className="mt-4 space-y-2 text-xs text-slate-500">
                <div className="flex items-center gap-2">
                  <User size={12} />
                  <span>{cls.students} sinh viên</span>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar size={12} />
                  <span>{cls.schedule}</span>
                </div>
                <div className="flex items-center gap-2">
                  <MapPin size={12} />
                  <span>Phòng {cls.room}</span>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-slate-50 flex gap-2">
                <button className="flex-1 text-xs text-primary font-medium hover:bg-blue-50 py-1.5 rounded-lg transition-colors">
                  Xem danh sách SV
                </button>
                <button className="flex-1 text-xs text-slate-600 font-medium hover:bg-slate-50 py-1.5 rounded-lg transition-colors">
                  Nhập điểm
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// ===== TeacherMaterials =====
export function TeacherMaterials() {
  const [showModal, setShowModal] = useState(false)
  const typeIcon: Record<string, string> = { pdf: '📄', docx: '📝', mp4: '🎬', pptx: '📊' }
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Tài liệu</h1>
          <p className="text-slate-500 text-sm mt-1">Tải lên và quản lý bài giảng, giáo trình</p>
        </div>
        <Button onClick={() => setShowModal(true)}><Upload size={15} />Tải lên tài liệu</Button>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Tổng tài liệu', value: mockMaterials.length, color: 'text-blue-600', bg: 'bg-blue-50' },
          { label: 'PDF / Slide', value: mockMaterials.filter((m) => m.type === 'pdf').length, color: 'text-emerald-600', bg: 'bg-emerald-50' },
          { label: 'Video bài giảng', value: mockMaterials.filter((m) => m.type === 'mp4').length, color: 'text-violet-600', bg: 'bg-violet-50' },
        ].map((s) => (
          <div key={s.label} className={`${s.bg} rounded-xl p-4 text-center`}>
            <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{s.label}</p>
          </div>
        ))}
      </div>

      <Card>
        <CardHeader><CardTitle>Danh sách tài liệu</CardTitle></CardHeader>
        <Table headers={['Tên tài liệu', 'Môn học', 'Loại', 'Dung lượng', 'Ngày tải', 'Hành động']}>
          {mockMaterials.map((m) => (
            <Tr key={m.id}>
              <Td>
                <div className="flex items-center gap-2.5">
                  <span className="text-lg">{typeIcon[m.type] ?? '📎'}</span>
                  <span className="font-medium text-slate-800">{m.title}</span>
                </div>
              </Td>
              <Td className="text-slate-500">{m.course}</Td>
              <Td><Badge variant="gray">{m.type.toUpperCase()}</Badge></Td>
              <Td className="text-slate-500">{m.size}</Td>
              <Td className="text-slate-500">{m.uploadedAt}</Td>
              <Td>
                <div className="flex items-center gap-1.5">
                  <button className="text-xs text-blue-500 hover:underline font-medium">Xem</button>
                  <span className="text-slate-300">|</span>
                  <button className="text-xs text-red-500 hover:underline font-medium">Xóa</button>
                </div>
              </Td>
            </Tr>
          ))}
        </Table>
      </Card>

      <Modal
        open={showModal}
        onClose={() => setShowModal(false)}
        title="Tải lên tài liệu mới"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowModal(false)}>Hủy</Button>
            <Button onClick={() => setShowModal(false)}><Upload size={14} />Tải lên</Button>
          </>
        }
      >
        <div className="space-y-4">
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Tên tài liệu</label>
            <input
              type="text"
              placeholder="Nhập tên tài liệu..."
              className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
            />
          </div>
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Môn học</label>
            <select className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
              {mockClasses.map((c) => <option key={c.id}>{c.name}</option>)}
            </select>
          </div>
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Chọn file</label>
            <div className="border-2 border-dashed border-slate-200 rounded-xl p-8 text-center hover:border-primary/50 transition-colors cursor-pointer">
              <Upload size={24} className="text-slate-400 mx-auto mb-2" />
              <p className="text-sm text-slate-500">
                Kéo thả file vào đây hoặc <span className="text-primary font-medium">chọn file</span>
              </p>
              <p className="text-xs text-slate-400 mt-1">PDF, DOCX, PPTX, MP4 (tối đa 500MB)</p>
            </div>
          </div>
        </div>
      </Modal>
    </div>
  )
}

// ===== TeacherExams =====
export function TeacherExams() {
  const [showModal, setShowModal] = useState(false)
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Kiểm tra</h1>
          <p className="text-slate-500 text-sm mt-1">Tạo đề thi, quản lý ngân hàng câu hỏi</p>
        </div>
        <Button onClick={() => setShowModal(true)}><Plus size={15} />Tạo đề kiểm tra</Button>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Tổng bài kiểm tra', value: mockExams.length, variant: 'blue' as const },
          { label: 'Sắp diễn ra', value: mockExams.filter((e) => e.status === 'upcoming').length, variant: 'yellow' as const },
          { label: 'Đã hoàn thành', value: mockExams.filter((e) => e.status === 'completed').length, variant: 'green' as const },
        ].map((s) => (
          <div key={s.label} className="bg-white rounded-xl p-4 border border-slate-100 shadow-sm text-center">
            <p className="text-2xl font-bold text-slate-800">{s.value}</p>
            <Badge variant={s.variant} className="mt-1">{s.label}</Badge>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {mockExams.map((exam) => (
          <Card key={exam.id} className="hover:shadow-md transition-shadow">
            <CardContent className="p-5">
              <div className="flex items-start justify-between">
                <div>
                  <Badge
                    variant={exam.type === 'final' ? 'red' : exam.type === 'midterm' ? 'yellow' : 'blue'}
                    className="mb-2"
                  >
                    {exam.type === 'final' ? '🎓 Cuối kỳ' : exam.type === 'midterm' ? '📋 Giữa kỳ' : '⚡ Quiz'}
                  </Badge>
                  <p className="font-semibold text-slate-800">{exam.title}</p>
                  <p className="text-sm text-slate-500 mt-1">{exam.course}</p>
                </div>
                <Badge variant={exam.status === 'completed' ? 'green' : 'blue'}>
                  {exam.status === 'completed' ? 'Hoàn thành' : 'Sắp diễn ra'}
                </Badge>
              </div>
              <div className="mt-3 pt-3 border-t border-slate-50 grid grid-cols-2 gap-2 text-xs text-slate-500">
                <div className="flex items-center gap-1.5">
                  <Calendar size={12} />
                  <span>{exam.date}</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Clock size={12} />
                  <span>{exam.duration} phút</span>
                </div>
              </div>
              {exam.status === 'completed' && exam.score != null && (
                <div className="mt-3 bg-emerald-50 rounded-lg px-3 py-2 text-xs text-emerald-700 flex items-center gap-1.5">
                  <CheckCircle size={12} />
                  <span>Điểm trung bình lớp: <strong>{exam.score}/100</strong></span>
                </div>
              )}
              <div className="mt-3 flex gap-2">
                <button className="flex-1 text-xs text-primary font-medium hover:bg-blue-50 py-1.5 rounded-lg transition-colors border border-blue-100">
                  Xem đề
                </button>
                <button className="flex-1 text-xs text-slate-600 font-medium hover:bg-slate-50 py-1.5 rounded-lg transition-colors border border-slate-100">
                  Kết quả
                </button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Modal
        open={showModal}
        onClose={() => setShowModal(false)}
        title="Tạo đề kiểm tra mới"
        size="lg"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowModal(false)}>Hủy</Button>
            <Button onClick={() => setShowModal(false)}>Tạo đề kiểm tra</Button>
          </>
        }
      >
        <div className="space-y-4">
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Tên bài kiểm tra</label>
            <input
              type="text"
              placeholder="VD: Kiểm tra giữa kỳ - Lập trình Web..."
              className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-700">Môn học</label>
              <select className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
                {mockClasses.map((c) => <option key={c.id}>{c.name}</option>)}
              </select>
            </div>
            <div className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-700">Loại kiểm tra</label>
              <select className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
                <option value="quiz">Quiz</option>
                <option value="midterm">Giữa kỳ</option>
                <option value="final">Cuối kỳ</option>
              </select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-700">Ngày kiểm tra</label>
              <input
                type="date"
                className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
              />
            </div>
            <div className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-700">Thời gian (phút)</label>
              <input
                type="number"
                defaultValue={60}
                min={15}
                max={180}
                className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
              />
            </div>
          </div>
          <div className="space-y-1.5">
            <label className="block text-sm font-medium text-slate-700">Ghi chú cho sinh viên</label>
            <textarea
              rows={3}
              placeholder="Hướng dẫn, quy định khi làm bài..."
              className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 resize-none"
            />
          </div>
        </div>
      </Modal>
    </div>
  )
}

// ===== TeacherNotifications =====
export function TeacherNotifications() {
  const [sent, setSent] = useState(false)
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Đăng thông báo</h1>
          <p className="text-slate-500 text-sm mt-1">Gửi thông báo cho sinh viên trong lớp</p>
        </div>
        <Badge variant="blue">{mockClasses.filter((c) => c.status === 'active').length} lớp đang dạy</Badge>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card>
            <CardHeader><CardTitle>Soạn thông báo mới</CardTitle></CardHeader>
            <CardContent>
              {sent ? (
                <div className="text-center py-8">
                  <div className="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-3">
                    <CheckCircle size={28} className="text-emerald-500" />
                  </div>
                  <p className="font-semibold text-slate-800">Thông báo đã được gửi!</p>
                  <p className="text-sm text-slate-500 mt-1">Sinh viên sẽ nhận được thông báo trong vài giây.</p>
                  <Button className="mt-4" variant="secondary" onClick={() => setSent(false)}>
                    Soạn thông báo khác
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="block text-sm font-medium text-slate-700">Tiêu đề thông báo</label>
                    <input
                      type="text"
                      placeholder="Nhập tiêu đề..."
                      className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="block text-sm font-medium text-slate-700">Gửi đến lớp</label>
                    <select className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30">
                      <option value="">-- Tất cả các lớp --</option>
                      {mockClasses.map((c) => (
                        <option key={c.id}>{c.name} ({c.students} SV)</option>
                      ))}
                    </select>
                  </div>
                  <div className="space-y-1.5">
                    <label className="block text-sm font-medium text-slate-700">Loại thông báo</label>
                    <div className="flex gap-2 flex-wrap">
                      {[
                        { value: 'info', label: 'Thông tin', color: 'text-blue-600 bg-blue-50 border-blue-200' },
                        { value: 'warning', label: 'Cảnh báo', color: 'text-amber-600 bg-amber-50 border-amber-200' },
                        { value: 'success', label: 'Tích cực', color: 'text-emerald-600 bg-emerald-50 border-emerald-200' },
                      ].map((t) => (
                        <label
                          key={t.value}
                          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium cursor-pointer ${t.color}`}
                        >
                          <input type="radio" name="notif-type" value={t.value} className="w-3 h-3" defaultChecked={t.value === 'info'} />
                          {t.label}
                        </label>
                      ))}
                    </div>
                  </div>
                  <div className="space-y-1.5">
                    <label className="block text-sm font-medium text-slate-700">Nội dung</label>
                    <textarea
                      rows={5}
                      placeholder="Nhập nội dung thông báo..."
                      className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary resize-none"
                    />
                  </div>
                  <Button onClick={() => setSent(true)} className="w-full">
                    Gửi thông báo
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader><CardTitle>Thông báo gần đây</CardTitle></CardHeader>
          <CardContent className="p-0">
            <div className="divide-y divide-slate-50">
              {mockNotifications.slice(0, 4).map((n) => (
                <div key={n.id} className="px-4 py-3 hover:bg-slate-50/50 transition-colors">
                  <p className="text-xs font-medium text-slate-800 line-clamp-1">{n.title}</p>
                  <p className="text-xs text-slate-400 mt-0.5">{n.time}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

// ===== TeacherProfile =====
const profileSchema = z.object({
  name: z.string().min(2, 'Tên phải có ít nhất 2 ký tự'),
  email: z.string().email('Email không hợp lệ'),
  phone: z.string().optional(),
  department: z.string().optional(),
  specialization: z.string().optional(),
  bio: z.string().optional(),
})
type ProfileForm = z.infer<typeof profileSchema>

export function TeacherProfile() {
  const { user } = useAuthStore()
  const [editing, setEditing] = useState(false)

  const { register, handleSubmit, formState: { errors } } = useForm<ProfileForm>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      name: user?.name ?? '',
      email: user?.email ?? '',
      phone: '0912 345 678',
      department: user?.department ?? 'Khoa Công nghệ Thông tin',
      specialization: 'Lập trình Web, Phát triển phần mềm',
      bio: 'Giảng viên với hơn 8 năm kinh nghiệm giảng dạy và nghiên cứu trong lĩnh vực công nghệ thông tin.',
    },
  })

  const onSubmit = (_data: ProfileForm) => {
    setEditing(false)
  }

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Hồ sơ Giảng viên</h1>
          <p className="text-slate-500 text-sm mt-1">Thông tin cá nhân và chuyên môn</p>
        </div>
        <Button variant={editing ? 'secondary' : 'primary'} onClick={() => setEditing(!editing)}>
          <Edit2 size={15} />
          {editing ? 'Hủy chỉnh sửa' : 'Chỉnh sửa'}
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Avatar card */}
        <Card>
          <CardContent className="flex flex-col items-center text-center py-8 px-5">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-2xl font-bold">
              {user?.name?.split(' ').map((n) => n[0]).slice(-2).join('') ?? 'GV'}
            </div>
            <h2 className="text-lg font-bold text-slate-800 mt-4">{user?.name}</h2>
            <p className="text-slate-500 text-sm">{user?.email}</p>
            <Badge variant="blue" className="mt-2">Giảng viên</Badge>
            <div className="mt-6 w-full space-y-3 text-left">
              <div className="flex items-center gap-2.5 text-sm text-slate-600">
                <User size={14} className="text-slate-400" />
                <span>Mã GV: <strong>GV002</strong></span>
              </div>
              <div className="flex items-center gap-2.5 text-sm text-slate-600">
                <BookOpenCheck size={14} className="text-slate-400" />
                <span>Khoa: <strong>CNTT</strong></span>
              </div>
              <div className="flex items-center gap-2.5 text-sm text-slate-600">
                <Calendar size={14} className="text-slate-400" />
                <span>Vào trường: <strong>2018</strong></span>
              </div>
            </div>
            <div className="mt-6 grid grid-cols-2 gap-3 w-full text-center text-xs">
              <div className="bg-blue-50 rounded-xl py-3">
                <p className="text-xl font-bold text-blue-700">3</p>
                <p className="text-blue-500">Lớp đang dạy</p>
              </div>
              <div className="bg-emerald-50 rounded-xl py-3">
                <p className="text-xl font-bold text-emerald-700">125</p>
                <p className="text-emerald-500">Sinh viên</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Info form */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader><CardTitle>Thông tin cá nhân</CardTitle></CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="block text-sm font-medium text-slate-700">Họ và tên</label>
                    <div className="relative">
                      <User size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                      <input
                        {...register('name')}
                        disabled={!editing}
                        className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-lg text-sm disabled:bg-slate-50 disabled:text-slate-600 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
                      />
                    </div>
                    {errors.name && <p className="text-xs text-red-500">{errors.name.message}</p>}
                  </div>
                  <div className="space-y-1.5">
                    <label className="block text-sm font-medium text-slate-700">Email</label>
                    <div className="relative">
                      <Mail size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                      <input
                        {...register('email')}
                        disabled={!editing}
                        className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-lg text-sm disabled:bg-slate-50 disabled:text-slate-600 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
                      />
                    </div>
                    {errors.email && <p className="text-xs text-red-500">{errors.email.message}</p>}
                  </div>
                  <div className="space-y-1.5">
                    <label className="block text-sm font-medium text-slate-700">Số điện thoại</label>
                    <div className="relative">
                      <Phone size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                      <input
                        {...register('phone')}
                        disabled={!editing}
                        className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-lg text-sm disabled:bg-slate-50 disabled:text-slate-600 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
                      />
                    </div>
                  </div>
                  <div className="space-y-1.5">
                    <label className="block text-sm font-medium text-slate-700">Khoa công tác</label>
                    <input
                      {...register('department')}
                      disabled={!editing}
                      className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm disabled:bg-slate-50 disabled:text-slate-600 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
                    />
                  </div>
                </div>
                <div className="space-y-1.5">
                  <label className="block text-sm font-medium text-slate-700">Chuyên môn</label>
                  <input
                    {...register('specialization')}
                    disabled={!editing}
                    className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm disabled:bg-slate-50 disabled:text-slate-600 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="block text-sm font-medium text-slate-700">Giới thiệu bản thân</label>
                  <textarea
                    {...register('bio')}
                    disabled={!editing}
                    rows={3}
                    className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm disabled:bg-slate-50 disabled:text-slate-600 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary resize-none"
                  />
                </div>
                {editing && (
                  <div className="flex gap-2 pt-1">
                    <Button type="submit"><Save size={15} />Lưu thay đổi</Button>
                    <Button type="button" variant="secondary" onClick={() => setEditing(false)}>Hủy</Button>
                  </div>
                )}
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

// ===== TeacherSettings =====
export function TeacherSettings() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Cài đặt tài khoản</h1>
        <p className="text-slate-500 text-sm mt-1">Quản lý mật khẩu và tuỳ chọn thông báo</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader><CardTitle>Đổi mật khẩu</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            {['Mật khẩu hiện tại', 'Mật khẩu mới', 'Xác nhận mật khẩu mới'].map((label) => (
              <div key={label} className="space-y-1.5">
                <label className="block text-sm font-medium text-slate-700">{label}</label>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
                />
              </div>
            ))}
            <Button className="w-full">Cập nhật mật khẩu</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Tuỳ chọn thông báo</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            {[
              { label: 'Thông báo khi SV nộp bài tập', enabled: true },
              { label: 'Nhắc nhở lịch dạy qua email', enabled: true },
              { label: 'Thông báo khi có điểm phúc khảo', enabled: false },
              { label: 'Bản tin định kỳ từ nhà trường', enabled: true },
              { label: 'Thông báo đẩy trên trình duyệt', enabled: false },
            ].map((s) => (
              <div key={s.label} className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <Bell size={14} className="text-slate-400" />
                  <span className="text-sm text-slate-700">{s.label}</span>
                </div>
                <div
                  className={`relative w-10 h-5 rounded-full transition-colors cursor-pointer ${s.enabled ? 'bg-blue-500' : 'bg-slate-200'}`}
                >
                  <div
                    className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform ${s.enabled ? 'left-5' : 'left-0.5'}`}
                  />
                </div>
              </div>
            ))}
            <Button className="w-full mt-2">Lưu cài đặt</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

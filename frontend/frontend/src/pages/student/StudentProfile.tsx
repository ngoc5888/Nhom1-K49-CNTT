import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Save, Edit2, User, Mail, Phone, Calendar, MapPin, BookOpen } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Avatar } from '../../components/ui/Avatar'
import { Button } from '../../components/ui/Button'
import { useAuthStore } from '../../store/authStore'

const profileSchema = z.object({
  name: z.string().min(2, 'Tên phải có ít nhất 2 ký tự'),
  email: z.string().email('Email không hợp lệ'),
  phone: z.string().optional(),
  address: z.string().optional(),
})
type ProfileForm = z.infer<typeof profileSchema>

export function StudentProfile() {
  const { user } = useAuthStore()
  const [editing, setEditing] = useState(false)

  const { register, handleSubmit, formState: { errors } } = useForm<ProfileForm>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      name: user?.name ?? '',
      email: user?.email ?? '',
      phone: '0901 234 567',
      address: 'Hà Nội, Việt Nam',
    },
  })

  const onSubmit = (data: ProfileForm) => {
    console.log('Profile updated:', data)
    setEditing(false)
  }

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Hồ sơ cá nhân</h1>
          <p className="text-slate-500 text-sm mt-1">Thông tin tài khoản và hồ sơ học tập</p>
        </div>
        <Button
          variant={editing ? 'secondary' : 'primary'}
          onClick={() => setEditing(!editing)}
        >
          <Edit2 size={15} />
          {editing ? 'Hủy chỉnh sửa' : 'Chỉnh sửa'}
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Avatar Card */}
        <Card>
          <CardContent className="flex flex-col items-center text-center py-8">
            <Avatar name={user?.name ?? 'User'} size="xl" />
            <h2 className="text-lg font-bold text-slate-800 mt-4">{user?.name}</h2>
            <p className="text-slate-500 text-sm">{user?.email}</p>
            <Badge variant="green" className="mt-2">Sinh viên</Badge>

            <div className="mt-6 w-full space-y-3 text-left">
              <div className="flex items-center gap-2.5 text-sm text-slate-600">
                <User size={14} className="text-slate-400" />
                <span>Mã SV: <strong>SV003</strong></span>
              </div>
              <div className="flex items-center gap-2.5 text-sm text-slate-600">
                <BookOpen size={14} className="text-slate-400" />
                <span>Lớp: <strong>CNTT-K22A</strong></span>
              </div>
              <div className="flex items-center gap-2.5 text-sm text-slate-600">
                <Calendar size={14} className="text-slate-400" />
                <span>Năm học: <strong>2022 - 2026</strong></span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Info Form */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Thông tin cá nhân</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="block text-sm font-medium text-slate-700">Họ và tên</label>
                    <div className="relative">
                      <User size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                      <input
                        {...register('name')}
                        disabled={!editing}
                        className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-lg text-sm disabled:bg-slate-50 disabled:text-slate-600 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
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
                        className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-lg text-sm disabled:bg-slate-50 disabled:text-slate-600 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
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
                        className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-lg text-sm disabled:bg-slate-50 disabled:text-slate-600 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
                      />
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="block text-sm font-medium text-slate-700">Địa chỉ</label>
                    <div className="relative">
                      <MapPin size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                      <input
                        {...register('address')}
                        disabled={!editing}
                        className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-lg text-sm disabled:bg-slate-50 disabled:text-slate-600 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
                      />
                    </div>
                  </div>
                </div>

                {editing && (
                  <div className="flex gap-2 pt-2">
                    <Button type="submit" variant="primary">
                      <Save size={15} />
                      Lưu thay đổi
                    </Button>
                    <Button type="button" variant="secondary" onClick={() => setEditing(false)}>
                      Hủy
                    </Button>
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

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { GraduationCap, Lock, User, Eye, EyeOff, Shield, BookOpen, Users } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import type { UserRole } from '../../types'

const loginSchema = z.object({
  username: z.string().min(1, 'Vui lòng nhập tài khoản'),
  password: z.string().min(1, 'Vui lòng nhập mật khẩu'),
  remember: z.boolean().optional(),
})

type LoginForm = z.infer<typeof loginSchema>

const dashboardByRole: Record<UserRole, string> = {
  ADMIN: '/admin/dashboard',
  TEACHER: '/teacher/dashboard',
  STUDENT: '/student/dashboard',
}

const demoAccounts: { role: UserRole; label: string; username: string; icon: typeof Shield; color: string }[] = [
  { role: 'ADMIN', label: 'Quản trị viên', username: 'admin', icon: Shield, color: 'from-violet-500 to-purple-600' },
  { role: 'TEACHER', label: 'Giảng viên', username: 'teacher', icon: BookOpen, color: 'from-blue-500 to-indigo-600' },
  { role: 'STUDENT', label: 'Sinh viên', username: 'student', icon: Users, color: 'from-emerald-500 to-teal-600' },
]

export function LoginPage() {
  const { login, loginAs } = useAuthStore()
  const navigate = useNavigate()
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const { register, handleSubmit, setValue, formState: { errors } } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: { remember: false },
  })

  const onSubmit = async (data: LoginForm) => {
    setLoading(true)
    setError('')
    try {
      const success = await login(data.username, data.password)
      if (success) {
        const { user } = useAuthStore.getState()
        navigate(dashboardByRole[user!.role])
      } else {
        setError('Tài khoản hoặc mật khẩu không đúng. Mật khẩu mặc định: 123456')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleQuickLogin = (role: UserRole) => {
    loginAs(role)
    navigate(dashboardByRole[role])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-indigo-950 flex items-center justify-center p-4">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-violet-500/5 rounded-full blur-3xl" />
      </div>

      <div className="relative w-full max-w-md">
        {/* Logo & Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 shadow-lg shadow-blue-500/30 mb-4">
            <GraduationCap size={32} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold text-white leading-tight">
            HỆ THỐNG QUẢN LÝ HỌC TẬP
          </h1>
          <p className="text-slate-400 text-sm mt-1">Learning Management System</p>
        </div>

        {/* Login Card */}
        <div className="bg-white/[0.07] backdrop-blur-xl rounded-2xl border border-white/10 shadow-2xl p-8">
          <h2 className="text-white font-semibold text-lg mb-6 text-center">ĐĂNG NHẬP</h2>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {/* Username */}
            <div className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-300">Tài khoản</label>
              <div className="relative">
                <User size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  {...register('username')}
                  id="username"
                  type="text"
                  placeholder="Nhập tài khoản..."
                  autoComplete="username"
                  className="w-full pl-9 pr-3 py-2.5 bg-white/10 border border-white/20 rounded-lg text-white placeholder:text-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-400 transition-colors"
                />
              </div>
              {errors.username && (
                <p className="text-red-400 text-xs">{errors.username.message}</p>
              )}
            </div>

            {/* Password */}
            <div className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-300">Mật khẩu</label>
              <div className="relative">
                <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  {...register('password')}
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Nhập mật khẩu..."
                  autoComplete="current-password"
                  className="w-full pl-9 pr-10 py-2.5 bg-white/10 border border-white/20 rounded-lg text-white placeholder:text-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-400 transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300 transition-colors"
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              {errors.password && (
                <p className="text-red-400 text-xs">{errors.password.message}</p>
              )}
            </div>

            {/* Remember + Forgot */}
            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  {...register('remember')}
                  id="remember"
                  type="checkbox"
                  className="w-4 h-4 rounded border-white/20 bg-white/10 text-blue-500 focus:ring-blue-500/30"
                />
                <span className="text-slate-300 text-sm">Ghi nhớ đăng nhập</span>
              </label>
              <button type="button" className="text-sm text-blue-400 hover:text-blue-300 transition-colors">
                Quên mật khẩu?
              </button>
            </div>

            {/* Error */}
            {error && (
              <div className="bg-red-500/10 border border-red-500/20 rounded-lg px-3 py-2.5">
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              id="login-submit"
              disabled={loading}
              className="w-full py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold rounded-lg transition-all duration-200 shadow-lg shadow-blue-500/25 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
              ) : null}
              ĐĂNG NHẬP
            </button>
          </form>

          {/* Divider */}
          <div className="flex items-center gap-3 my-6">
            <div className="flex-1 border-t border-white/10" />
            <span className="text-slate-500 text-xs">Đăng nhập nhanh Demo</span>
            <div className="flex-1 border-t border-white/10" />
          </div>

          {/* Quick Login */}
          <div className="grid grid-cols-3 gap-2.5">
            {demoAccounts.map(({ role, label, username, icon: Icon, color }) => (
              <button
                key={role}
                id={`quick-login-${role.toLowerCase()}`}
                onClick={() => handleQuickLogin(role)}
                className="group flex flex-col items-center gap-1.5 p-3 rounded-xl border border-white/10 hover:border-white/20 hover:bg-white/10 transition-all duration-200"
              >
                <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${color} flex items-center justify-center group-hover:scale-110 transition-transform`}>
                  <Icon size={16} className="text-white" />
                </div>
                <span className="text-slate-400 text-xs font-medium group-hover:text-slate-300 text-center leading-tight">
                  {label}
                </span>
                <span className="text-slate-600 text-[10px]">{username}</span>
              </button>
            ))}
          </div>
        </div>

        <p className="text-center text-slate-600 text-xs mt-6">
          © 2026 LMS System. Hệ thống Quản lý Học tập.
        </p>
      </div>
    </div>
  )
}

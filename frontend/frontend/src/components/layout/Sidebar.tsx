import { Link, useLocation } from 'react-router-dom'
import {
  LayoutDashboard, BookOpen, FileText, ClipboardList, GraduationCap, BarChart2,
  User, Bell, Users, Layers, School, BookMarked, Settings, LogOut, ChevronDown,
  ChevronRight, BookOpenCheck, Calendar, Award, Building2, Briefcase, Database,
  PieChart, Megaphone, FileBarChart, ClipboardCheck, Upload, Book, HomeIcon,
} from 'lucide-react'
import { cn } from '../../lib/utils'
import { useAuthStore } from '../../store/authStore'
import type { UserRole } from '../../types'
import { useState } from 'react'

interface NavItem {
  label: string
  href: string
  icon: React.ElementType
}

interface NavGroup {
  groupLabel?: string
  items: NavItem[]
}

const studentNav: NavGroup[] = [
  {
    items: [
      { label: 'Sổ tay hướng dẫn', href: '/student/handbook', icon: Book },
    ],
  },
  {
    groupLabel: 'TỔNG QUAN',
    items: [
      { label: 'Tổng quan', href: '/student/dashboard', icon: LayoutDashboard },
    ],
  },
  {
    groupLabel: 'HỌC TẬP',
    items: [
      { label: 'Lớp học', href: '/student/classes', icon: School },
      { label: 'Tài liệu', href: '/student/materials', icon: FileText },
      { label: 'Bài tập', href: '/student/assignments', icon: ClipboardList },
      { label: 'Kiểm tra', href: '/student/exams', icon: BookOpenCheck },
      { label: 'Kết quả học tập', href: '/student/results', icon: BarChart2 },
    ],
  },
  {
    groupLabel: 'CÁ NHÂN',
    items: [
      { label: 'Hồ sơ', href: '/student/profile', icon: User },
      { label: 'Thông báo', href: '/student/notifications', icon: Bell },
    ],
  },
]

const teacherNav: NavGroup[] = [
  {
    groupLabel: 'TỔNG QUAN',
    items: [
      { label: 'Dashboard', href: '/teacher/dashboard', icon: LayoutDashboard },
    ],
  },
  {
    groupLabel: 'QUẢN LÝ GIẢNG DẠY',
    items: [
      { label: 'Lớp học', href: '/teacher/classes', icon: School },
      { label: 'Sinh viên', href: '/teacher/students', icon: Users },
      { label: 'Tài liệu', href: '/teacher/materials', icon: Upload },
      { label: 'Bài tập', href: '/teacher/assignments', icon: ClipboardList },
      { label: 'Kiểm tra', href: '/teacher/exams', icon: BookOpenCheck },
      { label: 'Điểm', href: '/teacher/grades', icon: Award },
    ],
  },
  {
    groupLabel: 'QUẢN LÝ',
    items: [
      { label: 'Thông báo', href: '/teacher/notifications', icon: Megaphone },
      { label: 'Lịch học', href: '/teacher/schedule', icon: Calendar },
    ],
  },
  {
    groupLabel: 'CÁ NHÂN',
    items: [
      { label: 'Hồ sơ', href: '/teacher/profile', icon: User },
      { label: 'Cài đặt', href: '/teacher/settings', icon: Settings },
    ],
  },
]

const adminNav: NavGroup[] = [
  {
    groupLabel: 'TỔNG QUAN',
    items: [
      { label: 'Dashboard', href: '/admin/dashboard', icon: LayoutDashboard },
    ],
  },
  {
    groupLabel: 'QUẢN LÝ NGƯỜI DÙNG',
    items: [
      { label: 'Sinh viên', href: '/admin/students', icon: GraduationCap },
      { label: 'Giảng viên', href: '/admin/teachers', icon: Users },
      { label: 'Tài khoản', href: '/admin/accounts', icon: User },
    ],
  },
  {
    groupLabel: 'QUẢN LÝ ĐÀO TẠO',
    items: [
      { label: 'Khoa', href: '/admin/faculties', icon: Building2 },
      { label: 'Ngành', href: '/admin/majors', icon: Briefcase },
      { label: 'Lớp', href: '/admin/classes', icon: Layers },
      { label: 'Môn học', href: '/admin/courses', icon: BookOpen },
    ],
  },
  {
    groupLabel: 'QUẢN LÝ HỆ THỐNG',
    items: [
      { label: 'Nội dung học tập', href: '/admin/curriculum', icon: Database },
      { label: 'Thông báo', href: '/admin/notifications', icon: Megaphone },
      { label: 'Báo cáo', href: '/admin/reports', icon: FileBarChart },
      { label: 'Cài đặt', href: '/admin/settings', icon: Settings },
    ],
  },
]

const navByRole: Record<UserRole, NavGroup[]> = {
  STUDENT: studentNav,
  TEACHER: teacherNav,
  ADMIN: adminNav,
}

export function Sidebar() {
  const { user, logout } = useAuthStore()
  const location = useLocation()

  if (!user) return null

  const navGroups = navByRole[user.role]

  return (
    <aside className="w-64 min-h-screen bg-slate-900 flex flex-col border-r border-slate-800 flex-shrink-0">
      {/* Logo */}
      <div className="px-5 py-5 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center flex-shrink-0">
            <GraduationCap size={20} className="text-white" />
          </div>
          <div>
            <p className="text-white font-bold text-sm leading-tight">Hệ thống LMS</p>
            <p className="text-slate-400 text-xs">Quản lý Học tập</p>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        {navGroups.map((group, gi) => (
          <div key={gi} className="space-y-0.5">
            {group.groupLabel && (
              <p className="px-3 pt-3 pb-1 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                {group.groupLabel}
              </p>
            )}
            {group.items.map((item) => {
              const isActive = location.pathname === item.href ||
                (item.href !== '/' && location.pathname.startsWith(item.href))
              const Icon = item.icon
              return (
                <Link
                  key={item.href}
                  to={item.href}
                  className={cn(
                    'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                    isActive
                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/25'
                      : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                  )}
                >
                  <Icon size={17} className="flex-shrink-0" />
                  <span className="truncate">{item.label}</span>
                </Link>
              )
            })}
          </div>
        ))}
      </nav>

      {/* Logout */}
      <div className="px-3 py-4 border-t border-slate-800">
        <button
          onClick={logout}
          className="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm font-medium text-slate-400 hover:bg-red-900/30 hover:text-red-400 transition-all duration-200"
        >
          <LogOut size={17} />
          <span>Đăng xuất</span>
        </button>
      </div>
    </aside>
  )
}

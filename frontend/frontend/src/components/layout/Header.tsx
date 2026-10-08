import { useState, useRef, useEffect } from 'react'
import { Bell, ChevronDown, LogOut, User, Settings } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { Avatar } from '../ui/Avatar'
import { Badge } from '../ui/Badge'
import { mockNotifications } from '../../data/mockData'
import { cn } from '../../lib/utils'

const roleLabelMap = {
  ADMIN: { label: 'Quản trị viên', variant: 'red' as const },
  TEACHER: { label: 'Giảng viên', variant: 'blue' as const },
  STUDENT: { label: 'Sinh viên', variant: 'green' as const },
}

export function Header() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [showNotif, setShowNotif] = useState(false)
  const [showUser, setShowUser] = useState(false)
  const notifRef = useRef<HTMLDivElement>(null)
  const userRef = useRef<HTMLDivElement>(null)

  const unreadCount = mockNotifications.filter((n) => !n.read).length
  const roleInfo = user ? roleLabelMap[user.role] : null

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (notifRef.current && !notifRef.current.contains(e.target as Node)) setShowNotif(false)
      if (userRef.current && !userRef.current.contains(e.target as Node)) setShowUser(false)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const profileLink = user
    ? `/${user.role.toLowerCase()}/profile`
    : '/login'

  return (
    <header className="h-16 bg-white border-b border-slate-100 flex items-center justify-between px-6 flex-shrink-0 z-30">
      {/* Left */}
      <div className="flex items-center gap-3">
        <h1 className="text-slate-700 font-semibold text-sm hidden md:block">
          HỆ THỐNG QUẢN LÝ HỌC TẬP
        </h1>
        {roleInfo && (
          <Badge variant={roleInfo.variant}>{roleInfo.label}</Badge>
        )}
      </div>

      {/* Right */}
      <div className="flex items-center gap-2">
        {/* Notification Bell */}
        <div className="relative" ref={notifRef}>
          <button
            onClick={() => { setShowNotif(!showNotif); setShowUser(false) }}
            className="relative p-2 rounded-lg hover:bg-slate-100 transition-colors text-slate-600"
          >
            <Bell size={20} />
            {unreadCount > 0 && (
              <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 text-white text-[10px] rounded-full flex items-center justify-center font-bold">
                {unreadCount}
              </span>
            )}
          </button>

          {showNotif && (
            <div className="absolute right-0 top-12 w-80 bg-white rounded-xl shadow-xl border border-slate-100 z-50 animate-fade-in overflow-hidden">
              <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
                <span className="font-semibold text-slate-800 text-sm">Thông báo</span>
                {unreadCount > 0 && (
                  <Badge variant="red">{unreadCount} mới</Badge>
                )}
              </div>
              <div className="max-h-80 overflow-y-auto divide-y divide-slate-50">
                {mockNotifications.slice(0, 5).map((n) => (
                  <div
                    key={n.id}
                    className={cn(
                      'px-4 py-3 hover:bg-slate-50 transition-colors cursor-pointer',
                      !n.read && 'bg-blue-50/50'
                    )}
                  >
                    <div className="flex items-start gap-2">
                      {!n.read && (
                        <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-1.5 flex-shrink-0" />
                      )}
                      <div className={cn(!n.read ? '' : 'ml-3.5')}>
                        <p className="text-sm font-medium text-slate-800 leading-tight">{n.title}</p>
                        <p className="text-xs text-slate-500 mt-0.5 line-clamp-2">{n.message}</p>
                        <p className="text-xs text-slate-400 mt-1">{n.time}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="px-4 py-2.5 border-t border-slate-100 text-center">
                <Link
                  to={`/${user?.role.toLowerCase()}/notifications`}
                  className="text-xs text-primary hover:underline font-medium"
                  onClick={() => setShowNotif(false)}
                >
                  Xem tất cả thông báo
                </Link>
              </div>
            </div>
          )}
        </div>

        {/* User Menu */}
        <div className="relative" ref={userRef}>
          <button
            onClick={() => { setShowUser(!showUser); setShowNotif(false) }}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-slate-100 transition-colors"
          >
            <Avatar name={user?.name ?? 'User'} size="sm" />
            <div className="text-left hidden sm:block">
              <p className="text-sm font-medium text-slate-700 leading-tight">{user?.name}</p>
              <p className="text-xs text-slate-400">{user?.email}</p>
            </div>
            <ChevronDown size={14} className="text-slate-400" />
          </button>

          {showUser && (
            <div className="absolute right-0 top-12 w-52 bg-white rounded-xl shadow-xl border border-slate-100 z-50 animate-fade-in overflow-hidden">
              <div className="px-4 py-3 border-b border-slate-100">
                <p className="text-sm font-semibold text-slate-800">{user?.name}</p>
                <p className="text-xs text-slate-500">{user?.email}</p>
              </div>
              <div className="py-1">
                <Link
                  to={profileLink}
                  className="flex items-center gap-2.5 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                  onClick={() => setShowUser(false)}
                >
                  <User size={15} />
                  <span>Hồ sơ cá nhân</span>
                </Link>
                {user?.role !== 'STUDENT' && (
                  <Link
                    to={`/${user?.role.toLowerCase()}/settings`}
                    className="flex items-center gap-2.5 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                    onClick={() => setShowUser(false)}
                  >
                    <Settings size={15} />
                    <span>Cài đặt</span>
                  </Link>
                )}
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-2.5 w-full px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors"
                >
                  <LogOut size={15} />
                  <span>Đăng xuất</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}

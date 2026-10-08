import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import type { UserRole } from '../../types'

interface ProtectedRouteProps {
  allowedRole: UserRole
}

const dashboardByRole: Record<UserRole, string> = {
  ADMIN: '/admin/dashboard',
  TEACHER: '/teacher/dashboard',
  STUDENT: '/student/dashboard',
}

export function ProtectedRoute({ allowedRole }: ProtectedRouteProps) {
  const { user, isAuthenticated } = useAuthStore()

  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />
  }

  if (user.role !== allowedRole) {
    return <Navigate to={dashboardByRole[user.role]} replace />
  }

  return <Outlet />
}

export function PublicRoute() {
  const { user, isAuthenticated } = useAuthStore()

  if (isAuthenticated && user) {
    return <Navigate to={dashboardByRole[user.role]} replace />
  }

  return <Outlet />
}

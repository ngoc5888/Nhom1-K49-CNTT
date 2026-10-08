import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User, UserRole, AuthState } from '../types'

const MOCK_USERS: Record<string, User> = {
  admin: {
    id: '1',
    username: 'admin',
    name: 'Nguyễn Quản Trị',
    email: 'admin@lms.edu.vn',
    role: 'ADMIN',
    avatar: 'NT',
  },
  teacher: {
    id: '2',
    username: 'teacher',
    name: 'Trần Văn Giảng',
    email: 'teacher@lms.edu.vn',
    role: 'TEACHER',
    avatar: 'TG',
    department: 'Khoa Công nghệ Thông tin',
  },
  student: {
    id: '3',
    username: 'student',
    name: 'Lê Thị Sinh Viên',
    email: 'student@lms.edu.vn',
    role: 'STUDENT',
    avatar: 'SV',
  },
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,

      login: async (username: string, password: string): Promise<boolean> => {
        // Mock auth
        if (password === '123456' && MOCK_USERS[username]) {
          set({ user: MOCK_USERS[username], isAuthenticated: true })
          return true
        }
        return false
      },

      loginAs: (role: UserRole) => {
        const userMap: Record<UserRole, User> = {
          ADMIN: MOCK_USERS.admin,
          TEACHER: MOCK_USERS.teacher,
          STUDENT: MOCK_USERS.student,
        }
        set({ user: userMap[role], isAuthenticated: true })
      },

      logout: () => {
        set({ user: null, isAuthenticated: false })
      },
    }),
    {
      name: 'lms-auth',
    }
  )
)

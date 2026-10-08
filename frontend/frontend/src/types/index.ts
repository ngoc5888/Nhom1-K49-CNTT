export type UserRole = 'ADMIN' | 'TEACHER' | 'STUDENT'

export interface User {
  id: string
  username: string
  name: string
  email: string
  role: UserRole
  avatar?: string
  department?: string
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<boolean>
  loginAs: (role: UserRole) => void
  logout: () => void
}

export interface NavItem {
  label: string
  href: string
  icon?: string
  children?: NavItem[]
}

export interface NavGroup {
  groupLabel?: string
  items: NavItem[]
}

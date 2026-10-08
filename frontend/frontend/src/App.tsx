import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ProtectedRoute, PublicRoute } from './components/auth/ProtectedRoute'
import { DashboardLayout } from './components/layout/DashboardLayout'

// Auth
import { LoginPage } from './pages/auth/LoginPage'

// Admin
import { AdminDashboard } from './pages/admin/AdminDashboard'
import { AdminStudents } from './pages/admin/AdminStudents'
import {
  AdminTeachers,
  AdminAccounts,
  AdminFaculties,
  AdminMajors,
  AdminClasses,
  AdminCourses,
  AdminCurriculum,
  AdminNotifications,
  AdminReports,
  AdminSettings,
} from './pages/admin/AdminPages'

// Teacher
import { TeacherDashboard } from './pages/teacher/TeacherDashboard'
import { TeacherStudents } from './pages/teacher/TeacherStudents'
import { TeacherAssignments } from './pages/teacher/TeacherAssignments'
import { TeacherGrades } from './pages/teacher/TeacherGrades'
import { TeacherSchedule } from './pages/teacher/TeacherSchedule'
import {
  TeacherClasses,
  TeacherMaterials,
  TeacherExams,
  TeacherNotifications,
  TeacherProfile,
  TeacherSettings,
} from './pages/teacher/TeacherPages'

// Student
import { StudentDashboard } from './pages/student/StudentDashboard'
import { StudentHandbook } from './pages/student/StudentHandbook'
import { StudentClasses } from './pages/student/StudentClasses'
import { StudentMaterials } from './pages/student/StudentMaterials'
import { StudentAssignments } from './pages/student/StudentAssignments'
import { StudentExams } from './pages/student/StudentExams'
import { StudentResults } from './pages/student/StudentResults'
import { StudentProfile } from './pages/student/StudentProfile'
import { StudentNotifications } from './pages/student/StudentNotifications'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route element={<PublicRoute />}>
          <Route path="/login" element={<LoginPage />} />
        </Route>

        {/* Admin routes */}
        <Route element={<ProtectedRoute allowedRole="ADMIN" />}>
          <Route element={<DashboardLayout />}>
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/students" element={<AdminStudents />} />
            <Route path="/admin/teachers" element={<AdminTeachers />} />
            <Route path="/admin/accounts" element={<AdminAccounts />} />
            <Route path="/admin/faculties" element={<AdminFaculties />} />
            <Route path="/admin/majors" element={<AdminMajors />} />
            <Route path="/admin/classes" element={<AdminClasses />} />
            <Route path="/admin/courses" element={<AdminCourses />} />
            <Route path="/admin/curriculum" element={<AdminCurriculum />} />
            <Route path="/admin/notifications" element={<AdminNotifications />} />
            <Route path="/admin/reports" element={<AdminReports />} />
            <Route path="/admin/settings" element={<AdminSettings />} />
          </Route>
        </Route>

        {/* Teacher routes */}
        <Route element={<ProtectedRoute allowedRole="TEACHER" />}>
          <Route element={<DashboardLayout />}>
            <Route path="/teacher/dashboard" element={<TeacherDashboard />} />
            <Route path="/teacher/classes" element={<TeacherClasses />} />
            <Route path="/teacher/students" element={<TeacherStudents />} />
            <Route path="/teacher/materials" element={<TeacherMaterials />} />
            <Route path="/teacher/assignments" element={<TeacherAssignments />} />
            <Route path="/teacher/exams" element={<TeacherExams />} />
            <Route path="/teacher/grades" element={<TeacherGrades />} />
            <Route path="/teacher/notifications" element={<TeacherNotifications />} />
            <Route path="/teacher/schedule" element={<TeacherSchedule />} />
            <Route path="/teacher/profile" element={<TeacherProfile />} />
            <Route path="/teacher/settings" element={<TeacherSettings />} />
          </Route>
        </Route>

        {/* Student routes */}
        <Route element={<ProtectedRoute allowedRole="STUDENT" />}>
          <Route element={<DashboardLayout />}>
            <Route path="/student/handbook" element={<StudentHandbook />} />
            <Route path="/student/dashboard" element={<StudentDashboard />} />
            <Route path="/student/classes" element={<StudentClasses />} />
            <Route path="/student/materials" element={<StudentMaterials />} />
            <Route path="/student/assignments" element={<StudentAssignments />} />
            <Route path="/student/exams" element={<StudentExams />} />
            <Route path="/student/results" element={<StudentResults />} />
            <Route path="/student/profile" element={<StudentProfile />} />
            <Route path="/student/notifications" element={<StudentNotifications />} />
          </Route>
        </Route>

        {/* Fallback */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

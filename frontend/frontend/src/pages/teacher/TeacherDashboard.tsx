import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts'
import { School, Users, ClipboardCheck, BookOpenCheck, TrendingUp, Clock } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Avatar } from '../../components/ui/Avatar'
import { mockClasses, mockStudents, teacherAssignmentData, teacherDashboardStats, mockAssignments } from '../../data/mockData'
import { useAuthStore } from '../../store/authStore'

function StatCard({ label, value, icon: Icon, color, sub }: {
  label: string; value: string | number; icon: React.ElementType; color: string; sub?: string
}) {
  return (
    <div className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm hover:shadow-md transition-all duration-200">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-500 font-medium">{label}</p>
          <p className="text-3xl font-bold text-slate-800 mt-1">{value}</p>
          {sub && <p className="text-xs text-slate-400 mt-1">{sub}</p>}
        </div>
        <div className={`p-3 rounded-xl ${color}`}>
          <Icon size={22} className="text-white" />
        </div>
      </div>
    </div>
  )
}

export function TeacherDashboard() {
  const { user } = useAuthStore()

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">
          Xin chào, {user?.name}! 👋
        </h1>
        <p className="text-slate-500 text-sm mt-1">Tổng quan hoạt động giảng dạy của bạn</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Lớp phụ trách" value={teacherDashboardStats.totalClasses} icon={School} color="bg-blue-500" sub="Học kỳ hiện tại" />
        <StatCard label="Tổng sinh viên" value={teacherDashboardStats.totalStudents} icon={Users} color="bg-emerald-500" sub="Các lớp đang dạy" />
        <StatCard label="Bài tập chờ chấm" value={teacherDashboardStats.pendingGrading} icon={ClipboardCheck} color="bg-amber-500" sub="Cần xử lý sớm" />
        <StatCard label="Bài thi sắp diễn ra" value={teacherDashboardStats.upcomingExams} icon={BookOpenCheck} color="bg-violet-500" sub="Trong 2 tuần tới" />
      </div>

      {/* Chart + Recent Classes */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Thống kê bài tập nộp / chấm theo tuần</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={230}>
              <BarChart data={teacherAssignmentData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="week" tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.1)', fontSize: 12 }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="submitted" name="Đã nộp" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="graded" name="Đã chấm" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* My Classes */}
        <Card>
          <CardHeader>
            <CardTitle>Lớp đang phụ trách</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="divide-y divide-slate-50">
              {mockClasses.slice(0, 4).map((cls) => (
                <div key={cls.id} className="px-5 py-3.5 hover:bg-slate-50/50 transition-colors">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-slate-800 leading-tight">{cls.name}</p>
                      <p className="text-xs text-slate-500 mt-0.5">{cls.students} SV • {cls.schedule}</p>
                    </div>
                    <Badge variant={cls.status === 'active' ? 'green' : 'gray'}>
                      {cls.status === 'active' ? 'Đang dạy' : 'Kết thúc'}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent students */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Sinh viên gần đây</CardTitle>
            <button className="text-xs text-primary hover:underline font-medium">Xem tất cả</button>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-slate-50">
            {mockStudents.slice(0, 5).map((s) => (
              <div key={s.id} className="flex items-center justify-between px-5 py-3.5 hover:bg-slate-50/50 transition-colors">
                <div className="flex items-center gap-3">
                  <Avatar name={s.name} size="sm" />
                  <div>
                    <p className="text-sm font-medium text-slate-800">{s.name}</p>
                    <p className="text-xs text-slate-500">{s.class}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-slate-800">GPA: {s.gpa}</p>
                  <Badge variant={s.status === 'active' ? 'green' : 'gray'}>
                    {s.status === 'active' ? 'Đang học' : 'Bảo lưu'}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

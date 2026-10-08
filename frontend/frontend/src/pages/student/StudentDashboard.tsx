import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend,
} from 'recharts'
import {
  BookOpen, ClipboardList, TrendingUp, CheckCircle, Clock, AlertCircle, BookOpenCheck, Star,
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import {
  studentDashboardStats, gpaChartData, mockAssignments, mockExams, mockClasses,
} from '../../data/mockData'
import { useAuthStore } from '../../store/authStore'
import { formatDate } from '../../lib/utils'

function StatCard({ label, value, icon: Icon, color, sub }: {
  label: string; value: string | number; icon: React.ElementType; color: string; sub?: string
}) {
  return (
    <div className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm hover:shadow-md transition-all duration-200 hover:-translate-y-0.5">
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

export function StudentDashboard() {
  const { user } = useAuthStore()
  const pendingAssignments = mockAssignments.filter((a) => a.status === 'pending')
  const upcomingExams = mockExams.filter((e) => e.status === 'upcoming').slice(0, 3)

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      {/* Greeting */}
      <div>
        <h1 className="text-2xl font-bold text-slate-800">
          Xin chào, {user?.name?.split(' ').pop()}! 👋
        </h1>
        <p className="text-slate-500 text-sm mt-1">
          Chào mừng trở lại hệ thống quản lý học tập.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Lớp đã đăng ký"
          value={studentDashboardStats.enrolledClasses}
          icon={BookOpen}
          color="bg-blue-500"
          sub="Học kỳ 1 - 2026"
        />
        <StatCard
          label="Bài tập cần nộp"
          value={studentDashboardStats.pendingAssignments}
          icon={ClipboardList}
          color="bg-amber-500"
          sub="Trong tuần này"
        />
        <StatCard
          label="Tiến độ hoàn thành"
          value={`${studentDashboardStats.completionRate}%`}
          icon={TrendingUp}
          color="bg-emerald-500"
          sub="Tổng các môn học"
        />
        <StatCard
          label="GPA Tích lũy"
          value={studentDashboardStats.gpa}
          icon={Star}
          color="bg-violet-500"
          sub="Thang điểm 10"
        />
      </div>

      {/* Charts + Assignments */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* GPA Chart */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Biểu đồ GPA theo kỳ học</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={gpaChartData}>
                <defs>
                  <linearGradient id="gpaGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="semester" tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} />
                <YAxis domain={[6, 10]} tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.1)', fontSize: 12 }}
                  formatter={(val) => [Number(val).toFixed(1), 'GPA']}
                />
                <Area
                  type="monotone"
                  dataKey="gpa"
                  stroke="#3b82f6"
                  strokeWidth={2.5}
                  fill="url(#gpaGrad)"
                  dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Upcoming Exams */}
        <Card>
          <CardHeader>
            <CardTitle>Lịch kiểm tra sắp tới</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="divide-y divide-slate-50">
              {upcomingExams.map((exam) => (
                <div key={exam.id} className="px-5 py-3.5 hover:bg-slate-50/50 transition-colors">
                  <p className="text-sm font-medium text-slate-800 leading-tight">{exam.title}</p>
                  <p className="text-xs text-slate-500 mt-0.5">{exam.course}</p>
                  <div className="flex items-center justify-between mt-2">
                    <div className="flex items-center gap-1 text-xs text-slate-400">
                      <Clock size={12} />
                      <span>{formatDate(exam.date)} • {exam.duration} phút</span>
                    </div>
                    <Badge variant={exam.type === 'final' ? 'red' : exam.type === 'midterm' ? 'yellow' : 'blue'}>
                      {exam.type === 'final' ? 'Cuối kỳ' : exam.type === 'midterm' ? 'Giữa kỳ' : 'Quiz'}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Pending Assignments */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Bài tập cần hoàn thành</CardTitle>
            <Badge variant="yellow">{pendingAssignments.length} chưa nộp</Badge>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-slate-50">
            {mockAssignments.map((a) => {
              const statusMap = {
                pending: { label: 'Chưa làm', variant: 'yellow' as const, icon: Clock },
                submitted: { label: 'Đã nộp', variant: 'green' as const, icon: CheckCircle },
                overdue: { label: 'Quá hạn', variant: 'red' as const, icon: AlertCircle },
              }
              const st = statusMap[a.status as keyof typeof statusMap]
              const Icon = st.icon
              return (
                <div key={a.id} className="px-5 py-4 hover:bg-slate-50/50 transition-colors flex items-center justify-between">
                  <div className="flex items-start gap-3">
                    <div className={`p-1.5 rounded-lg mt-0.5 ${a.status === 'overdue' ? 'bg-red-100' : a.status === 'submitted' ? 'bg-emerald-100' : 'bg-amber-100'}`}>
                      <Icon size={14} className={a.status === 'overdue' ? 'text-red-600' : a.status === 'submitted' ? 'text-emerald-600' : 'text-amber-600'} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-slate-800">{a.title}</p>
                      <p className="text-xs text-slate-500 mt-0.5">{a.course} • Hạn: {formatDate(a.dueDate)}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    {a.score !== null && (
                      <span className="text-sm font-semibold text-slate-700">{a.score}/{a.maxScore}</span>
                    )}
                    <Badge variant={st.variant}>{st.label}</Badge>
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

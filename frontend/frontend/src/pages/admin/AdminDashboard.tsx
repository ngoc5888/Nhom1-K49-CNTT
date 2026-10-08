import {
  LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from 'recharts'
import { Users, GraduationCap, BookOpen, Layers, TrendingUp, School } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import {
  adminDashboardStats, adminUserGrowthData, classDistributionData, mockClasses, mockTeachers,
} from '../../data/mockData'

const PIE_COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']

function StatCard({ label, value, icon: Icon, color, sub, growth }: {
  label: string; value: string | number; icon: React.ElementType; color: string; sub?: string; growth?: string
}) {
  return (
    <div className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm hover:shadow-md transition-all duration-200 hover:-translate-y-0.5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-500 font-medium">{label}</p>
          <p className="text-3xl font-bold text-slate-800 mt-1">{value.toLocaleString()}</p>
          {sub && <p className="text-xs text-slate-400 mt-1">{sub}</p>}
          {growth && (
            <p className="text-xs text-emerald-600 font-medium mt-1">↑ {growth} so với tháng trước</p>
          )}
        </div>
        <div className={`p-3 rounded-xl ${color}`}>
          <Icon size={22} className="text-white" />
        </div>
      </div>
    </div>
  )
}

export function AdminDashboard() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Dashboard Quản trị viên</h1>
        <p className="text-slate-500 text-sm mt-1">Tổng quan toàn bộ hệ thống đào tạo</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <StatCard label="Tổng Sinh viên" value={adminDashboardStats.totalStudents} icon={GraduationCap} color="bg-blue-500" growth="3.5%" />
        <StatCard label="Giảng viên" value={adminDashboardStats.totalTeachers} icon={Users} color="bg-violet-500" />
        <StatCard label="Môn học" value={adminDashboardStats.totalCourses} icon={BookOpen} color="bg-emerald-500" />
        <StatCard label="Tổng lớp học" value={adminDashboardStats.totalClasses} icon={Layers} color="bg-amber-500" />
        <StatCard label="Lớp đang hoạt động" value={adminDashboardStats.activeClasses} icon={School} color="bg-rose-500" sub={`/${adminDashboardStats.totalClasses} tổng`} />
        <StatCard label="SV mới tháng này" value={adminDashboardStats.newStudentsThisMonth} icon={TrendingUp} color="bg-cyan-500" />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Biến động Người dùng (9 tháng gần nhất)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={adminUserGrowthData}>
                <defs>
                  <linearGradient id="svGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gvGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.25} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.1)', fontSize: 12 }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Area type="monotone" dataKey="students" name="Sinh viên" stroke="#3b82f6" strokeWidth={2} fill="url(#svGrad)" dot={{ r: 3 }} />
                <Area type="monotone" dataKey="teachers" name="Giảng viên" stroke="#10b981" strokeWidth={2} fill="url(#gvGrad)" dot={{ r: 3 }} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Phân bổ lớp học theo Khoa</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie
                  data={classDistributionData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {classDistributionData.map((_, index) => (
                    <Cell key={index} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ borderRadius: 8, border: 'none', fontSize: 12 }} />
                <Legend
                  iconType="circle"
                  iconSize={8}
                  wrapperStyle={{ fontSize: 11, paddingTop: 8 }}
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent Classes + Teachers */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Lớp học đang hoạt động</CardTitle>
              <Badge variant="green">{mockClasses.filter((c) => c.status === 'active').length} đang dạy</Badge>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <div className="divide-y divide-slate-50">
              {mockClasses.slice(0, 4).map((cls) => (
                <div key={cls.id} className="flex items-center justify-between px-5 py-3.5 hover:bg-slate-50/50 transition-colors">
                  <div>
                    <p className="text-sm font-medium text-slate-800">{cls.name}</p>
                    <p className="text-xs text-slate-500 mt-0.5">{cls.teacher} • {cls.students} SV</p>
                  </div>
                  <Badge variant={cls.status === 'active' ? 'green' : 'gray'}>
                    {cls.status === 'active' ? 'Đang dạy' : 'Kết thúc'}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Danh sách Giảng viên</CardTitle>
              <Badge variant="blue">{mockTeachers.length} giảng viên</Badge>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <div className="divide-y divide-slate-50">
              {mockTeachers.slice(0, 4).map((t) => (
                <div key={t.id} className="flex items-center justify-between px-5 py-3.5 hover:bg-slate-50/50 transition-colors">
                  <div>
                    <p className="text-sm font-medium text-slate-800">{t.name}</p>
                    <p className="text-xs text-slate-500 mt-0.5">{t.department} • {t.subject}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold text-slate-700">{t.classes} lớp</p>
                    <p className="text-xs text-slate-400">{t.students} SV</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

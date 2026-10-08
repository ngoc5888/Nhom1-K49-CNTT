import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts'
import { Award, TrendingUp, BookOpen } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Table, Td, Tr } from '../../components/ui/Table'
import { mockGrades } from '../../data/mockData'

const gradeVariant = (g: string | null) => {
  if (!g) return 'gray' as const
  if (g.startsWith('A')) return 'green' as const
  if (g.startsWith('B')) return 'blue' as const
  if (g.startsWith('C')) return 'yellow' as const
  return 'red' as const
}

const radarData = mockGrades
  .filter((g) => g.average !== null)
  .map((g) => ({ subject: g.code, score: g.average! }))

const barData = mockGrades
  .filter((g) => g.midterm !== null)
  .map((g) => ({ name: g.code, 'Giữa kỳ': g.midterm, 'Cuối kỳ': g.final ?? 0 }))

export function StudentResults() {
  const completedGrades = mockGrades.filter((g) => g.average !== null)
  const gpa10 = completedGrades.reduce((s, g) => s + g.average! * g.credits, 0) /
    completedGrades.reduce((s, g) => s + g.credits, 0)

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Kết quả học tập</h1>
        <p className="text-slate-500 text-sm mt-1">Bảng điểm chi tiết và thống kê GPA</p>
      </div>

      {/* GPA Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl p-5 text-white shadow-lg shadow-blue-500/25">
          <p className="text-blue-100 text-sm font-medium">GPA Tích lũy (thang 10)</p>
          <p className="text-4xl font-bold mt-1">{gpa10.toFixed(2)}</p>
          <p className="text-blue-200 text-xs mt-1">Xếp loại: Giỏi</p>
        </div>
        <div className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-emerald-100 rounded-xl">
            <BookOpen size={22} className="text-emerald-600" />
          </div>
          <div>
            <p className="text-sm text-slate-500">Tổng tín chỉ tích lũy</p>
            <p className="text-2xl font-bold text-slate-800">
              {completedGrades.reduce((s, g) => s + g.credits, 0)}
            </p>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 border border-slate-100 shadow-sm flex items-center gap-4">
          <div className="p-3 bg-amber-100 rounded-xl">
            <Award size={22} className="text-amber-600" />
          </div>
          <div>
            <p className="text-sm text-slate-500">Môn đạt điểm A</p>
            <p className="text-2xl font-bold text-slate-800">
              {completedGrades.filter((g) => g.grade?.startsWith('A')).length}
            </p>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <Card>
          <CardHeader><CardTitle>Biểu đồ điểm thành phần</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} />
                <YAxis domain={[0, 10]} tick={{ fontSize: 11, fill: '#94a3b8' }} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.1)', fontSize: 12 }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Bar dataKey="Giữa kỳ" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Cuối kỳ" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Phân bổ điểm các môn</CardTitle></CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={220}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11, fill: '#64748b' }} />
                <PolarRadiusAxis domain={[0, 10]} tick={{ fontSize: 10 }} />
                <Radar name="Điểm" dataKey="score" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.25} />
              </RadarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Grade Table */}
      <Card>
        <CardHeader><CardTitle>Bảng điểm chi tiết</CardTitle></CardHeader>
        <Table headers={['Môn học', 'Mã môn', 'Tín chỉ', 'Điểm GK', 'Điểm CK', 'Điểm TK', 'Xếp loại']}>
          {mockGrades.map((g) => (
            <Tr key={g.code}>
              <Td className="font-medium text-slate-800">{g.course}</Td>
              <Td className="text-slate-500">{g.code}</Td>
              <Td className="text-slate-600">{g.credits}</Td>
              <Td>{g.midterm !== null ? g.midterm : '-'}</Td>
              <Td>{g.final !== null ? g.final : <span className="text-slate-400 text-xs">Chưa có</span>}</Td>
              <Td>
                {g.average !== null ? (
                  <span className="font-semibold text-slate-800">{g.average.toFixed(1)}</span>
                ) : (
                  <span className="text-slate-400 text-xs">—</span>
                )}
              </Td>
              <Td>
                {g.grade ? (
                  <Badge variant={gradeVariant(g.grade)}>{g.grade}</Badge>
                ) : (
                  <span className="text-slate-400 text-xs">Chưa xếp</span>
                )}
              </Td>
            </Tr>
          ))}
        </Table>
      </Card>
    </div>
  )
}

import { Clock, CheckCircle, AlertCircle, Upload } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Table, Td, Tr } from '../../components/ui/Table'
import { mockAssignments } from '../../data/mockData'
import { formatDate } from '../../lib/utils'

const statusConfig = {
  pending: { label: 'Chưa làm', variant: 'yellow' as const, icon: Clock, bg: 'bg-amber-100 text-amber-700' },
  submitted: { label: 'Đã nộp', variant: 'green' as const, icon: CheckCircle, bg: 'bg-emerald-100 text-emerald-700' },
  overdue: { label: 'Quá hạn', variant: 'red' as const, icon: AlertCircle, bg: 'bg-red-100 text-red-700' },
}

export function StudentAssignments() {
  const counts = {
    pending: mockAssignments.filter((a) => a.status === 'pending').length,
    submitted: mockAssignments.filter((a) => a.status === 'submitted').length,
    overdue: mockAssignments.filter((a) => a.status === 'overdue').length,
  }

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Bài tập</h1>
        <p className="text-slate-500 text-sm mt-1">Danh sách bài tập theo các môn học</p>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-3 gap-4">
        {Object.entries(counts).map(([key, count]) => {
          const cfg = statusConfig[key as keyof typeof statusConfig]
          const Icon = cfg.icon
          return (
            <div key={key} className="bg-white rounded-xl p-4 border border-slate-100 shadow-sm flex items-center gap-4">
              <div className={`p-3 rounded-xl ${cfg.bg}`}>
                <Icon size={20} />
              </div>
              <div>
                <p className="text-2xl font-bold text-slate-800">{count}</p>
                <p className="text-sm text-slate-500">{cfg.label}</p>
              </div>
            </div>
          )
        })}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Tất cả bài tập</CardTitle>
        </CardHeader>
        <Table headers={['Tên bài tập', 'Môn học', 'Hạn nộp', 'Điểm', 'Trạng thái', 'Hành động']}>
          {mockAssignments.map((a) => {
            const cfg = statusConfig[a.status as keyof typeof statusConfig]
            return (
              <Tr key={a.id}>
                <Td>
                  <p className="font-medium text-slate-800">{a.title}</p>
                  <p className="text-xs text-slate-400">Điểm tối đa: {a.maxScore}</p>
                </Td>
                <Td className="text-slate-600">{a.course}</Td>
                <Td>
                  <div className="flex items-center gap-1.5 text-slate-600">
                    <Clock size={13} className={a.status === 'overdue' ? 'text-red-500' : ''} />
                    <span className={a.status === 'overdue' ? 'text-red-600 font-medium' : ''}>{formatDate(a.dueDate)}</span>
                  </div>
                </Td>
                <Td>
                  {a.score !== null ? (
                    <span className="font-semibold text-slate-800">{a.score}/{a.maxScore}</span>
                  ) : (
                    <span className="text-slate-400 text-xs">Chưa chấm</span>
                  )}
                </Td>
                <Td>
                  <Badge variant={cfg.variant}>{cfg.label}</Badge>
                </Td>
                <Td>
                  {a.status === 'pending' && (
                    <button className="flex items-center gap-1.5 text-xs text-primary hover:text-primary/80 font-medium transition-colors">
                      <Upload size={13} />
                      Nộp bài
                    </button>
                  )}
                  {a.status === 'submitted' && (
                    <span className="text-xs text-emerald-600 font-medium">✓ Đã nộp</span>
                  )}
                  {a.status === 'overdue' && (
                    <span className="text-xs text-red-600">Quá hạn</span>
                  )}
                </Td>
              </Tr>
            )
          })}
        </Table>
      </Card>
    </div>
  )
}

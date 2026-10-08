import { useState } from 'react'
import { Plus, CheckCircle, Clock, AlertCircle, Star } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Avatar } from '../../components/ui/Avatar'
import { Table, Td, Tr } from '../../components/ui/Table'
import { Button } from '../../components/ui/Button'
import { Modal } from '../../components/ui/Modal'
import { mockAssignments, mockStudents } from '../../data/mockData'
import { formatDate } from '../../lib/utils'

export function TeacherAssignments() {
  const [gradingModal, setGradingModal] = useState(false)
  const [selectedAssignment, setSelectedAssignment] = useState<(typeof mockAssignments)[0] | null>(null)

  const submissions = mockStudents.slice(0, 6).map((s, i) => ({
    student: s,
    submittedAt: '2026-09-25',
    score: i % 3 === 0 ? null : Math.floor(75 + Math.random() * 20),
    status: i % 3 === 0 ? 'pending' : 'graded',
  }))

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Bài tập</h1>
          <p className="text-slate-500 text-sm mt-1">Tạo, theo dõi và chấm điểm bài tập</p>
        </div>
        <Button>
          <Plus size={15} />
          Tạo bài tập mới
        </Button>
      </div>

      <Card>
        <CardHeader><CardTitle>Danh sách bài tập đã giao</CardTitle></CardHeader>
        <Table headers={['Bài tập', 'Môn học', 'Hạn nộp', 'Đã nộp', 'Điểm tối đa', 'Hành động']}>
          {mockAssignments.map((a) => (
            <Tr key={a.id}>
              <Td>
                <p className="font-medium text-slate-800">{a.title}</p>
              </Td>
              <Td className="text-slate-500">{a.course}</Td>
              <Td>
                <div className="flex items-center gap-1.5">
                  <Clock size={13} className="text-slate-400" />
                  <span className="text-slate-600">{formatDate(a.dueDate)}</span>
                </div>
              </Td>
              <Td>
                <span className="text-slate-700 font-medium">
                  {a.status === 'submitted' ? '1' : '0'}/{mockStudents.length}
                </span>
              </Td>
              <Td className="text-slate-600">{a.maxScore}</Td>
              <Td>
                <button
                  onClick={() => { setSelectedAssignment(a); setGradingModal(true) }}
                  className="flex items-center gap-1.5 text-xs text-primary hover:text-primary/80 font-medium transition-colors"
                >
                  <Star size={13} />
                  Chấm điểm
                </button>
              </Td>
            </Tr>
          ))}
        </Table>
      </Card>

      {/* Grading Modal */}
      <Modal
        open={gradingModal}
        onClose={() => setGradingModal(false)}
        title={`Chấm điểm: ${selectedAssignment?.title}`}
        size="lg"
        footer={
          <>
            <Button variant="secondary" onClick={() => setGradingModal(false)}>Đóng</Button>
            <Button>Lưu điểm</Button>
          </>
        }
      >
        <div className="space-y-3">
          {submissions.map((sub, i) => (
            <div key={i} className="flex items-center justify-between py-2.5 border-b border-slate-50 last:border-0">
              <div className="flex items-center gap-3">
                <Avatar name={sub.student.name} size="sm" />
                <div>
                  <p className="text-sm font-medium text-slate-800">{sub.student.name}</p>
                  <p className="text-xs text-slate-500">Nộp lúc: {formatDate(sub.submittedAt)}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                {sub.status === 'graded' ? (
                  <div className="flex items-center gap-1.5">
                    <CheckCircle size={14} className="text-emerald-500" />
                    <span className="text-sm font-semibold text-slate-800">{sub.score}/100</span>
                  </div>
                ) : (
                  <input
                    type="number"
                    min={0}
                    max={selectedAssignment?.maxScore ?? 100}
                    placeholder="Nhập điểm"
                    className="w-24 px-3 py-1.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30"
                  />
                )}
                <Badge variant={sub.status === 'graded' ? 'green' : 'yellow'}>
                  {sub.status === 'graded' ? 'Đã chấm' : 'Chờ chấm'}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </Modal>
    </div>
  )
}

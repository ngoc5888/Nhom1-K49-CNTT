import { Clock, Play, CheckCircle } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { mockExams } from '../../data/mockData'
import { formatDate } from '../../lib/utils'

const typeLabel = { quiz: 'Quiz', midterm: 'Giữa kỳ', final: 'Cuối kỳ' }
const typeVariant = { quiz: 'blue', midterm: 'yellow', final: 'red' } as const

export function StudentExams() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Kiểm tra & Thi</h1>
        <p className="text-slate-500 text-sm mt-1">Danh sách bài thi, quiz và bài kiểm tra</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {mockExams.map((exam) => (
          <div
            key={exam.id}
            className="bg-white rounded-xl border border-slate-100 shadow-sm hover:shadow-md transition-all duration-200 p-5"
          >
            <div className="flex items-start justify-between mb-3">
              <Badge variant={typeVariant[exam.type as keyof typeof typeVariant]}>
                {typeLabel[exam.type as keyof typeof typeLabel]}
              </Badge>
              <Badge variant={exam.status === 'completed' ? 'green' : 'blue'}>
                {exam.status === 'completed' ? 'Đã hoàn thành' : 'Sắp diễn ra'}
              </Badge>
            </div>

            <h3 className="font-semibold text-slate-800 text-base leading-tight">{exam.title}</h3>
            <p className="text-sm text-slate-500 mt-1">{exam.course}</p>

            <div className="mt-4 space-y-2">
              <div className="flex items-center justify-between text-sm text-slate-600">
                <div className="flex items-center gap-1.5">
                  <Clock size={14} />
                  <span>Ngày thi: {formatDate(exam.date)}</span>
                </div>
                <span className="text-slate-500">{exam.duration} phút</span>
              </div>
            </div>

            {exam.status === 'completed' && exam.score !== undefined && (
              <div className="mt-4 pt-4 border-t border-slate-50 flex items-center justify-between">
                <div className="flex items-center gap-1.5 text-emerald-600">
                  <CheckCircle size={16} />
                  <span className="text-sm font-medium">Kết quả: {exam.score}/100</span>
                </div>
                <button className="text-xs text-primary hover:underline font-medium">Xem chi tiết</button>
              </div>
            )}

            {exam.status === 'upcoming' && (
              <div className="mt-4 pt-4 border-t border-slate-50">
                <button className="w-full flex items-center justify-center gap-2 py-2 bg-primary/10 hover:bg-primary/20 text-primary text-sm font-medium rounded-lg transition-colors">
                  <Play size={14} />
                  Vào phòng thi
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

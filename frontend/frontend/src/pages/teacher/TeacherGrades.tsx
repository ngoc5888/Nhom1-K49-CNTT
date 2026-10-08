import { Download, Save } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Avatar } from '../../components/ui/Avatar'
import { Button } from '../../components/ui/Button'
import { mockStudents } from '../../data/mockData'

const gradeData = mockStudents.map((s, i) => ({
  ...s,
  midterm: (6.5 + i * 0.3) % 10 + 0.5,
  lab: (7 + i * 0.2) % 10 + 0.5,
  final: (7.5 + i * 0.25) % 10,
  average: ((6.5 + i * 0.3) % 10 + 0.5 + (7 + i * 0.2) % 10 + 0.5 + (7.5 + i * 0.25) % 10) / 3,
}))

function getLetterGrade(avg: number) {
  if (avg >= 9) return { g: 'A', v: 'green' as const }
  if (avg >= 8) return { g: 'B+', v: 'blue' as const }
  if (avg >= 7) return { g: 'B', v: 'blue' as const }
  if (avg >= 6) return { g: 'C+', v: 'yellow' as const }
  if (avg >= 5) return { g: 'C', v: 'yellow' as const }
  return { g: 'F', v: 'red' as const }
}

export function TeacherGrades() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Nhập điểm</h1>
          <p className="text-slate-500 text-sm mt-1">Bảng điểm chi tiết theo từng sinh viên</p>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary">
            <Download size={15} />
            Xuất Excel
          </Button>
          <Button>
            <Save size={15} />
            Lưu điểm
          </Button>
        </div>
      </div>

      <div className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 text-sm text-amber-800">
        ⚠️ <strong>Lưu ý:</strong> Bạn đang nhập điểm cho lớp <strong>Lập trình Web Nâng cao (IT4023)</strong>. Vui lòng kiểm tra kỹ trước khi lưu.
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Bảng điểm - IT4023 ({gradeData.length} sinh viên)</CardTitle>
        </CardHeader>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr>
                {['Sinh viên', 'Mã SV', 'Điểm GK (30%)', 'Điểm Lab (20%)', 'Điểm CK (50%)', 'Điểm TB', 'Xếp loại'].map((h) => (
                  <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider bg-slate-50 border-b border-slate-100">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {gradeData.map((g) => {
                const { g: letterGrade, v: variant } = getLetterGrade(g.average)
                return (
                  <tr key={g.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2.5">
                        <Avatar name={g.name} size="sm" />
                        <span className="font-medium text-slate-800">{g.name}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-slate-500 font-mono text-xs">{g.id}</td>
                    {[g.midterm, g.lab, g.final].map((score, i) => (
                      <td key={i} className="px-4 py-3">
                        <input
                          type="number"
                          defaultValue={score.toFixed(1)}
                          min={0}
                          max={10}
                          step={0.1}
                          className="w-20 px-2 py-1 border border-slate-200 rounded-lg text-sm text-center focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
                        />
                      </td>
                    ))}
                    <td className="px-4 py-3">
                      <span className="font-semibold text-slate-800">{g.average.toFixed(1)}</span>
                    </td>
                    <td className="px-4 py-3">
                      <Badge variant={variant}>{letterGrade}</Badge>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}

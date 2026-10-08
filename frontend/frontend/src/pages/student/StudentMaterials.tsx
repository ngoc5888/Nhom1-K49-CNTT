import { FileText, Download, File, Video, FileType } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Table, Td, Tr } from '../../components/ui/Table'
import { mockMaterials } from '../../data/mockData'
import { formatDate } from '../../lib/utils'

const typeIconMap: Record<string, { icon: React.ElementType; color: string; badge: 'red' | 'blue' | 'yellow' | 'gray' }> = {
  pdf: { icon: FileText, color: 'text-red-500 bg-red-50', badge: 'red' },
  docx: { icon: File, color: 'text-blue-500 bg-blue-50', badge: 'blue' },
  mp4: { icon: Video, color: 'text-purple-500 bg-purple-50', badge: 'purple' as any },
  pptx: { icon: FileType, color: 'text-amber-500 bg-amber-50', badge: 'yellow' },
}

export function StudentMaterials() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Tài liệu học tập</h1>
        <p className="text-slate-500 text-sm mt-1">Slide bài giảng, tài liệu tham khảo từ giảng viên</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Danh sách tài liệu ({mockMaterials.length})</CardTitle>
        </CardHeader>
        <Table headers={['Tài liệu', 'Môn học', 'Giảng viên', 'Loại', 'Dung lượng', 'Ngày đăng', 'Tải về']}>
          {mockMaterials.map((m) => {
            const typeInfo = typeIconMap[m.type] ?? { icon: File, color: 'text-gray-500 bg-gray-50', badge: 'gray' as const }
            const Icon = typeInfo.icon
            return (
              <Tr key={m.id}>
                <Td>
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${typeInfo.color}`}>
                      <Icon size={16} />
                    </div>
                    <span className="font-medium text-slate-800">{m.title}</span>
                  </div>
                </Td>
                <Td className="text-slate-500">{m.course}</Td>
                <Td className="text-slate-500">{m.teacher}</Td>
                <Td>
                  <Badge variant={typeInfo.badge}>{m.type.toUpperCase()}</Badge>
                </Td>
                <Td className="text-slate-500">{m.size}</Td>
                <Td className="text-slate-500">{formatDate(m.uploadedAt)}</Td>
                <Td>
                  <button className="flex items-center gap-1.5 text-primary hover:text-primary/80 text-sm font-medium transition-colors">
                    <Download size={14} />
                    Tải xuống
                  </button>
                </Td>
              </Tr>
            )
          })}
        </Table>
      </Card>
    </div>
  )
}

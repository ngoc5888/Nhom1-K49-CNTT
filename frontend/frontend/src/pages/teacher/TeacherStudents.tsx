import { useState } from 'react'
import { Search, Plus, Filter } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Avatar } from '../../components/ui/Avatar'
import { Table, Td, Tr } from '../../components/ui/Table'
import { Button } from '../../components/ui/Button'
import { mockStudents } from '../../data/mockData'

export function TeacherStudents() {
  const [search, setSearch] = useState('')
  const filtered = mockStudents.filter(
    (s) =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.id.toLowerCase().includes(search.toLowerCase()) ||
      s.class.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Sinh viên</h1>
          <p className="text-slate-500 text-sm mt-1">Danh sách sinh viên theo từng lớp phụ trách</p>
        </div>
        <Button>
          <Plus size={15} />
          Điểm danh
        </Button>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between gap-4">
            <CardTitle>Danh sách sinh viên ({filtered.length})</CardTitle>
            <div className="relative">
              <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Tìm kiếm sinh viên..."
                className="pl-9 pr-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary w-64"
              />
            </div>
          </div>
        </CardHeader>
        <Table headers={['Sinh viên', 'Mã SV', 'Lớp', 'Email', 'GPA', 'Trạng thái', 'Hành động']}>
          {filtered.map((s) => (
            <Tr key={s.id}>
              <Td>
                <div className="flex items-center gap-3">
                  <Avatar name={s.name} size="sm" />
                  <span className="font-medium text-slate-800">{s.name}</span>
                </div>
              </Td>
              <Td className="text-slate-500 font-mono text-xs">{s.id}</Td>
              <Td><Badge variant="blue">{s.class}</Badge></Td>
              <Td className="text-slate-500">{s.email}</Td>
              <Td>
                <span className={`font-semibold ${s.gpa >= 3.6 ? 'text-emerald-600' : s.gpa >= 3.0 ? 'text-blue-600' : s.gpa >= 2.5 ? 'text-amber-600' : 'text-red-600'}`}>
                  {s.gpa.toFixed(2)}
                </span>
              </Td>
              <Td>
                <Badge variant={s.status === 'active' ? 'green' : 'gray'}>
                  {s.status === 'active' ? 'Đang học' : 'Bảo lưu'}
                </Badge>
              </Td>
              <Td>
                <button className="text-xs text-primary hover:underline font-medium">Xem hồ sơ</button>
              </Td>
            </Tr>
          ))}
        </Table>
      </Card>
    </div>
  )
}

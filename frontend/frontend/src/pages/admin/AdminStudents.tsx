import { useState } from 'react'
import { Search, Plus, Edit2, Lock, Unlock, Trash2 } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { Avatar } from '../../components/ui/Avatar'
import { Table, Td, Tr } from '../../components/ui/Table'
import { Button } from '../../components/ui/Button'
import { Modal } from '../../components/ui/Modal'
import { mockStudents } from '../../data/mockData'

export function AdminStudents() {
  const [search, setSearch] = useState('')
  const [addModal, setAddModal] = useState(false)
  const [page, setPage] = useState(1)
  const perPage = 5

  const filtered = mockStudents.filter(
    (s) =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.id.toLowerCase().includes(search.toLowerCase()) ||
      s.class.toLowerCase().includes(search.toLowerCase())
  )
  const paginated = filtered.slice((page - 1) * perPage, page * perPage)
  const totalPages = Math.ceil(filtered.length / perPage)

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Quản lý Sinh viên</h1>
          <p className="text-slate-500 text-sm mt-1">Thêm, sửa, khóa tài khoản sinh viên</p>
        </div>
        <Button onClick={() => setAddModal(true)}>
          <Plus size={15} />
          Thêm sinh viên
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
                onChange={(e) => { setSearch(e.target.value); setPage(1) }}
                placeholder="Tìm kiếm..."
                className="pl-9 pr-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary w-64"
              />
            </div>
          </div>
        </CardHeader>
        <Table headers={['Sinh viên', 'Mã SV', 'Lớp', 'Email', 'GPA', 'Trạng thái', 'Hành động']}>
          {paginated.map((s) => (
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
                <span className={`font-semibold ${s.gpa >= 3.6 ? 'text-emerald-600' : s.gpa >= 3.0 ? 'text-blue-600' : 'text-amber-600'}`}>
                  {s.gpa.toFixed(2)}
                </span>
              </Td>
              <Td>
                <Badge variant={s.status === 'active' ? 'green' : 'gray'}>
                  {s.status === 'active' ? 'Hoạt động' : 'Bị khóa'}
                </Badge>
              </Td>
              <Td>
                <div className="flex items-center gap-1.5">
                  <button className="p-1.5 hover:bg-blue-50 rounded text-blue-500 transition-colors" title="Sửa">
                    <Edit2 size={13} />
                  </button>
                  <button className="p-1.5 hover:bg-amber-50 rounded text-amber-500 transition-colors" title="Khóa/Mở">
                    {s.status === 'active' ? <Lock size={13} /> : <Unlock size={13} />}
                  </button>
                  <button className="p-1.5 hover:bg-red-50 rounded text-red-500 transition-colors" title="Xóa">
                    <Trash2 size={13} />
                  </button>
                </div>
              </Td>
            </Tr>
          ))}
        </Table>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between px-5 py-3.5 border-t border-slate-100">
            <p className="text-xs text-slate-500">
              Hiển thị {(page - 1) * perPage + 1}-{Math.min(page * perPage, filtered.length)} / {filtered.length} kết quả
            </p>
            <div className="flex items-center gap-1">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
                <button
                  key={p}
                  onClick={() => setPage(p)}
                  className={`w-8 h-8 text-xs rounded-lg font-medium transition-colors ${
                    p === page
                      ? 'bg-primary text-white'
                      : 'text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>
        )}
      </Card>

      {/* Add Student Modal */}
      <Modal
        open={addModal}
        onClose={() => setAddModal(false)}
        title="Thêm Sinh viên mới"
        footer={
          <>
            <Button variant="secondary" onClick={() => setAddModal(false)}>Hủy</Button>
            <Button onClick={() => setAddModal(false)}>Thêm sinh viên</Button>
          </>
        }
      >
        <div className="space-y-4">
          {['Họ và tên', 'Mã sinh viên', 'Email', 'Lớp'].map((label) => (
            <div key={label} className="space-y-1.5">
              <label className="block text-sm font-medium text-slate-700">{label}</label>
              <input
                type="text"
                placeholder={`Nhập ${label.toLowerCase()}...`}
                className="w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary"
              />
            </div>
          ))}
        </div>
      </Modal>
    </div>
  )
}

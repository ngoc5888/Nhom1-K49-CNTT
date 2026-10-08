import { BookOpen, Users, Clock, MapPin, BookMarked } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { mockClasses } from '../../data/mockData'

export function StudentClasses() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Lớp học của tôi</h1>
        <p className="text-slate-500 text-sm mt-1">Danh sách các lớp học kỳ này</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        {mockClasses.map((cls, i) => {
          const colors = [
            'from-blue-500 to-indigo-600',
            'from-violet-500 to-purple-600',
            'from-emerald-500 to-teal-600',
            'from-amber-500 to-orange-600',
            'from-rose-500 to-pink-600',
          ]
          const color = colors[i % colors.length]

          return (
            <div
              key={cls.id}
              className="bg-white rounded-xl border border-slate-100 shadow-sm hover:shadow-md transition-all duration-200 hover:-translate-y-0.5 overflow-hidden"
            >
              <div className={`h-2 bg-gradient-to-r ${color}`} />
              <div className="p-5">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-semibold text-slate-800 leading-tight">{cls.name}</p>
                    <p className="text-xs text-slate-500 mt-0.5">{cls.code}</p>
                  </div>
                  <Badge variant={cls.status === 'active' ? 'green' : 'gray'}>
                    {cls.status === 'active' ? 'Đang học' : 'Đã kết thúc'}
                  </Badge>
                </div>

                <div className="mt-4 space-y-2">
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <Users size={13} />
                    <span>GV: {cls.teacher}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <Clock size={13} />
                    <span>{cls.schedule}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <MapPin size={13} />
                    <span>Phòng {cls.room}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <BookMarked size={13} />
                    <span>{cls.credits} tín chỉ</span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-slate-50 flex items-center justify-between">
                  <span className="text-xs text-slate-500">{cls.students} sinh viên</span>
                  <button className="text-xs text-primary hover:underline font-medium">
                    Xem chi tiết →
                  </button>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

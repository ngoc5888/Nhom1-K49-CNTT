import { Calendar, Clock, MapPin, BookOpen } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { scheduleData } from '../../data/mockData'

const days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7']
const dayColors = ['blue', 'emerald', 'violet', 'amber', 'rose', 'slate'] as const

export function TeacherSchedule() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <div className="p-2.5 bg-blue-100 rounded-xl">
          <Calendar size={22} className="text-blue-600" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Lịch dạy</h1>
          <p className="text-slate-500 text-sm">Tuần 26/09 - 02/10/2026</p>
        </div>
      </div>

      {/* Weekly schedule grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {days.slice(0, 5).map((day, i) => {
          const events = scheduleData.filter((s) => s.day === day)
          const color = dayColors[i]
          return (
            <div key={day} className="space-y-2">
              <div className={`text-center py-2 rounded-lg text-sm font-semibold bg-${color}-100 text-${color}-700`}>
                {day}
              </div>
              {events.length > 0 ? (
                events.map((ev, j) => (
                  <div key={j} className={`rounded-xl p-3 bg-${color}-50 border border-${color}-100`}>
                    <p className={`text-sm font-semibold text-${color}-800 leading-tight`}>{ev.subject}</p>
                    <div className="mt-2 space-y-1">
                      <div className={`flex items-center gap-1.5 text-xs text-${color}-600`}>
                        <Clock size={11} />
                        <span>{ev.time}</span>
                      </div>
                      <div className={`flex items-center gap-1.5 text-xs text-${color}-600`}>
                        <MapPin size={11} />
                        <span>P.{ev.room}</span>
                      </div>
                      <div className={`flex items-center gap-1.5 text-xs text-${color}-600`}>
                        <BookOpen size={11} />
                        <span>{ev.class}</span>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="rounded-xl p-3 bg-slate-50 border border-slate-100 text-center">
                  <p className="text-xs text-slate-400">Không có lịch</p>
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Table view */}
      <Card>
        <CardHeader><CardTitle>Chi tiết lịch dạy tuần này</CardTitle></CardHeader>
        <CardContent className="p-0">
          <div className="divide-y divide-slate-50">
            {scheduleData.map((s, i) => (
              <div key={i} className="flex items-center justify-between px-5 py-4 hover:bg-slate-50/50 transition-colors">
                <div className="flex items-center gap-4">
                  <div className="w-16 text-center">
                    <span className="text-xs font-semibold text-primary bg-primary/10 px-2 py-1 rounded-md">{s.day}</span>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-800">{s.subject}</p>
                    <div className="flex items-center gap-3 mt-0.5 text-xs text-slate-500">
                      <span className="flex items-center gap-1"><Clock size={11} />{s.time}</span>
                      <span className="flex items-center gap-1"><MapPin size={11} />Phòng {s.room}</span>
                    </div>
                  </div>
                </div>
                <Badge variant="blue">{s.class}</Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

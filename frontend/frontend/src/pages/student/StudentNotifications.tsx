import { Bell, CheckCheck, Info, AlertTriangle, CheckCircle, XCircle } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'
import { mockNotifications } from '../../data/mockData'
import { cn } from '../../lib/utils'

const typeConfig = {
  info: { icon: Info, color: 'text-blue-500 bg-blue-100', variant: 'blue' as const },
  success: { icon: CheckCircle, color: 'text-emerald-500 bg-emerald-100', variant: 'green' as const },
  warning: { icon: AlertTriangle, color: 'text-amber-500 bg-amber-100', variant: 'yellow' as const },
  error: { icon: XCircle, color: 'text-red-500 bg-red-100', variant: 'red' as const },
}

export function StudentNotifications() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Thông báo</h1>
          <p className="text-slate-500 text-sm mt-1">Tin tức và nhắc nhở từ nhà trường</p>
        </div>
        <button className="flex items-center gap-1.5 text-sm text-primary hover:underline font-medium">
          <CheckCheck size={15} />
          Đánh dấu đã đọc tất cả
        </button>
      </div>

      <Card>
        <CardContent className="p-0">
          <div className="divide-y divide-slate-50">
            {mockNotifications.map((n) => {
              const cfg = typeConfig[n.type as keyof typeof typeConfig]
              const Icon = cfg.icon
              return (
                <div
                  key={n.id}
                  className={cn(
                    'flex items-start gap-4 px-5 py-4 hover:bg-slate-50/50 transition-colors cursor-pointer',
                    !n.read && 'bg-blue-50/30'
                  )}
                >
                  <div className={`p-2.5 rounded-xl flex-shrink-0 ${cfg.color}`}>
                    <Icon size={18} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className={cn('text-sm font-medium', !n.read ? 'text-slate-900' : 'text-slate-700')}>
                          {n.title}
                        </p>
                        <p className="text-sm text-slate-500 mt-0.5">{n.message}</p>
                        <p className="text-xs text-slate-400 mt-1">{n.time}</p>
                      </div>
                      <div className="flex items-center gap-2 flex-shrink-0">
                        {!n.read && <div className="w-2 h-2 bg-blue-500 rounded-full" />}
                        <Badge variant={cfg.variant}>
                          {n.type === 'info' ? 'Thông tin' : n.type === 'success' ? 'Thành công' : n.type === 'warning' ? 'Cảnh báo' : 'Lỗi'}
                        </Badge>
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

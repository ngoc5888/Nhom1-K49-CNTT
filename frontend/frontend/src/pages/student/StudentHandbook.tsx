import { Book, GraduationCap, ChevronRight, BookOpen, AlertCircle, Info, Star } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { Badge } from '../../components/ui/Badge'

const sections = [
  {
    icon: GraduationCap,
    title: 'Quy chế học tập',
    color: 'from-blue-500 to-indigo-500',
    items: [
      'Quy chế đào tạo đại học theo hệ thống tín chỉ',
      'Điều kiện xét tốt nghiệp và công nhận bằng tốt nghiệp',
      'Quy định về đăng ký học phần và thay đổi học phần',
    ],
  },
  {
    icon: BookOpen,
    title: 'Hướng dẫn sử dụng hệ thống',
    color: 'from-emerald-500 to-teal-500',
    items: [
      'Đăng nhập và quản lý tài khoản cá nhân',
      'Xem lịch học, tài liệu và bài giảng trực tuyến',
      'Nộp bài tập và theo dõi kết quả chấm điểm',
      'Tham gia kiểm tra và thi trực tuyến',
    ],
  },
  {
    icon: AlertCircle,
    title: 'Quy định về đánh giá',
    color: 'from-amber-500 to-orange-500',
    items: [
      'Thang điểm chữ và điểm số 10: A (9-10), B+ (8-8.9), B (7-7.9)...',
      'Điểm quá trình (20-30%), kiểm tra giữa kỳ (20-30%), cuối kỳ (40-60%)',
      'Điều kiện thi cuối kỳ: tham dự đủ 80% số buổi học',
      'Quy định về phúc khảo điểm thi',
    ],
  },
  {
    icon: Info,
    title: 'Liên hệ hỗ trợ',
    color: 'from-violet-500 to-purple-500',
    items: [
      'Phòng Đào tạo: phong.daotao@university.edu.vn',
      'Bộ phận IT Hỗ trợ: it.support@university.edu.vn',
      'Hotline: 024 1234 5678 (Thứ 2-6, 8h-17h)',
    ],
  },
]

export function StudentHandbook() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <div className="p-2.5 bg-blue-100 rounded-xl">
          <Book size={24} className="text-blue-600" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Sổ tay Hướng dẫn Sinh viên</h1>
          <p className="text-slate-500 text-sm mt-0.5">Các thông tin quan trọng và hướng dẫn sử dụng hệ thống</p>
        </div>
      </div>

      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl p-6 text-white">
        <div className="flex items-center gap-2 mb-2">
          <Star size={18} className="text-yellow-300" />
          <Badge className="bg-white/20 text-white border-0">Hướng dẫn mới</Badge>
        </div>
        <h2 className="text-xl font-bold">Chào mừng đến với LMS!</h2>
        <p className="text-blue-100 mt-1 text-sm leading-relaxed">
          Hệ thống Quản lý Học tập giúp bạn theo dõi tiến độ học tập, nộp bài tập,
          kiểm tra điểm số và tương tác với giảng viên một cách thuận tiện.
        </p>
      </div>

      {/* Sections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {sections.map((section) => {
          const Icon = section.icon
          return (
            <Card key={section.title} className="hover:shadow-md transition-shadow duration-200">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className={`p-2.5 rounded-xl bg-gradient-to-br ${section.color}`}>
                    <Icon size={18} className="text-white" />
                  </div>
                  <CardTitle>{section.title}</CardTitle>
                </div>
              </CardHeader>
              <CardContent className="pt-0">
                <ul className="space-y-2.5">
                  {section.items.map((item, i) => (
                    <li key={i} className="flex items-start gap-2.5 text-sm text-slate-600">
                      <ChevronRight size={14} className="text-slate-400 mt-0.5 flex-shrink-0" />
                      {item}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}

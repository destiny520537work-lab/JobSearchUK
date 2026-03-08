import { useTranslation } from 'react-i18next'
import { Briefcase, Shield, PoundSterling, BarChart3 } from 'lucide-react'

function Card({ icon: Icon, label, value, color }) {
  return (
    <div className={`bg-white rounded-xl border border-gray-200 p-4 flex items-center gap-3`}>
      <div className={`p-2 rounded-lg ${color}`}>
        <Icon size={18} className="text-white" />
      </div>
      <div>
        <div className="text-xs text-gray-500 font-medium">{label}</div>
        <div className="text-xl font-bold text-gray-800">{value ?? '—'}</div>
      </div>
    </div>
  )
}

export default function StatsCards({ stats }) {
  const { t } = useTranslation()

  if (!stats) return null

  const sponsorPct = stats.sponsor_rate != null
    ? `${Math.round(stats.sponsor_rate * 100)}%`
    : '—'
  const avgSalary = stats.avg_salary != null
    ? `£${stats.avg_salary.toLocaleString()}`
    : '—'
  const salaryPct = stats.salary_disclosed_rate != null
    ? `${Math.round(stats.salary_disclosed_rate * 100)}%`
    : '—'

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <Card icon={Briefcase} label={t('stats.totalJobs')} value={stats.total_jobs} color="bg-blue-500" />
      <Card icon={Shield} label={t('stats.canSponsor')} value={sponsorPct} color="bg-green-500" />
      <Card icon={PoundSterling} label={t('stats.avgSalary')} value={avgSalary} color="bg-purple-500" />
      <Card icon={BarChart3} label={t('stats.withSalary')} value={salaryPct} color="bg-orange-500" />
    </div>
  )
}

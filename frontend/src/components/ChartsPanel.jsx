import { useTranslation } from 'react-i18next'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from 'recharts'

const VISA_COLORS = {
  '✅': '#16a34a',
  '⚠️': '#d97706',
  '🟡': '#ca8a04',
  '❌': '#dc2626',
  'Not specified': '#9ca3af',
}

function getVisaColor(status) {
  for (const [key, color] of Object.entries(VISA_COLORS)) {
    if (status && status.includes(key)) return color
  }
  return '#9ca3af'
}

export default function ChartsPanel({ stats }) {
  const { t } = useTranslation()

  if (!stats) return null

  const locationData = (stats.by_location || []).slice(0, 8).map(d => ({
    name: d.location?.replace(', England', '').replace(', United Kingdom', '') || '',
    count: d.count,
  }))

  const visaData = (stats.by_visa || []).map(d => ({
    name: d.status || 'Unknown',
    value: d.count,
    color: getVisaColor(d.status),
  }))

  const salaryData = (stats.by_salary_band || []).map(d => ({
    name: d.band,
    count: d.count,
  }))

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      {/* Location bar chart */}
      <div className="bg-white rounded-xl border border-gray-200 p-4">
        <div className="text-sm font-semibold text-gray-700 mb-3">{t('charts.byLocation')}</div>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={locationData} layout="vertical" margin={{ left: 0, right: 10 }}>
            <XAxis type="number" tick={{ fontSize: 10 }} />
            <YAxis type="category" dataKey="name" tick={{ fontSize: 10 }} width={80} />
            <Tooltip />
            <Bar dataKey="count" fill="#3b82f6" radius={[0, 3, 3, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Visa pie chart */}
      <div className="bg-white rounded-xl border border-gray-200 p-4">
        <div className="text-sm font-semibold text-gray-700 mb-3">{t('charts.byVisa')}</div>
        <ResponsiveContainer width="100%" height={220}>
          <PieChart margin={{ top: 10, bottom: 10, left: 0, right: 0 }}>
            <Pie
              data={visaData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={65}
              label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
              labelLine={false}
            >
              {visaData.map((entry, index) => (
                <Cell key={index} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip formatter={(val, name) => [val, name.substring(0, 30)]} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Salary bar chart */}
      <div className="bg-white rounded-xl border border-gray-200 p-4">
        <div className="text-sm font-semibold text-gray-700 mb-3">{t('charts.bySalary')}</div>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={salaryData} margin={{ left: -10, right: 10 }}>
            <XAxis dataKey="name" tick={{ fontSize: 9 }} />
            <YAxis tick={{ fontSize: 10 }} />
            <Tooltip />
            <Bar dataKey="count" fill="#8b5cf6" radius={[3, 3, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

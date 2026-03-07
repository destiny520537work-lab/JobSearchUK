import { useTranslation } from 'react-i18next'

const TABS = [
  { days: 1, key: 'today' },
  { days: 3, key: 'threeDays' },
  { days: 7, key: 'thisWeek' },
  { days: 14, key: 'twoWeeks' },
  { days: 365, key: 'all' },
]

export default function DateTabs({ activeDays, onChange, totalByDays = {} }) {
  const { t } = useTranslation()

  return (
    <div className="flex gap-2 flex-wrap">
      {TABS.map(tab => {
        const active = activeDays === tab.days
        const count = totalByDays[tab.days]
        return (
          <button
            key={tab.days}
            onClick={() => onChange(tab.days)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors border ${
              active
                ? 'bg-blue-600 text-white border-blue-600'
                : 'bg-white text-gray-600 border-gray-200 hover:border-blue-300 hover:text-blue-600'
            }`}
          >
            <div>{t(`dateTabs.${tab.key}`)}</div>
            {count !== undefined && (
              <div className={`text-xs font-bold ${active ? 'text-blue-100' : 'text-gray-400'}`}>
                {count}
              </div>
            )}
          </button>
        )
      })}
    </div>
  )
}

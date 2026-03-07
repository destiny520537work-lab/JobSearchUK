import { useTranslation } from 'react-i18next'
import { Target, DollarSign, Clock } from 'lucide-react'

const TABS = [
  { key: 'match', labelKey: 'bestMatch', hintKey: 'bestMatchHint', icon: Target },
  { key: 'salary', labelKey: 'topSalary', icon: DollarSign },
  { key: 'newest', labelKey: 'newest', icon: Clock },
]

export default function SortTabs({ activeSort, onChange, hasCV }) {
  const { t } = useTranslation()

  return (
    <div className="flex gap-2 flex-wrap">
      {TABS.map(tab => {
        const active = activeSort === tab.key
        const disabled = tab.key === 'match' && !hasCV
        const Icon = tab.icon
        return (
          <button
            key={tab.key}
            onClick={() => !disabled && onChange(tab.key)}
            title={disabled ? t('sortTabs.bestMatchHint') : undefined}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-colors border ${
              active
                ? 'bg-green-600 text-white border-green-600'
                : disabled
                ? 'bg-gray-50 text-gray-400 border-gray-200 cursor-not-allowed'
                : 'bg-white text-gray-600 border-gray-200 hover:border-green-300 hover:text-green-600'
            }`}
          >
            <Icon size={14} />
            <span>{t(`sortTabs.${tab.labelKey}`)}</span>
            {tab.key === 'match' && !hasCV && (
              <span className="text-xs text-gray-400 hidden sm:inline">
                {t('sortTabs.bestMatchHint')}
              </span>
            )}
          </button>
        )
      })}
    </div>
  )
}

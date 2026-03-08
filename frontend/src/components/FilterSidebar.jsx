import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import api from '../api'
import { ChevronDown, ChevronUp, X } from 'lucide-react'

const VISA_OPTIONS = [
  { value: '✅', label: '✅ Visa sponsored' },
  { value: '🟡', label: '🟡 Company licensed' },
  { value: '⚠️', label: '⚠️ Claims (unverified)' },
  { value: '❌', label: '❌ No sponsorship' },
  { value: 'Not specified', label: 'Not specified' },
]

const JOB_TYPE_MAP = {
  '软件': 'Software Eng',
  '数据': 'Data',
  'AI': 'AI / ML',
  '产品': 'Product',
  '商业': 'Business',
  '定量': 'Quantitative',
  '其他': 'Other',
}

const SALARY_BANDS = [
  { value: null, label: 'Any' },
  { value: 20000, label: '£20k+' },
  { value: 30000, label: '£30k+' },
  { value: 40000, label: '£40k+' },
  { value: 55000, label: '£55k+' },
]

function FilterSection({ title, children, defaultOpen = true }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="border-b border-gray-100 pb-3 mb-3">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center justify-between w-full text-sm font-semibold text-gray-700 mb-2"
      >
        {title}
        {open ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </button>
      {open && children}
    </div>
  )
}

function CheckboxList({ options, selected, onChange, maxVisible = 8 }) {
  const [showAll, setShowAll] = useState(false)
  const visible = showAll ? options : options.slice(0, maxVisible)

  return (
    <div className="space-y-1">
      {visible.map(opt => {
        const val = typeof opt === 'string' ? opt : opt.value
        const label = typeof opt === 'string' ? opt : opt.label
        const checked = selected.includes(val)
        return (
          <label key={val} className="flex items-center gap-2 cursor-pointer group">
            <input
              type="checkbox"
              checked={checked}
              onChange={() => {
                onChange(
                  checked ? selected.filter(v => v !== val) : [...selected, val]
                )
              }}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-xs text-gray-600 group-hover:text-gray-900 truncate">{label}</span>
          </label>
        )
      })}
      {options.length > maxVisible && (
        <button
          onClick={() => setShowAll(!showAll)}
          className="text-xs text-blue-500 hover:underline mt-1"
        >
          {showAll ? 'Show less' : `+${options.length - maxVisible} more`}
        </button>
      )}
    </div>
  )
}

export default function FilterSidebar({ filters, onUpdate }) {
  const { t } = useTranslation()
  const [filterOptions, setFilterOptions] = useState({
    locations: [], job_types: [], skills: [],
  })

  useEffect(() => {
    api.get('/api/filters').then(res => setFilterOptions(res.data)).catch(() => {})
  }, [])

  const hasActiveFilters =
    filters.visa.length > 0 ||
    filters.location.length > 0 ||
    filters.job_type.length > 0 ||
    filters.skills.length > 0

  return (
    <aside className="w-56 shrink-0">
      <div className="bg-white rounded-xl border border-gray-200 p-4 sticky top-20">
        <div className="flex items-center justify-between mb-4">
          <span className="font-semibold text-gray-800 text-sm">{t('filters.title')}</span>
          {hasActiveFilters && (
            <button
              onClick={() => onUpdate({ visa: [], location: [], job_type: [], skills: [] })}
              className="text-xs text-red-500 hover:underline flex items-center gap-0.5"
            >
              <X size={12} /> {t('filters.clearAll')}
            </button>
          )}
        </div>

        <FilterSection title={t('filters.visaStatus')}>
          <CheckboxList
            options={VISA_OPTIONS}
            selected={filters.visa}
            onChange={val => onUpdate({ visa: val })}
          />
        </FilterSection>

        <FilterSection title={t('filters.location')}>
          <CheckboxList
            options={filterOptions.locations}
            selected={filters.location}
            onChange={val => onUpdate({ location: val })}
          />
        </FilterSection>

        <FilterSection title={t('filters.jobType')}>
          <CheckboxList
            options={(filterOptions.job_types || []).map(t => ({
              value: t,
              label: JOB_TYPE_MAP[t] || t,
            }))}
            selected={filters.job_type}
            onChange={val => onUpdate({ job_type: val })}
          />
        </FilterSection>

        <FilterSection title={t('filters.skills')} defaultOpen={false}>
          <CheckboxList
            options={filterOptions.skills}
            selected={filters.skills}
            onChange={val => onUpdate({ skills: val })}
            maxVisible={10}
          />
        </FilterSection>
      </div>
    </aside>
  )
}

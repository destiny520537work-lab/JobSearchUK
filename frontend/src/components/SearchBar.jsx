import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Search } from 'lucide-react'

export default function SearchBar({ value, onSearch }) {
  const { t } = useTranslation()
  const [input, setInput] = useState(value || '')

  const handleSubmit = (e) => {
    e.preventDefault()
    onSearch(input.trim())
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <div className="relative flex-1">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder={t('search.placeholder')}
          className="w-full pl-9 pr-4 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <button
        type="submit"
        className="px-5 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors whitespace-nowrap"
      >
        {t('search.button')}
      </button>
    </form>
  )
}

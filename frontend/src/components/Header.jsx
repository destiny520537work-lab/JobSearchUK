import { useTranslation } from 'react-i18next'
import { Globe } from 'lucide-react'

const LANGUAGES = [
  { code: 'en', label: 'EN' },
  { code: 'zh', label: '中文' },
  { code: 'fr', label: 'FR' },
  { code: 'es', label: 'ES' },
  { code: 'nl', label: 'NL' },
]

export default function Header({ onUploadCV }) {
  const { t, i18n } = useTranslation()

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between sticky top-0 z-50 shadow-sm">
      <div>
        <div className="text-2xl font-bold text-blue-700">{t('header.title')}</div>
        <div className="text-xs text-gray-500 hidden sm:block">{t('header.subtitle')}</div>
      </div>

      <div className="flex items-center gap-3">
        {/* Language switcher */}
        <div className="flex items-center gap-1">
          <Globe size={14} className="text-gray-400" />
          {LANGUAGES.map(lang => (
            <button
              key={lang.code}
              onClick={() => i18n.changeLanguage(lang.code)}
              className={`px-2 py-0.5 text-xs rounded transition-colors ${
                i18n.language === lang.code
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {lang.label}
            </button>
          ))}
        </div>

        {/* Upload CV button */}
        <button
          onClick={onUploadCV}
          className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          {t('header.uploadCV')}
        </button>
      </div>
    </header>
  )
}

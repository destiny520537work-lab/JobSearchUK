import { useState } from 'react'
import { useTranslation } from 'react-i18next'

import Header from './components/Header'
import SearchBar from './components/SearchBar'
import DateTabs from './components/DateTabs'
import SortTabs from './components/SortTabs'
import FilterSidebar from './components/FilterSidebar'
import StatsCards from './components/StatsCards'
import ChartsPanel from './components/ChartsPanel'
import JobTable from './components/JobTable'
import CVUpload from './components/CVUpload'

import { useJobs } from './hooks/useJobs'
import { useStats } from './hooks/useStats'

export default function App() {
  const { t } = useTranslation()
  const [showCVUpload, setShowCVUpload] = useState(false)

  const {
    filters,
    updateFilters,
    setPage,
    data,
    loading,
    error,
    matchScores,
    setMatchScores,
  } = useJobs()

  const { stats } = useStats(filters.days)

  const hasCV = Object.keys(matchScores).length > 0

  const lastUpdated = stats?.last_updated
    ? new Date(stats.last_updated).toUTCString().slice(0, 25)
    : '—'

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header onUploadCV={() => setShowCVUpload(true)} />

      {/* Main content */}
      <main className="flex-1 max-w-screen-2xl mx-auto w-full px-4 py-5 flex flex-col gap-4">
        {/* Search bar */}
        <SearchBar
          value={filters.q}
          onSearch={q => updateFilters({ q })}
        />

        {/* Date tabs */}
        <DateTabs
          activeDays={filters.days}
          onChange={days => updateFilters({ days })}
        />

        {/* Sort tabs */}
        <SortTabs
          activeSort={filters.sort}
          onChange={sort => updateFilters({ sort })}
          hasCV={hasCV}
        />

        {/* Body: sidebar + main */}
        <div className="flex gap-5 items-start">
          <FilterSidebar filters={filters} onUpdate={updateFilters} />

          <div className="flex-1 min-w-0 flex flex-col gap-4">
            {/* Stats cards */}
            <StatsCards stats={stats} />

            {/* Charts */}
            <ChartsPanel stats={stats} />

            {/* Jobs table */}
            {error ? (
              <div className="bg-red-50 text-red-700 rounded-xl p-4 text-sm">
                Error loading jobs: {error}
              </div>
            ) : loading && data.items.length === 0 ? (
              <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
                <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
                <p className="text-sm text-gray-400">Loading jobs...</p>
              </div>
            ) : data.items.length === 0 ? (
              <div className="bg-white rounded-xl border border-gray-200 p-12 text-center text-gray-400 text-sm">
                {t('table.noResults')}
              </div>
            ) : (
              <JobTable
                jobs={data.items}
                total={data.total}
                page={data.page}
                pages={data.pages}
                pageSize={filters.page_size}
                onPageChange={setPage}
                filters={filters}
                sort={filters.sort}
              />
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 px-6 py-4 text-center text-xs text-gray-400 space-y-1">
        <div>{t('footer.updatedEvery')} | {t('footer.lastUpdate', { time: lastUpdated })}</div>
        <div>{t('footer.source')}</div>
        <div>{t('footer.disclaimer')}</div>
      </footer>

      {/* CV Upload Modal */}
      {showCVUpload && (
        <CVUpload
          onClose={() => setShowCVUpload(false)}
          onMatchScores={(scores) => {
            setMatchScores(scores)
            setShowCVUpload(false)
          }}
        />
      )}
    </div>
  )
}

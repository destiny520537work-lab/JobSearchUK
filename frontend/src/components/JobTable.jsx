import { useCallback, useMemo } from 'react'
import { useTranslation } from 'react-i18next'
import { AgGridReact } from 'ag-grid-react'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-alpine.css'
import { Download } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

const VISA_BG = {
  '✅': '#d5f5d5',
  '⚠️': '#fef3c7',
  '🟡': '#fef9c3',
  '❌': '#ffd5d5',
}

function getVisaBg(status) {
  if (!status) return null
  for (const [emoji, color] of Object.entries(VISA_BG)) {
    if (status.includes(emoji)) return color
  }
  return null
}

function VisaCellRenderer({ value }) {
  const bg = getVisaBg(value)
  return (
    <span
      style={{ backgroundColor: bg || 'transparent', padding: '2px 6px', borderRadius: 4, fontSize: 11 }}
    >
      {value || 'Not specified'}
    </span>
  )
}

function TitleCellRenderer({ value, data }) {
  return (
    <a
      href={data?.link}
      target="_blank"
      rel="noopener noreferrer"
      className="text-blue-600 hover:underline text-xs"
    >
      {value}
    </a>
  )
}

function ScoreCellRenderer({ value }) {
  if (value == null) return null
  const pct = Math.round(value)
  return (
    <div className="flex items-center gap-1.5">
      <div className="flex-1 bg-gray-200 rounded-full h-1.5 w-16">
        <div
          className="bg-green-500 h-1.5 rounded-full"
          style={{ width: `${Math.min(pct, 100)}%` }}
        />
      </div>
      <span className="text-xs text-gray-600">{pct}%</span>
    </div>
  )
}

export default function JobTable({ jobs, total, page, pages, pageSize, onPageChange, filters, sort }) {
  const { t } = useTranslation()

  const columnDefs = useMemo(() => {
    const cols = [
      {
        field: 'posted_date',
        headerName: t('table.date'),
        width: 80,
        valueFormatter: ({ value }) => value ? value.slice(5) : '',
        sortable: true,
      },
      { field: 'company', headerName: t('table.company'), width: 160, sortable: true },
      { field: 'project_type', headerName: t('table.type'), width: 90 },
      {
        field: 'title',
        headerName: t('table.jobTitle'),
        flex: 1,
        minWidth: 200,
        cellRenderer: TitleCellRenderer,
        sortable: true,
      },
      { field: 'location', headerName: t('table.location'), width: 130, sortable: true },
      { field: 'salary', headerName: t('table.salary'), width: 130 },
      {
        field: 'visa_status',
        headerName: t('table.visaStatus'),
        width: 140,
        cellRenderer: VisaCellRenderer,
      },
    ]

    if (sort === 'match') {
      cols.push({
        field: 'match_score',
        headerName: 'Match',
        width: 110,
        cellRenderer: ScoreCellRenderer,
        sortable: true,
        sort: 'desc',
      })
    }

    return cols
  }, [t, sort])

  const exportURL = useMemo(() => {
    const params = new URLSearchParams()
    if (filters.q) params.append('q', filters.q)
    filters.visa.forEach(v => params.append('visa', v))
    filters.location.forEach(l => params.append('location', l))
    filters.job_type.forEach(j => params.append('job_type', j))
    filters.skills.forEach(s => params.append('skills', s))
    params.append('days', filters.days)
    return `${API_BASE}/api/export?${params.toString()}`
  }, [filters])

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-100 bg-gray-50">
        <span className="text-xs text-gray-500">
          {t('table.showing', { count: jobs.length, total })}
        </span>
        <a
          href={exportURL}
          download
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-green-700 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 transition-colors"
        >
          <Download size={13} />
          {t('table.exportXLSX')}
        </a>
      </div>

      {/* AG Grid */}
      <div className="ag-theme-alpine" style={{ height: 480, width: '100%' }}>
        <AgGridReact
          rowData={jobs}
          columnDefs={columnDefs}
          defaultColDef={{ resizable: true, suppressMovable: false }}
          rowSelection="multiple"
          suppressRowClickSelection
          animateRows
          getRowId={({ data }) => data.job_id}
        />
      </div>

      {/* Pagination */}
      {pages > 1 && (
        <div className="flex items-center justify-center gap-2 px-4 py-3 border-t border-gray-100">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page <= 1}
            className="px-3 py-1 text-sm rounded border border-gray-200 disabled:opacity-40 hover:bg-gray-50"
          >
            ‹
          </button>
          <span className="text-sm text-gray-600">
            {page} / {pages}
          </span>
          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page >= pages}
            className="px-3 py-1 text-sm rounded border border-gray-200 disabled:opacity-40 hover:bg-gray-50"
          >
            ›
          </button>
        </div>
      )}
    </div>
  )
}

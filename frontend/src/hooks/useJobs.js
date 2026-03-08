import { useState, useEffect, useCallback } from 'react'
import api from '../api'

const DEFAULT_FILTERS = {
  q: '',
  visa: [],
  location: [],
  job_type: [],
  skills: [],
  days: 365,
  sort: 'newest',
  page: 1,
  page_size: 50,
}

export function useJobs() {
  const [filters, setFilters] = useState(DEFAULT_FILTERS)
  const [data, setData] = useState({ total: 0, page: 1, pages: 1, items: [] })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [matchScores, setMatchScores] = useState({})

  const fetchJobs = useCallback(async (f = filters) => {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams()
      if (f.q) params.append('q', f.q)
      f.visa.forEach(v => params.append('visa', v))
      f.location.forEach(l => params.append('location', l))
      f.job_type.forEach(j => params.append('job_type', j))
      f.skills.forEach(s => params.append('skills', s))
      params.append('days', f.days)
      params.append('sort', f.sort)
      params.append('page', f.page)
      params.append('page_size', f.page_size)

      const res = await api.get('/api/jobs?' + params.toString())
      let items = res.data.items

      // Apply match scores if available and sort=match
      if (f.sort === 'match' && Object.keys(matchScores).length > 0) {
        items = [...items].sort((a, b) => {
          const sa = matchScores[a.job_id] || 0
          const sb = matchScores[b.job_id] || 0
          return sb - sa
        })
        items = items.map(item => ({
          ...item,
          match_score: matchScores[item.job_id] || 0,
        }))
      }

      setData({ ...res.data, items })
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [filters, matchScores])

  useEffect(() => {
    fetchJobs(filters)
  }, [filters])

  const updateFilters = (patch) => {
    setFilters(prev => ({ ...prev, ...patch, page: 1 }))
  }

  const setPage = (page) => {
    setFilters(prev => ({ ...prev, page }))
  }

  return {
    filters,
    updateFilters,
    setPage,
    data,
    loading,
    error,
    matchScores,
    setMatchScores,
    refetch: fetchJobs,
  }
}

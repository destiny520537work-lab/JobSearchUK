import { useState, useEffect } from 'react'
import api from '../api'

export function useStats(days = 7) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    api.get(`/api/stats?days=${days}`)
      .then(res => setStats(res.data))
      .catch(() => setStats(null))
      .finally(() => setLoading(false))
  }, [days])

  return { stats, loading }
}

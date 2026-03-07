import axios from 'axios'

// In production: set VITE_API_BASE_URL to your Railway backend URL
// e.g. https://gradjobs-backend.up.railway.app
// In development: empty string → proxy to localhost:8000
const baseURL = import.meta.env.VITE_API_BASE_URL || ''

const api = axios.create({ baseURL })

export default api

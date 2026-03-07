import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  // In production, VITE_API_BASE_URL is set to the Railway backend URL
  // If not set, requests go to same origin (works if frontend and backend are on same domain)
  define: {
    __API_BASE__: JSON.stringify(process.env.VITE_API_BASE_URL || ''),
  },
}))

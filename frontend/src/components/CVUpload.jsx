import { useState, useRef } from 'react'
import { useTranslation } from 'react-i18next'
import api from '../api'
import { Upload, X, CheckCircle, AlertCircle } from 'lucide-react'

export default function CVUpload({ onClose, onMatchScores }) {
  const { t } = useTranslation()
  const [state, setState] = useState('idle') // idle | uploading | success | error
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef()

  const upload = async (file) => {
    if (!file) return
    const ext = file.name.split('.').pop().toLowerCase()
    if (!['pdf', 'docx'].includes(ext)) {
      setState('error')
      return
    }
    setState('uploading')
    const formData = new FormData()
    formData.append('file', file)
    try {
      const res = await api.post('/api/match', formData)
      onMatchScores(res.data.scores || {})
      setState('success')
    } catch {
      setState('error')
    }
  }

  const onDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    upload(e.dataTransfer.files[0])
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-gray-800">{t('cvUpload.title')}</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X size={20} />
          </button>
        </div>

        <p className="text-sm text-gray-500 mb-5">{t('cvUpload.description')}</p>

        {state === 'idle' || state === 'error' ? (
          <div
            onDragOver={e => { e.preventDefault(); setDragging(true) }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
            onClick={() => inputRef.current?.click()}
            className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
              dragging ? 'border-blue-400 bg-blue-50' : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'
            }`}
          >
            <Upload size={28} className="mx-auto mb-3 text-gray-400" />
            <p className="text-sm text-gray-500">{t('cvUpload.dropzone')}</p>
            <input
              ref={inputRef}
              type="file"
              accept=".pdf,.docx"
              className="hidden"
              onChange={e => upload(e.target.files[0])}
            />
          </div>
        ) : null}

        {state === 'uploading' && (
          <div className="text-center py-8">
            <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            <p className="text-sm text-gray-500">{t('cvUpload.uploading')}</p>
          </div>
        )}

        {state === 'success' && (
          <div className="text-center py-6">
            <CheckCircle size={36} className="text-green-500 mx-auto mb-3" />
            <p className="text-sm text-green-700 font-medium">{t('cvUpload.success')}</p>
            <button
              onClick={onClose}
              className="mt-4 px-4 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700"
            >
              {t('cvUpload.close')}
            </button>
          </div>
        )}

        {state === 'error' && (
          <div className="mt-3 flex items-center gap-2 text-red-600 text-sm">
            <AlertCircle size={16} />
            {t('cvUpload.error')}
          </div>
        )}
      </div>
    </div>
  )
}

function Pulse({ className }) {
  return <div className={`animate-pulse bg-gray-200 rounded ${className}`} />
}

function SkeletonCard() {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4 flex items-center gap-3">
      <Pulse className="w-10 h-10 rounded-lg shrink-0" />
      <div className="flex-1 space-y-2">
        <Pulse className="h-3 w-24" />
        <Pulse className="h-6 w-16" />
      </div>
    </div>
  )
}

function SkeletonChart() {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4">
      <Pulse className="h-3 w-28 mb-4" />
      <Pulse className="w-full h-44 rounded" />
    </div>
  )
}

function SkeletonRow() {
  return (
    <div className="flex items-center gap-3 px-3 py-2.5 border-b border-gray-100">
      <Pulse className="h-3 w-14 shrink-0" />
      <Pulse className="h-3 w-28 shrink-0" />
      <Pulse className="h-3 w-14 shrink-0" />
      <Pulse className="h-3 flex-1" />
      <Pulse className="h-3 w-24 shrink-0" />
      <Pulse className="h-3 w-20 shrink-0" />
      <Pulse className="h-5 w-28 rounded-full shrink-0" />
    </div>
  )
}

export default function SkeletonLoader() {
  return (
    <div className="flex-1 min-w-0 flex flex-col gap-4">
      {/* Stats cards skeleton */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {[...Array(4)].map((_, i) => <SkeletonCard key={i} />)}
      </div>

      {/* Charts skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {[...Array(3)].map((_, i) => <SkeletonChart key={i} />)}
      </div>

      {/* Table skeleton */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        {/* Header */}
        <div className="flex items-center gap-3 px-3 py-2.5 bg-gray-50 border-b border-gray-200">
          {[14, 28, 14, 'flex-1', 24, 20, 28].map((w, i) => (
            <Pulse key={i} className={`h-3 ${typeof w === 'number' ? `w-${w}` : w} shrink-0`} />
          ))}
        </div>
        {[...Array(8)].map((_, i) => <SkeletonRow key={i} />)}
      </div>
    </div>
  )
}

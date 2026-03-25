const CONFIDENCE_LABELS = {
  low: 'Low confidence — submit more text for accurate scoring',
  medium: 'Medium confidence — longer text recommended',
  high: 'High confidence',
  very_high: 'Very high confidence',
}

function scoreColor(score) {
  if (score >= 8) return 'text-green-600'
  if (score >= 5) return 'text-yellow-500'
  return 'text-red-500'
}

export default function OverallScore({ overallScore, proficiencyLevel, cefrLevel, confidenceLevel, wordCount }) {
  return (
    <div className="bg-white rounded-xl shadow p-4 sm:p-6 text-center">
      <p className="text-gray-500 text-sm mb-1">Overall Score</p>

      <div className="flex items-baseline justify-center gap-1">
        <span
          data-testid="overall-score-value"
          className={`text-5xl sm:text-7xl font-bold ${scoreColor(overallScore)}`}
        >
          {overallScore}
        </span>
        <span className="text-xl sm:text-2xl text-gray-400">/ 10</span>
      </div>

      <p className="mt-2 text-xl font-semibold text-gray-700">
        {cefrLevel && <span className="text-blue-600 mr-1">{cefrLevel} –</span>}
        {proficiencyLevel}
      </p>

      <p className="mt-3 text-sm text-gray-500">
        {wordCount} words &middot; {CONFIDENCE_LABELS[confidenceLevel]}
      </p>
    </div>
  )
}

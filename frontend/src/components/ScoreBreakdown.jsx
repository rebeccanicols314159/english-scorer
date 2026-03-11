const CATEGORY_LABELS = {
  grammar: 'Grammar',
  vocabulary: 'Vocabulary',
  spelling_mechanics: 'Spelling & Mechanics',
  sentence_structure: 'Sentence Structure',
  coherence_organization: 'Coherence & Organisation',
  fluency_naturalness: 'Fluency & Naturalness',
}

function barColor(score) {
  if (score >= 7.5) return 'bg-green-500'
  if (score >= 4.5) return 'bg-yellow-400'
  return 'bg-red-500'
}

export default function ScoreBreakdown({ scores }) {
  return (
    <div className="bg-white rounded-xl shadow p-6 flex flex-col gap-4">
      <h2 className="text-lg font-semibold text-gray-800">Score Breakdown</h2>
      {Object.entries(scores).map(([key, score]) => (
        <div key={key} className="flex flex-col gap-1">
          <div className="flex justify-between text-sm text-gray-700">
            <span>{CATEGORY_LABELS[key] ?? key}</span>
            <span className="font-semibold">{score.toFixed(1)}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              role="progressbar"
              aria-label={CATEGORY_LABELS[key] ?? key}
              aria-valuenow={score}
              aria-valuemin={0}
              aria-valuemax={10}
              className={`h-3 rounded-full ${barColor(score)}`}
              style={{ width: `${(score / 10) * 100}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  )
}

const CATEGORY_LABELS = {
  grammar: 'Grammar',
  vocabulary: 'Vocabulary',
  spelling_mechanics: 'Spelling & Mechanics',
  sentence_structure: 'Sentence Structure',
  coherence_organization: 'Coherence & Organisation',
  fluency_naturalness: 'Fluency & Naturalness',
}

function feedbackIcon(score) {
  if (score >= 7.5) return '★'
  if (score >= 4.5) return '↑'
  return '⚠'
}

function iconColor(score) {
  if (score >= 7.5) return 'text-green-600'
  if (score >= 4.5) return 'text-yellow-500'
  return 'text-red-500'
}

export default function FeedbackPanel({ feedback, scores }) {
  return (
    <div className="bg-white rounded-xl shadow p-6 flex flex-col gap-4">
      <h2 className="text-lg font-semibold text-gray-800">Feedback</h2>
      {Object.entries(feedback).map(([key, text]) => {
        const score = scores[key]
        return (
          <div
            key={key}
            data-testid={`feedback-${key}`}
            className="flex gap-3 items-start"
          >
            <span className={`text-xl font-bold ${iconColor(score)}`}>
              {feedbackIcon(score)}
            </span>
            <div>
              <p className="text-sm font-semibold text-gray-700">
                {CATEGORY_LABELS[key] ?? key}
              </p>
              <p className="text-sm text-gray-600">{text}</p>
            </div>
          </div>
        )
      })}
    </div>
  )
}

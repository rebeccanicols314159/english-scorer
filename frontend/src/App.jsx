import { useState } from 'react'
import { scoreText } from './api/scorer'
import { exportPdf } from './utils/exportPdf'
import TextInput from './components/TextInput'
import SubmitButton from './components/SubmitButton'
import OverallScore from './components/OverallScore'
import ScoreBreakdown from './components/ScoreBreakdown'
import FeedbackPanel from './components/FeedbackPanel'
import LoadingSpinner from './components/LoadingSpinner'
import ErrorMessage from './components/ErrorMessage'
import ExampleButtons from './components/ExampleButtons'

function wordCount(text) {
  return text.trim() === '' ? 0 : text.trim().split(/\s+/).length
}

const SUGGESTIONS = {
  NETWORK_ERROR: 'Please check your connection and try again.',
  PROCESSING_ERROR: 'Please try again in a moment.',
}

const RETRYABLE = new Set(['RATE_LIMITED', 'NETWORK_ERROR', 'PROCESSING_ERROR'])

export default function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const isTextEmpty = wordCount(text) === 0

  function handleTextChange(newText) {
    setText(newText)
    if (result || error) {
      setResult(null)
      setError(null)
    }
  }

  async function handleSubmit() {
    if (wordCount(text) < 5) {
      setError({ message: 'Please enter at least 5 words.', code: 'INVALID_INPUT' })
      return
    }
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const data = await scoreText(text)
      setResult(data)
    } catch (err) {
      setError({
        message: err.message ?? 'An unexpected error occurred. Please try again.',
        code: err.code ?? 'PROCESSING_ERROR',
      })
    } finally {
      setLoading(false)
    }
  }

  async function handleRetry() {
    await handleSubmit()
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-3xl mx-auto px-4 py-3 sm:py-5">
          <h1 className="text-2xl font-bold text-blue-700">English Scorer</h1>
          <p className="text-sm text-gray-500 mt-1">
            Paste your English text below to get an instant proficiency score.
          </p>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-5 sm:py-8 flex flex-col gap-6">
        <section className="flex flex-col gap-4">
          <ExampleButtons onLoadExample={handleTextChange} />
          <TextInput text={text} onTextChange={handleTextChange} />
          <div className="flex gap-2 sm:justify-end">
            <button
              onClick={() => handleTextChange('')}
              disabled={isTextEmpty}
              className="flex-1 sm:flex-none px-4 py-2 rounded-lg border border-gray-300 text-gray-600 hover:border-red-400 hover:text-red-600 disabled:opacity-40 disabled:cursor-not-allowed transition-colors cursor-pointer"
            >
              Clear
            </button>
            <SubmitButton
              disabled={isTextEmpty}
              loading={loading}
              onClick={handleSubmit}
              className="w-full sm:w-auto"
            />
          </div>
        </section>

        {loading && <LoadingSpinner />}

        <ErrorMessage
          message={error?.message}
          suggestion={error ? (SUGGESTIONS[error.code] ?? null) : null}
          onRetry={error && RETRYABLE.has(error.code) ? handleRetry : null}
        />

        {result && (
          <section data-testid="results-section" className="flex flex-col gap-4 animate-[fade-in_0.4s_ease-out_both]">
            <div className="flex justify-end">
              <button
                onClick={() => exportPdf(result)}
                className="px-4 py-2 text-sm font-medium text-blue-700 border border-blue-300 rounded-lg hover:bg-blue-50 transition-colors"
              >
                Download PDF
              </button>
            </div>
            <OverallScore
              overallScore={result.overall_score}
              proficiencyLevel={result.proficiency_level}
              cefrLevel={result.cefr_level}
              confidenceLevel={result.confidence_level}
              wordCount={result.word_count}
            />
            <ScoreBreakdown scores={result.subcategory_scores} />
            <FeedbackPanel
              feedback={result.feedback}
              scores={result.subcategory_scores}
            />
          </section>
        )}
      </main>
    </div>
  )
}

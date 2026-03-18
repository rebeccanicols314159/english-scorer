export default function ErrorMessage({ message, suggestion, onRetry }) {
  if (!message) return null
  return (
    <div role="alert" className="bg-red-50 border border-red-300 text-red-700 rounded-lg p-4 text-sm">
      <p>{message}</p>
      {suggestion && <p className="mt-1 text-red-600">{suggestion}</p>}
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-3 px-3 py-2 text-sm font-medium text-red-700 border border-red-300 rounded hover:bg-red-100 transition-colors"
        >
          Try again
        </button>
      )}
    </div>
  )
}

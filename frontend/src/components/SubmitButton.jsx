export default function SubmitButton({ disabled, loading, onClick }) {
  const isDisabled = disabled || loading

  return (
    <button
      onClick={onClick}
      disabled={isDisabled}
      className={`px-8 py-3 rounded-lg font-semibold text-white transition-colors
        ${isDisabled
          ? 'bg-gray-400 cursor-not-allowed'
          : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'
        }`}
    >
      {loading ? 'Scoring…' : 'Score My English'}
    </button>
  )
}

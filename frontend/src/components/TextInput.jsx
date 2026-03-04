const MAX_WORDS = 2000
const WARN_THRESHOLD = 1800

function countWords(text) {
  return text.trim() === '' ? 0 : text.trim().split(/\s+/).length
}

export default function TextInput({ text, onTextChange }) {
  const wordCount = countWords(text)
  const isNearLimit = wordCount > WARN_THRESHOLD

  return (
    <div className="flex flex-col gap-2">
      <textarea
        className="w-full min-h-52 p-4 border border-gray-300 rounded-lg resize-y focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800 text-base"
        placeholder="Paste or type your English text here..."
        value={text}
        onChange={e => onTextChange(e.target.value)}
      />
      <p
        data-testid="word-counter"
        className={`text-sm ${isNearLimit ? 'text-orange-500 font-semibold' : 'text-gray-500'}`}
      >
        {wordCount} / {MAX_WORDS} words
      </p>
    </div>
  )
}

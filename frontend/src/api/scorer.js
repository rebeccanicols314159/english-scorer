import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL ?? '/api'

export class ScorerError extends Error {
  constructor(message, code) {
    super(message)
    this.name = 'ScorerError'
    this.code = code
  }
}

export async function scoreText(text) {
  try {
    const response = await axios.post(`${BASE_URL}/score`, { text })
    if (!response.data.success) {
      const { code, message } = response.data.error ?? {}
      throw new ScorerError(message ?? 'Scoring failed', code ?? 'PROCESSING_ERROR')
    }
    return response.data.data
  } catch (err) {
    if (err instanceof ScorerError) throw err
    const code = err.response?.data?.error?.code
    const message = err.response?.data?.error?.message
    if (message) throw new ScorerError(message, code ?? 'PROCESSING_ERROR')
    if (!err.response) {
      throw new ScorerError(
        'Unable to reach the server.',
        'NETWORK_ERROR'
      )
    }
    throw new ScorerError(
      err.message ?? 'An unexpected error occurred. Please try again.',
      'PROCESSING_ERROR'
    )
  }
}

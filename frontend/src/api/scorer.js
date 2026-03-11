import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL ?? '/api'

export async function scoreText(text) {
  try {
    const response = await axios.post(`${BASE_URL}/score`, { text })
    if (!response.data.success) {
      throw new Error(response.data.error?.message ?? 'Scoring failed')
    }
    return response.data.data
  } catch (err) {
    const message = err.response?.data?.error?.message
    throw new Error(message ?? err.message ?? 'An unexpected error occurred. Please try again.')
  }
}

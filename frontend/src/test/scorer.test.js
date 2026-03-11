import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import { scoreText } from '../api/scorer'

vi.mock('axios')

describe('scoreText', () => {
  beforeEach(() => vi.clearAllMocks())

  it('returns data on success', async () => {
    axios.post.mockResolvedValue({ data: { success: true, data: { overall_score: 7.5 } } })
    const result = await scoreText('some text')
    expect(result.overall_score).toBe(7.5)
  })

  it('throws the server error message on 422', async () => {
    const axiosError = Object.assign(new Error('Request failed with status code 422'), {
      response: { data: { success: false, error: { message: 'Text is too short. Please enter at least 5 words.' } } },
    })
    axios.post.mockRejectedValue(axiosError)
    await expect(scoreText('hi')).rejects.toThrow('Text is too short. Please enter at least 5 words.')
  })

  it('falls back to axios message when no server body', async () => {
    axios.post.mockRejectedValue(new Error('Network Error'))
    await expect(scoreText('hi')).rejects.toThrow('Network Error')
  })
})

import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import { scoreText, ScorerError } from '../api/scorer'

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

  it('falls back to network error message when no server body', async () => {
    axios.post.mockRejectedValue(new Error('Network Error'))
    const err = await scoreText('hi').catch(e => e)
    expect(err).toBeInstanceOf(ScorerError)
    expect(err.code).toBe('NETWORK_ERROR')
    expect(err.message).toMatch(/unable to reach/i)
  })

  it('throws ScorerError with code INVALID_INPUT on 422 INVALID_INPUT response', async () => {
    const axiosError = Object.assign(new Error('Request failed with status code 422'), {
      response: { data: { error: { code: 'INVALID_INPUT', message: 'Text is too short. Please enter at least 5 words.' } } },
    })
    axios.post.mockRejectedValue(axiosError)
    const err = await scoreText('hi').catch(e => e)
    expect(err).toBeInstanceOf(ScorerError)
    expect(err.code).toBe('INVALID_INPUT')
    expect(err.message).toBe('Text is too short. Please enter at least 5 words.')
  })

  it('throws ScorerError with code NOT_ENGLISH on 422 NOT_ENGLISH response', async () => {
    const axiosError = Object.assign(new Error('Request failed with status code 422'), {
      response: { data: { error: { code: 'NOT_ENGLISH', message: 'Text does not appear to be in English.' } } },
    })
    axios.post.mockRejectedValue(axiosError)
    const err = await scoreText('hi').catch(e => e)
    expect(err).toBeInstanceOf(ScorerError)
    expect(err.code).toBe('NOT_ENGLISH')
  })

  it('throws ScorerError with code RATE_LIMITED on 429 response', async () => {
    const axiosError = Object.assign(new Error('Request failed with status code 429'), {
      response: { data: { error: { code: 'RATE_LIMITED', message: 'Too many requests. Please wait a moment.' } } },
    })
    axios.post.mockRejectedValue(axiosError)
    const err = await scoreText('hi').catch(e => e)
    expect(err).toBeInstanceOf(ScorerError)
    expect(err.code).toBe('RATE_LIMITED')
  })

  it('throws ScorerError with code PROCESSING_ERROR on unexpected HTTP error', async () => {
    const axiosError = Object.assign(new Error('Request failed with status code 500'), {
      response: { status: 500, data: {} },
    })
    axios.post.mockRejectedValue(axiosError)
    const err = await scoreText('hi').catch(e => e)
    expect(err).toBeInstanceOf(ScorerError)
    expect(err.code).toBe('PROCESSING_ERROR')
  })

  it('ScorerError is exported and is instanceof Error', () => {
    const err = new ScorerError('msg', 'CODE')
    expect(err).toBeInstanceOf(ScorerError)
    expect(err).toBeInstanceOf(Error)
    expect(err.code).toBe('CODE')
    expect(err.message).toBe('msg')
  })
})

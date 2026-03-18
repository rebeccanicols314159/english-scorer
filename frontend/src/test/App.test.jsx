import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import App from '../App'
import * as scorer from '../api/scorer'
import * as pdfUtils from '../utils/exportPdf'

vi.mock('../api/scorer', async (importOriginal) => {
  const actual = await importOriginal()
  return { ...actual, scoreText: vi.fn() }
})

vi.mock('../utils/exportPdf')

const { ScorerError } = await import('../api/scorer')

const mockResult = {
  overall_score: 7.5,
  proficiency_level: 'Upper-Intermediate',
  subcategory_scores: {
    grammar: 8.0,
    vocabulary: 7.2,
    spelling_mechanics: 9.0,
    sentence_structure: 7.0,
    coherence_organization: 7.3,
    fluency_naturalness: 6.8,
  },
  feedback: {
    grammar: 'Excellent grammar.',
    vocabulary: 'Good vocab.',
    spelling_mechanics: 'Great spelling.',
    sentence_structure: 'Good structure.',
    coherence_organization: 'Clear organisation.',
    fluency_naturalness: 'Natural phrasing.',
  },
  confidence_level: 'high',
  word_count: 45,
}

const VALID_TEXT =
  'The quick brown fox jumps over the lazy dog. ' +
  'This text is used for testing the English scorer application. ' +
  'It contains several sentences with varied vocabulary.'

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the app title', () => {
    render(<App />)
    expect(screen.getByText(/english scorer/i)).toBeInTheDocument()
  })

  it('renders the text input area', () => {
    render(<App />)
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('renders the submit button', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /score my english/i })).toBeInTheDocument()
  })

  it('submit button is disabled when text area is empty', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /score my english/i })).toBeDisabled()
  })

  it('submit button enables when text is entered', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    expect(screen.getByRole('button', { name: /score my english/i })).not.toBeDisabled()
  })

  it('shows loading state while scoring', async () => {
    scorer.scoreText.mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(mockResult), 100))
    )
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('displays results after successful scoring', async () => {
    scorer.scoreText.mockResolvedValue(mockResult)
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => expect(screen.getByText('7.5')).toBeInTheDocument())
    expect(screen.getByText(/upper-intermediate/i)).toBeInTheDocument()
  })

  it('displays subcategory scores after scoring', async () => {
    scorer.scoreText.mockResolvedValue(mockResult)
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => expect(screen.getByText('8.0')).toBeInTheDocument())
  })

  it('displays feedback after scoring', async () => {
    scorer.scoreText.mockResolvedValue(mockResult)
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => expect(screen.getByText(/excellent grammar/i)).toBeInTheDocument())
  })

  it('shows error message when API call fails', async () => {
    scorer.scoreText.mockRejectedValue(new Error('Network error'))
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => expect(screen.getByRole('alert')).toBeInTheDocument())
  })

  it('hides results section before scoring', () => {
    render(<App />)
    expect(screen.queryByTestId('results-section')).not.toBeInTheDocument()
  })

  it('shows results section after successful scoring', async () => {
    scorer.scoreText.mockResolvedValue(mockResult)
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() =>
      expect(screen.getByTestId('results-section')).toBeInTheDocument()
    )
  })

  it('renders example buttons', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /beginner/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /intermediate/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /advanced/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /proficient/i })).toBeInTheDocument()
  })

  it('clicking an example button populates the textarea', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.click(screen.getByRole('button', { name: /beginner/i }))
    expect(screen.getByRole('textbox').value.length).toBeGreaterThan(0)
  })

  it('clicking an example button enables the submit button', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.click(screen.getByRole('button', { name: /intermediate/i }))
    expect(screen.getByRole('button', { name: /score my english/i })).not.toBeDisabled()
  })

  it('renders the clear button', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /clear/i })).toBeInTheDocument()
  })

  it('clear button is disabled when text area is empty', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /clear/i })).toBeDisabled()
  })

  it('clear button empties the textarea', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /clear/i }))
    expect(screen.getByRole('textbox').value).toBe('')
  })

  it('clear button dismisses results', async () => {
    scorer.scoreText.mockResolvedValue(mockResult)
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByTestId('results-section'))
    await user.click(screen.getByRole('button', { name: /clear/i }))
    expect(screen.queryByTestId('results-section')).not.toBeInTheDocument()
  })

  it('clears error and results when user edits text after scoring', async () => {
    scorer.scoreText.mockResolvedValue(mockResult)
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByTestId('results-section'))
    await user.type(screen.getByRole('textbox'), ' more text')
    expect(screen.queryByTestId('results-section')).not.toBeInTheDocument()
  })

  it('shows no separate suggestion for RATE_LIMITED (message is self-contained)', async () => {
    scorer.scoreText.mockRejectedValue(new ScorerError('Too many requests. Please wait a moment before trying again.', 'RATE_LIMITED'))
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByRole('alert'))
    expect(screen.getByRole('alert')).toHaveTextContent(/too many requests/i)
    expect(screen.getByRole('alert').querySelectorAll('p')).toHaveLength(1)
  })

  it('shows no separate suggestion for NOT_ENGLISH (message is self-contained)', async () => {
    scorer.scoreText.mockRejectedValue(new ScorerError('Text does not appear to be in English. Please submit English text.', 'NOT_ENGLISH'))
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByRole('alert'))
    expect(screen.getByRole('alert')).toHaveTextContent(/does not appear to be in english/i)
    expect(screen.getByRole('alert').querySelectorAll('p')).toHaveLength(1)
  })

  it('shows suggestion for NETWORK_ERROR (message and suggestion are distinct)', async () => {
    scorer.scoreText.mockRejectedValue(new ScorerError('Unable to reach the server.', 'NETWORK_ERROR'))
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByRole('alert'))
    expect(screen.getByText(/please check your connection/i)).toBeInTheDocument()
  })

  it('shows retry button for RATE_LIMITED error', async () => {
    scorer.scoreText.mockRejectedValue(new ScorerError('Too many requests.', 'RATE_LIMITED'))
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByRole('alert'))
    expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument()
  })

  it('shows retry button for NETWORK_ERROR', async () => {
    scorer.scoreText.mockRejectedValue(new ScorerError('Unable to reach the server.', 'NETWORK_ERROR'))
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByRole('alert'))
    expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument()
  })

  it('does NOT show retry button for INVALID_INPUT error', async () => {
    scorer.scoreText.mockRejectedValue(new ScorerError('Text is too short.', 'INVALID_INPUT'))
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByRole('alert'))
    expect(screen.queryByRole('button', { name: /try again/i })).not.toBeInTheDocument()
  })

  it('does NOT show retry button for NOT_ENGLISH error', async () => {
    scorer.scoreText.mockRejectedValue(new ScorerError('Not English.', 'NOT_ENGLISH'))
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByRole('alert'))
    expect(screen.queryByRole('button', { name: /try again/i })).not.toBeInTheDocument()
  })

  it('shows client-side validation error when fewer than 5 words are entered', async () => {
    const scoreSpy = vi.spyOn(scorer, 'scoreText')
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), 'one two three')
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    expect(screen.getByRole('alert')).toHaveTextContent(/please enter at least 5 words/i)
    expect(scoreSpy).not.toHaveBeenCalled()
  })

  it('clears client-side validation error when user edits text', async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), 'one two three')
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByRole('alert'))
    await user.type(screen.getByRole('textbox'), ' more words')
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('Download PDF button not shown before scoring', () => {
    render(<App />)
    expect(screen.queryByRole('button', { name: /download pdf/i })).not.toBeInTheDocument()
  })

  it('Download PDF button shown after successful scoring', async () => {
    scorer.scoreText.mockResolvedValue(mockResult)
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() =>
      expect(screen.getByRole('button', { name: /download pdf/i })).toBeInTheDocument()
    )
  })

  it('clicking Download PDF button calls exportPdf with the result data', async () => {
    scorer.scoreText.mockResolvedValue(mockResult)
    pdfUtils.exportPdf.mockImplementation(() => {})
    const user = userEvent.setup()
    render(<App />)
    await user.type(screen.getByRole('textbox'), VALID_TEXT)
    await user.click(screen.getByRole('button', { name: /score my english/i }))
    await waitFor(() => screen.getByRole('button', { name: /download pdf/i }))
    await user.click(screen.getByRole('button', { name: /download pdf/i }))
    expect(pdfUtils.exportPdf).toHaveBeenCalledWith(mockResult)
  })
})

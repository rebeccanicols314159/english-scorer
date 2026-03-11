import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import App from '../App'
import * as scorer from '../api/scorer'

vi.mock('../api/scorer')

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
})

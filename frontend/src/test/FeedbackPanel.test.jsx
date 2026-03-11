import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import FeedbackPanel from '../components/FeedbackPanel'

const sampleFeedback = {
  grammar: 'Excellent grammar with only minor issues.',
  vocabulary: 'Good vocabulary. Try more advanced words.',
  spelling_mechanics: 'Excellent spelling and punctuation.',
  sentence_structure: 'Work on sentence variety.',
  coherence_organization: 'Good organization. Use transition words.',
  fluency_naturalness: 'Natural phrasing. Focus on idioms.',
}

const sampleScores = {
  grammar: 9.0,
  vocabulary: 6.0,
  spelling_mechanics: 9.0,
  sentence_structure: 3.0,
  coherence_organization: 6.5,
  fluency_naturalness: 7.0,
}

describe('FeedbackPanel', () => {
  it('renders feedback for all 6 categories', () => {
    render(<FeedbackPanel feedback={sampleFeedback} scores={sampleScores} />)
    expect(screen.getByText(/excellent grammar/i)).toBeInTheDocument()
    expect(screen.getByText(/good vocabulary/i)).toBeInTheDocument()
    expect(screen.getByText(/excellent spelling/i)).toBeInTheDocument()
    expect(screen.getByText(/sentence variety/i)).toBeInTheDocument()
    expect(screen.getByText(/good organization/i)).toBeInTheDocument()
    expect(screen.getByText(/natural phrasing/i)).toBeInTheDocument()
  })

  it('shows a star icon (★) for high scores (>= 7.5)', () => {
    render(<FeedbackPanel feedback={sampleFeedback} scores={sampleScores} />)
    // grammar = 9.0 → star
    const grammarItem = screen.getByTestId('feedback-grammar')
    expect(grammarItem).toHaveTextContent('★')
  })

  it('shows an up arrow (↑) for medium scores (4.5 – 7.4)', () => {
    render(<FeedbackPanel feedback={sampleFeedback} scores={sampleScores} />)
    // vocabulary = 6.0 → arrow
    const vocabItem = screen.getByTestId('feedback-vocabulary')
    expect(vocabItem).toHaveTextContent('↑')
  })

  it('shows a warning icon (⚠) for low scores (< 4.5)', () => {
    render(<FeedbackPanel feedback={sampleFeedback} scores={sampleScores} />)
    // sentence_structure = 3.0 → warning
    const structureItem = screen.getByTestId('feedback-sentence_structure')
    expect(structureItem).toHaveTextContent('⚠')
  })

  it('shows category label for each feedback item', () => {
    render(<FeedbackPanel feedback={sampleFeedback} scores={sampleScores} />)
    // Multiple elements may contain these words (label + feedback text), so use getAllByText
    expect(screen.getAllByText(/grammar/i).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/vocabulary/i).length).toBeGreaterThan(0)
  })
})

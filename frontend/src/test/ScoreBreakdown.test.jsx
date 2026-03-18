import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import ScoreBreakdown from '../components/ScoreBreakdown'

const sampleScores = {
  grammar: 8.0,
  vocabulary: 7.2,
  spelling_mechanics: 9.0,
  sentence_structure: 7.0,
  coherence_organization: 7.3,
  fluency_naturalness: 6.8,
}

describe('ScoreBreakdown', () => {
  it('renders all 6 category names', () => {
    render(<ScoreBreakdown scores={sampleScores} />)
    expect(screen.getByText(/grammar/i)).toBeInTheDocument()
    expect(screen.getByText(/vocabulary/i)).toBeInTheDocument()
    expect(screen.getByText(/spelling/i)).toBeInTheDocument()
    expect(screen.getByText(/sentence structure/i)).toBeInTheDocument()
    expect(screen.getByText(/coherence/i)).toBeInTheDocument()
    expect(screen.getByText(/fluency/i)).toBeInTheDocument()
  })

  it('displays the numerical score for each category', () => {
    render(<ScoreBreakdown scores={sampleScores} />)
    expect(screen.getByText('8.0')).toBeInTheDocument()
    expect(screen.getByText('7.2')).toBeInTheDocument()
    expect(screen.getByText('9.0')).toBeInTheDocument()
    expect(screen.getByText('7.0')).toBeInTheDocument()
    expect(screen.getByText('7.3')).toBeInTheDocument()
    expect(screen.getByText('6.8')).toBeInTheDocument()
  })

  it('renders 6 progress bars', () => {
    render(<ScoreBreakdown scores={sampleScores} />)
    const bars = screen.getAllByRole('progressbar')
    expect(bars).toHaveLength(6)
  })

  it('progress bar width reflects score proportion (score/10 * 100%)', () => {
    render(<ScoreBreakdown scores={sampleScores} />)
    // Grammar = 8.0 → --bar-width: 80%
    const bars = screen.getAllByRole('progressbar')
    const grammarBar = bars.find(b => b.getAttribute('aria-label')?.match(/grammar/i))
    expect(grammarBar.style.getPropertyValue('--bar-width')).toBe('80%')
  })

  it('high score bar has green color', () => {
    render(<ScoreBreakdown scores={{ ...sampleScores, grammar: 9.0 }} />)
    const bars = screen.getAllByRole('progressbar')
    const grammarBar = bars.find(b => b.getAttribute('aria-label')?.match(/grammar/i))
    expect(grammarBar).toHaveClass('bg-green-500')
  })

  it('medium score bar has yellow color', () => {
    render(<ScoreBreakdown scores={{ ...sampleScores, vocabulary: 6.0 }} />)
    const bars = screen.getAllByRole('progressbar')
    const vocabBar = bars.find(b => b.getAttribute('aria-label')?.match(/vocabulary/i))
    expect(vocabBar).toHaveClass('bg-yellow-400')
  })

  it('low score bar has red color', () => {
    render(<ScoreBreakdown scores={{ ...sampleScores, fluency_naturalness: 3.0 }} />)
    const bars = screen.getAllByRole('progressbar')
    const fluencyBar = bars.find(b => b.getAttribute('aria-label')?.match(/fluency/i))
    expect(fluencyBar).toHaveClass('bg-red-500')
  })
})

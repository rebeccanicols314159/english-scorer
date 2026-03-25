import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import OverallScore from '../components/OverallScore'

const defaultProps = {
  overallScore: 7.5,
  proficiencyLevel: 'Upper-Intermediate',
  cefrLevel: 'C1',
  confidenceLevel: 'high',
  wordCount: 150,
}

describe('OverallScore', () => {
  it('displays the overall score', () => {
    render(<OverallScore {...defaultProps} />)
    expect(screen.getByText('7.5')).toBeInTheDocument()
  })

  it('displays the proficiency level', () => {
    render(<OverallScore {...defaultProps} />)
    expect(screen.getByText(/upper-intermediate/i)).toBeInTheDocument()
  })

  it('displays the word count', () => {
    render(<OverallScore {...defaultProps} />)
    expect(screen.getByText(/150/)).toBeInTheDocument()
  })

  it('displays confidence level', () => {
    render(<OverallScore {...defaultProps} />)
    expect(screen.getByText(/high confidence/i)).toBeInTheDocument()
  })

  it('shows low confidence warning for "low" confidence', () => {
    render(<OverallScore {...defaultProps} confidenceLevel="low" />)
    expect(screen.getByText(/low confidence/i)).toBeInTheDocument()
  })

  it('shows "very high confidence" text', () => {
    render(<OverallScore {...defaultProps} confidenceLevel="very_high" />)
    expect(screen.getByText(/very high confidence/i)).toBeInTheDocument()
  })

  it('applies green color class for high score (>= 8)', () => {
    render(<OverallScore {...defaultProps} overallScore={8.5} />)
    expect(screen.getByTestId('overall-score-value')).toHaveClass('text-green-600')
  })

  it('applies yellow/orange color for medium score (5–7.9)', () => {
    render(<OverallScore {...defaultProps} overallScore={6.0} />)
    expect(screen.getByTestId('overall-score-value')).toHaveClass('text-yellow-500')
  })

  it('applies red color for low score (< 5)', () => {
    render(<OverallScore {...defaultProps} overallScore={3.0} />)
    expect(screen.getByTestId('overall-score-value')).toHaveClass('text-red-500')
  })

  it('shows score out of 10', () => {
    render(<OverallScore {...defaultProps} />)
    expect(screen.getByText(/\/ 10/)).toBeInTheDocument()
  })

  it('displays the CEFR level', () => {
    render(<OverallScore {...defaultProps} />)
    expect(screen.getByText(/C1/)).toBeInTheDocument()
  })

  it('renders without cefrLevel prop gracefully', () => {
    const { cefrLevel, ...propsWithoutCefr } = defaultProps
    render(<OverallScore {...propsWithoutCefr} />)
    expect(screen.getByText(/upper-intermediate/i)).toBeInTheDocument()
  })
})

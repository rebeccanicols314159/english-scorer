import { describe, it, expect, vi, beforeEach } from 'vitest'

const mockDoc = vi.hoisted(() => ({
  setFontSize: vi.fn(),
  setTextColor: vi.fn(),
  setFillColor: vi.fn(),
  text: vi.fn(),
  rect: vi.fn(),
  circle: vi.fn(),
  splitTextToSize: vi.fn((t) => [t]),
  save: vi.fn(),
}))

vi.mock('jspdf', () => ({ default: vi.fn(function () { return mockDoc }) }))

import { exportPdf } from '../utils/exportPdf'

const mockResult = {
  overall_score: 7.5,
  proficiency_level: 'Upper-Intermediate',
  cefr_level: 'C1',
  confidence_level: 'high',
  word_count: 145,
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
    vocabulary: 'Good vocabulary range.',
    spelling_mechanics: 'Great spelling.',
    sentence_structure: 'Good structure.',
    coherence_organization: 'Clear organisation.',
    fluency_naturalness: 'Natural phrasing.',
  },
}

// A result with one score in the red zone to test red colour paths
const lowScoreResult = {
  ...mockResult,
  subcategory_scores: { ...mockResult.subcategory_scores, grammar: 3.0 },
  feedback: { ...mockResult.feedback },
}

function allTextArgs() {
  return mockDoc.text.mock.calls.flatMap((args) => {
    const first = args[0]
    return Array.isArray(first) ? first : [first]
  })
}

describe('exportPdf', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('calls save() with a filename containing english-scorer-report and a timestamp', () => {
    exportPdf(mockResult)
    expect(mockDoc.save).toHaveBeenCalledWith(
      expect.stringMatching(/^english-scorer-report-\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}\.pdf$/)
    )
  })

  it('includes the report title in text()', () => {
    exportPdf(mockResult)
    expect(allTextArgs()).toEqual(expect.arrayContaining(['English Scorer Report']))
  })

  it('includes overall score in text()', () => {
    exportPdf(mockResult)
    expect(allTextArgs()).toEqual(expect.arrayContaining(['7.5 / 10']))
  })

  it('includes proficiency level in text()', () => {
    exportPdf(mockResult)
    expect(allTextArgs()).toEqual(
      expect.arrayContaining([expect.stringContaining('Upper-Intermediate')])
    )
  })

  it('includes CEFR level in the proficiency line', () => {
    exportPdf(mockResult)
    expect(allTextArgs()).toEqual(
      expect.arrayContaining([expect.stringContaining('C1')])
    )
  })

  it('omits CEFR prefix when cefr_level is absent', () => {
    const { cefr_level, ...resultWithoutCefr } = mockResult
    exportPdf(resultWithoutCefr)
    expect(allTextArgs()).toEqual(
      expect.arrayContaining([expect.stringContaining('Proficiency: Upper-Intermediate')])
    )
  })

  it('includes confidence level in text()', () => {
    exportPdf(mockResult)
    expect(allTextArgs()).toEqual(
      expect.arrayContaining([expect.stringContaining('High')])
    )
  })

  it('includes word count in text()', () => {
    exportPdf(mockResult)
    expect(allTextArgs()).toEqual(
      expect.arrayContaining([expect.stringContaining('145')])
    )
  })

  it('includes each of the 6 subcategory scores in text()', () => {
    exportPdf(mockResult)
    const texts = allTextArgs()
    expect(texts).toEqual(expect.arrayContaining([expect.stringContaining('Grammar')]))
    expect(texts).toEqual(expect.arrayContaining([expect.stringContaining('Vocabulary')]))
    expect(texts).toEqual(expect.arrayContaining([expect.stringContaining('Spelling & Mechanics')]))
    expect(texts).toEqual(expect.arrayContaining([expect.stringContaining('Sentence Structure')]))
    expect(texts).toEqual(expect.arrayContaining([expect.stringContaining('Coherence & Organisation')]))
    expect(texts).toEqual(expect.arrayContaining([expect.stringContaining('Fluency & Naturalness')]))
  })

  it('includes feedback text for each of the 6 categories in text()', () => {
    exportPdf(mockResult)
    const texts = allTextArgs()
    expect(texts).toEqual(expect.arrayContaining(['Excellent grammar.']))
    expect(texts).toEqual(expect.arrayContaining(['Good vocabulary range.']))
    expect(texts).toEqual(expect.arrayContaining(['Great spelling.']))
    expect(texts).toEqual(expect.arrayContaining(['Good structure.']))
    expect(texts).toEqual(expect.arrayContaining(['Clear organisation.']))
    expect(texts).toEqual(expect.arrayContaining(['Natural phrasing.']))
  })

  // --- coloured bars ---

  it('draws a grey background bar and a coloured fill bar for each of the 6 subcategories', () => {
    exportPdf(mockResult)
    // 6 grey backgrounds + 6 coloured fills = 12 rect calls
    expect(mockDoc.rect).toHaveBeenCalledTimes(12)
  })

  it('uses green fill colour for scores >= 7.5', () => {
    exportPdf(mockResult) // grammar 8.0 → green-500
    expect(mockDoc.setFillColor).toHaveBeenCalledWith(34, 197, 94)
  })

  it('uses yellow fill colour for scores between 4.5 and 7.5', () => {
    exportPdf(mockResult) // vocabulary 7.2 → yellow-400
    expect(mockDoc.setFillColor).toHaveBeenCalledWith(250, 204, 21)
  })

  it('uses red fill colour for scores below 4.5', () => {
    exportPdf(lowScoreResult) // grammar 3.0 → red-500
    expect(mockDoc.setFillColor).toHaveBeenCalledWith(239, 68, 68)
  })

  it('sets grey fill colour for the bar track background', () => {
    exportPdf(mockResult)
    expect(mockDoc.setFillColor).toHaveBeenCalledWith(229, 231, 235)
  })

  // --- coloured feedback circles ---

  it('draws a coloured circle for each of the 6 feedback categories', () => {
    exportPdf(mockResult)
    expect(mockDoc.circle).toHaveBeenCalledTimes(6)
  })

  it('uses green-600 fill colour for high-score feedback circles', () => {
    exportPdf(mockResult) // grammar 8.0 → green-600
    expect(mockDoc.setFillColor).toHaveBeenCalledWith(22, 163, 74)
  })

  it('uses yellow-500 fill colour for medium-score feedback circles', () => {
    exportPdf(mockResult) // vocabulary 7.2 → yellow-500
    expect(mockDoc.setFillColor).toHaveBeenCalledWith(234, 179, 8)
  })

  it('uses red fill colour for low-score feedback circles', () => {
    exportPdf(lowScoreResult) // grammar 3.0 → red-500
    expect(mockDoc.setFillColor).toHaveBeenCalledWith(239, 68, 68)
  })

  it('resets text colour to black for non-icon text', () => {
    exportPdf(mockResult)
    expect(mockDoc.setTextColor).toHaveBeenCalledWith(0, 0, 0)
  })
})

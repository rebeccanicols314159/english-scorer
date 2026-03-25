import jsPDF from 'jspdf'

const CATEGORY_LABELS = {
  grammar: 'Grammar',
  vocabulary: 'Vocabulary',
  spelling_mechanics: 'Spelling & Mechanics',
  sentence_structure: 'Sentence Structure',
  coherence_organization: 'Coherence & Organisation',
  fluency_naturalness: 'Fluency & Naturalness',
}

// Matches barColor() in ScoreBreakdown.jsx (green-500 / yellow-400 / red-500)
function barColor(score) {
  if (score >= 7.5) return [34, 197, 94]
  if (score >= 4.5) return [250, 204, 21]
  return [239, 68, 68]
}

// Matches iconColor() in FeedbackPanel.jsx (green-600 / yellow-500 / red-500)
function iconColor(score) {
  if (score >= 7.5) return [22, 163, 74]
  if (score >= 4.5) return [234, 179, 8]
  return [239, 68, 68]
}

export function exportPdf(result) {
  const doc = new jsPDF()
  const now = new Date()
  const date = now.toLocaleDateString()
  const timestamp = now.toISOString().replace(/[:.]/g, '-').slice(0, 19)

  // Title + date
  doc.setTextColor(0, 0, 0)
  doc.setFontSize(16)
  doc.text('English Scorer Report', 20, 15)
  doc.setFontSize(8)
  doc.text(`Generated: ${date}`, 20, 22)

  // Overall Score (compact — three short lines)
  doc.setFontSize(13)
  doc.text('Overall Score', 20, 31)
  doc.setFontSize(11)
  doc.text(`${result.overall_score.toFixed(1)} / 10`, 20, 39)
  doc.setFontSize(9)
  const cefrPrefix = result.cefr_level ? `${result.cefr_level} – ` : ''
  doc.text(`Proficiency: ${cefrPrefix}${result.proficiency_level}`, 20, 46)
  const confidence = result.confidence_level.charAt(0).toUpperCase() + result.confidence_level.slice(1)
  doc.text(`${confidence} confidence · ${result.word_count} words`, 20, 52)

  // Score Breakdown with coloured progress bars
  doc.setFontSize(13)
  doc.text('Score Breakdown', 20, 62)
  doc.setFontSize(9)
  let y = 70
  for (const [key, score] of Object.entries(result.subcategory_scores)) {
    doc.setTextColor(0, 0, 0)
    doc.text(CATEGORY_LABELS[key], 20, y)
    doc.text(score.toFixed(1), 190, y, { align: 'right' })

    // Grey track
    doc.setFillColor(229, 231, 235)
    doc.rect(20, y + 1.5, 170, 2, 'F')

    // Coloured fill proportional to score
    const [r, g, b] = barColor(score)
    doc.setFillColor(r, g, b)
    doc.rect(20, y + 1.5, (score / 10) * 170, 2, 'F')

    y += 9
  }

  // Feedback with coloured circle indicators
  y += 4
  doc.setFontSize(13)
  doc.setTextColor(0, 0, 0)
  doc.text('Feedback', 20, y)
  y += 9
  for (const [key, text] of Object.entries(result.feedback)) {
    const score = result.subcategory_scores[key]
    const [ir, ig, ib] = iconColor(score)

    // Coloured filled circle as indicator (font-independent)
    doc.setFillColor(ir, ig, ib)
    doc.circle(22.5, y - 1.2, 1.5, 'F')

    // Category label in black
    doc.setFontSize(9)
    doc.setTextColor(0, 0, 0)
    doc.text(CATEGORY_LABELS[key], 27, y)
    y += 5

    // Feedback text
    doc.setFontSize(8)
    const lines = doc.splitTextToSize(text, 163)
    doc.text(lines, 27, y)
    y += lines.length * 4.5 + 4
  }

  doc.save(`english-scorer-report-${timestamp}.pdf`)
}

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import TextInput from '../components/TextInput'

describe('TextInput', () => {
  it('renders a textarea', () => {
    render(<TextInput text="" onTextChange={() => {}} />)
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('shows placeholder text', () => {
    render(<TextInput text="" onTextChange={() => {}} />)
    expect(screen.getByPlaceholderText(/paste or type/i)).toBeInTheDocument()
  })

  it('shows "0 / 2000 words" initially', () => {
    render(<TextInput text="" onTextChange={() => {}} />)
    expect(screen.getByText(/0 \/ 2000 words/i)).toBeInTheDocument()
  })

  it('shows correct word count for provided text', () => {
    render(<TextInput text="hello world foo" onTextChange={() => {}} />)
    expect(screen.getByText(/3 \/ 2000 words/i)).toBeInTheDocument()
  })

  it('calls onTextChange when user types', async () => {
    const user = userEvent.setup()
    const onTextChange = vi.fn()
    render(<TextInput text="" onTextChange={onTextChange} />)
    await user.type(screen.getByRole('textbox'), 'hello')
    expect(onTextChange).toHaveBeenCalled()
  })

  it('displays the current text value', () => {
    render(<TextInput text="some existing text" onTextChange={() => {}} />)
    expect(screen.getByRole('textbox')).toHaveValue('some existing text')
  })

  it('word counter turns warning color when over 1800 words', () => {
    const longText = Array(1801).fill('word').join(' ')
    render(<TextInput text={longText} onTextChange={() => {}} />)
    const counter = screen.getByTestId('word-counter')
    expect(counter).toHaveClass('text-orange-500')
  })

  it('word counter is normal color under 1800 words', () => {
    render(<TextInput text="hello world" onTextChange={() => {}} />)
    const counter = screen.getByTestId('word-counter')
    expect(counter).not.toHaveClass('text-orange-500')
  })
})

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import SubmitButton from '../components/SubmitButton'

describe('SubmitButton', () => {
  it('renders "Score My English" label', () => {
    render(<SubmitButton disabled={false} loading={false} onClick={() => {}} />)
    expect(screen.getByRole('button', { name: /score my english/i })).toBeInTheDocument()
  })

  it('is disabled when disabled prop is true', () => {
    render(<SubmitButton disabled={true} loading={false} onClick={() => {}} />)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('is enabled when disabled prop is false', () => {
    render(<SubmitButton disabled={false} loading={false} onClick={() => {}} />)
    expect(screen.getByRole('button')).not.toBeDisabled()
  })

  it('is disabled when loading', () => {
    render(<SubmitButton disabled={false} loading={true} onClick={() => {}} />)
    expect(screen.getByRole('button')).toBeDisabled()
  })

  it('shows loading text when loading', () => {
    render(<SubmitButton disabled={false} loading={true} onClick={() => {}} />)
    expect(screen.getByText(/scoring/i)).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup()
    const onClick = vi.fn()
    render(<SubmitButton disabled={false} loading={false} onClick={onClick} />)
    await user.click(screen.getByRole('button'))
    expect(onClick).toHaveBeenCalledOnce()
  })

  it('does not call onClick when disabled', async () => {
    const user = userEvent.setup()
    const onClick = vi.fn()
    render(<SubmitButton disabled={true} loading={false} onClick={onClick} />)
    await user.click(screen.getByRole('button'))
    expect(onClick).not.toHaveBeenCalled()
  })
})

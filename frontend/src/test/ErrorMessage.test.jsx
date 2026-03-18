import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import ErrorMessage from '../components/ErrorMessage'

describe('ErrorMessage', () => {
  it('renders the error message', () => {
    render(<ErrorMessage message="Something went wrong." />)
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument()
  })

  it('renders nothing when message is null', () => {
    const { container } = render(<ErrorMessage message={null} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('renders nothing when message is empty string', () => {
    const { container } = render(<ErrorMessage message="" />)
    expect(container).toBeEmptyDOMElement()
  })

  it('has an error role or alert role for accessibility', () => {
    render(<ErrorMessage message="Oops!" />)
    expect(screen.getByRole('alert')).toBeInTheDocument()
  })

  it('renders suggestion text when suggestion prop is provided', () => {
    render(<ErrorMessage message="Oops!" suggestion="Please try again." />)
    expect(screen.getByText(/please try again/i)).toBeInTheDocument()
  })

  it('does not render suggestion when suggestion is null', () => {
    render(<ErrorMessage message="Oops!" suggestion={null} />)
    expect(screen.queryByText(/please try again/i)).not.toBeInTheDocument()
  })

  it('renders a "Try again" button when onRetry is provided', () => {
    render(<ErrorMessage message="Oops!" onRetry={vi.fn()} />)
    expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument()
  })

  it('calls onRetry when "Try again" button is clicked', async () => {
    const user = userEvent.setup()
    const onRetry = vi.fn()
    render(<ErrorMessage message="Oops!" onRetry={onRetry} />)
    await user.click(screen.getByRole('button', { name: /try again/i }))
    expect(onRetry).toHaveBeenCalledOnce()
  })

  it('does not render a "Try again" button when onRetry is not provided', () => {
    render(<ErrorMessage message="Oops!" />)
    expect(screen.queryByRole('button')).not.toBeInTheDocument()
  })
})

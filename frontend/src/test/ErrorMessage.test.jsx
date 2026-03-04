import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
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
})

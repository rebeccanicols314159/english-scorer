import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import ExampleButtons from '../components/ExampleButtons'

describe('ExampleButtons', () => {
  it('renders the "Try an example:" label', () => {
    render(<ExampleButtons onLoadExample={() => {}} />)
    expect(screen.getByText(/try an example/i)).toBeInTheDocument()
  })

  it('renders Beginner button', () => {
    render(<ExampleButtons onLoadExample={() => {}} />)
    expect(screen.getByRole('button', { name: /beginner/i })).toBeInTheDocument()
  })

  it('renders Intermediate button', () => {
    render(<ExampleButtons onLoadExample={() => {}} />)
    expect(screen.getByRole('button', { name: /intermediate/i })).toBeInTheDocument()
  })

  it('renders Advanced button', () => {
    render(<ExampleButtons onLoadExample={() => {}} />)
    expect(screen.getByRole('button', { name: /advanced/i })).toBeInTheDocument()
  })

  it('renders Proficient button', () => {
    render(<ExampleButtons onLoadExample={() => {}} />)
    expect(screen.getByRole('button', { name: /proficient/i })).toBeInTheDocument()
  })

  it('calls onLoadExample with non-empty text when Beginner is clicked', async () => {
    const user = userEvent.setup()
    const onLoadExample = vi.fn()
    render(<ExampleButtons onLoadExample={onLoadExample} />)
    await user.click(screen.getByRole('button', { name: /beginner/i }))
    expect(onLoadExample).toHaveBeenCalledOnce()
    expect(onLoadExample.mock.calls[0][0].length).toBeGreaterThan(0)
  })

  it('calls onLoadExample with non-empty text when Intermediate is clicked', async () => {
    const user = userEvent.setup()
    const onLoadExample = vi.fn()
    render(<ExampleButtons onLoadExample={onLoadExample} />)
    await user.click(screen.getByRole('button', { name: /intermediate/i }))
    expect(onLoadExample).toHaveBeenCalledOnce()
    expect(onLoadExample.mock.calls[0][0].length).toBeGreaterThan(0)
  })

  it('calls onLoadExample with non-empty text when Advanced is clicked', async () => {
    const user = userEvent.setup()
    const onLoadExample = vi.fn()
    render(<ExampleButtons onLoadExample={onLoadExample} />)
    await user.click(screen.getByRole('button', { name: /advanced/i }))
    expect(onLoadExample).toHaveBeenCalledOnce()
    expect(onLoadExample.mock.calls[0][0].length).toBeGreaterThan(0)
  })

  it('calls onLoadExample with non-empty text when Proficient is clicked', async () => {
    const user = userEvent.setup()
    const onLoadExample = vi.fn()
    render(<ExampleButtons onLoadExample={onLoadExample} />)
    await user.click(screen.getByRole('button', { name: /proficient/i }))
    expect(onLoadExample).toHaveBeenCalledOnce()
    expect(onLoadExample.mock.calls[0][0].length).toBeGreaterThan(0)
  })

  it('each button loads different text', async () => {
    const user = userEvent.setup()
    const texts = []
    const onLoadExample = vi.fn(t => texts.push(t))
    render(<ExampleButtons onLoadExample={onLoadExample} />)
    await user.click(screen.getByRole('button', { name: /beginner/i }))
    await user.click(screen.getByRole('button', { name: /intermediate/i }))
    await user.click(screen.getByRole('button', { name: /advanced/i }))
    await user.click(screen.getByRole('button', { name: /proficient/i }))
    expect(new Set(texts).size).toBe(4)
  })
})

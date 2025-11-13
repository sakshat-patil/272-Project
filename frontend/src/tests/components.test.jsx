import { describe, it, expect } from 'vitest'
import { renderWithProviders } from './utils'
import { screen } from '@testing-library/react'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import Alert from '../components/ui/Alert'

describe('Button Component', () => {
  it('should render button with text', () => {
    renderWithProviders(<Button>Click Me</Button>)
    expect(screen.getByText('Click Me')).toBeInTheDocument()
  })

  it('should render primary variant by default', () => {
    renderWithProviders(<Button>Primary</Button>)
    const button = screen.getByText('Primary')
    expect(button).toHaveClass('bg-primary')
  })

  it('should render secondary variant', () => {
    renderWithProviders(<Button variant="secondary">Secondary</Button>)
    const button = screen.getByText('Secondary')
    expect(button).toHaveClass('bg-secondary')
  })

  it('should be disabled when disabled prop is true', () => {
    renderWithProviders(<Button disabled>Disabled</Button>)
    const button = screen.getByText('Disabled')
    expect(button).toBeDisabled()
  })
})

describe('Input Component', () => {
  it('should render input field', () => {
    renderWithProviders(<Input placeholder="Enter text" />)
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument()
  })

  it('should render with error styling', () => {
    renderWithProviders(<Input className="border-red-300" />)
    const input = screen.getByRole('textbox')
    expect(input).toHaveClass('border-red-300')
  })

  it('should accept different input types', () => {
    const { rerender } = renderWithProviders(<Input type="email" data-testid="input" />)
    expect(screen.getByTestId('input')).toHaveAttribute('type', 'email')

    rerender(<Input type="password" data-testid="input" />)
    expect(screen.getByTestId('input')).toHaveAttribute('type', 'password')
  })
})

describe('Card Component', () => {
  it('should render card with children', () => {
    renderWithProviders(
      <Card>
        <div>Card Content</div>
      </Card>
    )
    expect(screen.getByText('Card Content')).toBeInTheDocument()
  })

  it('should apply custom className', () => {
    renderWithProviders(
      <Card className="custom-class">
        <div>Content</div>
      </Card>
    )
    const card = screen.getByText('Content').parentElement
    expect(card).toHaveClass('custom-class')
  })
})

describe('Badge Component', () => {
  it('should render badge with text', () => {
    renderWithProviders(<Badge>New</Badge>)
    expect(screen.getByText('New')).toBeInTheDocument()
  })

  it('should render different variants', () => {
    const { rerender } = renderWithProviders(<Badge variant="default">Default</Badge>)
    let badge = screen.getByText('Default')
    expect(badge).toHaveClass('bg-primary')

    rerender(<Badge variant="secondary">Secondary</Badge>)
    badge = screen.getByText('Secondary')
    expect(badge).toHaveClass('bg-secondary')

    rerender(<Badge variant="destructive">Destructive</Badge>)
    badge = screen.getByText('Destructive')
    expect(badge).toHaveClass('bg-destructive')
  })
})

describe('Alert Component', () => {
  it('should render alert with message', () => {
    renderWithProviders(<Alert>Alert Message</Alert>)
    expect(screen.getByText('Alert Message')).toBeInTheDocument()
  })

  it('should render different variants', () => {
    const { rerender } = renderWithProviders(
      <Alert variant="success">Success message</Alert>
    )
    let alert = screen.getByRole('alert')
    expect(alert).toHaveClass('bg-green-50')

    rerender(<Alert variant="destructive">Error message</Alert>)
    alert = screen.getByRole('alert')
    expect(alert).toHaveClass('bg-destructive/10')

    rerender(<Alert variant="warning">Warning message</Alert>)
    alert = screen.getByRole('alert')
    expect(alert).toHaveClass('bg-yellow-50')
  })
})

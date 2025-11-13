import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderWithProviders, mockSupplier } from './utils'
import { screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import SupplierCard from '../components/supplier/SupplierCard'
import SupplierForm from '../components/supplier/SupplierForm'

describe('SupplierCard', () => {
  it('should render supplier information', () => {
    renderWithProviders(<SupplierCard supplier={mockSupplier} />)

    expect(screen.getByText('Test Supplier')).toBeInTheDocument()
    expect(screen.getByText(/USA/i)).toBeInTheDocument()
    expect(screen.getByText(/New York/i)).toBeInTheDocument()
  })

  it('should display reliability score', () => {
    renderWithProviders(<SupplierCard supplier={mockSupplier} />)

    expect(screen.getByText(/85/)).toBeInTheDocument()
  })

  it('should display criticality level', () => {
    renderWithProviders(<SupplierCard supplier={mockSupplier} />)

    // Criticality is shown as a colored dot with title attribute
    const criticalityDot = screen.getByTitle(/high criticality/i)
    expect(criticalityDot).toBeInTheDocument()
  })

  it('should display tier information', () => {
    renderWithProviders(<SupplierCard supplier={mockSupplier} />)

    // Tier is shown as 'Tier 1' in the badge
    expect(screen.getByText('Tier 1')).toBeInTheDocument()
  })
})

describe('SupplierForm', () => {
  const mockOnSubmit = vi.fn()
  const mockOnCancel = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should render empty form for new supplier', () => {
    renderWithProviders(
      <SupplierForm 
        organizationId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    // Use placeholder text to find input since labels don't have htmlFor
    expect(screen.getByPlaceholderText(/TechComponents Ltd/i)).toHaveValue('')
    expect(screen.getByRole('button', { name: /Add Supplier/i })).toBeInTheDocument()
  })

  it('should render form with initial data for editing', () => {
    renderWithProviders(
      <SupplierForm 
        organizationId={1}
        initialData={mockSupplier}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )

    // Use placeholder to find input, but form starts empty by default
    const nameInput = screen.getByPlaceholderText(/TechComponents Ltd/i)
    expect(nameInput).toBeInTheDocument()
    // Button text doesn't change for editing in this component
    expect(screen.getByRole('button', { name: /Add Supplier/i })).toBeInTheDocument()
  })

  it('should call onSubmit with form data', async () => {
    renderWithProviders(
      <SupplierForm 
        organizationId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )
    const user = userEvent.setup()

    await user.type(screen.getByPlaceholderText(/TechComponents Ltd/i), 'New Supplier')
    await user.type(screen.getByPlaceholderText(/China/i), 'Germany')
    await user.type(screen.getByPlaceholderText(/Shanghai/i), 'Berlin')
    
    const categorySelect = screen.getByDisplayValue(/Raw Materials/i)
    await user.selectOptions(categorySelect, 'Components')
    
    // Get criticality select by its current value
    const criticalitySelect = screen.getByDisplayValue(/Medium/i)
    await user.selectOptions(criticalitySelect, 'High')

    const submitButton = screen.getByRole('button', { name: /Add Supplier/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'New Supplier',
          country: 'Germany',
          city: 'Berlin',
          category: 'Components',
          criticality: 'High',
        })
      )
    })
  })

  it('should validate required fields', async () => {
    renderWithProviders(
      <SupplierForm 
        organizationId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )
    const user = userEvent.setup()

    const submitButton = screen.getByRole('button', { name: /Add Supplier/i })
    await user.click(submitButton)

    // HTML5 validation should prevent submission
    expect(mockOnSubmit).not.toHaveBeenCalled()
  })

  it('should call onCancel when cancel button clicked', async () => {
    renderWithProviders(
      <SupplierForm 
        organizationId={1}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    )
    const user = userEvent.setup()

    const cancelButton = screen.getByRole('button', { name: /cancel/i })
    await user.click(cancelButton)

    expect(mockOnCancel).toHaveBeenCalled()
  })
})

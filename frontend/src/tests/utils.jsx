/**
 * Test utilities and helper functions
 */
import { render } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from '../contexts/AuthContext'

/**
 * Custom render function that includes all necessary providers
 */
export function renderWithProviders(ui, options = {}) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })

  function Wrapper({ children }) {
    return (
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <AuthProvider>
            {children}
          </AuthProvider>
        </BrowserRouter>
      </QueryClientProvider>
    )
  }

  return render(ui, { wrapper: Wrapper, ...options })
}

/**
 * Mock user data
 */
export const mockUser = {
  id: 1,
  email: 'test@example.com',
  username: 'testuser',
  full_name: 'Test User',
  is_active: true,
  is_admin: false,
  created_at: '2024-01-01T00:00:00Z',
}

/**
 * Mock organization data
 */
export const mockOrganization = {
  id: 1,
  name: 'Test Corp',
  industry: 'technology',
  headquarters_location: 'San Francisco, CA',
  description: 'Test organization',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
}

/**
 * Mock supplier data
 */
export const mockSupplier = {
  id: 1,
  name: 'Test Supplier',
  country: 'USA',
  city: 'New York',
  category: 'manufacturing',
  criticality: 'high',
  tier: 1,
  lead_time_days: 30,
  reliability_score: 85.0,
  capacity_utilization: 70.0,
  organization_id: 1,
  created_at: '2024-01-01T00:00:00Z',
}

/**
 * Mock event data
 */
export const mockEvent = {
  id: 1,
  title: 'Port Disruption',
  description: 'Major port closure due to weather',
  event_type: 'natural_disaster',
  severity: 'high',
  status: 'active',
  organization_id: 1,
  created_at: '2024-01-01T00:00:00Z',
}

export * from '@testing-library/react'

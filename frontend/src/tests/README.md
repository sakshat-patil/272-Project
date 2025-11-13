# Frontend Unit Tests

This directory contains comprehensive unit tests for the frontend React application.

## Test Structure

- `setup.js` - Test environment configuration
- `utils.jsx` - Test utilities and helper functions
- `mocks/` - Mock data and axios mocks
- `auth.test.jsx` - Authentication component tests
- `organization.test.jsx` - Organization component tests
- `supplier.test.jsx` - Supplier component tests
- `components.test.jsx` - UI component tests
- `utils.test.js` - Utility function tests

## Running Tests

Install dependencies:
```bash
npm install
```

Run all tests:
```bash
npm test
```

Run tests with UI:
```bash
npm run test:ui
```

Run with coverage:
```bash
npm run test:coverage
```

Watch mode (auto-rerun on changes):
```bash
npm test -- --watch
```

## Test Coverage

The test suite covers:
- ✅ Authentication flow (login, signup, logout)
- ✅ Password strength validation
- ✅ Form validation and submission
- ✅ Organization components (card, form, list)
- ✅ Supplier components (card, form, list)
- ✅ UI components (Button, Input, Card, Badge, Alert)
- ✅ Utility functions (formatters, risk utils)
- ✅ Error handling
- ✅ User interactions

## Testing Library

We use:
- **Vitest** - Fast unit test framework
- **React Testing Library** - Component testing utilities
- **@testing-library/user-event** - User interaction simulation
- **jsdom** - DOM environment for tests

## Writing Tests

Example test structure:
```javascript
import { describe, it, expect } from 'vitest'
import { renderWithProviders } from './utils'
import { screen } from '@testing-library/react'
import MyComponent from '../components/MyComponent'

describe('MyComponent', () => {
  it('should render correctly', () => {
    renderWithProviders(<MyComponent />)
    expect(screen.getByText('Hello')).toBeInTheDocument()
  })
})
```

## Best Practices

1. Use `renderWithProviders` to wrap components with necessary providers
2. Use semantic queries (getByRole, getByLabelText) over test IDs
3. Test user behavior, not implementation details
4. Keep tests isolated and independent
5. Mock external dependencies (API calls, localStorage)

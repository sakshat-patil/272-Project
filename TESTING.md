# Testing Guide

This document provides instructions for running unit tests for both the backend and frontend of the Supply Chain Risk Monitor application.

## 📋 Overview

The project includes comprehensive unit tests covering:
- Authentication and authorization
- CRUD operations (Organizations, Suppliers, Events)
- Form validation and user interactions
- UI components
- Utility functions
- Password strength validation
- API endpoints

## 🔧 Backend Tests (Python/FastAPI)

### Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Activate your virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

3. Install test dependencies:
```bash
pip install -r requirements-test.txt
```

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run with verbose output:**
```bash
pytest -v
```

**Run with coverage report:**
```bash
pytest --cov=app --cov-report=html
```
Then open `htmlcov/index.html` in your browser to view the coverage report.

**Run specific test file:**
```bash
pytest tests/test_auth.py
pytest tests/test_organizations.py
pytest tests/test_suppliers.py
pytest tests/test_schemas.py
```

**Run specific test:**
```bash
pytest tests/test_auth.py::TestAuthEndpoints::test_login_success
```

**Run tests matching a pattern:**
```bash
pytest -k "password"  # Runs all tests with "password" in the name
```

### Backend Test Coverage

✅ **Authentication (`test_auth.py`):**
- Password hashing and verification
- JWT token creation
- User signup with validation
- User login with credentials
- Password strength requirements
- Duplicate username/email detection
- Unauthorized access handling

✅ **Organizations (`test_organizations.py`):**
- CRUD operations (Create, Read, Update, Delete)
- Authorization requirements
- Data validation

✅ **Suppliers (`test_suppliers.py`):**
- Supplier management
- Organization association
- Score validation

✅ **Schemas (`test_schemas.py`):**
- Pydantic validation
- Required fields
- Password complexity rules
- Email format validation

## 🎨 Frontend Tests (React/Vitest)

### Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies (including test libraries):
```bash
npm install
```

### Running Tests

**Run all tests:**
```bash
npm test
```

**Run with UI (interactive mode):**
```bash
npm run test:ui
```

**Run with coverage:**
```bash
npm run test:coverage
```
Coverage report will be generated in `coverage/` directory.

**Watch mode (auto-rerun on changes):**
```bash
npm test -- --watch
```

**Run specific test file:**
```bash
npm test auth.test.jsx
npm test organization.test.jsx
npm test supplier.test.jsx
npm test components.test.jsx
```

**Run tests matching a pattern:**
```bash
npm test -- --grep "password"
```

### Frontend Test Coverage

✅ **Authentication (`auth.test.jsx`):**
- Login form submission
- Signup form with password validation
- Password requirements display
- Password confirmation matching
- Authentication state management
- Error handling

✅ **Organizations (`organization.test.jsx`):**
- Organization card display
- Organization form validation
- Create/Edit functionality
- Form submission and cancellation

✅ **Suppliers (`supplier.test.jsx`):**
- Supplier card rendering
- Supplier form validation
- Reliability scores display
- Tier and criticality badges

✅ **UI Components (`components.test.jsx`):**
- Button variants and states
- Input field types and error states
- Card layouts
- Badge variants
- Alert messages

✅ **Utils (`utils.test.js`):**
- Date formatting
- Number formatting
- Currency formatting
- Risk color coding
- Risk level labels

## 🎯 Test Structure

### Backend
```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures and configuration
│   ├── test_auth.py         # Authentication tests
│   ├── test_organizations.py # Organization tests
│   ├── test_suppliers.py    # Supplier tests
│   └── test_schemas.py      # Schema validation tests
├── pytest.ini               # Pytest configuration
└── requirements-test.txt    # Test dependencies
```

### Frontend
```
frontend/
├── src/
│   └── tests/
│       ├── setup.js              # Test environment setup
│       ├── utils.jsx             # Test utilities
│       ├── mocks/
│       │   └── axios.js          # Axios mocks
│       ├── auth.test.jsx         # Auth component tests
│       ├── organization.test.jsx # Organization tests
│       ├── supplier.test.jsx     # Supplier tests
│       ├── components.test.jsx   # UI component tests
│       └── utils.test.js         # Utility function tests
└── vite.config.js           # Test configuration
```

## 📊 Continuous Integration

Both test suites are designed to run in CI/CD pipelines:

**Backend CI command:**
```bash
cd backend && pytest --cov=app --cov-report=xml
```

**Frontend CI command:**
```bash
cd frontend && npm test -- --run --coverage
```

## 🐛 Debugging Tests

### Backend
Use the `-s` flag to see print statements:
```bash
pytest -s tests/test_auth.py
```

Use `--pdb` to drop into debugger on failure:
```bash
pytest --pdb tests/test_auth.py
```

### Frontend
Add `console.log()` statements in tests and run:
```bash
npm test -- --reporter=verbose
```

Use the UI mode for easier debugging:
```bash
npm run test:ui
```

## 📝 Writing New Tests

### Backend Example
```python
def test_create_organization(client, auth_headers):
    """Test creating an organization"""
    response = client.post(
        "/api/organizations/",
        headers=auth_headers,
        json={
            "name": "Test Corp",
            "industry": "technology"
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Corp"
```

### Frontend Example
```javascript
it('should render component', () => {
  renderWithProviders(<MyComponent />)
  expect(screen.getByText('Hello')).toBeInTheDocument()
})
```

## ✅ Best Practices

1. **Run tests before committing** - Ensure all tests pass
2. **Write tests for new features** - Maintain test coverage
3. **Keep tests isolated** - Tests should not depend on each other
4. **Use descriptive test names** - Make test purpose clear
5. **Test edge cases** - Include error scenarios and boundary conditions
6. **Mock external dependencies** - Keep tests fast and reliable

## 🚀 Quick Start

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements-test.txt
pytest -v
```

**Frontend:**
```bash
cd frontend
npm install
npm test
```

## 📈 Coverage Goals

- Backend: >80% code coverage
- Frontend: >75% code coverage
- Critical paths (auth, CRUD): 100% coverage

---

For more information, see the README files in:
- `backend/tests/README.md`
- `frontend/src/tests/README.md`

# Backend Unit Tests

This directory contains comprehensive unit tests for the backend API.

## Test Structure

- `conftest.py` - Pytest fixtures and test configuration
- `test_auth.py` - Authentication and authorization tests
- `test_organizations.py` - Organization CRUD operation tests
- `test_suppliers.py` - Supplier CRUD operation tests
- `test_schemas.py` - Pydantic schema validation tests

## Running Tests

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_auth.py
```

Run specific test:
```bash
pytest tests/test_auth.py::TestAuthEndpoints::test_login_success
```

## Test Coverage

The test suite covers:
- ✅ Password hashing and verification
- ✅ JWT token creation and validation
- ✅ User authentication endpoints (signup, login, get current user)
- ✅ Password strength validation (8+ chars, uppercase, lowercase, number, special char)
- ✅ Organization CRUD operations
- ✅ Supplier CRUD operations
- ✅ Schema validation
- ✅ Error handling and edge cases
- ✅ Authorization requirements

## Test Database

Tests use an in-memory SQLite database that is created fresh for each test, ensuring test isolation and fast execution.

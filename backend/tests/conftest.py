"""
Pytest configuration and fixtures for testing
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.models import Base, User, Organization, Supplier, Event
from app.main import app
from app.auth import get_password_hash

# Create in-memory SQLite database for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with test database"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        hashed_password=get_password_hash("TestPassword123!"),
        is_active=True,
        is_admin=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin_user(db_session):
    """Create a test admin user"""
    user = User(
        email="admin@example.com",
        username="adminuser",
        full_name="Admin User",
        hashed_password=get_password_hash("AdminPassword123!"),
        is_active=True,
        is_admin=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user"""
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "TestPassword123!"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_organization(db_session, test_user):
    """Create a test organization"""
    from app.models import IndustryType, CriticalityLevel
    org = Organization(
        name="Test Corp",
        industry=IndustryType.ELECTRONICS,
        headquarters_location="San Francisco, CA",
        description="Test organization"
    )
    db_session.add(org)
    db_session.commit()
    db_session.refresh(org)
    return org


@pytest.fixture
def test_supplier(db_session, test_organization):
    """Create a test supplier"""
    from app.models import SupplierCategory, CriticalityLevel, SupplierTier
    supplier = Supplier(
        name="Test Supplier",
        country="USA",
        city="New York",
        category=SupplierCategory.COMPONENTS,
        criticality=CriticalityLevel.HIGH,
        tier=SupplierTier.TIER_1,
        lead_time_days=30,
        reliability_score=85.0,
        capacity_utilization=70.0,
        organization_id=test_organization.id
    )
    db_session.add(supplier)
    db_session.commit()
    db_session.refresh(supplier)
    return supplier

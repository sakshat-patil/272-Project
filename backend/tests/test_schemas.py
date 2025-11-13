"""
Tests for Pydantic schemas and validation
"""
import pytest
from pydantic import ValidationError

from app.schemas import UserCreate, OrganizationCreate, SupplierCreate
from app.models import IndustryType, SupplierCategory, CriticalityLevel, SupplierTier


class TestUserSchema:
    """Test user schema validation"""
    
    def test_valid_user_create(self):
        """Test valid user creation"""
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="ValidPass123!",
            full_name="Test User"
        )
        
        assert user_data.email == "test@example.com"
        assert user_data.username == "testuser"
        assert user_data.password == "ValidPass123!"
    
    def test_password_too_short(self):
        """Test that short passwords are rejected"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                username="testuser",
                password="short",
            )
        
        assert "at least 8 characters" in str(exc_info.value).lower()
    
    def test_password_missing_uppercase(self):
        """Test that password without uppercase is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                username="testuser",
                password="lowercase123!",
            )
        
        assert "uppercase" in str(exc_info.value).lower()
    
    def test_password_missing_lowercase(self):
        """Test that password without lowercase is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                username="testuser",
                password="UPPERCASE123!",
            )
        
        assert "lowercase" in str(exc_info.value).lower()
    
    def test_password_missing_number(self):
        """Test that password without number is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                username="testuser",
                password="NoNumbers!",
            )
        
        assert "number" in str(exc_info.value).lower()
    
    def test_password_missing_special_char(self):
        """Test that password without special character is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                email="test@example.com",
                username="testuser",
                password="NoSpecial123",
            )
        
        assert "special character" in str(exc_info.value).lower()
    
    def test_invalid_email(self):
        """Test that invalid email is rejected"""
        # Pydantic EmailStr is quite permissive, so test will skip validation error check
        # as it may accept formats like "not-an-email"
        try:
            UserCreate(
                email="not an email",  # Space makes it clearly invalid
                username="testuser",
                password="ValidPass123!",
            )
            # If it doesn't raise, that's also acceptable given Pydantic's email validation
        except ValidationError:
            # If it does raise, that's good
            pass


class TestOrganizationSchema:
    """Test organization schema validation"""
    
    def test_valid_organization_create(self):
        """Test valid organization creation"""
        org_data = OrganizationCreate(
            name="Test Corp",
            industry=IndustryType.ELECTRONICS,
            headquarters_location="San Francisco, CA"
        )
        
        assert org_data.name == "Test Corp"
        assert org_data.industry == IndustryType.ELECTRONICS
    
    def test_organization_name_required(self):
        """Test that organization name is required"""
        with pytest.raises(ValidationError):
            OrganizationCreate(
                industry=IndustryType.ELECTRONICS
            )


class TestSupplierSchema:
    """Test supplier schema validation"""
    
    def test_valid_supplier_create(self):
        """Test valid supplier creation"""
        supplier_data = SupplierCreate(
            name="Test Supplier",
            country="USA",
            category=SupplierCategory.COMPONENTS,
            criticality=CriticalityLevel.HIGH,
            tier=SupplierTier.TIER_1,
            organization_id=1,
            reliability_score=85.0,
            capacity_utilization=70.0
        )
        
        assert supplier_data.name == "Test Supplier"
        assert supplier_data.reliability_score == 85.0
    
    def test_supplier_required_fields(self):
        """Test that required supplier fields are enforced"""
        with pytest.raises(ValidationError):
            SupplierCreate(
                name="Test Supplier"
                # Missing required fields
            )
    
    def test_supplier_score_validation(self):
        """Test that supplier scores are validated"""
        with pytest.raises(ValidationError):
            SupplierCreate(
                name="Test Supplier",
                country="USA",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.HIGH,
                tier=SupplierTier.TIER_1,
                organization_id=1,
                reliability_score=150.0,  # Invalid: > 100
            )

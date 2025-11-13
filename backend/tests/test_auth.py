"""
Tests for authentication functionality
"""
import pytest
from fastapi import status

from app.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    authenticate_user,
    get_user_by_username,
    get_user_by_email
)


class TestPasswordHashing:
    """Test password hashing and verification"""
    
    def test_password_hash_and_verify(self):
        """Test that password hashing and verification work correctly"""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("WrongPassword123!", hashed) is False
    
    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes"""
        password = "TestPassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestJWTToken:
    """Test JWT token creation"""
    
    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0


class TestUserQueries:
    """Test user database queries"""
    
    def test_get_user_by_username(self, db_session, test_user):
        """Test getting user by username"""
        user = get_user_by_username(db_session, "testuser")
        
        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
    
    def test_get_user_by_username_not_found(self, db_session):
        """Test getting non-existent user by username"""
        user = get_user_by_username(db_session, "nonexistent")
        assert user is None
    
    def test_get_user_by_email(self, db_session, test_user):
        """Test getting user by email"""
        user = get_user_by_email(db_session, "test@example.com")
        
        assert user is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
    
    def test_get_user_by_email_not_found(self, db_session):
        """Test getting non-existent user by email"""
        user = get_user_by_email(db_session, "nonexistent@example.com")
        assert user is None


class TestAuthentication:
    """Test user authentication"""
    
    def test_authenticate_user_success(self, db_session, test_user):
        """Test successful user authentication"""
        user = authenticate_user(db_session, "testuser", "TestPassword123!")
        
        assert user is not None
        assert user.username == "testuser"
    
    def test_authenticate_user_wrong_password(self, db_session, test_user):
        """Test authentication with wrong password"""
        user = authenticate_user(db_session, "testuser", "WrongPassword123!")
        assert user is None
    
    def test_authenticate_user_wrong_username(self, db_session):
        """Test authentication with wrong username"""
        user = authenticate_user(db_session, "nonexistent", "TestPassword123!")
        assert user is None


class TestAuthEndpoints:
    """Test authentication API endpoints"""
    
    def test_signup_success(self, client):
        """Test successful user signup"""
        response = client.post(
            "/api/auth/signup/",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "NewPassword123!",
                "full_name": "New User"
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert data["full_name"] == "New User"
        assert "hashed_password" not in data
    
    def test_signup_duplicate_username(self, client, test_user):
        """Test signup with duplicate username"""
        response = client.post(
            "/api/auth/signup/",
            json={
                "email": "another@example.com",
                "username": "testuser",  # Already exists
                "password": "Password123!",
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username already registered" in response.json()["detail"]
    
    def test_signup_duplicate_email(self, client, test_user):
        """Test signup with duplicate email"""
        response = client.post(
            "/api/auth/signup/",
            json={
                "email": "test@example.com",  # Already exists
                "username": "anotheruser",
                "password": "Password123!",
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_signup_weak_password(self, client):
        """Test signup with weak password (missing requirements)"""
        response = client.post(
            "/api/auth/signup/",
            json={
                "email": "weak@example.com",
                "username": "weakuser",
                "password": "weak",  # Too short, no uppercase, no special char
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "TestPassword123!"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password"""
        response = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "WrongPassword123!"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post(
            "/api/auth/login",
            data={"username": "nonexistent", "password": "Password123!"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user info"""
        response = client.get("/api/auth/me/", headers=auth_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without token"""
        response = client.get("/api/auth/me/")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

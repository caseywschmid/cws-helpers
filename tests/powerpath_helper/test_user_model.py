"""
Tests for the PowerPath User model.

This module contains tests for the PowerPathUser model.
"""

import pytest
from datetime import datetime
from uuid import UUID

from cws_helpers.powerpath_helper.models import PowerPathUser


def test_user_model_creation():
    """Test that we can create a user model with required fields."""
    user = PowerPathUser(
        email="test@example.com",
        givenName="John",
        familyName="Doe"
    )
    
    assert user.email == "test@example.com"
    assert user.given_name == "John"
    assert user.family_name == "Doe"


def test_user_model_with_all_fields():
    """Test that we can create a user model with all fields."""
    user = PowerPathUser(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        email="test@example.com",
        givenName="John",
        familyName="Doe",
        username="johndoe",
        preferredFirstName="Johnny",
        preferredLastName="D",
        preferredMiddleName="A",
        middleName="Adam",
        status="active",
        grades="9,10,11",
        pronouns="he/him",
        phone="123-456-7890",
        sms="123-456-7890",
        readingLevel=5,
        dateLastModified=datetime(2023, 1, 1)
    )
    
    assert user.id == 123
    assert user.uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert user.email == "test@example.com"
    assert user.given_name == "John"
    assert user.family_name == "Doe"
    assert user.username == "johndoe"
    assert user.preferred_first_name == "Johnny"
    assert user.preferred_last_name == "D"
    assert user.preferred_middle_name == "A"
    assert user.middle_name == "Adam"
    assert user.status == "active"
    assert user.grades == "9,10,11"
    assert user.pronouns == "he/him"
    assert user.phone == "123-456-7890"
    assert user.sms == "123-456-7890"
    assert user.reading_level == 5
    assert user.date_last_modified == datetime(2023, 1, 1)


def test_user_model_email_validation():
    """Test that email validation works."""
    # Valid email should work
    user = PowerPathUser(
        email="test@example.com",
        givenName="John",
        familyName="Doe"
    )
    assert user.email == "test@example.com"
    
    # Invalid email should raise ValueError
    with pytest.raises(ValueError, match="Invalid email format"):
        PowerPathUser(
            email="invalid-email",
            givenName="John",
            familyName="Doe"
        )


def test_user_model_to_create_dict():
    """Test that to_create_dict works correctly."""
    user = PowerPathUser(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        email="test@example.com",
        givenName="John",
        familyName="Doe",
        username="johndoe",
        dateLastModified=datetime(2023, 1, 1)
    )
    
    create_dict = user.to_create_dict()
    
    # These fields should be excluded
    assert "id" not in create_dict
    assert "uuid" not in create_dict
    assert "dateLastModified" not in create_dict
    
    # These fields should be included
    assert create_dict["email"] == "test@example.com"
    assert create_dict["givenName"] == "John"
    assert create_dict["familyName"] == "Doe"
    assert create_dict["username"] == "johndoe"


def test_user_model_to_update_dict():
    """Test that to_update_dict works correctly."""
    user = PowerPathUser(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        email="test@example.com",
        givenName="John",
        familyName="Doe",
        username=None,  # This should be excluded because it's None
        dateLastModified=datetime(2023, 1, 1)
    )
    
    update_dict = user.to_update_dict()
    
    # These fields should be excluded
    assert "id" not in update_dict
    assert "uuid" not in update_dict
    assert "dateLastModified" not in update_dict
    assert "username" not in update_dict  # None values should be excluded
    
    # These fields should be included
    assert update_dict["email"] == "test@example.com"
    assert update_dict["givenName"] == "John"
    assert update_dict["familyName"] == "Doe" 
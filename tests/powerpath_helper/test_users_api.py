"""
Tests for the User API functions.

This module contains tests for the User API functions in the PowerPath API.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from cws_helpers.powerpath_helper import PowerPathClient, PowerPathUser
from cws_helpers.powerpath_helper.api.users import (
    get_all_users,
    search_users,
    list_users,
    get_user,
    create_user,
    update_user,
    delete_user
)


@pytest.fixture
def mock_client():
    """
    Create a mock PowerPath client for testing.
    
    Returns:
        MagicMock: A mock PowerPath client
    """
    client = MagicMock(spec=PowerPathClient)
    return client


@pytest.fixture
def sample_user_data():
    """
    Create sample user data for testing.
    
    Returns:
        dict: Sample user data
    """
    return {
        "id": 123,
        "uuid": "550e8400-e29b-41d4-a716-446655440000",
        "email": "user@example.com",
        "givenName": "John",
        "familyName": "Doe",
        "username": "johndoe",
        "status": "active",
        "grades": "9,10,11",
        "pronouns": "he/him",
        "phone": "555-123-4567",
        "sms": "555-123-4567",
        "readingLevel": 5,
        "dateLastModified": "2023-01-01T12:00:00Z"
    }


@pytest.fixture
def sample_list_user_data():
    """
    Create sample list user data for testing.
    
    Returns:
        list: Sample list user data
    """
    return [
        {
            "id": 123,
            "email": "user@example.com",
            "givenName": "John",
            "familyName": "Doe"
        },
        {
            "id": 124,
            "email": "user2@example.com",
            "givenName": "Jane",
            "familyName": "Doe"
        }
    ]


def test_get_all_users(mock_client, sample_user_data):
    """
    Test getting all users.
    
    Args:
        mock_client: A mock PowerPath client
        sample_user_data: Sample user data
    """
    # Setup
    mock_client.get.return_value = [sample_user_data]
    
    # Execute
    result = get_all_users(mock_client)
    
    # Verify
    mock_client.get.assert_called_once_with("/users")
    assert len(result) == 1
    assert isinstance(result[0], PowerPathUser)
    assert result[0].id == sample_user_data["id"]
    assert result[0].email == sample_user_data["email"]
    assert result[0].given_name == sample_user_data["givenName"]
    assert result[0].family_name == sample_user_data["familyName"]
    assert result[0].username == sample_user_data["username"]
    assert result[0].status == sample_user_data["status"]


def test_search_users(mock_client, sample_user_data):
    """
    Test searching for users by exact parameter matching.
    
    Args:
        mock_client: A mock PowerPath client
        sample_user_data: Sample user data
    """
    # Setup
    search_params = {"email": "user@example.com"}
    mock_client.get.return_value = [sample_user_data]
    
    # Execute
    result = search_users(mock_client, search_params)
    
    # Verify
    mock_client.get.assert_called_once_with("/users", params=search_params)
    assert len(result) == 1
    assert isinstance(result[0], PowerPathUser)
    assert result[0].id == sample_user_data["id"]
    assert result[0].email == sample_user_data["email"]
    assert result[0].given_name == sample_user_data["givenName"]
    assert result[0].family_name == sample_user_data["familyName"]


def test_list_users(mock_client, sample_list_user_data):
    """
    Test listing users by search term with pagination.
    
    Args:
        mock_client: A mock PowerPath client
        sample_list_user_data: Sample list user data
    """
    # Setup
    term = "doe"
    limit = 10
    offset = 0
    mock_client.get.return_value = sample_list_user_data
    
    # Execute
    result = list_users(mock_client, term, limit, offset)
    
    # Verify
    mock_client.get.assert_called_once_with("/users/list", params={"term": term, "limit": limit, "offset": offset})
    assert result == sample_list_user_data
    assert len(result) == 2
    assert result[0]["email"] == "user@example.com"
    assert result[1]["email"] == "user2@example.com"


def test_get_user(mock_client, sample_user_data):
    """
    Test getting a specific user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_user_data: Sample user data
    """
    # Setup
    user_id = "123"
    mock_client.get.return_value = sample_user_data
    
    # Execute
    result = get_user(mock_client, user_id)
    
    # Verify
    mock_client.get.assert_called_once_with(f"/users/{user_id}")
    assert isinstance(result, PowerPathUser)
    assert result.id == sample_user_data["id"]
    assert result.email == sample_user_data["email"]
    assert result.given_name == sample_user_data["givenName"]
    assert result.family_name == sample_user_data["familyName"]
    assert result.username == sample_user_data["username"]
    assert result.status == sample_user_data["status"]


def test_create_user(mock_client, sample_user_data):
    """
    Test creating a new user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_user_data: Sample user data
    """
    # Setup
    user_data = {
        "email": "user@example.com",
        "givenName": "John",
        "familyName": "Doe",
        "username": "johndoe",
        "status": "active"
    }
    mock_client.post.return_value = sample_user_data
    
    # Execute
    result = create_user(mock_client, user_data)
    
    # Verify
    mock_client.post.assert_called_once_with("/users", json_data=user_data)
    assert isinstance(result, PowerPathUser)
    assert result.id == sample_user_data["id"]
    assert result.email == sample_user_data["email"]
    assert result.given_name == sample_user_data["givenName"]
    assert result.family_name == sample_user_data["familyName"]
    assert result.username == sample_user_data["username"]
    assert result.status == sample_user_data["status"]


def test_update_user(mock_client, sample_user_data):
    """
    Test updating an existing user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_user_data: Sample user data
    """
    # Setup
    user_id = "123"
    user_data = {
        "email": "updated@example.com",
        "status": "inactive"
    }
    updated_user_data = sample_user_data.copy()
    updated_user_data["email"] = "updated@example.com"
    updated_user_data["status"] = "inactive"
    mock_client.patch.return_value = updated_user_data
    
    # Execute
    result = update_user(mock_client, user_id, user_data)
    
    # Verify
    mock_client.patch.assert_called_once_with(f"/users/{user_id}", json_data=user_data)
    assert isinstance(result, PowerPathUser)
    assert result.id == updated_user_data["id"]
    assert result.email == updated_user_data["email"]
    assert result.given_name == updated_user_data["givenName"]
    assert result.family_name == updated_user_data["familyName"]
    assert result.username == updated_user_data["username"]
    assert result.status == updated_user_data["status"]


def test_delete_user(mock_client):
    """
    Test deleting a user.
    
    Args:
        mock_client: A mock PowerPath client
    """
    # Setup
    user_id = "123"
    mock_client.delete.return_value = {"success": True}
    
    # Execute
    result = delete_user(mock_client, user_id)
    
    # Verify
    mock_client.delete.assert_called_once_with(f"/users/{user_id}")
    assert result == {"success": True} 
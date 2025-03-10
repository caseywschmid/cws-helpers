"""
Tests for the Goals API functions.

This module contains tests for the Goals API functions in the PowerPath API.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from cws_helpers.powerpath_helper import PowerPathClient, PowerPathGoal, PowerPathUser
from cws_helpers.powerpath_helper.api.goals import (
    get_user_goals,
    create_user_goal,
    update_user_goal,
    delete_user_goal,
    get_course_goals
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
def sample_goal_data():
    """
    Create sample goal data for testing.
    
    Returns:
        dict: Sample goal data
    """
    return {
        "id": 123,
        "description": "Complete 10 math exercises",
        "xp": 500,
        "userId": 456,
        "courseId": 789,
        "cutoffDate": "2023-12-31T23:59:59Z",
        "dailyOverride": 50,
        "createdAt": "2023-01-01T12:00:00Z",
        "updatedAt": "2023-01-01T12:00:00Z"
    }


@pytest.fixture
def sample_user_data():
    """
    Create sample user data for testing.
    
    Returns:
        dict: Sample user data
    """
    return {
        "id": 456,
        "email": "student@example.com",
        "givenName": "John",
        "familyName": "Doe",
        "username": "johndoe",
        "status": "active"
    }


def test_get_user_goals(mock_client, sample_goal_data):
    """
    Test getting goals for a user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_goal_data: Sample goal data
    """
    # Setup
    user_id = "456"
    mock_client.get.return_value = [sample_goal_data]
    
    # Execute
    result = get_user_goals(mock_client, user_id)
    
    # Verify
    mock_client.get.assert_called_once_with(f"/users/{user_id}/goals")
    assert len(result) == 1
    assert isinstance(result[0], PowerPathGoal)
    assert result[0].id == sample_goal_data["id"]
    assert result[0].description == sample_goal_data["description"]
    assert result[0].xp == sample_goal_data["xp"]
    assert result[0].user_id == sample_goal_data["userId"]
    assert result[0].course_id == sample_goal_data["courseId"]


def test_create_user_goal(mock_client, sample_goal_data):
    """
    Test creating a new goal for a user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_goal_data: Sample goal data
    """
    # Setup
    user_id = "456"
    goal_data = {
        "description": "Complete 10 math exercises",
        "xp": 500,
        "courseId": 789,
        "cutoffDate": "2023-12-31T23:59:59Z",
        "dailyOverride": 50
    }
    mock_client.post.return_value = sample_goal_data
    
    # Execute
    result = create_user_goal(mock_client, user_id, goal_data)
    
    # Verify
    mock_client.post.assert_called_once_with(f"/users/{user_id}/goals", json_data=goal_data)
    assert isinstance(result, PowerPathGoal)
    assert result.id == sample_goal_data["id"]
    assert result.description == sample_goal_data["description"]
    assert result.xp == sample_goal_data["xp"]
    assert result.user_id == sample_goal_data["userId"]
    assert result.course_id == sample_goal_data["courseId"]


def test_update_user_goal(mock_client, sample_goal_data):
    """
    Test updating an existing goal for a user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_goal_data: Sample goal data
    """
    # Setup
    user_id = "456"
    goal_id = "123"
    goal_data = {
        "description": "Complete 20 math exercises",
        "xp": 1000
    }
    updated_goal_data = sample_goal_data.copy()
    updated_goal_data["description"] = "Complete 20 math exercises"
    updated_goal_data["xp"] = 1000
    mock_client.patch.return_value = updated_goal_data
    
    # Execute
    result = update_user_goal(mock_client, user_id, goal_id, goal_data)
    
    # Verify
    mock_client.patch.assert_called_once_with(f"/users/{user_id}/goals/{goal_id}", json_data=goal_data)
    assert isinstance(result, PowerPathGoal)
    assert result.id == updated_goal_data["id"]
    assert result.description == updated_goal_data["description"]
    assert result.xp == updated_goal_data["xp"]
    assert result.user_id == updated_goal_data["userId"]
    assert result.course_id == updated_goal_data["courseId"]


def test_delete_user_goal(mock_client):
    """
    Test deleting a goal for a user.
    
    Args:
        mock_client: A mock PowerPath client
    """
    # Setup
    user_id = "456"
    goal_id = "123"
    mock_client.delete.return_value = {"success": True}
    
    # Execute
    result = delete_user_goal(mock_client, user_id, goal_id)
    
    # Verify
    mock_client.delete.assert_called_once_with(f"/users/{user_id}/goals/{goal_id}")
    assert result == {"success": True}


def test_get_course_goals(mock_client, sample_user_data):
    """
    Test getting goals for a course.
    
    Args:
        mock_client: A mock PowerPath client
        sample_user_data: Sample user data
    """
    # Setup
    course_id = "789"
    mock_client.get.return_value = [sample_user_data]
    
    # Execute
    result = get_course_goals(mock_client, course_id)
    
    # Verify
    mock_client.get.assert_called_once_with(f"/courses/{course_id}/goals")
    assert len(result) == 1
    assert isinstance(result[0], PowerPathUser)
    assert result[0].id == sample_user_data["id"]
    assert result[0].email == sample_user_data["email"]
    assert result[0].given_name == sample_user_data["givenName"]
    assert result[0].family_name == sample_user_data["familyName"]
    assert result[0].username == sample_user_data["username"]
    assert result[0].status == sample_user_data["status"] 
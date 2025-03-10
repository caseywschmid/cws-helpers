"""
Tests for the Progress API functions.

This module contains tests for the Progress API functions in the PowerPath API.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from cws_helpers.powerpath_helper import PowerPathClient, PowerPathModule
from cws_helpers.powerpath_helper.api.progress import (
    get_user_course_progress,
    get_user_course_progress_v2,
    get_user_module_progress,
    get_user_item_progress
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
def sample_module_data():
    """
    Create sample module data for testing.
    
    Returns:
        dict: Sample module data
    """
    return {
        "id": 123,
        "uuid": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Math Module 1",
        "state": "active",
        "items": [
            {
                "id": 456,
                "name": "Math Quiz 1",
                "contentType": "quiz",
                "xp": 100,
                "state": "active"
            },
            {
                "id": 457,
                "name": "Math Quiz 2",
                "contentType": "quiz",
                "xp": 150,
                "state": "active"
            }
        ]
    }


@pytest.fixture
def sample_item_progress_data():
    """
    Create sample item progress data for testing.
    
    Returns:
        dict: Sample item progress data
    """
    return {
        "id": 456,
        "name": "Math Quiz 1",
        "contentType": "quiz",
        "xp": 100,
        "state": "active",
        "metadata": {
            "completed": True,
            "score": 85,
            "attempts": 1
        }
    }


def test_get_user_course_progress(mock_client, sample_module_data):
    """
    Test getting course progress for a user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_module_data: Sample module data
    """
    # Setup
    user_id = "456"
    course_id = "789"
    mock_client.get.return_value = [sample_module_data]
    
    # Execute
    result = get_user_course_progress(mock_client, user_id, course_id)
    
    # Verify
    mock_client.get.assert_called_once_with(f"/users/{user_id}/courses/{course_id}")
    assert len(result) == 1
    assert isinstance(result[0], PowerPathModule)
    assert result[0].id == sample_module_data["id"]
    assert result[0].name == sample_module_data["name"]
    assert len(result[0].items) == 2
    assert result[0].items[0].id == sample_module_data["items"][0]["id"]
    assert result[0].items[1].id == sample_module_data["items"][1]["id"]


def test_get_user_course_progress_v2(mock_client, sample_module_data):
    """
    Test getting course progress for a user (v2 endpoint).
    
    Args:
        mock_client: A mock PowerPath client
        sample_module_data: Sample module data
    """
    # Setup
    user_id = "456"
    course_id = "789"
    mock_client.get.return_value = [sample_module_data]
    
    # Execute
    result = get_user_course_progress_v2(mock_client, user_id, course_id)
    
    # Verify
    mock_client.get.assert_called_once_with(f"/users/{user_id}/courses/{course_id}/v2")
    assert len(result) == 1
    assert isinstance(result[0], PowerPathModule)
    assert result[0].id == sample_module_data["id"]
    assert result[0].name == sample_module_data["name"]
    assert len(result[0].items) == 2
    assert result[0].items[0].id == sample_module_data["items"][0]["id"]
    assert result[0].items[1].id == sample_module_data["items"][1]["id"]


def test_get_user_module_progress(mock_client, sample_module_data):
    """
    Test getting module progress for a user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_module_data: Sample module data
    """
    # Setup
    user_id = "456"
    module_id = "123"
    mock_client.get.return_value = [sample_module_data]
    
    # Execute
    result = get_user_module_progress(mock_client, user_id, module_id)
    
    # Verify
    mock_client.get.assert_called_once_with(f"/users/{user_id}/modules/{module_id}")
    assert len(result) == 1
    assert isinstance(result[0], PowerPathModule)
    assert result[0].id == sample_module_data["id"]
    assert result[0].name == sample_module_data["name"]
    assert len(result[0].items) == 2
    assert result[0].items[0].id == sample_module_data["items"][0]["id"]
    assert result[0].items[1].id == sample_module_data["items"][1]["id"]


def test_get_user_item_progress(mock_client, sample_item_progress_data):
    """
    Test getting item progress for a user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_item_progress_data: Sample item progress data
    """
    # Setup
    user_id = "456"
    item_id = "456"
    mock_client.get.return_value = sample_item_progress_data
    
    # Execute
    result = get_user_item_progress(mock_client, user_id, item_id)
    
    # Verify
    mock_client.get.assert_called_once_with(f"/users/{user_id}/items/{item_id}")
    assert result == sample_item_progress_data
    assert result["id"] == sample_item_progress_data["id"]
    assert result["name"] == sample_item_progress_data["name"]
    assert result["metadata"]["completed"] == sample_item_progress_data["metadata"]["completed"]
    assert result["metadata"]["score"] == sample_item_progress_data["metadata"]["score"] 
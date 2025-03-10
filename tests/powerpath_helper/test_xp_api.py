"""
Tests for the XP API functions.

This module contains tests for the XP API functions in the PowerPath API.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

from cws_helpers.powerpath_helper import PowerPathClient, PowerPathXP
from cws_helpers.powerpath_helper.api.xp import get_user_xp, create_user_xp


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
def sample_xp_data():
    """
    Create sample XP data for testing.
    
    Returns:
        dict: Sample XP data
    """
    return {
        "id": 123,
        "uuid": "550e8400-e29b-41d4-a716-446655440000",
        "userId": 456,
        "user_uuid": "550e8400-e29b-41d4-a716-446655440001",
        "course_id": 789,
        "courseCode": "MATH101",
        "item_id": 101,
        "subject": "Mathematics",
        "amount": 100,
        "awardedOn": "2023-01-01T12:00:00Z",
        "appName": "PowerPath"
    }


def test_get_user_xp(mock_client, sample_xp_data):
    """
    Test getting XP records for a user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_xp_data: Sample XP data
    """
    # Setup
    user_id = "456"
    mock_client.get.return_value = [sample_xp_data]
    
    # Execute
    result = get_user_xp(mock_client, user_id)
    
    # Verify
    mock_client.get.assert_called_once_with(f"/users/{user_id}/xp", params={})
    assert len(result) == 1
    assert isinstance(result[0], PowerPathXP)
    assert result[0].id == sample_xp_data["id"]
    assert result[0].amount == sample_xp_data["amount"]
    assert result[0].subject == sample_xp_data["subject"]


def test_get_user_xp_with_filters(mock_client, sample_xp_data):
    """
    Test getting XP records for a user with filters.
    
    Args:
        mock_client: A mock PowerPath client
        sample_xp_data: Sample XP data
    """
    # Setup
    user_id = "456"
    course_id = "789"
    course_code = "MATH101"
    subject = "Mathematics"
    item_id = "101"
    mock_client.get.return_value = [sample_xp_data]
    
    # Execute - Test with course_id filter
    result = get_user_xp(mock_client, user_id, course_id=course_id)
    
    # Verify
    mock_client.get.assert_called_with(f"/users/{user_id}/xp", params={"courseId": course_id})
    assert len(result) == 1
    
    # Execute - Test with course_code filter
    result = get_user_xp(mock_client, user_id, course_code=course_code)
    
    # Verify
    mock_client.get.assert_called_with(f"/users/{user_id}/xp", params={"courseCode": course_code})
    assert len(result) == 1
    
    # Execute - Test with subject filter
    result = get_user_xp(mock_client, user_id, subject=subject)
    
    # Verify
    mock_client.get.assert_called_with(f"/users/{user_id}/xp", params={"subject": subject})
    assert len(result) == 1
    
    # Execute - Test with item_id filter
    result = get_user_xp(mock_client, user_id, item_id=item_id)
    
    # Verify
    mock_client.get.assert_called_with(f"/users/{user_id}/xp", params={"itemId": item_id})
    assert len(result) == 1
    
    # Execute - Test with multiple filters
    result = get_user_xp(
        mock_client, 
        user_id, 
        course_id=course_id, 
        course_code=course_code, 
        subject=subject, 
        item_id=item_id
    )
    
    # Verify
    mock_client.get.assert_called_with(
        f"/users/{user_id}/xp", 
        params={
            "courseId": course_id,
            "courseCode": course_code,
            "subject": subject,
            "itemId": item_id
        }
    )
    assert len(result) == 1


def test_create_user_xp(mock_client, sample_xp_data):
    """
    Test creating a new XP record for a user.
    
    Args:
        mock_client: A mock PowerPath client
        sample_xp_data: Sample XP data
    """
    # Setup
    user_id = "456"
    xp_data = {
        "amount": 100,
        "courseId": 789,
        "courseCode": "MATH101",
        "itemId": 101,
        "subject": "Mathematics",
        "appName": "PowerPath"
    }
    mock_client.post.return_value = sample_xp_data
    
    # Execute
    result = create_user_xp(mock_client, user_id, xp_data)
    
    # Verify
    mock_client.post.assert_called_once_with(f"/users/{user_id}/xp", json=xp_data)
    assert isinstance(result, PowerPathXP)
    assert result.id == sample_xp_data["id"]
    assert result.amount == sample_xp_data["amount"]
    assert result.subject == sample_xp_data["subject"] 
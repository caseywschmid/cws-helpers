"""
Tests for the PowerPath results API functions.

This module contains tests for the PowerPath results API functions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID
from datetime import datetime

from cws_helpers.powerpath_helper import (
    PowerPathClient,
    PowerPathResult,
    get_user_results,
    get_user_result,
    create_user_result,
    update_user_result,
    delete_user_result,
)

@pytest.fixture
def mock_client():
    """Create a mock PowerPath client."""
    client = MagicMock(spec=PowerPathClient)
    return client

@pytest.fixture
def sample_result_data():
    """Create sample result data for testing."""
    return {
        "id": 123,
        "userId": 456,
        "type": "assessment",
        "value": 85.5,
        "achievedLevel": "proficient",
        "status": "completed"
    }

def test_get_user_results(mock_client, sample_result_data):
    """Test getting results for a user."""
    # Setup
    mock_client.get_resources.return_value = [PowerPathResult(**sample_result_data)]
    
    # Execute
    result = get_user_results(mock_client, "456")
    
    # Verify
    mock_client.get_resources.assert_called_once_with("/users/456/results", PowerPathResult, params={})
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], PowerPathResult)
    assert result[0].id == 123
    assert result[0].user_id == 456
    assert result[0].type == "assessment"
    assert result[0].value == 85.5

def test_get_user_results_with_filters(mock_client, sample_result_data):
    """Test getting results for a user with filters."""
    # Setup
    mock_client.get_resources.return_value = [PowerPathResult(**sample_result_data)]
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    # Execute
    result = get_user_results(
        mock_client, 
        "456", 
        item_id="789", 
        cc_item_id="101112", 
        start_date=start_date, 
        end_date=end_date
    )
    
    # Verify
    mock_client.get_resources.assert_called_once_with(
        "/users/456/results", 
        PowerPathResult, 
        params={
            "itemId": "789",
            "ccItemId": "101112",
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat()
        }
    )
    assert isinstance(result, list)
    assert len(result) == 1

def test_get_user_result(mock_client, sample_result_data):
    """Test getting a specific result for a user."""
    # Setup
    mock_client.get_resource.return_value = PowerPathResult(**sample_result_data)
    
    # Execute
    result = get_user_result(mock_client, "456", "123")
    
    # Verify
    mock_client.get_resource.assert_called_once_with("/users/456/results/123", PowerPathResult)
    assert isinstance(result, PowerPathResult)
    assert result.id == 123
    assert result.user_id == 456
    assert result.type == "assessment"
    assert result.value == 85.5

def test_create_user_result(mock_client, sample_result_data):
    """Test creating a result for a user."""
    # Setup
    mock_client.create_resource.return_value = PowerPathResult(**sample_result_data)
    result_data = {
        "type": "assessment",
        "value": 85.5,
        "achievedLevel": "proficient",
        "status": "completed"
    }
    
    # Execute
    result = create_user_result(mock_client, "456", result_data)
    
    # Verify
    mock_client.create_resource.assert_called_once_with("/users/456/results", PowerPathResult, result_data)
    assert isinstance(result, PowerPathResult)
    assert result.id == 123
    assert result.user_id == 456
    assert result.type == "assessment"
    assert result.value == 85.5

def test_update_user_result(mock_client, sample_result_data):
    """Test updating a result for a user."""
    # Setup
    mock_client.patch.return_value = sample_result_data
    result_data = {
        "value": 90.0,
        "achievedLevel": "advanced"
    }
    
    # Execute
    result = update_user_result(mock_client, "456", "123", result_data)
    
    # Verify
    mock_client.patch.assert_called_once_with("/users/456/results/123", json_data=result_data)
    assert result == sample_result_data

def test_delete_user_result(mock_client):
    """Test deleting a result for a user."""
    # Setup
    mock_client.delete.return_value = {"success": True}
    
    # Execute
    result = delete_user_result(mock_client, "456", "123")
    
    # Verify
    mock_client.delete.assert_called_once_with("/users/456/results/123")
    assert result == {"success": True} 
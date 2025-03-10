"""
Tests for the PowerPath responses API functions.

This module contains tests for the PowerPath responses API functions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID

from cws_helpers.powerpath_helper import (
    PowerPathClient,
    PowerPathResponse,
    create_question_response,
    update_response,
    delete_response,
)

@pytest.fixture
def mock_client():
    """Create a mock PowerPath client."""
    client = MagicMock(spec=PowerPathClient)
    return client

@pytest.fixture
def sample_response_data():
    """Create sample response data for testing."""
    return {
        "id": 101,
        "ccItemId": 789,
        "label": "4",
        "isCorrect": True
    }

def test_create_question_response(mock_client, sample_response_data):
    """Test creating a response for a question."""
    # Setup
    mock_client.create_resource.return_value = PowerPathResponse(**sample_response_data)
    response_data = {"label": "4", "isCorrect": True}
    
    # Execute
    result = create_question_response(mock_client, "789", response_data)
    
    # Verify
    mock_client.create_resource.assert_called_once_with(
        "/modules/ccItem/789/responses", 
        PowerPathResponse, 
        response_data
    )
    assert isinstance(result, PowerPathResponse)
    assert result.id == 101
    assert result.cc_item_id == 789
    assert result.label == "4"
    assert result.is_correct == True

def test_update_response(mock_client, sample_response_data):
    """Test updating a response."""
    # Setup
    mock_client.put.return_value = sample_response_data
    response_data = {"label": "4", "isCorrect": True}
    
    # Execute
    result = update_response(mock_client, "101", response_data)
    
    # Verify
    mock_client.put.assert_called_once_with("/modules/responses/101", json_data=response_data)
    assert result == sample_response_data

def test_delete_response(mock_client):
    """Test deleting a response."""
    # Setup
    mock_client.delete.return_value = {"success": True}
    
    # Execute
    result = delete_response(mock_client, "101")
    
    # Verify
    mock_client.delete.assert_called_once_with("/modules/responses/101")
    assert result == {"success": True} 
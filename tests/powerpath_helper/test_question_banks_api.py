"""
Tests for the PowerPath question banks API functions.

This module contains tests for the PowerPath question banks API functions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID

from cws_helpers.powerpath_helper import (
    PowerPathClient,
    get_question_bank,
    create_question_bank_item,
    delete_question_bank_item,
    delete_object_bank,
)

@pytest.fixture
def mock_client():
    """Create a mock PowerPath client."""
    client = MagicMock(spec=PowerPathClient)
    return client

@pytest.fixture
def sample_question_bank_data():
    """Create sample question bank data for testing."""
    return [
        {
            "id": 789,
            "material": "What is 2+2?",
            "difficulty": 1
        },
        {
            "id": 790,
            "material": "What is 3+3?",
            "difficulty": 1
        }
    ]

def test_get_question_bank(mock_client, sample_question_bank_data):
    """Test getting the question bank for an item."""
    # Setup
    mock_client.get.return_value = sample_question_bank_data
    
    # Execute
    result = get_question_bank(mock_client, "123", "456")
    
    # Verify
    mock_client.get.assert_called_once_with("/modules/123/items/456/questionBank")
    assert result == sample_question_bank_data

def test_create_question_bank_item(mock_client):
    """Test creating a question bank item."""
    # Setup
    mock_client.post.return_value = {"id": 789, "material": "What is 2+2?", "difficulty": 1}
    question_data = {"material": "What is 2+2?", "difficulty": 1}
    
    # Execute
    result = create_question_bank_item(mock_client, "123", "456", question_data)
    
    # Verify
    mock_client.post.assert_called_once_with("/modules/123/items/questionBank", json_data=question_data)
    assert result == {"id": 789, "material": "What is 2+2?", "difficulty": 1}

def test_delete_question_bank_item(mock_client):
    """Test deleting a question bank item."""
    # Setup
    mock_client.delete.return_value = {"success": True}
    
    # Execute
    result = delete_question_bank_item(mock_client, "123", "456", "789")
    
    # Verify
    mock_client.delete.assert_called_once_with("/modules/123/items/456/questionBank/789")
    assert result == {"success": True}

def test_delete_object_bank(mock_client):
    """Test deleting the object bank for an item."""
    # Setup
    mock_client.delete.return_value = {"success": True}
    
    # Execute
    result = delete_object_bank(mock_client, "123", "456")
    
    # Verify
    mock_client.delete.assert_called_once_with("/modules/123/items/456/objectBank")
    assert result == {"success": True} 
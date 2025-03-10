"""
Tests for the PowerPath questions API functions.

This module contains tests for the PowerPath questions API functions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID

from cws_helpers.powerpath_helper import (
    PowerPathClient,
    PowerPathCCItem,
    get_question,
    create_question,
    update_question,
)

@pytest.fixture
def mock_client():
    """Create a mock PowerPath client."""
    client = MagicMock(spec=PowerPathClient)
    return client

@pytest.fixture
def sample_question_data():
    """Create sample question data for testing."""
    return {
        "id": 789,
        "uuid": "98765432-9876-5432-9876-987654321098",
        "material": "What is 2+2?",
        "difficulty": 1
    }

def test_get_question(mock_client, sample_question_data):
    """Test getting a question."""
    # Setup
    mock_client.get_resource.return_value = PowerPathCCItem(**sample_question_data)
    
    # Execute
    result = get_question(mock_client, "789")
    
    # Verify
    mock_client.get_resource.assert_called_once_with("/modules/ccItem/789", PowerPathCCItem)
    assert isinstance(result, PowerPathCCItem)
    assert result.id == 789
    assert result.material == "What is 2+2?"

def test_create_question(mock_client, sample_question_data):
    """Test creating a question."""
    # Setup
    mock_client.create_resource.return_value = PowerPathCCItem(**sample_question_data)
    question_data = {"material": "What is 2+2?", "difficulty": 1}
    
    # Execute
    result = create_question(mock_client, question_data)
    
    # Verify
    mock_client.create_resource.assert_called_once_with("/modules/ccItem", PowerPathCCItem, question_data)
    assert isinstance(result, PowerPathCCItem)
    assert result.id == 789
    assert result.material == "What is 2+2?"

def test_update_question(mock_client, sample_question_data):
    """Test updating a question."""
    # Setup
    mock_client.put.return_value = sample_question_data
    question_data = {"material": "What is 2+2?", "difficulty": 2}
    
    # Execute
    result = update_question(mock_client, "789", question_data)
    
    # Verify
    mock_client.put.assert_called_once_with("/modules/ccItem/789", json_data=question_data)
    assert result == sample_question_data 
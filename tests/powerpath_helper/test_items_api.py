"""
Tests for the PowerPath items API functions.

This module contains tests for the PowerPath items API functions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID

from cws_helpers.powerpath_helper import (
    PowerPathClient,
    PowerPathItem,
    get_module_items,
    get_module_item,
    create_module_item,
    update_module_items,
)

@pytest.fixture
def mock_client():
    """Create a mock PowerPath client."""
    client = MagicMock(spec=PowerPathClient)
    return client

@pytest.fixture
def sample_item_data():
    """Create sample item data for testing."""
    return {
        "id": 456,
        "uuid": "12345678-1234-5678-1234-567812345678",
        "name": "Test Item",
        "contentType": "article",
        "xp": 100
    }

def test_get_module_items(mock_client, sample_item_data):
    """Test getting all items in a module."""
    # Setup
    mock_client.get_resources.return_value = [PowerPathItem(**sample_item_data)]
    
    # Execute
    result = get_module_items(mock_client, "123")
    
    # Verify
    mock_client.get_resources.assert_called_once_with("/modules/123/items", PowerPathItem)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], PowerPathItem)
    assert result[0].id == 456
    assert result[0].name == "Test Item"

def test_get_module_item(mock_client, sample_item_data):
    """Test getting a specific item in a module."""
    # Setup
    mock_client.get_resource.return_value = PowerPathItem(**sample_item_data)
    
    # Execute
    result = get_module_item(mock_client, "123", "456")
    
    # Verify
    mock_client.get_resource.assert_called_once_with("/modules/123/items/456", PowerPathItem)
    assert isinstance(result, PowerPathItem)
    assert result.id == 456
    assert result.name == "Test Item"

def test_create_module_item(mock_client, sample_item_data):
    """Test creating a new item in a module."""
    # Setup
    mock_client.create_resource.return_value = PowerPathItem(**sample_item_data)
    item_data = {"name": "Test Item", "contentType": "article", "xp": 100}
    
    # Execute
    result = create_module_item(mock_client, "123", item_data)
    
    # Verify
    mock_client.create_resource.assert_called_once_with("/modules/123/items", PowerPathItem, item_data)
    assert isinstance(result, PowerPathItem)
    assert result.id == 456
    assert result.name == "Test Item"

def test_update_module_items(mock_client):
    """Test updating items in a module."""
    # Setup
    mock_client.put.return_value = {"success": True}
    items_data = [{"id": 456, "name": "Updated Item", "contentType": "article", "xp": 200}]
    
    # Execute
    result = update_module_items(mock_client, "123", items_data)
    
    # Verify
    mock_client.put.assert_called_once_with("/modules/123/items", json_data=items_data)
    assert result == {"success": True} 
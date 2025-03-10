"""
Tests for the PowerPath modules API functions.

This module contains tests for the PowerPath modules API functions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID

from cws_helpers.powerpath_helper import (
    PowerPathClient,
    PowerPathModule,
    get_all_modules,
    get_module,
    create_module,
    update_module,
    delete_module,
)

@pytest.fixture
def mock_client():
    """Create a mock PowerPath client."""
    client = MagicMock(spec=PowerPathClient)
    return client

@pytest.fixture
def sample_module_data():
    """Create sample module data for testing."""
    return {
        "id": 123,
        "uuid": "12345678-1234-5678-1234-567812345678",
        "name": "Test Module",
        "state": "active",
        "startingItemId": 456
    }

def test_get_all_modules(mock_client, sample_module_data):
    """Test getting all modules."""
    # Setup
    mock_client.get_resources.return_value = [PowerPathModule(**sample_module_data)]
    
    # Execute
    result = get_all_modules(mock_client)
    
    # Verify
    mock_client.get_resources.assert_called_once_with("/modules", PowerPathModule)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], PowerPathModule)
    assert result[0].id == 123
    assert result[0].name == "Test Module"

def test_get_module(mock_client, sample_module_data):
    """Test getting a module."""
    # Setup
    mock_client.get_resource.return_value = PowerPathModule(**sample_module_data)
    
    # Execute
    result = get_module(mock_client, "123")
    
    # Verify
    mock_client.get_resource.assert_called_once_with("/modules/123", PowerPathModule)
    assert isinstance(result, PowerPathModule)
    assert result.id == 123
    assert result.name == "Test Module"

def test_create_module(mock_client, sample_module_data):
    """Test creating a module."""
    # Setup
    mock_client.create_resource.return_value = PowerPathModule(**sample_module_data)
    module_data = {"name": "Test Module", "state": "active"}
    
    # Execute
    result = create_module(mock_client, module_data)
    
    # Verify
    mock_client.create_resource.assert_called_once_with("/modules", PowerPathModule, module_data)
    assert isinstance(result, PowerPathModule)
    assert result.id == 123
    assert result.name == "Test Module"

def test_update_module(mock_client, sample_module_data):
    """Test updating a module."""
    # Setup
    mock_client.update_resource.return_value = PowerPathModule(**sample_module_data)
    module_data = {"name": "Updated Module", "state": "inactive"}
    
    # Execute
    result = update_module(mock_client, "123", module_data)
    
    # Verify
    mock_client.update_resource.assert_called_once_with("/modules/123", PowerPathModule, module_data)
    assert isinstance(result, PowerPathModule)
    assert result.id == 123
    assert result.name == "Test Module"

def test_delete_module(mock_client):
    """Test deleting a module."""
    # Setup
    mock_client.delete_resource.return_value = {"success": True}
    
    # Execute
    result = delete_module(mock_client, "123")
    
    # Verify
    mock_client.delete_resource.assert_called_once_with("/modules/123")
    assert result == {"success": True} 
"""
Tests for the PowerPath item associations API functions.

This module contains tests for the PowerPath item associations API functions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID

from cws_helpers.powerpath_helper import (
    PowerPathClient,
    PowerPathItemAssociation,
    get_item_associations,
    create_item_association,
    associate_item_with_module,
    update_item_associations,
    delete_item_associations,
    delete_item_association,
)

@pytest.fixture
def mock_client():
    """Create a mock PowerPath client."""
    client = MagicMock(spec=PowerPathClient)
    return client

@pytest.fixture
def sample_association_data():
    """Create sample association data for testing."""
    return {
        "moduleId": 123,
        "originItemId": 456,
        "destinationItemId": 789,
        "relationship": "prerequisite"
    }

def test_get_item_associations(mock_client, sample_association_data):
    """Test getting item associations."""
    # Setup
    mock_client.get_resources.return_value = [PowerPathItemAssociation(**sample_association_data)]
    
    # Execute
    result = get_item_associations(mock_client, "123", "456")
    
    # Verify
    mock_client.get_resources.assert_called_once_with(
        "/modules/123/items/456/associations", 
        PowerPathItemAssociation
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], PowerPathItemAssociation)
    assert result[0].module_id == 123
    assert result[0].origin_item_id == 456
    assert result[0].destination_item_id == 789
    assert result[0].relationship == "prerequisite"

def test_create_item_association(mock_client, sample_association_data):
    """Test creating an item association."""
    # Setup
    mock_client.create_resource.return_value = PowerPathItemAssociation(**sample_association_data)
    
    # Execute
    result = create_item_association(mock_client, "123", sample_association_data)
    
    # Verify
    mock_client.create_resource.assert_called_once_with(
        "/modules/123/items/associations", 
        PowerPathItemAssociation, 
        sample_association_data
    )
    assert isinstance(result, PowerPathItemAssociation)
    assert result.module_id == 123
    assert result.origin_item_id == 456
    assert result.destination_item_id == 789
    assert result.relationship == "prerequisite"

def test_associate_item_with_module(mock_client):
    """Test associating an item with a module."""
    # Setup
    mock_client.post.return_value = {"success": True}
    
    # Execute
    result = associate_item_with_module(mock_client, "123", "456")
    
    # Verify
    mock_client.post.assert_called_once_with("/modules/123/items/456/associations")
    assert result == {"success": True}

def test_update_item_associations(mock_client, sample_association_data):
    """Test updating item associations."""
    # Setup
    mock_client.update_resource.return_value = PowerPathItemAssociation(**sample_association_data)
    
    # Execute
    result = update_item_associations(mock_client, "123", "456", sample_association_data)
    
    # Verify
    mock_client.update_resource.assert_called_once_with(
        "/modules/123/items/456/associations", 
        PowerPathItemAssociation, 
        sample_association_data
    )
    assert isinstance(result, PowerPathItemAssociation)
    assert result.module_id == 123
    assert result.origin_item_id == 456
    assert result.destination_item_id == 789
    assert result.relationship == "prerequisite"

def test_delete_item_associations(mock_client):
    """Test deleting all item associations."""
    # Setup
    mock_client.delete_resource.return_value = {"success": True}
    
    # Execute
    result = delete_item_associations(mock_client, "123", "456")
    
    # Verify
    mock_client.delete_resource.assert_called_once_with("/modules/123/items/456/associations")
    assert result == {"success": True}

def test_delete_item_association(mock_client):
    """Test deleting a specific item association."""
    # Setup
    mock_client.delete_resource.return_value = {"success": True}
    
    # Execute
    result = delete_item_association(mock_client, "123", "456", "789")
    
    # Verify
    mock_client.delete_resource.assert_called_once_with("/modules/123/items/456/associations/789")
    assert result == {"success": True} 
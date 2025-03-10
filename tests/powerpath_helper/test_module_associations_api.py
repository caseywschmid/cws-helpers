"""
Tests for the PowerPath module associations API functions.

This module contains tests for the PowerPath module associations API functions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID

from cws_helpers.powerpath_helper import (
    PowerPathClient,
    PowerPathModuleAssociation,
    get_module_associations,
    create_module_association,
    update_module_association,
    delete_module_association,
)

@pytest.fixture
def mock_client():
    """Create a mock PowerPath client."""
    client = MagicMock(spec=PowerPathClient)
    return client

@pytest.fixture
def sample_module_association_data():
    """Create sample module association data for testing."""
    return {
        "originModuleId": 123,
        "destinationModuleId": 456,
        "relationship": "prerequisite"
    }

@pytest.fixture
def sample_sql_result():
    """Create sample SQL query result data for testing."""
    return {
        "rows": [
            {
                "originModuleId": 123,
                "destinationModuleId": 456,
                "relationship": "prerequisite"
            },
            {
                "originModuleId": 123,
                "destinationModuleId": 789,
                "relationship": "prerequisite"
            }
        ],
        "rowCount": 2
    }

def test_get_module_associations(mock_client, sample_sql_result):
    """Test getting module associations."""
    # Setup
    with patch('cws_helpers.powerpath_helper.api.module_associations.execute_sql_query') as mock_execute_sql:
        mock_execute_sql.return_value = sample_sql_result
        
        # Execute
        result = get_module_associations(mock_client, "123")
        
        # Verify
        mock_execute_sql.assert_called_once_with(
            mock_client, 
            'SELECT * FROM "moduleAssociations" WHERE "originModuleId" = 123;'
        )
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], PowerPathModuleAssociation)
        assert result[0].origin_module_id == 123
        assert result[0].destination_module_id == 456
        assert result[0].relationship == "prerequisite"
        assert result[1].origin_module_id == 123
        assert result[1].destination_module_id == 789
        assert result[1].relationship == "prerequisite"

def test_create_module_association(mock_client, sample_module_association_data):
    """Test creating a module association."""
    # Setup
    mock_client.create_resource.return_value = PowerPathModuleAssociation(**sample_module_association_data)
    
    # Execute
    result = create_module_association(mock_client, sample_module_association_data)
    
    # Verify
    mock_client.create_resource.assert_called_once_with(
        "/modules/associations", 
        PowerPathModuleAssociation, 
        sample_module_association_data
    )
    assert isinstance(result, PowerPathModuleAssociation)
    assert result.origin_module_id == 123
    assert result.destination_module_id == 456
    assert result.relationship == "prerequisite"

def test_update_module_association(mock_client, sample_module_association_data):
    """Test updating a module association."""
    # Setup
    mock_client.update_resource.return_value = PowerPathModuleAssociation(**sample_module_association_data)
    
    # Execute
    result = update_module_association(mock_client, sample_module_association_data)
    
    # Verify
    mock_client.update_resource.assert_called_once_with(
        "/modules/associations", 
        PowerPathModuleAssociation, 
        sample_module_association_data
    )
    assert isinstance(result, PowerPathModuleAssociation)
    assert result.origin_module_id == 123
    assert result.destination_module_id == 456
    assert result.relationship == "prerequisite"

def test_delete_module_association(mock_client):
    """Test deleting a module association."""
    # Setup
    mock_client.delete_resource.return_value = {"success": True}
    
    # Execute
    result = delete_module_association(mock_client, "123", "456")
    
    # Verify
    mock_client.delete_resource.assert_called_once_with("/modules/associations/123/456")
    assert result == {"success": True} 
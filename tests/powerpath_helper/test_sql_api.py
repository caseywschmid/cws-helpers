"""
Tests for the PowerPath SQL API functions.

This module contains tests for the PowerPath SQL API functions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID

from cws_helpers.powerpath_helper import (
    PowerPathClient,
    execute_sql_query,
)

@pytest.fixture
def mock_client():
    """Create a mock PowerPath client."""
    client = MagicMock(spec=PowerPathClient)
    return client

@pytest.fixture
def sample_sql_result():
    """Create sample SQL query result data for testing."""
    return {
        "rows": [
            {"id": 1, "name": "Test 1"},
            {"id": 2, "name": "Test 2"}
        ],
        "rowCount": 2
    }

def test_execute_sql_query(mock_client, sample_sql_result):
    """Test executing a SQL query."""
    # Setup
    mock_client.post.return_value = sample_sql_result
    sql_query = 'SELECT * FROM "users" LIMIT 2;'
    
    # Execute
    result = execute_sql_query(mock_client, sql_query)
    
    # Verify
    mock_client.post.assert_called_once_with("/sql", json_data={"sql": sql_query})
    assert result == sample_sql_result
    assert len(result["rows"]) == 2
    assert result["rowCount"] == 2 
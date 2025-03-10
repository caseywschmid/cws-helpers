"""
SQL API functions for PowerPath.

This module provides functions for executing custom SQL queries against the PowerPath API.
It allows for more flexible data retrieval when standard endpoints don't provide the needed functionality.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient

def execute_sql_query(client: PowerPathClient, sql_query: str) -> Dict[str, Any]:
    """
    Execute a custom SQL query against the PowerPath database.
    
    This function sends a SQL query to the PowerPath API's /sql endpoint.
    Use this with caution as it provides direct access to the database.
    
    Args:
        client: The PowerPath API client
        sql_query: The SQL query to execute
        
    Returns:
        Dict[str, Any]: The query results, typically containing 'rows' and 'rowCount' keys
        
    Raises:
        PowerPathClientError: If the request fails
        PowerPathAuthenticationError: If the user doesn't have permission to execute SQL queries
        
    Example:
        >>> result = execute_sql_query(client, 'SELECT * FROM "users" LIMIT 10;')
        >>> for user in result['rows']:
        ...     print(user['email'])
    """
    return client.post("/sql", json_data={"sql": sql_query}) 
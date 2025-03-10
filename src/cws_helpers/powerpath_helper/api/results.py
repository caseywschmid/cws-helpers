"""
Results API functions for PowerPath.

This module provides functions for working with results in the PowerPath API.
It includes operations for creating, retrieving, updating, and deleting results for users.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from ..core import PowerPathClient
from ..models import PowerPathResult

def get_user_results(
    client: PowerPathClient, 
    user_id: str, 
    item_id: Optional[str] = None,
    cc_item_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[PowerPathResult]:
    """
    Get results for a user.
    
    This function retrieves results for a specific user from the PowerPath API.
    It can optionally filter results by item, content creation item, or date range.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user
        item_id: Optional - Filter results by item ID
        cc_item_id: Optional - Filter results by content creation item ID (question ID)
        start_date: Optional - Filter results by start date
        end_date: Optional - Filter results by end date
        
    Returns:
        List[PowerPathResult]: The results for the user
        
    Raises:
        PowerPathNotFoundError: If the user does not exist
        PowerPathClientError: If the request fails
    """
    params = {}
    if item_id:
        params["itemId"] = item_id
    if cc_item_id:
        params["ccItemId"] = cc_item_id
    if start_date:
        params["startDate"] = start_date.isoformat()
    if end_date:
        params["endDate"] = end_date.isoformat()
    
    return client.get_resources(f"/users/{user_id}/results", PowerPathResult, params=params)

def get_user_result(client: PowerPathClient, user_id: str, result_id: str) -> PowerPathResult:
    """
    Get a specific result for a user.
    
    This function retrieves a specific result for a user from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user
        result_id: The ID of the result
        
    Returns:
        PowerPathResult: The requested result
        
    Raises:
        PowerPathNotFoundError: If the user or result does not exist
        PowerPathClientError: If the request fails
    """
    return client.get_resource(f"/users/{user_id}/results/{result_id}", PowerPathResult)

def create_user_result(client: PowerPathClient, user_id: str, result_data: Dict[str, Any]) -> PowerPathResult:
    """
    Create a new result for a user.
    
    This function creates a new result for a user in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user
        result_data: The data for the new result
        
    Returns:
        PowerPathResult: The created result
        
    Raises:
        PowerPathNotFoundError: If the user does not exist
        PowerPathClientError: If the request fails
    """
    return client.create_resource(f"/users/{user_id}/results", PowerPathResult, result_data)

def update_user_result(client: PowerPathClient, user_id: str, result_id: str, result_data: Dict[str, Any]) -> PowerPathResult:
    """
    Update a result for a user.
    
    This function updates an existing result for a user in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user
        result_id: The ID of the result to update
        result_data: The updated data for the result
        
    Returns:
        PowerPathResult: The updated result
        
    Raises:
        PowerPathNotFoundError: If the user or result does not exist
        PowerPathClientError: If the request fails
    """
    return client.patch(f"/users/{user_id}/results/{result_id}", json_data=result_data)

def delete_user_result(client: PowerPathClient, user_id: str, result_id: str) -> Dict[str, Any]:
    """
    Delete a result for a user.
    
    This function deletes a result for a user from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user
        result_id: The ID of the result to delete
        
    Returns:
        Dict[str, Any]: The response from the API
        
    Raises:
        PowerPathNotFoundError: If the user or result does not exist
        PowerPathClientError: If the request fails
    """
    return client.delete(f"/users/{user_id}/results/{result_id}") 
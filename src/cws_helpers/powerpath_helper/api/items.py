"""
Item API functions for PowerPath.

This module provides functions for working with items in the PowerPath API.
It includes basic CRUD operations for items within modules.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient
from ..models import PowerPathItem

def get_module_items(client: PowerPathClient, module_id: str) -> List[PowerPathItem]:
    """
    Get all items in a module.
    
    This function retrieves all items in a specific module from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        
    Returns:
        List[PowerPathItem]: The items in the module
        
    Raises:
        PowerPathNotFoundError: If the module does not exist
        PowerPathClientError: If the request fails
    """
    return client.get_resources(f"/modules/{module_id}/items", PowerPathItem)

def get_module_item(client: PowerPathClient, module_id: str, item_id: str) -> PowerPathItem:
    """
    Get a specific item in a module.
    
    This function retrieves a specific item in a module from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        item_id: The ID of the item
        
    Returns:
        PowerPathItem: The requested item
        
    Raises:
        PowerPathNotFoundError: If the module or item does not exist
        PowerPathClientError: If the request fails
    """
    return client.get_resource(f"/modules/{module_id}/items/{item_id}", PowerPathItem)

def create_module_item(client: PowerPathClient, module_id: str, item_data: Dict[str, Any]) -> PowerPathItem:
    """
    Create a new item in a module.
    
    This function creates a new item in a module in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        item_data: The data for the new item
        
    Returns:
        PowerPathItem: The created item
        
    Raises:
        PowerPathNotFoundError: If the module does not exist
        PowerPathClientError: If the request fails
    """
    return client.create_resource(f"/modules/{module_id}/items", PowerPathItem, item_data)

def update_module_items(client: PowerPathClient, module_id: str, items_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Update items in a module.
    
    This function updates multiple items in a module in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        items_data: The updated data for the items
        
    Returns:
        Dict[str, Any]: The response from the API
        
    Raises:
        PowerPathNotFoundError: If the module does not exist
        PowerPathClientError: If the request fails
    """
    return client.put(f"/modules/{module_id}/items", json_data=items_data) 
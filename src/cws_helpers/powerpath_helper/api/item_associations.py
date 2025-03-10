"""
Item Association API functions for PowerPath.

This module provides functions for working with item associations in the PowerPath API.
It includes operations for creating, retrieving, and deleting associations between items.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient
from ..models import PowerPathItemAssociation

def get_item_associations(client: PowerPathClient, module_id: str, item_id: str) -> List[PowerPathItemAssociation]:
    """
    Get all associations for an item.
    
    This function retrieves all associations for a specific item in a module from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        item_id: The ID of the item
        
    Returns:
        List[PowerPathItemAssociation]: The associations for the item
        
    Raises:
        PowerPathNotFoundError: If the module or item does not exist
        PowerPathClientError: If the request fails
    """
    return client.get_resources(f"/modules/{module_id}/items/{item_id}/associations", PowerPathItemAssociation)

def create_item_association(client: PowerPathClient, module_id: str, association_data: Dict[str, Any]) -> PowerPathItemAssociation:
    """
    Create a new association between items.
    
    This function creates a new association between items in a module in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        association_data: The data for the new association
        
    Returns:
        PowerPathItemAssociation: The created association
        
    Raises:
        PowerPathNotFoundError: If the module does not exist
        PowerPathClientError: If the request fails
    """
    return client.create_resource(f"/modules/{module_id}/items/associations", PowerPathItemAssociation, association_data)

def associate_item_with_module(client: PowerPathClient, module_id: str, item_id: str) -> Dict[str, Any]:
    """
    Associate an existing item with a module.
    
    This function associates an existing item with a module in the PowerPath API.
    This might be used to associate an item with an additional module beyond the one
    it was originally created in, enabling item reuse across modules.
    
    Note: When items are created using POST /modules/{moduleId}/items, they are
    automatically associated with that module. This function would only be needed
    for special cases.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module to associate the item with
        item_id: The ID of the existing item
        
    Returns:
        Dict[str, Any]: The response from the API
        
    Raises:
        PowerPathNotFoundError: If the module or item does not exist
        PowerPathClientError: If the request fails
    """
    return client.post(f"/modules/{module_id}/items/{item_id}/associations")

def update_item_associations(client: PowerPathClient, module_id: str, item_id: str, association_data: Dict[str, Any]) -> PowerPathItemAssociation:
    """
    Update associations for an item.
    
    This function updates associations for a specific item in a module in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        item_id: The ID of the item
        association_data: The updated data for the associations
        
    Returns:
        PowerPathItemAssociation: The updated association
        
    Raises:
        PowerPathNotFoundError: If the module or item does not exist
        PowerPathClientError: If the request fails
    """
    return client.update_resource(f"/modules/{module_id}/items/{item_id}/associations", PowerPathItemAssociation, association_data)

def delete_item_associations(client: PowerPathClient, module_id: str, item_id: str) -> Dict[str, Any]:
    """
    Delete all associations for an item.
    
    This function deletes all associations for a specific item in a module in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        item_id: The ID of the item
        
    Returns:
        Dict[str, Any]: The response from the API
        
    Raises:
        PowerPathNotFoundError: If the module or item does not exist
        PowerPathClientError: If the request fails
    """
    return client.delete_resource(f"/modules/{module_id}/items/{item_id}/associations")

def delete_item_association(
    client: PowerPathClient, 
    module_id: str, 
    origin_item_id: str, 
    destination_item_id: str
) -> Dict[str, Any]:
    """
    Delete an association between items.
    
    This function deletes an association between items in a module in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        origin_item_id: The ID of the origin item
        destination_item_id: The ID of the destination item
        
    Returns:
        Dict[str, Any]: The response from the API
        
    Raises:
        PowerPathNotFoundError: If the association does not exist
        PowerPathClientError: If the request fails
    """
    return client.delete_resource(
        f"/modules/{module_id}/items/{origin_item_id}/associations/{destination_item_id}"
    ) 
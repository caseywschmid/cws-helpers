"""
Question Bank API functions for PowerPath.

This module provides functions for working with question banks in the PowerPath API.
It includes operations for retrieving, creating, and deleting question bank items.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient
from ..models import PowerPathCCItem

def get_question_bank(client: PowerPathClient, module_id: str, item_id: str) -> List[Dict[str, Any]]:
    """
    Get the question bank for an item.
    
    This function retrieves the question bank for a specific item in a module from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        item_id: The ID of the item
        
    Returns:
        List[Dict[str, Any]]: The question bank items
        
    Raises:
        PowerPathNotFoundError: If the module or item does not exist
        PowerPathClientError: If the request fails
    """
    return client.get(f"/modules/{module_id}/items/{item_id}/questionBank")

def create_question_bank_item(client: PowerPathClient, module_id: str, item_id: str, question_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new question bank item.
    
    This function creates a new question for a specific item in a module in the PowerPath API.
    Questions are internally referred to as 'ccItem' in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        item_id: The ID of the item
        question_data: The data for the new question
        
    Returns:
        Dict[str, Any]: The created question
        
    Raises:
        PowerPathNotFoundError: If the module or item does not exist
        PowerPathClientError: If the request fails
    """
    return client.post(f"/modules/{module_id}/items/questionBank", json_data=question_data)

def delete_question_bank_item(client: PowerPathClient, module_id: str, item_id: str, question_id: str) -> Dict[str, Any]:
    """
    Delete a question bank item.
    
    This function deletes a question from a specific item in a module in the PowerPath API.
    Questions are internally referred to as 'ccItem' in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module
        item_id: The ID of the item
        question_id: The ID of the question
        
    Returns:
        Dict[str, Any]: The response from the API
        
    Raises:
        PowerPathNotFoundError: If the module, item, or question does not exist
        PowerPathClientError: If the request fails
    """
    return client.delete(f"/modules/{module_id}/items/{item_id}/questionBank/{question_id}")

def delete_object_bank(client: PowerPathClient, module_id: str, item_id: str) -> Dict[str, Any]:
    """
    Delete the object bank for an item.
    
    This function deletes the object bank for a specific item in a module in the PowerPath API.
    The exact purpose of this endpoint is not well documented, but it appears to delete all
    objects associated with an item.
    
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
    return client.delete(f"/modules/{module_id}/items/{item_id}/objectBank") 
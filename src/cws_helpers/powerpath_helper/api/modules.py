"""
Module API functions for PowerPath.

This module provides functions for working with modules in the PowerPath API.
It includes basic CRUD operations for modules.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient
from ..models import PowerPathModule

def get_all_modules(client: PowerPathClient) -> List[PowerPathModule]:
    """
    Get all modules.
    
    This function retrieves all modules from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        
    Returns:
        List[PowerPathModule]: The list of modules
        
    Raises:
        PowerPathClientError: If the request fails
    """
    return client.get_resources("/modules", PowerPathModule)

def get_module(client: PowerPathClient, module_id: str) -> PowerPathModule:
    """
    Get a module by ID.
    
    This function retrieves a specific module from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module to retrieve
        
    Returns:
        PowerPathModule: The requested module
        
    Raises:
        PowerPathNotFoundError: If the module does not exist
        PowerPathClientError: If the request fails
    """
    return client.get_resource(f"/modules/{module_id}", PowerPathModule)

def create_module(client: PowerPathClient, module_data: Dict[str, Any]) -> PowerPathModule:
    """
    Create a new module.
    
    This function creates a new module in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_data: The data for the new module
        
    Returns:
        PowerPathModule: The created module
        
    Raises:
        PowerPathClientError: If the request fails
    """
    return client.create_resource("/modules", PowerPathModule, module_data)

def update_module(client: PowerPathClient, module_id: str, module_data: Dict[str, Any]) -> PowerPathModule:
    """
    Update a module.
    
    This function updates an existing module in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module to update
        module_data: The updated data for the module
        
    Returns:
        PowerPathModule: The updated module
        
    Raises:
        PowerPathNotFoundError: If the module does not exist
        PowerPathClientError: If the request fails
    """
    return client.update_resource(f"/modules/{module_id}", PowerPathModule, module_data)

def delete_module(client: PowerPathClient, module_id: str) -> Dict[str, Any]:
    """
    Delete a module.
    
    This function deletes a module from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the module to delete
        
    Returns:
        Dict[str, Any]: The response from the API
        
    Raises:
        PowerPathNotFoundError: If the module does not exist
        PowerPathClientError: If the request fails
    """
    return client.delete_resource(f"/modules/{module_id}") 
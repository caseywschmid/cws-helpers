"""
Module Association API functions for PowerPath.

This module provides functions for working with module associations in the PowerPath API.
It includes operations for creating, updating, and deleting associations between modules.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient
from ..models import PowerPathModuleAssociation
from .sql import execute_sql_query

def get_module_associations(client: PowerPathClient, module_id: str) -> List[PowerPathModuleAssociation]:
    """
    Get all associations for a specific module.
    
    This function retrieves all associations where the specified module is the origin module.
    Since there's no direct API endpoint for this, it uses a SQL query to fetch the data.
    
    Args:
        client: The PowerPath API client
        module_id: The ID of the origin module
        
    Returns:
        List[PowerPathModuleAssociation]: The associations for the module
        
    Raises:
        PowerPathClientError: If the request fails
        
    Note:
        This function uses the SQL endpoint which may require special permissions.
    """
    # Execute SQL query to get all associations for the module
    result = execute_sql_query(
        client, 
        f'SELECT * FROM "moduleAssociations" WHERE "originModuleId" = {module_id};'
    )
    
    # Convert the raw data to PowerPathModuleAssociation objects
    associations = []
    for row in result.get('rows', []):
        associations.append(PowerPathModuleAssociation(**row))
    
    return associations

def create_module_association(client: PowerPathClient, association_data: Dict[str, Any]) -> PowerPathModuleAssociation:
    """
    Create a new association between modules.
    
    This function creates a new association between modules in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        association_data: The data for the new association
        
    Returns:
        PowerPathModuleAssociation: The created association
        
    Raises:
        PowerPathClientError: If the request fails
    """
    return client.create_resource("/modules/associations", PowerPathModuleAssociation, association_data)

def update_module_association(client: PowerPathClient, association_data: Dict[str, Any]) -> PowerPathModuleAssociation:
    """
    Update an association between modules.
    
    This function updates an association between modules in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        association_data: The updated data for the association
        
    Returns:
        PowerPathModuleAssociation: The updated association
        
    Raises:
        PowerPathClientError: If the request fails
    """
    return client.update_resource("/modules/associations", PowerPathModuleAssociation, association_data)

def delete_module_association(client: PowerPathClient, origin_module_id: str, destination_module_id: str) -> Dict[str, Any]:
    """
    Delete an association between modules.
    
    This function deletes an association between modules in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        origin_module_id: The ID of the origin module
        destination_module_id: The ID of the destination module
        
    Returns:
        Dict[str, Any]: The response from the API
        
    Raises:
        PowerPathNotFoundError: If the association does not exist
        PowerPathClientError: If the request fails
    """
    return client.delete_resource(f"/modules/associations/{origin_module_id}/{destination_module_id}") 
"""
Association models for PowerPath API.

This module provides models for working with associations between modules and items
in the PowerPath API.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Literal
from uuid import UUID
from pydantic import BaseModel, Field

from .base import PowerPathBase


class PowerPathItemAssociation(PowerPathBase):
    """
    PowerPath Item Association model.
    
    This model represents an association between two items in the PowerPath system.
    Item associations define relationships like prerequisites or dependencies.
    
    API Endpoints:
    - POST /modules/:moduleId/items/associations - Creates a new item association
    - POST /modules/:moduleId/items/:itemId/associations - Creates a new item association
    - GET /modules/:moduleId/items/:itemId/associations - Returns associations for an item
    - PATCH /modules/:moduleId/items/:itemId/associations - Updates an item association
    - DELETE /modules/:moduleId/items/:itemId/associations - Deletes an item association
    - DELETE /modules/:moduleId/items/:originItemId/associations/:destinationItemId - Deletes a specific association
    
    Database Table: itemAssociations
    Related Tables:
    - items (via originItemId and destinationItemId)
    - modules (via moduleId)
    
    Attributes:
        module_id: The ID of the module containing the items (moduleId in API)
        origin_item_id: The ID of the origin item (originItemId in API)
        origin_item_uuid: The UUID of the origin item (originItemUUID in API)
        destination_item_id: The ID of the destination item (destinationItemId in API)
        destination_item_uuid: The UUID of the destination item (destinationItemUUID in API)
        relationship: The type of relationship between the items
    """
    module_id: int = Field(alias="moduleId")
    origin_item_id: int = Field(alias="originItemId")
    origin_item_uuid: Optional[UUID] = Field(None, alias="originItemUUID")
    destination_item_id: int = Field(alias="destinationItemId")
    destination_item_uuid: Optional[UUID] = Field(None, alias="destinationItemUUID")
    relationship: str
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations.
        
        This method is used when creating a new item association via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new item association
        """
        return self.model_dump(
            exclude_unset=True, 
            by_alias=True
        )


class PowerPathModuleAssociation(PowerPathBase):
    """
    PowerPath Module Association model.
    
    This model represents an association between two modules in the PowerPath system.
    Module associations define relationships like prerequisites or dependencies.
    
    API Endpoints:
    - POST /modules/associations - Creates a new module association
    - PATCH /modules/associations - Updates a module association
    - DELETE /modules/associations/:originModuleId/:destinationModuleId - Deletes a module association
    
    Database Table: moduleAssociations
    Related Tables:
    - modules (via originModuleId and destinationModuleId)
    
    Attributes:
        origin_module_id: The ID of the origin module (originModuleId in API)
        origin_module_uuid: The UUID of the origin module (originModuleUUID in API)
        destination_module_id: The ID of the destination module (destinationModuleId in API)
        destination_module_uuid: The UUID of the destination module (destinationModuleUUID in API)
        relationship: The type of relationship between the modules
    """
    origin_module_id: int = Field(alias="originModuleId")
    origin_module_uuid: Optional[UUID] = Field(None, alias="originModuleUUID")
    destination_module_id: int = Field(alias="destinationModuleId")
    destination_module_uuid: Optional[UUID] = Field(None, alias="destinationModuleUUID")
    relationship: str
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations.
        
        This method is used when creating a new module association via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new module association
        """
        return self.model_dump(
            exclude_unset=True, 
            by_alias=True
        ) 
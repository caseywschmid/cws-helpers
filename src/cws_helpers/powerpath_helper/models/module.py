"""
Module and Item models for PowerPath API.

This module provides models for working with modules and items in the PowerPath API.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union, ForwardRef
from uuid import UUID
from pydantic import BaseModel, Field

from .base import PowerPathBase

# Forward reference for PowerPathItem to handle circular dependency
PowerPathItemRef = ForwardRef('PowerPathItem')


class PowerPathItem(PowerPathBase):
    """
    PowerPath Item model.
    
    This model represents an item in the PowerPath system.
    Items are the basic content units within modules.
    
    API Endpoints:
    - GET /modules/:moduleId/items/:itemId - Returns a single item
    - POST /modules/:moduleId/items - Creates a new item
    - PUT /modules/:moduleId/items - Updates items in a module
    
    Database Table: items
    Related Tables:
    - moduleItems (links items to modules)
    - itemAssociations (links items to other items)
    
    Attributes:
        id: The item's numeric ID
        uuid: The item's UUID
        name: The item's name
        content_type: The type of content (contentType in API)
        xp: The experience points for the item
        attempts: The number of attempts allowed
        state: The item's state
        metadata: Additional metadata for the item
        is_placement_test: Whether the item is a placement test (isPlacementTest in API)
        third_party_id: ID from a third-party system (thirdPartyId in API)
        lti_url: URL for LTI content (lti_url in API)
    """
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    name: str
    content_type: str = Field(alias="contentType")
    xp: int
    attempts: Optional[int] = None
    state: Optional[str] = None
    metadata: Optional[str] = None
    is_placement_test: Optional[bool] = Field(None, alias="isPlacementTest")
    third_party_id: Optional[str] = Field(None, alias="thirdPartyId")
    lti_url: Optional[str] = Field(None, alias="lti_url")
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations, excluding read-only fields.
        
        This method is used when creating a new item via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new item
        """
        return self.model_dump(
            exclude={'id', 'uuid'}, 
            exclude_unset=True, 
            by_alias=True
        )
    
    def to_update_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for PATCH operations, excluding read-only fields.
        
        This method is used when updating an existing item via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for updating an existing item
        """
        return self.model_dump(
            exclude={'id', 'uuid'}, 
            exclude_unset=True, 
            exclude_none=True,
            by_alias=True
        )


class PowerPathModule(PowerPathBase):
    """
    PowerPath Module model.
    
    This model represents a module in the PowerPath system.
    Modules are containers for items and can be linked to courses.
    
    API Endpoints:
    - GET /modules/:moduleId - Returns a single module
    - POST /modules - Creates a new module
    - PATCH /modules/:moduleId - Updates an existing module
    - DELETE /modules/:moduleId - Deletes a module
    
    Database Table: modules
    Related Tables: 
    - moduleItems (links modules to items)
    - moduleAssociations (links modules to other modules)
    - courses (via defaultModuleId)
    
    Attributes:
        id: The module's numeric ID
        uuid: The module's UUID
        name: The module's name
        state: The module's state
        unlock_at: When the module unlocks (unlock_at in API)
        starting_item_id: The ID of the starting item (startingItemId in API)
        starting_item_uuid: The UUID of the starting item (startingItemUUID in API)
        starting_module_id: The ID of the starting module (startingModuleId in API)
        items: List of items in the module (optional)
    """
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    name: str
    state: Optional[str] = None
    unlock_at: Optional[datetime] = Field(None, alias="unlock_at")
    starting_item_id: Optional[int] = Field(None, alias="startingItemId")
    starting_item_uuid: Optional[UUID] = Field(None, alias="startingItemUUID")
    starting_module_id: Optional[int] = Field(None, alias="startingModuleId")
    items: Optional[List[PowerPathItem]] = None
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations, excluding read-only fields.
        
        This method is used when creating a new module via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new module
        """
        return self.model_dump(
            exclude={'id', 'uuid', 'items'}, 
            exclude_unset=True, 
            by_alias=True
        )
    
    def to_update_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for PATCH operations, excluding read-only fields.
        
        This method is used when updating an existing module via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for updating an existing module
        """
        return self.model_dump(
            exclude={'id', 'uuid', 'items'}, 
            exclude_unset=True, 
            exclude_none=True,
            by_alias=True
        )


# Resolve forward references
PowerPathModule.model_rebuild()
PowerPathItem.model_rebuild() 
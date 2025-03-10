"""
Base models for PowerPath API.

This module provides the base model class for all PowerPath API models.
It includes common configurations and utility methods used across all models.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class PowerPathBase(BaseModel):
    """
    Base model with common configurations for PowerPath API models.
    
    This provides consistent handling of field names, extra fields,
    and common utility methods for all PowerPath models.
    
    Attributes:
        None directly, but provides configuration for all derived models
    """
    
    # Pydantic V2 style configuration
    model_config = ConfigDict(
        # Allow extra fields in case API adds new fields
        extra="ignore",
        # Allow both camelCase and snake_case
        populate_by_name=True,
        # Keep the order of fields as defined
        from_attributes=True,
    )
    
    def to_api_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for API requests, using camelCase keys.
        
        This method is useful when sending data to the API, which expects
        camelCase field names.
        
        Returns:
            Dict[str, Any]: Dictionary with camelCase keys for API requests
        """
        return self.model_dump(by_alias=True, exclude_unset=True)
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations, excluding read-only fields.
        
        This method should be overridden by subclasses to exclude specific
        read-only fields for that model.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new resource
        """
        return self.model_dump(exclude_unset=True, by_alias=True)
    
    def to_update_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for PATCH operations, excluding read-only fields.
        
        This method should be overridden by subclasses to exclude specific
        read-only fields for that model and to exclude None values.
        
        Returns:
            Dict[str, Any]: Dictionary for updating an existing resource
        """
        return self.model_dump(
            exclude_unset=True, 
            exclude_none=True,
            by_alias=True
        )

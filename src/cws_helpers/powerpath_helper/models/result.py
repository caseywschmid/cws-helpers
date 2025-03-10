"""
Result models for PowerPath API.

This module provides models for working with assessment results in the PowerPath API.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field

from .base import PowerPathBase


class PowerPathResult(PowerPathBase):
    """
    PowerPath Result model.
    
    This model represents an assessment result in the PowerPath system.
    Results are created when users complete assessments or other evaluated activities.
    
    API Endpoints:
    - GET /users/:studentId/results - Returns a list of results for a user
    - GET /users/:studentId/results/:resultId - Returns a specific result
    - POST /users/:studentId/results - Creates a new result for a user
    - PATCH /users/:studentId/results/:resultId - Updates an existing result
    - DELETE /users/:studentId/results/:resultId - Deletes a result
    - GET /users/:studentId/results?itemId=:itemId - Returns results for a specific item
    - GET /users/:studentId/results?ccItemId=:ccItemId - Returns results for a specific CC item
    - GET /users/:studentId/results?startDate=:startDate&endDate=:endDate - Returns results within a date range
    
    Database Table: results
    Related Tables:
    - users (via userId)
    - ccItemResults (via resultId)
    - userModuleItems (via clrResultId)
    
    Attributes:
        id: The result's numeric ID
        uuid: The result's UUID
        user_id: The ID of the user who earned the result (userId in API)
        type: The type of result
        value: The numeric value of the result
        achieved_level: The level achieved (achievedLevel in API)
        alignments: Alignment information
        status: The status of the result
        result_description: Description of the result (resultDescription in API)
    """
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    user_id: int = Field(alias="userId")
    type: str
    value: float
    achieved_level: Optional[str] = Field(None, alias="achievedLevel")
    alignments: Optional[str] = None
    status: Optional[str] = None
    result_description: Optional[str] = Field(None, alias="resultDescription")
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations, excluding read-only fields.
        
        This method is used when creating a new result via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new result
        """
        return self.model_dump(
            exclude={'id', 'uuid'}, 
            exclude_unset=True, 
            by_alias=True
        )
    
    def to_update_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for PATCH operations, excluding read-only fields.
        
        This method is used when updating an existing result via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for updating an existing result
        """
        return self.model_dump(
            exclude={'id', 'uuid', 'user_id'}, 
            exclude_unset=True, 
            exclude_none=True,
            by_alias=True
        ) 
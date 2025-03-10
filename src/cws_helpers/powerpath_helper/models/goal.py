"""
Goal models for PowerPath API.

This module provides models for working with user goals in the PowerPath API.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field

from .base import PowerPathBase


class PowerPathGoal(PowerPathBase):
    """
    PowerPath Goal model.
    
    This model represents a user goal in the PowerPath system.
    Goals are targets that users set for themselves, often related to XP.
    
    API Endpoints:
    - GET /users/:studentId/goals - Returns a list of goals for a user
    - POST /users/:studentId/goals - Creates a new goal for a user
    - PATCH /users/:studentId/goals/:goalId - Updates an existing goal
    - DELETE /users/:studentId/goals/:goalId - Deletes a goal
    - GET /courses/:courseId/goals - Returns a list of goals for a course
    
    Database Table: goals
    Related Tables:
    - users (via userId)
    - courses (via courseId)
    
    Attributes:
        id: The goal's numeric ID
        description: The goal's description
        xp: The XP target for the goal
        user_id: The ID of the user who owns the goal (userId in API)
        course_id: The ID of the course the goal is for (courseId in API)
        cutoff_date: The deadline for the goal (cutoffDate in API)
        daily_override: Daily XP override (dailyOverride in API)
        created_at: When the goal was created (createdAt in API)
        updated_at: When the goal was last updated (updatedAt in API)
    """
    id: Optional[int] = None
    description: str
    xp: int
    user_id: int = Field(alias="userId")
    course_id: int = Field(alias="courseId")
    cutoff_date: Optional[datetime] = Field(None, alias="cutoffDate")
    daily_override: Optional[int] = Field(None, alias="dailyOverride")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations, excluding read-only fields.
        
        This method is used when creating a new goal via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new goal
        """
        return self.model_dump(
            exclude={'id', 'created_at', 'updated_at'}, 
            exclude_unset=True, 
            by_alias=True
        )
    
    def to_update_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for PATCH operations, excluding read-only fields.
        
        This method is used when updating an existing goal via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for updating an existing goal
        """
        return self.model_dump(
            exclude={'id', 'created_at', 'updated_at'}, 
            exclude_unset=True, 
            exclude_none=True,
            by_alias=True
        ) 
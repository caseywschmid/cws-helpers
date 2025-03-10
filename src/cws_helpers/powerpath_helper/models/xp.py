"""
XP models for PowerPath API.

This module provides models for working with experience points (XP) in the PowerPath API.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field

from .base import PowerPathBase


class PowerPathXP(PowerPathBase):
    """
    PowerPath XP model.
    
    This model represents experience points (XP) in the PowerPath system.
    XP is awarded to users for completing items, courses, or other achievements.
    
    API Endpoints:
    - GET /users/:studentId/xp - Returns a list of XP records for a user
    - GET /users/:studentId/xp?courseId=:courseId - Returns XP for a specific course
    - GET /users/:studentId/xp?courseCode=:courseCode - Returns XP for a specific course code
    - GET /users/:studentId/xp?subject=:subject - Returns XP for a specific subject
    - GET /users/:studentId/xp?itemId=:itemId - Returns XP for a specific item
    - POST /users/:studentId/xp - Creates a new XP record for a user
    
    Database Table: xp
    Related Tables:
    - users (via userId)
    - courses (via course_id)
    - items (via item_id)
    
    Attributes:
        id: The XP record's numeric ID
        uuid: The XP record's UUID
        user_id: The ID of the user who earned the XP (userId in API)
        user_uuid: The UUID of the user who earned the XP (user_uuid in API)
        course_id: The ID of the course the XP is for (course_id in API)
        course_code: The code of the course the XP is for (courseCode in API)
        item_id: The ID of the item the XP is for (item_id in API)
        subject: The subject the XP is for
        amount: The amount of XP awarded
        awarded_on: When the XP was awarded (awardedOn in API)
        app_name: The name of the app (appName in API)
    """
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    user_id: int = Field(alias="userId")
    user_uuid: Optional[UUID] = Field(None, alias="user_uuid")
    course_id: Optional[int] = Field(None, alias="course_id")
    course_code: Optional[str] = Field(None, alias="courseCode")
    item_id: Optional[int] = Field(None, alias="item_id")
    subject: Optional[str] = None
    amount: int
    awarded_on: Optional[datetime] = Field(None, alias="awardedOn")
    app_name: Optional[str] = Field(None, alias="appName")
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations, excluding read-only fields.
        
        This method is used when creating a new XP record via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new XP record
        """
        return self.model_dump(
            exclude={'id', 'uuid', 'awarded_on'}, 
            exclude_unset=True, 
            by_alias=True
        ) 
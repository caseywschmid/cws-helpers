"""
Enrollment and Progress models for PowerPath API.

This module provides models for working with enrollment and user progress data in the PowerPath API.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field

from .base import PowerPathBase


class PowerPathEnrollment(PowerPathBase):
    """
    PowerPath Enrollment model.
    
    This model represents a user's enrollment in a course.
    
    Database Table: enrollment
    Related Tables:
    - users (via userId)
    - courses (via courseId)
    
    Attributes:
        id: The enrollment's numeric ID
        uuid: The enrollment's UUID
        user_id: The ID of the enrolled user (userId in API)
        user_id_uuid: The UUID of the enrolled user (userIdUUID in API)
        course_id: The ID of the course (courseId in API)
        course_uuid: The UUID of the course (courseUUID in API)
        role: The user's role in the course
        status: The enrollment status
        begin_date: When the enrollment begins (beginDate in API)
        end_date: When the enrollment ends (endDate in API)
        primary: Whether this is the user's primary enrollment
        school: The school associated with the enrollment
        metadata: Additional metadata
        date_last_modified: When the enrollment was last modified (dateLastModified in API)
    """
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    user_id: int = Field(alias="userId")
    user_id_uuid: Optional[UUID] = Field(None, alias="userIdUUID")
    course_id: int = Field(alias="courseId")
    course_uuid: Optional[UUID] = Field(None, alias="courseUUID")
    role: Optional[str] = None
    status: Optional[str] = None
    begin_date: Optional[date] = Field(None, alias="beginDate")
    end_date: Optional[date] = Field(None, alias="endDate")
    primary: Optional[str] = None
    school: Optional[str] = None
    metadata: Optional[str] = None
    date_last_modified: Optional[datetime] = Field(None, alias="dateLastModified")
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations, excluding read-only fields.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new enrollment
        """
        return self.model_dump(
            exclude={'id', 'uuid', 'date_last_modified'}, 
            exclude_unset=True, 
            by_alias=True
        )
    
    def to_update_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for PATCH operations, excluding read-only fields.
        
        Returns:
            Dict[str, Any]: Dictionary for updating an existing enrollment
        """
        return self.model_dump(
            exclude={'id', 'uuid', 'date_last_modified'}, 
            exclude_unset=True, 
            exclude_none=True,
            by_alias=True
        )


class PowerPathUserModuleItem(PowerPathBase):
    """
    PowerPath User Module Item model.
    
    This model represents a user's progress on a specific item within a module.
    
    Database Table: userModuleItems
    Related Tables:
    - users (via userId)
    - items (via itemId)
    - results (via clrResultId)
    
    Attributes:
        user_id: The ID of the user (userId in API)
        user_uuid: The UUID of the user (userUUID in API)
        item_id: The ID of the item (itemId in API)
        item_uuid: The UUID of the item (itemUUID in API)
        clr_result_id: The ID of the CLR result (clrResultId in API)
        clr_result_uuid: The UUID of the CLR result (clrResultUUID in API)
        attempt: The attempt number
        started_at: When the user started the item (startedAt in API)
        completed_at: When the user completed the item (completedAt in API)
    """
    user_id: int = Field(alias="userId")
    user_uuid: Optional[UUID] = Field(None, alias="userUUID")
    item_id: int = Field(alias="itemId")
    item_uuid: Optional[UUID] = Field(None, alias="itemUUID")
    clr_result_id: Optional[int] = Field(None, alias="clrResultId")
    clr_result_uuid: Optional[UUID] = Field(None, alias="clrResultUUID")
    attempt: Optional[int] = None
    started_at: Optional[datetime] = Field(None, alias="startedAt")
    completed_at: Optional[datetime] = Field(None, alias="completedAt")


class PowerPathUserModuleSequence(PowerPathBase):
    """
    PowerPath User Module Sequence model.
    
    This model represents a customized sequence of modules for a user.
    
    Database Table: userModuleSequence
    Related Tables:
    - users (via userId)
    - modules (via originModuleId, insertedModuleId, destinationModuleId)
    
    Attributes:
        id: The sequence's numeric ID
        user_id: The ID of the user (userId in API)
        user_uuid: The UUID of the user (userUUID in API)
        origin_module_id: The ID of the origin module (originModuleId in API)
        origin_module_uuid: The UUID of the origin module (originModuleUUID in API)
        inserted_module_id: The ID of the inserted module (insertedModuleId in API)
        inserted_module_uuid: The UUID of the inserted module (insertedModuleUUID in API)
        destination_module_id: The ID of the destination module (destinationModuleId in API)
        destination_module_uuid: The UUID of the destination module (destinationModuleUUID in API)
    """
    id: Optional[int] = None
    user_id: int = Field(alias="userId")
    user_uuid: Optional[UUID] = Field(None, alias="userUUID")
    origin_module_id: int = Field(alias="originModuleId")
    origin_module_uuid: Optional[UUID] = Field(None, alias="originModuleUUID")
    inserted_module_id: int = Field(alias="insertedModuleId")
    inserted_module_uuid: Optional[UUID] = Field(None, alias="insertedModuleUUID")
    destination_module_id: int = Field(alias="destinationModuleId")
    destination_module_uuid: Optional[UUID] = Field(None, alias="destinationModuleUUID")


class PowerPathGradeLevelTest(PowerPathBase):
    """
    PowerPath Grade Level Test model.
    
    This model represents a grade level test.
    
    Database Table: gradeLevelTests
    Related Tables:
    - items (via itemId)
    - courses (via courseId)
    
    Attributes:
        id: The test's numeric ID
        item_id: The ID of the item (itemId in API)
        course_id: The ID of the course (courseId in API)
    """
    id: Optional[int] = None
    item_id: int = Field(alias="itemId")
    course_id: int = Field(alias="courseId") 
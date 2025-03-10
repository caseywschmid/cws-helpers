"""
Course models for PowerPath API.

This module provides models for working with course data in the PowerPath API.
It includes models for courses and related data.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field

from .base import PowerPathBase


class PowerPathCourse(PowerPathBase):
    """
    PowerPath Course model.
    
    This model represents a course in the PowerPath system.
    
    API Endpoints:
    - GET /courses - Returns a list of courses
    - GET /courses/:courseId - Returns a single course
    - POST /courses - Creates a new course
    - PATCH /courses/:courseId - Updates an existing course
    - DELETE /courses/:courseId - Deletes a course
    
    Database Table: courses
    Related Tables: 
    - modules (via defaultModuleId)
    
    Attributes:
        id: The course's numeric ID
        uuid: The course's UUID
        title: The course's title
        course_code: The course's code (courseCode in API)
        school_year: The school year for the course (schoolYear in API)
        grades: The grade levels for the course
        subjects: The subjects covered by the course
        subject_codes: The subject codes for the course (subjectCodes in API)
        status: The course's status
        metadata: Additional metadata for the course
        default_module_id: The ID of the default module (defaultModuleId in API)
        default_module_uuid: The UUID of the default module (defaultModuleUUID in API)
        is_placement_test: Whether the course is a placement test (isPlacementTest in API)
        app_name: The name of the app (appName in API)
        date_last_modified: When the course was last modified (dateLastModified in API)
    """
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    title: str
    course_code: str = Field(alias="courseCode")
    school_year: Optional[str] = Field(None, alias="schoolYear")
    grades: Optional[str] = None
    subjects: Optional[str] = None
    subject_codes: Optional[str] = Field(None, alias="subjectCodes")
    status: Optional[str] = None
    metadata: Optional[str] = None
    default_module_id: Optional[int] = Field(None, alias="defaultModuleId")
    default_module_uuid: Optional[UUID] = Field(None, alias="defaultModuleUUID")
    is_placement_test: Optional[bool] = Field(None, alias="isPlacementTest")
    app_name: Optional[str] = Field(None, alias="appName")
    date_last_modified: Optional[datetime] = Field(None, alias="dateLastModified")
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations, excluding read-only fields.
        
        This method is used when creating a new course via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new course
        """
        return self.model_dump(
            exclude={'id', 'uuid', 'date_last_modified'}, 
            exclude_unset=True, 
            by_alias=True
        )
    
    def to_update_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for PATCH operations, excluding read-only fields.
        
        This method is used when updating an existing course via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for updating an existing course
        """
        return self.model_dump(
            exclude={'id', 'uuid', 'date_last_modified'}, 
            exclude_unset=True, 
            exclude_none=True,
            by_alias=True
        ) 
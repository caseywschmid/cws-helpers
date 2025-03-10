"""
User models for PowerPath API.

This module provides models for working with user data in the PowerPath API.
It includes models for user profiles, user progress, and related data.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field, field_validator

from .base import PowerPathBase


class PowerPathUser(PowerPathBase):
    """
    PowerPath User model.
    
    This model represents a user in the PowerPath system.
    
    API Endpoints:
    - GET /users - Returns a list of users
    - GET /users/:studentId - Returns a single user
    - POST /users - Creates a new user
    - PATCH /users/:studentId - Updates an existing user
    - DELETE /users/:studentId - Deletes a user
    
    Database Table: users
    
    Attributes:
        id: The user's numeric ID
        uuid: The user's UUID
        email: The user's email address
        given_name: The user's first name (givenName in API)
        family_name: The user's last name (familyName in API)
        username: The user's username
        preferred_first_name: The user's preferred first name
        preferred_last_name: The user's preferred last name
        preferred_middle_name: The user's preferred middle name
        middle_name: The user's middle name
        status: The user's status
        grades: The user's grade levels
        pronouns: The user's pronouns
        phone: The user's phone number
        sms: The user's SMS number
        reading_level: The user's reading level
        date_last_modified: When the user was last modified
    """
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    email: str
    given_name: str = Field(alias="givenName")
    family_name: str = Field(alias="familyName")
    username: Optional[str] = None
    preferred_first_name: Optional[str] = Field(None, alias="preferredFirstName")
    preferred_last_name: Optional[str] = Field(None, alias="preferredLastName")
    preferred_middle_name: Optional[str] = Field(None, alias="preferredMiddleName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    status: Optional[str] = None
    grades: Optional[str] = None
    pronouns: Optional[str] = None
    phone: Optional[str] = None
    sms: Optional[str] = None
    reading_level: Optional[int] = Field(None, alias="readingLevel")
    date_last_modified: Optional[datetime] = Field(None, alias="dateLastModified")
    
    @field_validator('email')
    @classmethod
    def email_must_be_valid(cls, v: str) -> str:
        """
        Validate email format.
        
        Args:
            v: The email value to validate
            
        Returns:
            str: The validated email
            
        Raises:
            ValueError: If the email is invalid
        """
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations, excluding read-only fields.
        
        This method is used when creating a new user via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new user
        """
        return self.model_dump(
            exclude={'id', 'uuid', 'date_last_modified'}, 
            exclude_unset=True, 
            by_alias=True
        )
    
    def to_update_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for PATCH operations, excluding read-only fields.
        
        This method is used when updating an existing user via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for updating an existing user
        """
        return self.model_dump(
            exclude={'id', 'uuid', 'date_last_modified'}, 
            exclude_unset=True, 
            exclude_none=True,
            by_alias=True
        )

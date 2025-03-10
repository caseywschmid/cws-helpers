"""
Content Creation models for PowerPath API.

This module provides models for working with content creation data in the PowerPath API.
These models represent questions, responses, and other content elements.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
import json
from pydantic import BaseModel, Field, field_validator

from .base import PowerPathBase


class PowerPathCCItem(PowerPathBase):
    """
    PowerPath Content Creation Item model.
    
    This model represents a content creation item in the PowerPath system.
    CC Items are questions or other content elements.
    
    API Endpoints:
    - GET /modules/:moduleId/items/:itemId/questionBank - Returns a list of CC items
    - POST /modules/ccItem - Creates a new CC item
    - GET /modules/ccItem/:ccItemId - Returns a specific CC item
    - PUT /modules/ccItem/:ccItemId - Updates a CC item
    
    Database Table: ccItem
    Related Tables:
    - ccItemObjectBank (via ccItemId)
    - ccItemResults (via ccItemId)
    - response (via ccItemId)
    
    Attributes:
        id: The item's numeric ID
        uuid: The item's UUID
        material: The item's content material
        grade: The grade level for the item
        difficulty: The difficulty level of the item
        reference_text: Reference text for the item (referenceText in API)
        explanation: Explanation for the item
        metadata: JSON data with additional metadata
    """
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    material: str
    grade: Optional[int] = None
    difficulty: Optional[int] = None
    reference_text: Optional[str] = Field(None, alias="referenceText")
    explanation: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @field_validator('metadata', mode='before')
    @classmethod
    def parse_json_if_string(cls, v):
        """Parse JSON string to dict if needed."""
        if isinstance(v, str):
            return json.loads(v)
        return v


class PowerPathResponse(PowerPathBase):
    """
    PowerPath Response model.
    
    This model represents a response option for a content creation item.
    
    API Endpoints:
    - POST /modules/ccItem/:ccItemId/responses - Creates a new response
    - PUT /modules/responses/:responseId - Updates a response
    - DELETE /modules/responses/:responseId - Deletes a response
    
    Database Table: response
    Related Tables:
    - ccItem (via ccItemId)
    - ccItemResults (via responseId)
    
    Attributes:
        id: The response's numeric ID
        cc_item_id: The ID of the CC item this response belongs to (ccItemId in API)
        label: The response label
        explanation: Explanation for this response
        is_correct: Whether this response is correct (isCorrect in API)
    """
    id: Optional[int] = None
    cc_item_id: int = Field(alias="ccItemId")
    label: str
    explanation: Optional[str] = None
    is_correct: bool = Field(alias="isCorrect")


class PowerPathObjectBank(PowerPathBase):
    """
    PowerPath Object Bank model.
    
    This model represents an object bank in the PowerPath system.
    Object banks are collections of items.
    
    Database Table: objectBank
    Related Tables:
    - items (via itemId)
    - ccItemObjectBank (via objectBankId)
    
    Attributes:
        id: The object bank's numeric ID
        uuid: The object bank's UUID
        item_id: The ID of the item this object bank belongs to (itemId in API)
        item_uuid: The UUID of the item this object bank belongs to (itemUUID in API)
    """
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    item_id: int = Field(alias="itemId")
    item_uuid: Optional[UUID] = Field(None, alias="itemUUID")


class PowerPathCCItemObjectBank(PowerPathBase):
    """
    PowerPath CC Item Object Bank model.
    
    This model represents a relationship between a CC item and an object bank.
    
    Database Table: ccItemObjectBank
    Related Tables:
    - ccItem (via ccItemId)
    - objectBank (via objectBankId)
    
    Attributes:
        cc_item_id: The ID of the CC item (ccItemId in API)
        cc_item_uuid: The UUID of the CC item (ccItemUUID in API)
        object_bank_id: The ID of the object bank (objectBankId in API)
        object_bank_uuid: The UUID of the object bank (objectBankUUID in API)
    """
    cc_item_id: int = Field(alias="ccItemId")
    cc_item_uuid: Optional[UUID] = Field(None, alias="ccItemUUID")
    object_bank_id: int = Field(alias="objectBankId")
    object_bank_uuid: Optional[UUID] = Field(None, alias="objectBankUUID")


class PowerPathCCItemResult(PowerPathBase):
    """
    PowerPath CC Item Result model.
    
    This model represents a result for a content creation item.
    
    Database Table: ccItemResults
    Related Tables:
    - ccItem (via ccItemId)
    - response (via responseId)
    - results (via resultId)
    - users (via userId)
    
    Attributes:
        cc_item_id: The ID of the CC item (ccItemId in API)
        cc_item_uuid: The UUID of the CC item (ccItemUUID in API)
        response_id: The ID of the response (responseId in API)
        response: The text of the response
        result_id: The ID of the result (resultId in API)
        result_uuid: The UUID of the result (resultUUID in API)
        user_id: The ID of the user (userId in API)
        is_correct: Whether the response was correct (isCorrect in API)
        created_at: When the result was created (createdAt in API)
    """
    cc_item_id: int = Field(alias="ccItemId")
    cc_item_uuid: Optional[UUID] = Field(None, alias="ccItemUUID")
    response_id: Optional[int] = Field(None, alias="responseId")
    response: Optional[str] = None
    result_id: Optional[int] = Field(None, alias="resultId")
    result_uuid: Optional[UUID] = Field(None, alias="resultUUID")
    user_id: int = Field(alias="userId")
    is_correct: bool = Field(alias="isCorrect")
    created_at: Optional[datetime] = Field(None, alias="createdAt") 
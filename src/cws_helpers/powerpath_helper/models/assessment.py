"""
Assessment models for PowerPath API.

This module provides models for working with assessment data in the PowerPath API.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field

from .base import PowerPathBase


class PowerPathAssessmentResult(PowerPathBase):
    """
    PowerPath Assessment Result model.
    
    This model represents an assessment result in the PowerPath system.
    Assessment results are standardized test scores or other external assessments.
    
    Database Table: AssessmentResults
    Related Tables:
    - users (via user_id)
    
    Attributes:
        id: The assessment result's numeric ID
        user_id: The ID of the user who took the assessment
        user_uuid: The UUID of the user who took the assessment
        subject_name: The subject of the assessment
        test_name: The name of the assessment test
        term_name: The term when the assessment was taken
        test_date: The date when the assessment was taken
        score: The raw score on the assessment
        percentile: The percentile score on the assessment
        projected_growth: The projected growth based on the assessment
        observed_growth: The observed growth based on the assessment
    """
    id: Optional[int] = None
    user_id: int
    user_uuid: Optional[UUID] = Field(None, alias="userUUID")
    subject_name: str = Field(alias="subject_name")
    test_name: str = Field(alias="test_name")
    term_name: Optional[str] = Field(None, alias="term_name")
    test_date: Optional[date] = Field(None, alias="test_date")
    score: Optional[int] = None
    percentile: Optional[int] = None
    projected_growth: Optional[float] = Field(None, alias="projected_growth")
    observed_growth: Optional[float] = Field(None, alias="observed_growth")
    
    def to_create_dict(self) -> Dict[str, Any]:
        """
        Convert model to dict for POST operations, excluding read-only fields.
        
        This method is used when creating a new assessment result via the API.
        
        Returns:
            Dict[str, Any]: Dictionary for creating a new assessment result
        """
        return self.model_dump(
            exclude={'id'}, 
            exclude_unset=True, 
            by_alias=True
        ) 
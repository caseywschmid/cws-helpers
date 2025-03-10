"""
PowerPath API models.

This package contains Pydantic models for the PowerPath API.
These models provide type-safe representations of the API's data structures.
"""

from .base import PowerPathBase
from .user import PowerPathUser
from .course import PowerPathCourse
from .module import PowerPathModule, PowerPathItem
from .goal import PowerPathGoal
from .xp import PowerPathXP
from .result import PowerPathResult
from .association import PowerPathItemAssociation, PowerPathModuleAssociation
from .assessment import PowerPathAssessmentResult
from .curriculum import PowerPathCFDocument, PowerPathCFItem, PowerPathCFAssociation
from .content import (
    PowerPathCCItem,
    PowerPathResponse,
    PowerPathObjectBank,
    PowerPathCCItemObjectBank,
    PowerPathCCItemResult,
)
from .enrollment import (
    PowerPathEnrollment,
    PowerPathUserModuleItem,
    PowerPathUserModuleSequence,
    PowerPathGradeLevelTest,
)

__all__ = [
    # Base model
    'PowerPathBase',
    
    # User models
    'PowerPathUser',
    
    # Course models
    'PowerPathCourse',
    'PowerPathModule',
    'PowerPathItem',
    
    # Progress models
    'PowerPathGoal',
    'PowerPathXP',
    'PowerPathResult',
    
    # Relationship models
    'PowerPathItemAssociation',
    'PowerPathModuleAssociation',
    
    # Assessment models
    'PowerPathAssessmentResult',
    
    # Curriculum models
    'PowerPathCFDocument',
    'PowerPathCFItem',
    'PowerPathCFAssociation',
    
    # Content models
    'PowerPathCCItem',
    'PowerPathResponse',
    'PowerPathObjectBank',
    'PowerPathCCItemObjectBank',
    'PowerPathCCItemResult',
    
    # Enrollment models
    'PowerPathEnrollment',
    'PowerPathUserModuleItem',
    'PowerPathUserModuleSequence',
    'PowerPathGradeLevelTest',
]

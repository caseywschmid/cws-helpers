"""
PowerPath API Helper.

This package provides tools for working with the PowerPath API.
It includes models, API clients, utility functions, and usage examples.

The package is self-contained and includes:
- Models for all PowerPath resources
- A client for making API requests
- API functions for interacting with PowerPath endpoints
- Examples demonstrating how to use the package

To see examples of how to use this package, check the 'examples' directory.
"""

# Import models
from .models import (
    # Base model
    PowerPathBase,
    
    # User models
    PowerPathUser,
    
    # Course models
    PowerPathCourse,
    PowerPathModule,
    PowerPathItem,
    
    # Progress models
    PowerPathGoal,
    PowerPathXP,
    PowerPathResult,
    
    # Relationship models
    PowerPathItemAssociation,
    PowerPathModuleAssociation,
    
    # Assessment models
    PowerPathAssessmentResult,
    
    # Curriculum models
    PowerPathCFDocument,
    PowerPathCFItem,
    PowerPathCFAssociation,
    
    # Content models
    PowerPathCCItem,
    PowerPathResponse,
    PowerPathObjectBank,
    PowerPathCCItemObjectBank,
    PowerPathCCItemResult,
    
    # Enrollment models
    PowerPathEnrollment,
    PowerPathUserModuleItem,
    PowerPathUserModuleSequence,
    PowerPathGradeLevelTest,
)

# Import client
from .core import (
    PowerPathClient,
    PowerPathClientError,
    PowerPathRequestError,
    PowerPathAuthenticationError,
    PowerPathNotFoundError,
    PowerPathServerError,
    PowerPathRateLimitError,
)

# Import API functions
from .api import (
    # Courses
    get_all_courses,
    get_course,
    create_course,
    update_course,
    delete_course,
    
    # Users
    get_all_users,
    search_users,
    list_users,
    get_user,
    create_user,
    update_user,
    delete_user,
    
    # Modules
    get_all_modules,
    get_module,
    create_module,
    update_module,
    delete_module,
    
    # Module Associations
    get_module_associations,
    create_module_association,
    update_module_association,
    delete_module_association,
    
    # Items
    get_module_items,
    get_module_item,
    create_module_item,
    update_module_items,
    
    # Item Associations
    get_item_associations,
    create_item_association,
    associate_item_with_module,
    update_item_associations,
    delete_item_associations,
    delete_item_association,
    
    # Questions
    get_question,
    create_question,
    update_question,
    
    # Responses
    create_question_response,
    update_response,
    delete_response,
    
    # Question Banks
    get_question_bank,
    create_question_bank_item,
    delete_question_bank_item,
    delete_object_bank,
    
    # Results
    get_user_results,
    get_user_result,
    create_user_result,
    update_user_result,
    delete_user_result,
    
    # XP
    get_user_xp,
    create_user_xp,
    
    # Goals
    get_user_goals,
    create_user_goal,
    update_user_goal,
    delete_user_goal,
    get_course_goals,
    
    # Progress
    get_user_course_progress,
    get_user_course_progress_v2,
    get_user_module_progress,
    get_user_item_progress,
    
    # SQL
    execute_sql_query,
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
    
    # Client
    'PowerPathClient',
    'PowerPathClientError',
    'PowerPathRequestError',
    'PowerPathAuthenticationError',
    'PowerPathNotFoundError',
    'PowerPathServerError',
    'PowerPathRateLimitError',
    
    # API functions - Courses
    'get_all_courses',
    'get_course',
    'create_course',
    'update_course',
    'delete_course',
    
    # API functions - Users
    'get_all_users',
    'search_users',
    'list_users',
    'get_user',
    'create_user',
    'update_user',
    'delete_user',
    
    # API functions - Modules
    'get_all_modules',
    'get_module',
    'create_module',
    'update_module',
    'delete_module',
    
    # API functions - Module Associations
    'get_module_associations',
    'create_module_association',
    'update_module_association',
    'delete_module_association',
    
    # API functions - Items
    'get_module_items',
    'get_module_item',
    'create_module_item',
    'update_module_items',
    
    # API functions - Item Associations
    'get_item_associations',
    'create_item_association',
    'associate_item_with_module',
    'update_item_associations',
    'delete_item_associations',
    'delete_item_association',
    
    # API functions - Questions
    'get_question',
    'create_question',
    'update_question',
    
    # API functions - Responses
    'create_question_response',
    'update_response',
    'delete_response',
    
    # API functions - Question Banks
    'get_question_bank',
    'create_question_bank_item',
    'delete_question_bank_item',
    'delete_object_bank',
    
    # API functions - Results
    'get_user_results',
    'get_user_result',
    'create_user_result',
    'update_user_result',
    'delete_user_result',
    
    # API functions - XP
    'get_user_xp',
    'create_user_xp',
    
    # API functions - Goals
    'get_user_goals',
    'create_user_goal',
    'update_user_goal',
    'delete_user_goal',
    'get_course_goals',
    
    # API functions - Progress
    'get_user_course_progress',
    'get_user_course_progress_v2',
    'get_user_module_progress',
    'get_user_item_progress',
    
    # API functions - SQL
    'execute_sql_query',
]

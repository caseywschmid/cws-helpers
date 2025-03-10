"""
PowerPath API endpoints.

This package provides functions for working with the PowerPath API endpoints.
"""

# Courses API
from .courses import (
    get_all_courses,
    get_course,
    create_course,
    update_course,
    delete_course,
)

# Users API
from .users import (
    get_all_users,
    search_users,
    list_users,
    get_user,
    create_user,
    update_user,
    delete_user,
)

# Modules API
from .modules import (
    get_all_modules,
    get_module,
    create_module,
    update_module,
    delete_module,
)

# Module Associations API
from .module_associations import (
    get_module_associations,
    create_module_association,
    update_module_association,
    delete_module_association,
)

# Items API
from .items import (
    get_module_items,
    get_module_item,
    create_module_item,
    update_module_items,
)

# Item Associations API
from .item_associations import (
    get_item_associations,
    create_item_association,
    associate_item_with_module,
    update_item_associations,
    delete_item_associations,
    delete_item_association,
)

# Questions API
from .questions import (
    get_question,
    create_question,
    update_question,
)

# Responses API
from .responses import (
    create_question_response,
    update_response,
    delete_response,
)

# Question Banks API
from .question_banks import (
    get_question_bank,
    create_question_bank_item,
    delete_question_bank_item,
    delete_object_bank,
)

# Results API
from .results import (
    get_user_results,
    get_user_result,
    create_user_result,
    update_user_result,
    delete_user_result,
)

# XP API
from .xp import (
    get_user_xp,
    create_user_xp,
)

# Goals API
from .goals import (
    get_user_goals,
    create_user_goal,
    update_user_goal,
    delete_user_goal,
    get_course_goals,
)

# Progress API
from .progress import (
    get_user_course_progress,
    get_user_course_progress_v2,
    get_user_module_progress,
    get_user_item_progress,
)

# SQL API
from .sql import (
    execute_sql_query,
)

__all__ = [
    # Courses
    'get_all_courses',
    'get_course',
    'create_course',
    'update_course',
    'delete_course',
    
    # Users
    'get_all_users',
    'search_users',
    'list_users',
    'get_user',
    'create_user',
    'update_user',
    'delete_user',
    
    # Modules
    'get_all_modules',
    'get_module',
    'create_module',
    'update_module',
    'delete_module',
    
    # Module Associations
    'get_module_associations',
    'create_module_association',
    'update_module_association',
    'delete_module_association',
    
    # Items
    'get_module_items',
    'get_module_item',
    'create_module_item',
    'update_module_items',
    
    # Item Associations
    'get_item_associations',
    'create_item_association',
    'associate_item_with_module',
    'update_item_associations',
    'delete_item_associations',
    'delete_item_association',
    
    # Questions
    'get_question',
    'create_question',
    'update_question',
    
    # Responses
    'create_question_response',
    'update_response',
    'delete_response',
    
    # Question Banks
    'get_question_bank',
    'create_question_bank_item',
    'delete_question_bank_item',
    'delete_object_bank',
    
    # Results
    'get_user_results',
    'get_user_result',
    'create_user_result',
    'update_user_result',
    'delete_user_result',
    
    # XP
    'get_user_xp',
    'create_user_xp',
    
    # Goals
    'get_user_goals',
    'create_user_goal',
    'update_user_goal',
    'delete_user_goal',
    'get_course_goals',
    
    # Progress
    'get_user_course_progress',
    'get_user_course_progress_v2',
    'get_user_module_progress',
    'get_user_item_progress',
    
    # SQL
    'execute_sql_query',
] 
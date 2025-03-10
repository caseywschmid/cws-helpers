"""
Progress API functions for PowerPath.

This module provides functions for working with user progress in the PowerPath API.
It includes operations for retrieving user progress for courses, modules, and items.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient
from ..models import PowerPathModule, PowerPathItem


def get_user_course_progress(client: PowerPathClient, user_id: str, course_id: str) -> List[PowerPathModule]:
    """
    Get progress for a user in a specific course.
    
    This function retrieves the progress for a specific user in a specific course from the PowerPath API.
    The XP parameter for items will be different depending on whether the item is complete or not:
    - If not complete, it's the 100% XP value
    - If complete, it's the XP value the user earned
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to get progress for
        course_id: The ID of the course to get progress for
        
    Returns:
        A list of PowerPathModule objects representing the user's progress in the course
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}/courses/{course_id}"
    response = client.get(endpoint)
    
    # Convert the response to PowerPathModule objects
    modules = [PowerPathModule.model_validate(module) for module in response]
    return modules


def get_user_course_progress_v2(client: PowerPathClient, user_id: str, course_id: str) -> List[PowerPathModule]:
    """
    Get progress for a user in a specific course (faster version).
    
    This function is a faster version of get_user_course_progress. It returns the same data
    except the Items don't contain the "attempts" and "uuid" fields (which aren't used anyway).
    
    The XP parameter for items will be different depending on whether the item is complete or not:
    - If not complete, it's the 100% XP value
    - If complete, it's the XP value the user earned
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to get progress for
        course_id: The ID of the course to get progress for
        
    Returns:
        A list of PowerPathModule objects representing the user's progress in the course
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}/courses/{course_id}/v2"
    response = client.get(endpoint)
    
    # Convert the response to PowerPathModule objects
    modules = [PowerPathModule.model_validate(module) for module in response]
    return modules


def get_user_module_progress(client: PowerPathClient, user_id: str, module_id: str) -> List[PowerPathModule]:
    """
    Get progress for a user in a specific module.
    
    This function retrieves the progress for a specific user in a specific module from the PowerPath API.
    The XP parameter for items will be different depending on whether the item is complete or not:
    - If not complete, it's the 100% XP value
    - If complete, it's the XP value the user earned
    
    This endpoint returns the metadata for each Item in the Module, which is different from the course endpoint.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to get progress for
        module_id: The ID of the module to get progress for
        
    Returns:
        A list of PowerPathModule objects representing the user's progress in the module
        (though there's only one module in the array)
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}/modules/{module_id}"
    response = client.get(endpoint)
    
    # Convert the response to PowerPathModule objects
    modules = [PowerPathModule.model_validate(module) for module in response]
    return modules


def get_user_item_progress(client: PowerPathClient, user_id: str, item_id: str) -> Dict[str, Any]:
    """
    Get progress for a user on a specific item.
    
    This function retrieves the progress for a specific user on a specific item from the PowerPath API.
    The XP parameter will be different depending on whether the item is complete or not:
    - If not complete, it's the 100% XP value
    - If complete, it's the XP value the user earned
    
    This endpoint returns the metadata for the Item, which is different from the course endpoint.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to get progress for
        item_id: The ID of the item to get progress for
        
    Returns:
        A dictionary representing the user's progress on the item (SingleItemProgress)
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}/items/{item_id}"
    response = client.get(endpoint)
    
    # Return the response as is, since we don't have a specific model for SingleItemProgress
    return response 
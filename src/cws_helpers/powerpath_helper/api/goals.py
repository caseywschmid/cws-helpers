"""
Goals API functions for PowerPath.

This module provides functions for working with user goals in the PowerPath API.
It includes operations for creating, retrieving, updating, and deleting goals for users,
as well as retrieving goals for courses.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient
from ..models import PowerPathGoal, PowerPathUser


def get_user_goals(client: PowerPathClient, user_id: str) -> List[PowerPathGoal]:
    """
    Get all goals for a specific user.
    
    This function retrieves all goals for a specific user from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to get goals for
        
    Returns:
        A list of PowerPathGoal objects representing the user's goals
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}/goals"
    response = client.get(endpoint)
    
    # Convert the response to PowerPathGoal objects
    goals = [PowerPathGoal.model_validate(goal) for goal in response]
    return goals


def create_user_goal(client: PowerPathClient, user_id: str, goal_data: Dict[str, Any]) -> PowerPathGoal:
    """
    Create a new goal for a user.
    
    This function creates a new goal for a specific user in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to create the goal for
        goal_data: The data for the new goal
            Required fields:
            - description: The goal's description
            - xp: The XP target for the goal
            - courseId: The ID of the course the goal is for
            Optional fields:
            - cutoffDate: The deadline for the goal
            - dailyOverride: Daily XP override
            
    Returns:
        A PowerPathGoal object representing the newly created goal
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}/goals"
    response = client.post(endpoint, json_data=goal_data)
    
    # Convert the response to a PowerPathGoal object
    goal = PowerPathGoal.model_validate(response)
    return goal


def update_user_goal(client: PowerPathClient, user_id: str, goal_id: str, goal_data: Dict[str, Any]) -> PowerPathGoal:
    """
    Update an existing goal for a user.
    
    This function updates an existing goal for a specific user in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user who owns the goal
        goal_id: The ID of the goal to update
        goal_data: The updated data for the goal
            Optional fields:
            - description: The goal's description
            - xp: The XP target for the goal
            - courseId: The ID of the course the goal is for
            - cutoffDate: The deadline for the goal
            - dailyOverride: Daily XP override
            
    Returns:
        A PowerPathGoal object representing the updated goal
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}/goals/{goal_id}"
    response = client.patch(endpoint, json_data=goal_data)
    
    # Convert the response to a PowerPathGoal object
    goal = PowerPathGoal.model_validate(response)
    return goal


def delete_user_goal(client: PowerPathClient, user_id: str, goal_id: str) -> Dict[str, Any]:
    """
    Delete a goal for a user.
    
    This function deletes a goal for a specific user in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user who owns the goal
        goal_id: The ID of the goal to delete
        
    Returns:
        A dictionary containing the API response
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}/goals/{goal_id}"
    response = client.delete(endpoint)
    
    return response


def get_course_goals(client: PowerPathClient, course_id: str) -> List[PowerPathUser]:
    """
    Get all goals for a specific course.
    
    This function retrieves all users with goals for a specific course from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        course_id: The ID of the course to get goals for
        
    Returns:
        A list of PowerPathUser objects representing users with goals for the course
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/courses/{course_id}/goals"
    response = client.get(endpoint)
    
    # Convert the response to PowerPathUser objects
    users = [PowerPathUser.model_validate(user) for user in response]
    return users 
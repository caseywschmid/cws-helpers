"""
XP API functions for PowerPath.

This module provides functions for working with experience points (XP) in the PowerPath API.
It includes operations for retrieving and creating XP records for users, with various filtering options.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from ..core import PowerPathClient
from ..models import PowerPathXP


def get_user_xp(
    client: PowerPathClient,
    user_id: str,
    course_id: Optional[str] = None,
    course_code: Optional[str] = None,
    subject: Optional[str] = None,
    item_id: Optional[str] = None
) -> List[PowerPathXP]:
    """
    Get XP records for a user with optional filters.
    
    This function retrieves XP records for a specific user from the PowerPath API.
    It supports filtering by course ID, course code, subject, or item ID.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to get XP records for
        course_id: Optional filter for a specific course ID
        course_code: Optional filter for a specific course code
        subject: Optional filter for a specific subject
        item_id: Optional filter for a specific item ID
        
    Returns:
        A list of PowerPathXP objects representing the user's XP records
        
    Raises:
        HTTPError: If the API request fails
    """
    # Build query parameters based on provided filters
    params = {}
    if course_id:
        params["courseId"] = course_id
    if course_code:
        params["courseCode"] = course_code
    if subject:
        params["subject"] = subject
    if item_id:
        params["itemId"] = item_id
    
    # Make the API request
    endpoint = f"/users/{user_id}/xp"
    response = client.get(endpoint, params=params)
    
    # Convert the response to PowerPathXP objects
    xp_records = [PowerPathXP.model_validate(xp) for xp in response]
    return xp_records


def create_user_xp(client: PowerPathClient, user_id: str, xp_data: Dict[str, Any]) -> PowerPathXP:
    """
    Create a new XP record for a user.
    
    This function creates a new XP record for a specific user in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to create the XP record for
        xp_data: The data for the new XP record
            Required fields:
            - amount: The amount of XP to award
            Optional fields:
            - courseId: The ID of the course the XP is for
            - courseCode: The code of the course the XP is for
            - itemId: The ID of the item the XP is for
            - subject: The subject the XP is for
            - appName: The name of the app
            
    Returns:
        A PowerPathXP object representing the newly created XP record
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}/xp"
    response = client.post(endpoint, json=xp_data)
    
    # Convert the response to a PowerPathXP object
    xp_record = PowerPathXP.model_validate(response)
    return xp_record 
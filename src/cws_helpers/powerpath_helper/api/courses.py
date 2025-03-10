"""
PowerPath API courses endpoints.

This module provides functions for working with courses in the PowerPath API.
"""

from typing import List, Optional, Dict, Any

from ..core import PowerPathClient
from ..models import PowerPathCourse


def get_all_courses(client: PowerPathClient) -> List[PowerPathCourse]:
    """
    Get all courses from the PowerPath API.
    
    This function corresponds to the GET /courses endpoint.
    
    Args:
        client: The PowerPath API client
        
    Returns:
        List[PowerPathCourse]: A list of course objects
        
    Raises:
        PowerPathClientError: If the request fails
    """
    return client.get_resources("/courses", PowerPathCourse)


def get_course(client: PowerPathClient, course_id: str) -> PowerPathCourse:
    """
    Get a specific course by ID.
    
    This function corresponds to the GET /courses/:courseId endpoint.
    
    Args:
        client: The PowerPath API client
        course_id: The ID of the course to retrieve
        
    Returns:
        PowerPathCourse: The course object
        
    Raises:
        PowerPathNotFoundError: If the course is not found
        PowerPathClientError: If the request fails
    """
    return client.get_resource(f"/courses/{course_id}", PowerPathCourse)


def create_course(client: PowerPathClient, course_data: Dict[str, Any]) -> PowerPathCourse:
    """
    Create a new course.
    
    This function corresponds to the POST /courses endpoint.
    
    Args:
        client: The PowerPath API client
        course_data: The data for the new course
        
    Returns:
        PowerPathCourse: The created course object
        
    Raises:
        PowerPathClientError: If the request fails
    """
    return client.create_resource("/courses", PowerPathCourse, course_data)


def update_course(client: PowerPathClient, course_id: str, course_data: Dict[str, Any]) -> PowerPathCourse:
    """
    Update an existing course.
    
    This function corresponds to the PATCH /courses/:courseId endpoint.
    
    Args:
        client: The PowerPath API client
        course_id: The ID of the course to update
        course_data: The data to update the course with
        
    Returns:
        PowerPathCourse: The updated course object
        
    Raises:
        PowerPathNotFoundError: If the course is not found
        PowerPathClientError: If the request fails
    """
    return client.update_resource(f"/courses/{course_id}", PowerPathCourse, course_data)


def delete_course(client: PowerPathClient, course_id: str) -> Dict[str, Any]:
    """
    Delete a course.
    
    This function corresponds to the DELETE /courses/:courseId endpoint.
    
    Args:
        client: The PowerPath API client
        course_id: The ID of the course to delete
        
    Returns:
        Dict[str, Any]: The response data
        
    Raises:
        PowerPathNotFoundError: If the course is not found
        PowerPathClientError: If the request fails
    """
    return client.delete_resource(f"/courses/{course_id}") 
"""
User API functions for PowerPath.

This module provides functions for working with users in the PowerPath API.
It includes operations for creating, retrieving, updating, and deleting users,
as well as searching for users by various criteria.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient
from ..models import PowerPathUser


def get_all_users(client: PowerPathClient) -> List[PowerPathUser]:
    """
    Get all users.
    
    This function retrieves all users from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        
    Returns:
        A list of PowerPathUser objects representing all users
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = "/users"
    response = client.get(endpoint)
    
    # Convert the response to PowerPathUser objects
    users = [PowerPathUser.model_validate(user) for user in response]
    return users


def search_users(client: PowerPathClient, search_params: Dict[str, Any]) -> List[PowerPathUser]:
    """
    Search for users by exact parameter matching.
    
    This function searches for users by exact parameter matching.
    You can search by any parameter in the PowerPathUser model.
    The information provided must be an exact match.
    
    Args:
        client: The PowerPath API client
        search_params: Dictionary of search parameters (e.g., {"email": "user@example.com"})
        
    Returns:
        A list of PowerPathUser objects matching the search criteria
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = "/users"
    response = client.get(endpoint, params=search_params)
    
    # Convert the response to PowerPathUser objects
    users = [PowerPathUser.model_validate(user) for user in response]
    return users


def list_users(client: PowerPathClient, term: str, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    List users by search term with pagination.
    
    This function searches for users by a search term for the user's email, givenName, or familyName.
    The term parameter is REQUIRED for this API call. The limit and offset parameters are optional.
    
    Args:
        client: The PowerPath API client
        term: Search term for the user's email, givenName, or familyName
        limit: Optional limit for the number of results
        offset: Optional offset for pagination
        
    Returns:
        A list of dictionaries representing users matching the search term (ListPowerPathUser[])
        
    Raises:
        HTTPError: If the API request fails
    """
    # Build query parameters
    params = {"term": term}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    
    # Make the API request
    endpoint = "/users/list"
    response = client.get(endpoint, params=params)
    
    # Return the response as is, since we don't have a specific model for ListPowerPathUser
    return response


def get_user(client: PowerPathClient, user_id: str) -> PowerPathUser:
    """
    Get a specific user.
    
    This function retrieves a specific user from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to retrieve
        
    Returns:
        A PowerPathUser object representing the user
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}"
    response = client.get(endpoint)
    
    # Convert the response to a PowerPathUser object
    user = PowerPathUser.model_validate(response)
    return user


def create_user(client: PowerPathClient, user_data: Dict[str, Any]) -> PowerPathUser:
    """
    Create a new user.
    
    This function creates a new user in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_data: The data for the new user
            Required fields:
            - email: The user's email address
            - givenName: The user's first name
            - familyName: The user's last name
            Optional fields:
            - username: The user's username
            - preferredFirstName: The user's preferred first name
            - preferredLastName: The user's preferred last name
            - preferredMiddleName: The user's preferred middle name
            - middleName: The user's middle name
            - status: The user's status
            - grades: The user's grade levels
            - pronouns: The user's pronouns
            - phone: The user's phone number
            - sms: The user's SMS number
            - readingLevel: The user's reading level
            
    Returns:
        A PowerPathUser object representing the newly created user
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = "/users"
    response = client.post(endpoint, json_data=user_data)
    
    # Convert the response to a PowerPathUser object
    user = PowerPathUser.model_validate(response)
    return user


def update_user(client: PowerPathClient, user_id: str, user_data: Dict[str, Any]) -> PowerPathUser:
    """
    Update an existing user.
    
    This function updates an existing user in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to update
        user_data: The updated data for the user
            Optional fields:
            - email: The user's email address
            - givenName: The user's first name
            - familyName: The user's last name
            - username: The user's username
            - preferredFirstName: The user's preferred first name
            - preferredLastName: The user's preferred last name
            - preferredMiddleName: The user's preferred middle name
            - middleName: The user's middle name
            - status: The user's status
            - grades: The user's grade levels
            - pronouns: The user's pronouns
            - phone: The user's phone number
            - sms: The user's SMS number
            - readingLevel: The user's reading level
            
    Returns:
        A PowerPathUser object representing the updated user
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}"
    response = client.patch(endpoint, json_data=user_data)
    
    # Convert the response to a PowerPathUser object
    user = PowerPathUser.model_validate(response)
    return user


def delete_user(client: PowerPathClient, user_id: str) -> Dict[str, Any]:
    """
    Delete a user.
    
    This function deletes a user from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        user_id: The ID of the user to delete
        
    Returns:
        A dictionary containing the API response
        
    Raises:
        HTTPError: If the API request fails
    """
    # Make the API request
    endpoint = f"/users/{user_id}"
    response = client.delete(endpoint)
    
    return response 
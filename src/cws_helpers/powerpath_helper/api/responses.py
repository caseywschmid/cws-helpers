"""
Response API functions for PowerPath.

This module provides functions for working with responses in the PowerPath API.
It includes operations for creating, updating, and deleting responses to questions.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient
from ..models import PowerPathResponse

def create_question_response(client: PowerPathClient, question_id: str, response_data: Dict[str, Any]) -> PowerPathResponse:
    """
    Create a new response for a question.
    
    This function creates a new response for a question in the PowerPath API.
    Questions are internally referred to as 'ccItem' in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        question_id: The ID of the question
        response_data: The data for the new response
        
    Returns:
        PowerPathResponse: The created response
        
    Raises:
        PowerPathNotFoundError: If the question does not exist
        PowerPathClientError: If the request fails
    """
    return client.create_resource(f"/modules/ccItem/{question_id}/responses", PowerPathResponse, response_data)

def update_response(client: PowerPathClient, response_id: str, response_data: Dict[str, Any]) -> PowerPathResponse:
    """
    Update a response.
    
    This function updates an existing response in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        response_id: The ID of the response to update
        response_data: The updated data for the response
        
    Returns:
        PowerPathResponse: The updated response
        
    Raises:
        PowerPathNotFoundError: If the response does not exist
        PowerPathClientError: If the request fails
    """
    return client.put(f"/modules/responses/{response_id}", json_data=response_data)

def delete_response(client: PowerPathClient, response_id: str) -> Dict[str, Any]:
    """
    Delete a response.
    
    This function deletes a response from the PowerPath API.
    
    Args:
        client: The PowerPath API client
        response_id: The ID of the response to delete
        
    Returns:
        Dict[str, Any]: The response from the API
        
    Raises:
        PowerPathNotFoundError: If the response does not exist
        PowerPathClientError: If the request fails
    """
    return client.delete(f"/modules/responses/{response_id}") 
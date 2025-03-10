"""
Question API functions for PowerPath.

This module provides functions for working with questions in the PowerPath API.
It includes operations for creating, retrieving, and updating questions.
Questions are internally referred to as 'ccItem' in the PowerPath API.
"""

from typing import Dict, List, Any, Optional

from ..core import PowerPathClient
from ..models import PowerPathCCItem

def get_question(client: PowerPathClient, question_id: str) -> PowerPathCCItem:
    """
    Get a question by ID.
    
    This function retrieves a specific question from the PowerPath API.
    Questions are internally referred to as 'ccItem' in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        question_id: The ID of the question to retrieve
        
    Returns:
        PowerPathCCItem: The requested question
        
    Raises:
        PowerPathNotFoundError: If the question does not exist
        PowerPathClientError: If the request fails
    """
    return client.get_resource(f"/modules/ccItem/{question_id}", PowerPathCCItem)

def create_question(client: PowerPathClient, question_data: Dict[str, Any]) -> PowerPathCCItem:
    """
    Create a new question.
    
    This function creates a new question in the PowerPath API.
    Questions are internally referred to as 'ccItem' in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        question_data: The data for the new question
        
    Returns:
        PowerPathCCItem: The created question
        
    Raises:
        PowerPathClientError: If the request fails
    """
    return client.create_resource("/modules/ccItem", PowerPathCCItem, question_data)

def update_question(client: PowerPathClient, question_id: str, question_data: Dict[str, Any]) -> PowerPathCCItem:
    """
    Update a question.
    
    This function updates an existing question in the PowerPath API.
    Questions are internally referred to as 'ccItem' in the PowerPath API.
    
    Args:
        client: The PowerPath API client
        question_id: The ID of the question to update
        question_data: The updated data for the question
        
    Returns:
        PowerPathCCItem: The updated question
        
    Raises:
        PowerPathNotFoundError: If the question does not exist
        PowerPathClientError: If the request fails
    """
    return client.put(f"/modules/ccItem/{question_id}", json_data=question_data) 
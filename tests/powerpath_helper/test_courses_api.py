"""
Tests for the PowerPath courses API module.

This module contains tests for the courses API functions.
"""

import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID

from cws_helpers.powerpath_helper.core import PowerPathClient
from cws_helpers.powerpath_helper.models import PowerPathCourse
from cws_helpers.powerpath_helper.api.courses import (
    get_all_courses,
    get_course,
    create_course,
    update_course,
    delete_course,
)


@pytest.fixture
def mock_client():
    """Create a mock PowerPath client."""
    client = MagicMock(spec=PowerPathClient)
    return client


@pytest.fixture
def sample_course_data():
    """Sample course data for testing."""
    return {
        "id": 123,
        "uuid": "12345678-1234-5678-1234-567812345678",
        "title": "Test Course",
        "courseCode": "TEST101",
        "schoolYear": "2023-2024",
        "grades": "9,10,11",
        "subjects": "Mathematics",
        "subjectCodes": "MATH",
        "status": "active",
        "metadata": "Some metadata",
        "defaultModuleId": 456,
        "defaultModuleUUID": "87654321-8765-4321-8765-432187654321",
        "isPlacementTest": False,
        "appName": "PowerPath",
        "dateLastModified": "2023-01-01T00:00:00Z"
    }


def test_get_all_courses(mock_client, sample_course_data):
    """Test get_all_courses function."""
    # Set up the mock
    mock_client.get_resources.return_value = [PowerPathCourse.model_validate(sample_course_data)]
    
    # Call the function
    courses = get_all_courses(mock_client)
    
    # Verify the result
    assert len(courses) == 1
    assert courses[0].id == 123
    assert courses[0].title == "Test Course"
    assert courses[0].course_code == "TEST101"
    
    # Verify the mock was called correctly
    mock_client.get_resources.assert_called_once_with("/courses", PowerPathCourse)


def test_get_course(mock_client, sample_course_data):
    """Test get_course function."""
    # Set up the mock
    mock_client.get_resource.return_value = PowerPathCourse.model_validate(sample_course_data)
    
    # Call the function
    course = get_course(mock_client, "123")
    
    # Verify the result
    assert course.id == 123
    assert course.title == "Test Course"
    assert course.course_code == "TEST101"
    
    # Verify the mock was called correctly
    mock_client.get_resource.assert_called_once_with("/courses/123", PowerPathCourse)


def test_create_course(mock_client, sample_course_data):
    """Test create_course function."""
    # Set up the mock
    mock_client.create_resource.return_value = PowerPathCourse.model_validate(sample_course_data)
    
    # Course data to create
    new_course_data = {
        "title": "New Course",
        "courseCode": "NEW101",
        "schoolYear": "2023-2024",
        "grades": "9,10,11",
        "subjects": "Mathematics"
    }
    
    # Call the function
    course = create_course(mock_client, new_course_data)
    
    # Verify the result
    assert course.id == 123  # From the mock response
    assert course.title == "Test Course"  # From the mock response
    
    # Verify the mock was called correctly
    mock_client.create_resource.assert_called_once_with("/courses", PowerPathCourse, new_course_data)


def test_update_course(mock_client, sample_course_data):
    """Test update_course function."""
    # Set up the mock
    mock_client.update_resource.return_value = PowerPathCourse.model_validate(sample_course_data)
    
    # Course data to update
    update_data = {
        "title": "Updated Course",
        "status": "inactive"
    }
    
    # Call the function
    course = update_course(mock_client, "123", update_data)
    
    # Verify the result
    assert course.id == 123  # From the mock response
    assert course.title == "Test Course"  # From the mock response
    
    # Verify the mock was called correctly
    mock_client.update_resource.assert_called_once_with("/courses/123", PowerPathCourse, update_data)


def test_delete_course(mock_client):
    """Test delete_course function."""
    # Set up the mock
    mock_client.delete_resource.return_value = {"status": "success"}
    
    # Call the function
    result = delete_course(mock_client, "123")
    
    # Verify the result
    assert result == {"status": "success"}
    
    # Verify the mock was called correctly
    mock_client.delete_resource.assert_called_once_with("/courses/123") 
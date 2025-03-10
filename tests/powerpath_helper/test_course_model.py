"""
Tests for the PowerPath Course model.

This module contains tests for the PowerPathCourse model.
"""

import pytest
from datetime import datetime
from uuid import UUID

from cws_helpers.powerpath_helper.models.course import PowerPathCourse


def test_course_model_creation():
    """Test that we can create a course model with required fields."""
    course = PowerPathCourse(
        title="Math 101",
        courseCode="MATH101"
    )
    
    assert course.title == "Math 101"
    assert course.course_code == "MATH101"


def test_course_model_with_all_fields():
    """Test that we can create a course model with all fields."""
    course = PowerPathCourse(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        title="Math 101",
        courseCode="MATH101",
        schoolYear="2023-2024",
        grades="9,10,11",
        subjects="Mathematics",
        subjectCodes="MATH",
        status="active",
        metadata="Some metadata",
        defaultModuleId=456,
        defaultModuleUUID=UUID("87654321-8765-4321-8765-432187654321"),
        isPlacementTest=False,
        appName="PowerPath",
        dateLastModified=datetime(2023, 1, 1)
    )
    
    assert course.id == 123
    assert course.uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert course.title == "Math 101"
    assert course.course_code == "MATH101"
    assert course.school_year == "2023-2024"
    assert course.grades == "9,10,11"
    assert course.subjects == "Mathematics"
    assert course.subject_codes == "MATH"
    assert course.status == "active"
    assert course.metadata == "Some metadata"
    assert course.default_module_id == 456
    assert course.default_module_uuid == UUID("87654321-8765-4321-8765-432187654321")
    assert course.is_placement_test is False
    assert course.app_name == "PowerPath"
    assert course.date_last_modified == datetime(2023, 1, 1)


def test_course_model_to_create_dict():
    """Test that to_create_dict works correctly."""
    course = PowerPathCourse(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        title="Math 101",
        courseCode="MATH101",
        defaultModuleId=456,
        dateLastModified=datetime(2023, 1, 1)
    )
    
    create_dict = course.to_create_dict()
    
    # These fields should be excluded
    assert "id" not in create_dict
    assert "uuid" not in create_dict
    assert "dateLastModified" not in create_dict
    
    # These fields should be included
    assert create_dict["title"] == "Math 101"
    assert create_dict["courseCode"] == "MATH101"
    assert create_dict["defaultModuleId"] == 456


def test_course_model_to_update_dict():
    """Test that to_update_dict works correctly."""
    course = PowerPathCourse(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        title="Math 101",
        courseCode="MATH101",
        subjects=None,  # This should be excluded because it's None
        dateLastModified=datetime(2023, 1, 1)
    )
    
    update_dict = course.to_update_dict()
    
    # These fields should be excluded
    assert "id" not in update_dict
    assert "uuid" not in update_dict
    assert "dateLastModified" not in update_dict
    assert "subjects" not in update_dict  # None values should be excluded
    
    # These fields should be included
    assert update_dict["title"] == "Math 101"
    assert update_dict["courseCode"] == "MATH101" 
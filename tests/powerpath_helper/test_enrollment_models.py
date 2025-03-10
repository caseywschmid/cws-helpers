"""
Tests for the PowerPath Enrollment and Progress models.

This module contains tests for the PowerPathEnrollment, PowerPathUserModuleItem,
PowerPathUserModuleSequence, and PowerPathGradeLevelTest models.
"""

import pytest
from datetime import date, datetime
from uuid import UUID

from cws_helpers.powerpath_helper.models import (
    PowerPathEnrollment,
    PowerPathUserModuleItem,
    PowerPathUserModuleSequence,
    PowerPathGradeLevelTest,
)


def test_enrollment_model_creation():
    """Test that we can create an enrollment model with required fields."""
    enrollment = PowerPathEnrollment(
        userId=123,
        courseId=456
    )
    
    assert enrollment.user_id == 123
    assert enrollment.course_id == 456


def test_enrollment_model_with_all_fields():
    """Test that we can create an enrollment model with all fields."""
    enrollment = PowerPathEnrollment(
        id=789,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        userId=123,
        userIdUUID=UUID("11111111-1111-1111-1111-111111111111"),
        courseId=456,
        courseUUID=UUID("22222222-2222-2222-2222-222222222222"),
        role="student",
        status="active",
        beginDate=date(2023, 1, 1),
        endDate=date(2023, 12, 31),
        primary="true",
        school="Example School",
        metadata="Some metadata",
        dateLastModified=datetime(2023, 1, 1)
    )
    
    assert enrollment.id == 789
    assert enrollment.uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert enrollment.user_id == 123
    assert enrollment.user_id_uuid == UUID("11111111-1111-1111-1111-111111111111")
    assert enrollment.course_id == 456
    assert enrollment.course_uuid == UUID("22222222-2222-2222-2222-222222222222")
    assert enrollment.role == "student"
    assert enrollment.status == "active"
    assert enrollment.begin_date == date(2023, 1, 1)
    assert enrollment.end_date == date(2023, 12, 31)
    assert enrollment.primary == "true"
    assert enrollment.school == "Example School"
    assert enrollment.metadata == "Some metadata"
    assert enrollment.date_last_modified == datetime(2023, 1, 1)


def test_enrollment_to_create_dict():
    """Test that to_create_dict works correctly for enrollments."""
    enrollment = PowerPathEnrollment(
        id=789,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        userId=123,
        courseId=456,
        role="student",
        dateLastModified=datetime(2023, 1, 1)
    )
    
    create_dict = enrollment.to_create_dict()
    
    # These fields should be excluded
    assert "id" not in create_dict
    assert "uuid" not in create_dict
    assert "dateLastModified" not in create_dict
    
    # These fields should be included
    assert create_dict["userId"] == 123
    assert create_dict["courseId"] == 456
    assert create_dict["role"] == "student"


def test_enrollment_to_update_dict():
    """Test that to_update_dict works correctly for enrollments."""
    enrollment = PowerPathEnrollment(
        id=789,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        userId=123,
        courseId=456,
        role="student",
        status=None,  # This should be excluded because it's None
        dateLastModified=datetime(2023, 1, 1)
    )
    
    update_dict = enrollment.to_update_dict()
    
    # These fields should be excluded
    assert "id" not in update_dict
    assert "uuid" not in update_dict
    assert "dateLastModified" not in update_dict
    assert "status" not in update_dict  # None values should be excluded
    
    # These fields should be included
    assert update_dict["userId"] == 123
    assert update_dict["courseId"] == 456
    assert update_dict["role"] == "student"


def test_user_module_item_model_creation():
    """Test that we can create a user module item model with required fields."""
    user_module_item = PowerPathUserModuleItem(
        userId=123,
        itemId=456
    )
    
    assert user_module_item.user_id == 123
    assert user_module_item.item_id == 456


def test_user_module_item_model_with_all_fields():
    """Test that we can create a user module item model with all fields."""
    user_module_item = PowerPathUserModuleItem(
        userId=123,
        userUUID=UUID("12345678-1234-5678-1234-567812345678"),
        itemId=456,
        itemUUID=UUID("87654321-8765-4321-8765-432187654321"),
        clrResultId=789,
        clrResultUUID=UUID("11111111-1111-1111-1111-111111111111"),
        attempt=1,
        startedAt=datetime(2023, 1, 1, 10, 0, 0),
        completedAt=datetime(2023, 1, 1, 10, 15, 0)
    )
    
    assert user_module_item.user_id == 123
    assert user_module_item.user_uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert user_module_item.item_id == 456
    assert user_module_item.item_uuid == UUID("87654321-8765-4321-8765-432187654321")
    assert user_module_item.clr_result_id == 789
    assert user_module_item.clr_result_uuid == UUID("11111111-1111-1111-1111-111111111111")
    assert user_module_item.attempt == 1
    assert user_module_item.started_at == datetime(2023, 1, 1, 10, 0, 0)
    assert user_module_item.completed_at == datetime(2023, 1, 1, 10, 15, 0)


def test_user_module_sequence_model_creation():
    """Test that we can create a user module sequence model with required fields."""
    user_module_sequence = PowerPathUserModuleSequence(
        userId=123,
        originModuleId=456,
        insertedModuleId=789,
        destinationModuleId=101
    )
    
    assert user_module_sequence.user_id == 123
    assert user_module_sequence.origin_module_id == 456
    assert user_module_sequence.inserted_module_id == 789
    assert user_module_sequence.destination_module_id == 101


def test_user_module_sequence_model_with_all_fields():
    """Test that we can create a user module sequence model with all fields."""
    user_module_sequence = PowerPathUserModuleSequence(
        id=202,
        userId=123,
        userUUID=UUID("12345678-1234-5678-1234-567812345678"),
        originModuleId=456,
        originModuleUUID=UUID("11111111-1111-1111-1111-111111111111"),
        insertedModuleId=789,
        insertedModuleUUID=UUID("22222222-2222-2222-2222-222222222222"),
        destinationModuleId=101,
        destinationModuleUUID=UUID("33333333-3333-3333-3333-333333333333")
    )
    
    assert user_module_sequence.id == 202
    assert user_module_sequence.user_id == 123
    assert user_module_sequence.user_uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert user_module_sequence.origin_module_id == 456
    assert user_module_sequence.origin_module_uuid == UUID("11111111-1111-1111-1111-111111111111")
    assert user_module_sequence.inserted_module_id == 789
    assert user_module_sequence.inserted_module_uuid == UUID("22222222-2222-2222-2222-222222222222")
    assert user_module_sequence.destination_module_id == 101
    assert user_module_sequence.destination_module_uuid == UUID("33333333-3333-3333-3333-333333333333")


def test_grade_level_test_model_creation():
    """Test that we can create a grade level test model with required fields."""
    grade_level_test = PowerPathGradeLevelTest(
        itemId=123,
        courseId=456
    )
    
    assert grade_level_test.item_id == 123
    assert grade_level_test.course_id == 456


def test_grade_level_test_model_with_all_fields():
    """Test that we can create a grade level test model with all fields."""
    grade_level_test = PowerPathGradeLevelTest(
        id=789,
        itemId=123,
        courseId=456
    )
    
    assert grade_level_test.id == 789
    assert grade_level_test.item_id == 123
    assert grade_level_test.course_id == 456 
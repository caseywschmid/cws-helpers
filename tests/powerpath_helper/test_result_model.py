"""
Tests for the PowerPath Result model.

This module contains tests for the PowerPathResult model.
"""

import pytest
from datetime import datetime
from uuid import UUID

from cws_helpers.powerpath_helper.models import PowerPathResult


def test_result_model_creation():
    """Test that we can create a result model with required fields."""
    result = PowerPathResult(
        userId=123,
        type="quiz",
        value=85.5
    )
    
    assert result.user_id == 123
    assert result.type == "quiz"
    assert result.value == 85.5


def test_result_model_with_all_fields():
    """Test that we can create a result model with all fields."""
    result = PowerPathResult(
        id=456,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        userId=123,
        type="quiz",
        value=85.5,
        achievedLevel="Proficient",
        alignments="Common Core",
        status="completed",
        resultDescription="Student demonstrated proficiency"
    )
    
    assert result.id == 456
    assert result.uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert result.user_id == 123
    assert result.type == "quiz"
    assert result.value == 85.5
    assert result.achieved_level == "Proficient"
    assert result.alignments == "Common Core"
    assert result.status == "completed"
    assert result.result_description == "Student demonstrated proficiency"


def test_result_model_to_create_dict():
    """Test that to_create_dict works correctly."""
    result = PowerPathResult(
        id=456,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        userId=123,
        type="quiz",
        value=85.5,
        achievedLevel="Proficient"
    )
    
    create_dict = result.to_create_dict()
    
    # These fields should be excluded
    assert "id" not in create_dict
    assert "uuid" not in create_dict
    
    # These fields should be included
    assert create_dict["userId"] == 123
    assert create_dict["type"] == "quiz"
    assert create_dict["value"] == 85.5
    assert create_dict["achievedLevel"] == "Proficient"


def test_result_model_to_update_dict():
    """Test that to_update_dict works correctly."""
    result = PowerPathResult(
        id=456,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        userId=123,
        type="quiz",
        value=85.5,
        status=None  # This should be excluded because it's None
    )
    
    update_dict = result.to_update_dict()
    
    # These fields should be excluded
    assert "id" not in update_dict
    assert "uuid" not in update_dict
    assert "userId" not in update_dict  # user_id is excluded in to_update_dict
    assert "status" not in update_dict  # None values should be excluded
    
    # These fields should be included
    assert update_dict["type"] == "quiz"
    assert update_dict["value"] == 85.5 
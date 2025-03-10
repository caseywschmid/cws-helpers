"""
Tests for the PowerPath Goal model.

This module contains tests for the PowerPathGoal model.
"""

import pytest
from datetime import datetime
from uuid import UUID

from cws_helpers.powerpath_helper.models import PowerPathGoal


def test_goal_model_creation():
    """Test that we can create a goal model with required fields."""
    goal = PowerPathGoal(
        description="Complete 5 modules",
        xp=1000,
        userId=123,
        courseId=456
    )
    
    assert goal.description == "Complete 5 modules"
    assert goal.xp == 1000
    assert goal.user_id == 123
    assert goal.course_id == 456


def test_goal_model_with_all_fields():
    """Test that we can create a goal model with all fields."""
    goal = PowerPathGoal(
        id=789,
        description="Complete 5 modules",
        xp=1000,
        userId=123,
        courseId=456,
        cutoffDate=datetime(2023, 12, 31),
        dailyOverride=100,
        createdAt=datetime(2023, 1, 1),
        updatedAt=datetime(2023, 1, 2)
    )
    
    assert goal.id == 789
    assert goal.description == "Complete 5 modules"
    assert goal.xp == 1000
    assert goal.user_id == 123
    assert goal.course_id == 456
    assert goal.cutoff_date == datetime(2023, 12, 31)
    assert goal.daily_override == 100
    assert goal.created_at == datetime(2023, 1, 1)
    assert goal.updated_at == datetime(2023, 1, 2)


def test_goal_model_to_create_dict():
    """Test that to_create_dict works correctly."""
    goal = PowerPathGoal(
        id=789,
        description="Complete 5 modules",
        xp=1000,
        userId=123,
        courseId=456,
        cutoffDate=datetime(2023, 12, 31),
        dailyOverride=100,
        createdAt=datetime(2023, 1, 1),
        updatedAt=datetime(2023, 1, 2)
    )
    
    create_dict = goal.to_create_dict()
    
    # These fields should be excluded
    assert "id" not in create_dict
    assert "createdAt" not in create_dict
    assert "updatedAt" not in create_dict
    
    # These fields should be included
    assert create_dict["description"] == "Complete 5 modules"
    assert create_dict["xp"] == 1000
    assert create_dict["userId"] == 123
    assert create_dict["courseId"] == 456
    assert create_dict["cutoffDate"] == datetime(2023, 12, 31)
    assert create_dict["dailyOverride"] == 100


def test_goal_model_to_update_dict():
    """Test that to_update_dict works correctly."""
    goal = PowerPathGoal(
        id=789,
        description="Complete 5 modules",
        xp=1000,
        userId=123,
        courseId=456,
        dailyOverride=None,  # This should be excluded because it's None
        createdAt=datetime(2023, 1, 1),
        updatedAt=datetime(2023, 1, 2)
    )
    
    update_dict = goal.to_update_dict()
    
    # These fields should be excluded
    assert "id" not in update_dict
    assert "createdAt" not in update_dict
    assert "updatedAt" not in update_dict
    assert "dailyOverride" not in update_dict  # None values should be excluded
    
    # These fields should be included
    assert update_dict["description"] == "Complete 5 modules"
    assert update_dict["xp"] == 1000
    assert update_dict["userId"] == 123
    assert update_dict["courseId"] == 456 
"""
Tests for the PowerPath XP model.

This module contains tests for the PowerPathXP model.
"""

import pytest
from datetime import datetime
from uuid import UUID

from cws_helpers.powerpath_helper.models import PowerPathXP


def test_xp_model_creation():
    """Test that we can create an XP model with required fields."""
    xp = PowerPathXP(
        userId=123,
        amount=100
    )
    
    assert xp.user_id == 123
    assert xp.amount == 100


def test_xp_model_with_all_fields():
    """Test that we can create an XP model with all fields."""
    xp = PowerPathXP(
        id=456,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        userId=123,
        user_uuid=UUID("87654321-8765-4321-8765-432187654321"),
        course_id=789,
        courseCode="MATH101",
        item_id=101,
        subject="Mathematics",
        amount=100,
        awardedOn=datetime(2023, 1, 1),
        appName="PowerPath"
    )
    
    assert xp.id == 456
    assert xp.uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert xp.user_id == 123
    assert xp.user_uuid == UUID("87654321-8765-4321-8765-432187654321")
    assert xp.course_id == 789
    assert xp.course_code == "MATH101"
    assert xp.item_id == 101
    assert xp.subject == "Mathematics"
    assert xp.amount == 100
    assert xp.awarded_on == datetime(2023, 1, 1)
    assert xp.app_name == "PowerPath"


def test_xp_model_to_create_dict():
    """Test that to_create_dict works correctly."""
    xp = PowerPathXP(
        id=456,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        userId=123,
        course_id=789,
        amount=100,
        awardedOn=datetime(2023, 1, 1)
    )
    
    create_dict = xp.to_create_dict()
    
    # These fields should be excluded
    assert "id" not in create_dict
    assert "uuid" not in create_dict
    assert "awardedOn" not in create_dict
    
    # These fields should be included
    assert create_dict["userId"] == 123
    assert create_dict["course_id"] == 789
    assert create_dict["amount"] == 100 
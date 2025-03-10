"""
Tests for the PowerPath Module and Item models.

This module contains tests for the PowerPathModule and PowerPathItem models.
"""

import pytest
from datetime import datetime
from uuid import UUID

from cws_helpers.powerpath_helper.models.module import PowerPathModule, PowerPathItem


def test_item_model_creation():
    """Test that we can create an item model with required fields."""
    item = PowerPathItem(
        name="Quiz 1",
        contentType="quiz",
        xp=100
    )
    
    assert item.name == "Quiz 1"
    assert item.content_type == "quiz"
    assert item.xp == 100


def test_item_model_with_all_fields():
    """Test that we can create an item model with all fields."""
    item = PowerPathItem(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        name="Quiz 1",
        contentType="quiz",
        xp=100,
        attempts=3,
        state="active",
        metadata="Some metadata",
        isPlacementTest=False,
        thirdPartyId="ext-123",
        lti_url="https://example.com/lti"
    )
    
    assert item.id == 123
    assert item.uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert item.name == "Quiz 1"
    assert item.content_type == "quiz"
    assert item.xp == 100
    assert item.attempts == 3
    assert item.state == "active"
    assert item.metadata == "Some metadata"
    assert item.is_placement_test is False
    assert item.third_party_id == "ext-123"
    assert item.lti_url == "https://example.com/lti"


def test_module_model_creation():
    """Test that we can create a module model with required fields."""
    module = PowerPathModule(
        name="Module 1"
    )
    
    assert module.name == "Module 1"


def test_module_model_with_all_fields():
    """Test that we can create a module model with all fields."""
    module = PowerPathModule(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        name="Module 1",
        state="active",
        unlock_at=datetime(2023, 1, 1),
        startingItemId=456,
        startingItemUUID=UUID("87654321-8765-4321-8765-432187654321"),
        startingModuleId=789
    )
    
    assert module.id == 123
    assert module.uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert module.name == "Module 1"
    assert module.state == "active"
    assert module.unlock_at == datetime(2023, 1, 1)
    assert module.starting_item_id == 456
    assert module.starting_item_uuid == UUID("87654321-8765-4321-8765-432187654321")
    assert module.starting_module_id == 789


def test_module_with_items():
    """Test that we can create a module with items."""
    module = PowerPathModule(
        name="Module 1",
        items=[
            PowerPathItem(name="Item 1", contentType="quiz", xp=100),
            PowerPathItem(name="Item 2", contentType="assignment", xp=200)
        ]
    )
    
    assert module.name == "Module 1"
    assert len(module.items) == 2
    assert module.items[0].name == "Item 1"
    assert module.items[0].content_type == "quiz"
    assert module.items[0].xp == 100
    assert module.items[1].name == "Item 2"
    assert module.items[1].content_type == "assignment"
    assert module.items[1].xp == 200


def test_item_to_create_dict():
    """Test that to_create_dict works correctly for items."""
    item = PowerPathItem(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        name="Quiz 1",
        contentType="quiz",
        xp=100
    )
    
    create_dict = item.to_create_dict()
    
    # These fields should be excluded
    assert "id" not in create_dict
    assert "uuid" not in create_dict
    
    # These fields should be included
    assert create_dict["name"] == "Quiz 1"
    assert create_dict["contentType"] == "quiz"
    assert create_dict["xp"] == 100


def test_module_to_create_dict():
    """Test that to_create_dict works correctly for modules."""
    module = PowerPathModule(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        name="Module 1",
        items=[
            PowerPathItem(name="Item 1", contentType="quiz", xp=100)
        ]
    )
    
    create_dict = module.to_create_dict()
    
    # These fields should be excluded
    assert "id" not in create_dict
    assert "uuid" not in create_dict
    assert "items" not in create_dict
    
    # These fields should be included
    assert create_dict["name"] == "Module 1" 
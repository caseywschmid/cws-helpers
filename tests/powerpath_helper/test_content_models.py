"""
Tests for the PowerPath Content Creation models.

This module contains tests for the PowerPathCCItem, PowerPathResponse, PowerPathObjectBank,
PowerPathCCItemObjectBank, and PowerPathCCItemResult models.
"""

import pytest
import json
from datetime import datetime
from uuid import UUID

from cws_helpers.powerpath_helper.models import (
    PowerPathCCItem,
    PowerPathResponse,
    PowerPathObjectBank,
    PowerPathCCItemObjectBank,
    PowerPathCCItemResult,
)


def test_cc_item_model_creation():
    """Test that we can create a CC item model with required fields."""
    item = PowerPathCCItem(
        material="What is 2 + 2?"
    )
    
    assert item.material == "What is 2 + 2?"


def test_cc_item_model_with_all_fields():
    """Test that we can create a CC item model with all fields."""
    item = PowerPathCCItem(
        id=123,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        material="What is 2 + 2?",
        grade=2,
        difficulty=1,
        referenceText="Basic addition",
        explanation="This tests basic addition skills",
        metadata={"type": "multiple_choice", "points": 5}
    )
    
    assert item.id == 123
    assert item.uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert item.material == "What is 2 + 2?"
    assert item.grade == 2
    assert item.difficulty == 1
    assert item.reference_text == "Basic addition"
    assert item.explanation == "This tests basic addition skills"
    assert item.metadata == {"type": "multiple_choice", "points": 5}


def test_cc_item_json_parsing():
    """Test that JSON fields are properly parsed."""
    item = PowerPathCCItem(
        material="What is 2 + 2?",
        metadata='{"type": "multiple_choice", "points": 5}'
    )
    
    assert item.metadata == {"type": "multiple_choice", "points": 5}


def test_response_model_creation():
    """Test that we can create a response model with required fields."""
    response = PowerPathResponse(
        ccItemId=123,
        label="4",
        isCorrect=True
    )
    
    assert response.cc_item_id == 123
    assert response.label == "4"
    assert response.is_correct is True


def test_response_model_with_all_fields():
    """Test that we can create a response model with all fields."""
    response = PowerPathResponse(
        id=456,
        ccItemId=123,
        label="4",
        explanation="Four is the correct answer to 2 + 2",
        isCorrect=True
    )
    
    assert response.id == 456
    assert response.cc_item_id == 123
    assert response.label == "4"
    assert response.explanation == "Four is the correct answer to 2 + 2"
    assert response.is_correct is True


def test_object_bank_model_creation():
    """Test that we can create an object bank model with required fields."""
    object_bank = PowerPathObjectBank(
        itemId=123
    )
    
    assert object_bank.item_id == 123


def test_object_bank_model_with_all_fields():
    """Test that we can create an object bank model with all fields."""
    object_bank = PowerPathObjectBank(
        id=456,
        uuid=UUID("12345678-1234-5678-1234-567812345678"),
        itemId=123,
        itemUUID=UUID("87654321-8765-4321-8765-432187654321")
    )
    
    assert object_bank.id == 456
    assert object_bank.uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert object_bank.item_id == 123
    assert object_bank.item_uuid == UUID("87654321-8765-4321-8765-432187654321")


def test_cc_item_object_bank_model_creation():
    """Test that we can create a CC item object bank model with required fields."""
    cc_item_object_bank = PowerPathCCItemObjectBank(
        ccItemId=123,
        objectBankId=456
    )
    
    assert cc_item_object_bank.cc_item_id == 123
    assert cc_item_object_bank.object_bank_id == 456


def test_cc_item_object_bank_model_with_all_fields():
    """Test that we can create a CC item object bank model with all fields."""
    cc_item_object_bank = PowerPathCCItemObjectBank(
        ccItemId=123,
        ccItemUUID=UUID("12345678-1234-5678-1234-567812345678"),
        objectBankId=456,
        objectBankUUID=UUID("87654321-8765-4321-8765-432187654321")
    )
    
    assert cc_item_object_bank.cc_item_id == 123
    assert cc_item_object_bank.cc_item_uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert cc_item_object_bank.object_bank_id == 456
    assert cc_item_object_bank.object_bank_uuid == UUID("87654321-8765-4321-8765-432187654321")


def test_cc_item_result_model_creation():
    """Test that we can create a CC item result model with required fields."""
    cc_item_result = PowerPathCCItemResult(
        ccItemId=123,
        userId=456,
        isCorrect=True
    )
    
    assert cc_item_result.cc_item_id == 123
    assert cc_item_result.user_id == 456
    assert cc_item_result.is_correct is True


def test_cc_item_result_model_with_all_fields():
    """Test that we can create a CC item result model with all fields."""
    cc_item_result = PowerPathCCItemResult(
        ccItemId=123,
        ccItemUUID=UUID("12345678-1234-5678-1234-567812345678"),
        responseId=789,
        response="4",
        resultId=101,
        resultUUID=UUID("11111111-1111-1111-1111-111111111111"),
        userId=456,
        isCorrect=True,
        createdAt=datetime(2023, 1, 1)
    )
    
    assert cc_item_result.cc_item_id == 123
    assert cc_item_result.cc_item_uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert cc_item_result.response_id == 789
    assert cc_item_result.response == "4"
    assert cc_item_result.result_id == 101
    assert cc_item_result.result_uuid == UUID("11111111-1111-1111-1111-111111111111")
    assert cc_item_result.user_id == 456
    assert cc_item_result.is_correct is True
    assert cc_item_result.created_at == datetime(2023, 1, 1) 
"""
Tests for the PowerPath Assessment Result model.

This module contains tests for the PowerPathAssessmentResult model.
"""

import pytest
from datetime import date, datetime
from uuid import UUID

from cws_helpers.powerpath_helper.models import PowerPathAssessmentResult


def test_assessment_result_model_creation():
    """Test that we can create an assessment result model with required fields."""
    assessment_result = PowerPathAssessmentResult(
        user_id=123,
        subject_name="Mathematics",
        test_name="MAP Growth"
    )
    
    assert assessment_result.user_id == 123
    assert assessment_result.subject_name == "Mathematics"
    assert assessment_result.test_name == "MAP Growth"


def test_assessment_result_model_with_all_fields():
    """Test that we can create an assessment result model with all fields."""
    assessment_result = PowerPathAssessmentResult(
        id=456,
        user_id=123,
        userUUID=UUID("12345678-1234-5678-1234-567812345678"),
        subject_name="Mathematics",
        test_name="MAP Growth",
        term_name="Fall 2023",
        test_date=date(2023, 9, 15),
        score=220,
        percentile=75,
        projected_growth=10.5,
        observed_growth=12.3
    )
    
    assert assessment_result.id == 456
    assert assessment_result.user_id == 123
    assert assessment_result.user_uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert assessment_result.subject_name == "Mathematics"
    assert assessment_result.test_name == "MAP Growth"
    assert assessment_result.term_name == "Fall 2023"
    assert assessment_result.test_date == date(2023, 9, 15)
    assert assessment_result.score == 220
    assert assessment_result.percentile == 75
    assert assessment_result.projected_growth == 10.5
    assert assessment_result.observed_growth == 12.3


def test_assessment_result_to_create_dict():
    """Test that to_create_dict works correctly for assessment results."""
    assessment_result = PowerPathAssessmentResult(
        id=456,
        user_id=123,
        subject_name="Mathematics",
        test_name="MAP Growth",
        score=220
    )
    
    create_dict = assessment_result.to_create_dict()
    
    # These fields should be excluded
    assert "id" not in create_dict
    
    # These fields should be included
    assert create_dict["user_id"] == 123
    assert create_dict["subject_name"] == "Mathematics"
    assert create_dict["test_name"] == "MAP Growth"
    assert create_dict["score"] == 220 
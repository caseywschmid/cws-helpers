"""
Tests for the PowerPath Curriculum Framework models.

This module contains tests for the PowerPathCFDocument, PowerPathCFItem, and PowerPathCFAssociation models.
"""

import pytest
import json
from datetime import datetime
from uuid import UUID

from cws_helpers.powerpath_helper.models import (
    PowerPathCFDocument,
    PowerPathCFItem,
    PowerPathCFAssociation,
)


def test_cf_document_model_creation():
    """Test that we can create a CF document model with required fields."""
    document = PowerPathCFDocument(
        identifier=UUID("12345678-1234-5678-1234-567812345678"),
        uri="https://example.com/documents/12345678-1234-5678-1234-567812345678",
        title="Common Core Math Standards"
    )
    
    assert document.identifier == UUID("12345678-1234-5678-1234-567812345678")
    assert document.uri == "https://example.com/documents/12345678-1234-5678-1234-567812345678"
    assert document.title == "Common Core Math Standards"


def test_cf_document_model_with_all_fields():
    """Test that we can create a CF document model with all fields."""
    document = PowerPathCFDocument(
        identifier=UUID("12345678-1234-5678-1234-567812345678"),
        uri="https://example.com/documents/12345678-1234-5678-1234-567812345678",
        title="Common Core Math Standards",
        description="Mathematics standards for K-12 education",
        creator="Common Core State Standards Initiative",
        publisher="Department of Education",
        version="1.0",
        adoptionStatus="adopted",
        statusStartDate=datetime(2020, 1, 1),
        statusEndDate=datetime(2025, 12, 31),
        subject={"name": "Mathematics", "code": "MATH"},
        subjectURI="https://example.com/subjects/math",
        language="en",
        caseVersion="1.0",
        officialSourceURL="https://example.com/standards/math",
        notes="These standards are widely adopted across the United States",
        lastChangeDateTime=datetime(2020, 1, 1)
    )
    
    assert document.identifier == UUID("12345678-1234-5678-1234-567812345678")
    assert document.uri == "https://example.com/documents/12345678-1234-5678-1234-567812345678"
    assert document.title == "Common Core Math Standards"
    assert document.description == "Mathematics standards for K-12 education"
    assert document.creator == "Common Core State Standards Initiative"
    assert document.publisher == "Department of Education"
    assert document.version == "1.0"
    assert document.adoption_status == "adopted"
    assert document.status_start_date == datetime(2020, 1, 1)
    assert document.status_end_date == datetime(2025, 12, 31)
    assert document.subject == {"name": "Mathematics", "code": "MATH"}
    assert document.subject_uri == "https://example.com/subjects/math"
    assert document.language == "en"
    assert document.case_version == "1.0"
    assert document.official_source_url == "https://example.com/standards/math"
    assert document.notes == "These standards are widely adopted across the United States"
    assert document.last_change_date_time == datetime(2020, 1, 1)


def test_cf_document_json_parsing():
    """Test that JSON fields are properly parsed."""
    document = PowerPathCFDocument(
        identifier=UUID("12345678-1234-5678-1234-567812345678"),
        uri="https://example.com/documents/12345678-1234-5678-1234-567812345678",
        title="Common Core Math Standards",
        subject='{"name": "Mathematics", "code": "MATH"}'
    )
    
    assert document.subject == {"name": "Mathematics", "code": "MATH"}


def test_cf_item_model_creation():
    """Test that we can create a CF item model with required fields."""
    item = PowerPathCFItem(
        identifier=UUID("12345678-1234-5678-1234-567812345678"),
        uri="https://example.com/items/12345678-1234-5678-1234-567812345678",
        documentId=UUID("87654321-8765-4321-8765-432187654321")
    )
    
    assert item.identifier == UUID("12345678-1234-5678-1234-567812345678")
    assert item.uri == "https://example.com/items/12345678-1234-5678-1234-567812345678"
    assert item.document_id == UUID("87654321-8765-4321-8765-432187654321")


def test_cf_item_model_with_all_fields():
    """Test that we can create a CF item model with all fields."""
    item = PowerPathCFItem(
        identifier=UUID("12345678-1234-5678-1234-567812345678"),
        uri="https://example.com/items/12345678-1234-5678-1234-567812345678",
        documentId=UUID("87654321-8765-4321-8765-432187654321"),
        humanCodingScheme="MATH.K.CC.1",
        listEnumeration="1",
        abbreviatedStatement="Count to 100",
        fullStatement="Count to 100 by ones and by tens.",
        alternativeLabel="Counting to 100",
        CFItemType="Standard",
        CFItemTypeURI={"type": "Standard", "uri": "https://example.com/types/standard"},
        notes="This is a foundational skill for kindergarten mathematics",
        educationLevel={"grade": "K"},
        language="en",
        statusStartDate=datetime(2020, 1, 1),
        statusEndDate=datetime(2025, 12, 31),
        lastChangeDateTime=datetime(2020, 1, 1),
        extensions={"difficulty": "beginner"}
    )
    
    assert item.identifier == UUID("12345678-1234-5678-1234-567812345678")
    assert item.uri == "https://example.com/items/12345678-1234-5678-1234-567812345678"
    assert item.document_id == UUID("87654321-8765-4321-8765-432187654321")
    assert item.human_coding_scheme == "MATH.K.CC.1"
    assert item.list_enumeration == "1"
    assert item.abbreviated_statement == "Count to 100"
    assert item.full_statement == "Count to 100 by ones and by tens."
    assert item.alternative_label == "Counting to 100"
    assert item.cf_item_type == "Standard"
    assert item.cf_item_type_uri == {"type": "Standard", "uri": "https://example.com/types/standard"}
    assert item.notes == "This is a foundational skill for kindergarten mathematics"
    assert item.education_level == {"grade": "K"}
    assert item.language == "en"
    assert item.status_start_date == datetime(2020, 1, 1)
    assert item.status_end_date == datetime(2025, 12, 31)
    assert item.last_change_date_time == datetime(2020, 1, 1)
    assert item.extensions == {"difficulty": "beginner"}


def test_cf_item_json_parsing():
    """Test that JSON fields are properly parsed."""
    item = PowerPathCFItem(
        identifier=UUID("12345678-1234-5678-1234-567812345678"),
        uri="https://example.com/items/12345678-1234-5678-1234-567812345678",
        documentId=UUID("87654321-8765-4321-8765-432187654321"),
        CFItemTypeURI='{"type": "Standard", "uri": "https://example.com/types/standard"}',
        educationLevel='{"grade": "K"}',
        extensions='{"difficulty": "beginner"}'
    )
    
    assert item.cf_item_type_uri == {"type": "Standard", "uri": "https://example.com/types/standard"}
    assert item.education_level == {"grade": "K"}
    assert item.extensions == {"difficulty": "beginner"}


def test_cf_association_model_creation():
    """Test that we can create a CF association model with required fields."""
    association = PowerPathCFAssociation(
        identifier=UUID("12345678-1234-5678-1234-567812345678"),
        originNodeURI=UUID("11111111-1111-1111-1111-111111111111"),
        destinationNodeURI=UUID("22222222-2222-2222-2222-222222222222"),
        associationType="prerequisite"
    )
    
    assert association.identifier == UUID("12345678-1234-5678-1234-567812345678")
    assert association.origin_node_uri == UUID("11111111-1111-1111-1111-111111111111")
    assert association.destination_node_uri == UUID("22222222-2222-2222-2222-222222222222")
    assert association.association_type == "prerequisite"


def test_cf_association_model_with_all_fields():
    """Test that we can create a CF association model with all fields."""
    association = PowerPathCFAssociation(
        identifier=UUID("12345678-1234-5678-1234-567812345678"),
        uri="https://example.com/associations/12345678-1234-5678-1234-567812345678",
        originNodeURI=UUID("11111111-1111-1111-1111-111111111111"),
        destinationNodeURI=UUID("22222222-2222-2222-2222-222222222222"),
        associationType="prerequisite",
        sequenceNumber=1,
        CFDocumentURI="https://example.com/documents/33333333-3333-3333-3333-333333333333",
        lastChangeDateTime=datetime(2020, 1, 1)
    )
    
    assert association.identifier == UUID("12345678-1234-5678-1234-567812345678")
    assert association.uri == "https://example.com/associations/12345678-1234-5678-1234-567812345678"
    assert association.origin_node_uri == UUID("11111111-1111-1111-1111-111111111111")
    assert association.destination_node_uri == UUID("22222222-2222-2222-2222-222222222222")
    assert association.association_type == "prerequisite"
    assert association.sequence_number == 1
    assert association.cf_document_uri == "https://example.com/documents/33333333-3333-3333-3333-333333333333"
    assert association.last_change_date_time == datetime(2020, 1, 1) 
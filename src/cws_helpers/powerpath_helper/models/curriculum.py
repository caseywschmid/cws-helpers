"""
Curriculum Framework models for PowerPath API.

This module provides models for working with curriculum framework data in the PowerPath API.
These models represent standards, learning objectives, and other curriculum elements.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
import json
from pydantic import BaseModel, Field, field_validator

from .base import PowerPathBase


class PowerPathCFDocument(PowerPathBase):
    """
    PowerPath Curriculum Framework Document model.
    
    This model represents a curriculum framework document in the PowerPath system.
    CF Documents are containers for curriculum standards and learning objectives.
    
    Database Table: CFDocuments
    Related Tables:
    - CFItems (via documentId)
    
    Attributes:
        identifier: The document's UUID identifier
        uri: The document's URI
        title: The document's title
        description: The document's description
        creator: The document's creator
        publisher: The document's publisher
        version: The document's version
        adoption_status: The document's adoption status (adoptionStatus in API)
        status_start_date: When the status became effective (statusStartDate in API)
        status_end_date: When the status expires (statusEndDate in API)
        subject: JSON data about the subject
        subject_uri: URI for the subject (subjectURI in API)
        language: The document's language
        case_version: The CASE version (caseVersion in API)
        official_source_url: URL to the official source (officialSourceURL in API)
        notes: Additional notes about the document
        last_change_date_time: When the document was last changed (lastChangeDateTime in API)
    """
    identifier: UUID
    uri: str
    title: str
    description: Optional[str] = None
    creator: Optional[str] = None
    publisher: Optional[str] = None
    version: Optional[str] = None
    adoption_status: Optional[str] = Field(None, alias="adoptionStatus")
    status_start_date: Optional[datetime] = Field(None, alias="statusStartDate")
    status_end_date: Optional[datetime] = Field(None, alias="statusEndDate")
    subject: Optional[Dict[str, Any]] = None
    subject_uri: Optional[str] = Field(None, alias="subjectURI")
    language: Optional[str] = None
    case_version: Optional[str] = Field(None, alias="caseVersion")
    official_source_url: Optional[str] = Field(None, alias="officialSourceURL")
    notes: Optional[str] = None
    last_change_date_time: Optional[datetime] = Field(None, alias="lastChangeDateTime")
    
    @field_validator('subject', mode='before')
    @classmethod
    def parse_json_if_string(cls, v):
        """Parse JSON string to dict if needed."""
        if isinstance(v, str):
            return json.loads(v)
        return v


class PowerPathCFItem(PowerPathBase):
    """
    PowerPath Curriculum Framework Item model.
    
    This model represents a curriculum framework item in the PowerPath system.
    CF Items are individual standards or learning objectives.
    
    Database Table: CFItems
    Related Tables:
    - CFDocuments (via documentId)
    - CFAssociations (via identifier)
    
    Attributes:
        identifier: The item's UUID identifier
        uri: The item's URI
        document_id: The UUID of the document this item belongs to (documentId in API)
        human_coding_scheme: The human-readable code for this item (humanCodingScheme in API)
        list_enumeration: The list enumeration for this item (listEnumeration in API)
        abbreviated_statement: The abbreviated statement (abbreviatedStatement in API)
        full_statement: The full statement (fullStatement in API)
        alternative_label: An alternative label (alternativeLabel in API)
        cf_item_type: The type of item (CFItemType in API)
        cf_item_type_uri: URI for the item type (CFItemTypeURI in API)
        notes: Additional notes about the item
        education_level: JSON data about the education level
        language: The item's language
        status_start_date: When the status became effective (statusStartDate in API)
        status_end_date: When the status expires (statusEndDate in API)
        last_change_date_time: When the item was last changed (lastChangeDateTime in API)
        extensions: JSON data with extensions
    """
    identifier: UUID
    uri: str
    document_id: UUID = Field(alias="documentId")
    human_coding_scheme: Optional[str] = Field(None, alias="humanCodingScheme")
    list_enumeration: Optional[str] = Field(None, alias="listEnumeration")
    abbreviated_statement: Optional[str] = Field(None, alias="abbreviatedStatement")
    full_statement: Optional[str] = Field(None, alias="fullStatement")
    alternative_label: Optional[str] = Field(None, alias="alternativeLabel")
    cf_item_type: Optional[str] = Field(None, alias="CFItemType")
    cf_item_type_uri: Optional[Dict[str, Any]] = Field(None, alias="CFItemTypeURI")
    notes: Optional[str] = None
    education_level: Optional[Dict[str, Any]] = Field(None, alias="educationLevel")
    language: Optional[str] = None
    status_start_date: Optional[datetime] = Field(None, alias="statusStartDate")
    status_end_date: Optional[datetime] = Field(None, alias="statusEndDate")
    last_change_date_time: Optional[datetime] = Field(None, alias="lastChangeDateTime")
    extensions: Optional[Dict[str, Any]] = None
    
    @field_validator('cf_item_type_uri', 'education_level', 'extensions', mode='before')
    @classmethod
    def parse_json_if_string(cls, v):
        """Parse JSON string to dict if needed."""
        if isinstance(v, str):
            return json.loads(v)
        return v


class PowerPathCFAssociation(PowerPathBase):
    """
    PowerPath Curriculum Framework Association model.
    
    This model represents an association between curriculum framework items.
    CF Associations define relationships between standards or learning objectives.
    
    Database Table: CFAssociations
    Related Tables:
    - CFItems (via originNodeURI and destinationNodeURI)
    
    Attributes:
        identifier: The association's UUID identifier
        uri: The association's URI
        origin_node_uri: The URI of the origin node (originNodeURI in API)
        destination_node_uri: The URI of the destination node (destinationNodeURI in API)
        association_type: The type of association (associationType in API)
        sequence_number: The sequence number (sequenceNumber in API)
        cf_document_uri: The URI of the document (CFDocumentURI in API)
        last_change_date_time: When the association was last changed (lastChangeDateTime in API)
    """
    identifier: UUID
    uri: Optional[str] = None
    origin_node_uri: UUID = Field(alias="originNodeURI")
    destination_node_uri: UUID = Field(alias="destinationNodeURI")
    association_type: str = Field(alias="associationType")
    sequence_number: Optional[int] = Field(None, alias="sequenceNumber")
    cf_document_uri: Optional[str] = Field(None, alias="CFDocumentURI")
    last_change_date_time: Optional[datetime] = Field(None, alias="lastChangeDateTime") 
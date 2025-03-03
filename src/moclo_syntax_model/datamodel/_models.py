from __future__ import annotations

import re
import sys
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, ClassVar, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )
    pass


class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta(
    {
        "default_prefix": "moclo_syntax_model",
        "default_range": "string",
        "description": "A LinkML model to describe MoClo syntax",
        "id": "https://w3id.org/OpenCloning/moclo-syntax-model",
        "imports": ["linkml:types"],
        "license": "MIT",
        "name": "moclo-syntax-model",
        "prefixes": {
            "PATO": {"prefix_prefix": "PATO", "prefix_reference": "http://purl.obolibrary.org/obo/PATO_"},
            "biolink": {"prefix_prefix": "biolink", "prefix_reference": "https://w3id.org/biolink/"},
            "example": {"prefix_prefix": "example", "prefix_reference": "https://example.org/"},
            "linkml": {"prefix_prefix": "linkml", "prefix_reference": "https://w3id.org/linkml/"},
            "moclo_syntax_model": {
                "prefix_prefix": "moclo_syntax_model",
                "prefix_reference": "https://w3id.org/OpenCloning/moclo-syntax-model/",
            },
            "schema": {"prefix_prefix": "schema", "prefix_reference": "http://schema.org/"},
        },
        "see_also": ["https://OpenCloning.github.io/moclo-syntax-model"],
        "source_file": "src/moclo_syntax_model/schema/moclo_syntax_model.yaml",
        "title": "MoClo Syntax Model",
        "types": {
            "Color": {
                "description": "A hex color code",
                "from_schema": "https://w3id.org/OpenCloning/moclo-syntax-model",
                "name": "Color",
                "pattern": "^#([0-9a-fA-F]{6})$",
                "typeof": "string",
            },
            "Overhang": {
                "description": "A string of DNA representing an " "overhang",
                "from_schema": "https://w3id.org/OpenCloning/moclo-syntax-model",
                "name": "Overhang",
                "pattern": "^[ACGT]{4}$",
                "typeof": "string",
            },
        },
    }
)


class FeatureType(str, Enum):
    # A coding sequence
    CDS = "CDS"
    # A promoter
    promoter = "promoter"
    # A terminator
    terminator = "terminator"
    # A ribosome binding site
    rbs = "rbs"
    # A miscellaneous feature
    misc_feature = "misc_feature"


class PartDefinition(ConfiguredBaseModel):
    """
    A definition of a part
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "https://w3id.org/OpenCloning/moclo-syntax-model"})

    id: str = Field(
        default=...,
        description="""A unique identifier for a thing""",
        json_schema_extra={
            "linkml_meta": {"alias": "id", "domain_of": ["PartDefinition"], "slot_uri": "schema:identifier"}
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""A human-readable name for a thing""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["PartDefinition", "Syntax", "Assembly", "Kit"],
                "slot_uri": "schema:name",
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""A human-readable description for a thing""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["PartDefinition", "Syntax", "Assembly", "Kit"],
                "slot_uri": "schema:description",
            }
        },
    )
    color: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "color", "domain_of": ["PartDefinition"], "id_prefixes": ["Color"]}
        },
    )
    left_overhang: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "left_overhang", "domain_of": ["PartDefinition"], "id_prefixes": ["Overhang"]}
        },
    )
    right_overhang: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "linkml_meta": {"alias": "right_overhang", "domain_of": ["PartDefinition"], "id_prefixes": ["Overhang"]}
        },
    )


class Syntax(ConfiguredBaseModel):
    """
    A syntax for a MoClo method
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "https://w3id.org/OpenCloning/moclo-syntax-model"})

    name: Optional[str] = Field(
        default=None,
        description="""A human-readable name for a thing""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["PartDefinition", "Syntax", "Assembly", "Kit"],
                "slot_uri": "schema:name",
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""A human-readable description for a thing""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["PartDefinition", "Syntax", "Assembly", "Kit"],
                "slot_uri": "schema:description",
            }
        },
    )
    overhangs: List[str] = Field(
        default=..., json_schema_extra={"linkml_meta": {"alias": "overhangs", "domain_of": ["Syntax"]}}
    )


class Assembly(ConfiguredBaseModel):
    """
    An assembly of a MoClo method
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "https://w3id.org/OpenCloning/moclo-syntax-model"})

    name: Optional[str] = Field(
        default=None,
        description="""A human-readable name for a thing""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["PartDefinition", "Syntax", "Assembly", "Kit"],
                "slot_uri": "schema:name",
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""A human-readable description for a thing""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["PartDefinition", "Syntax", "Assembly", "Kit"],
                "slot_uri": "schema:description",
            }
        },
    )
    parts: List[str] = Field(
        default=..., json_schema_extra={"linkml_meta": {"alias": "parts", "domain_of": ["Assembly"]}}
    )


class Kit(ConfiguredBaseModel):
    """
    A kit for a MoClo method
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "https://w3id.org/OpenCloning/moclo-syntax-model"})

    name: Optional[str] = Field(
        default=None,
        description="""A human-readable name for a thing""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["PartDefinition", "Syntax", "Assembly", "Kit"],
                "slot_uri": "schema:name",
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""A human-readable description for a thing""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": ["PartDefinition", "Syntax", "Assembly", "Kit"],
                "slot_uri": "schema:description",
            }
        },
    )
    assemblies: List[Assembly] = Field(
        default=..., json_schema_extra={"linkml_meta": {"alias": "assemblies", "domain_of": ["Kit"]}}
    )
    syntax: Syntax = Field(default=..., json_schema_extra={"linkml_meta": {"alias": "syntax", "domain_of": ["Kit"]}})
    part_definitions: List[PartDefinition] = Field(
        default=..., json_schema_extra={"linkml_meta": {"alias": "part_definitions", "domain_of": ["Kit"]}}
    )


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
PartDefinition.model_rebuild()
Syntax.model_rebuild()
Assembly.model_rebuild()
Kit.model_rebuild()

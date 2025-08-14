"""
Model creation utilities for the declarative agent framework.

This module handles the creation of Pydantic models from JSON schemas
and provides utilities for working with structured output.
"""

from typing import Dict, Type, Union, List, Tuple
from pydantic import BaseModel, Field, create_model

from framework.types import FieldType, OutputSchema


class ModelFactory:
    """Factory for creating Pydantic models from schemas."""

    @staticmethod
    def create_output_model_from_schema(
        schema: OutputSchema, model_name: str
    ) -> Type[BaseModel]:
        """Create a Pydantic model from an output schema definition.

        Supports primitive fields, arrays (including arrays of objects), and
        nested object types by recursively constructing Pydantic sub-models.
        """
        if not schema.properties:
            raise ValueError(f"Schema for {model_name} must have properties")

        fields: Dict[str, Union[Type, Tuple[Type, Field]]] = {}  # type: ignore[valid-type]
        for field_name, field_def in schema.properties.items():
            field_type = ModelFactory._python_type_from_schema(field_def, f"{model_name}_{field_name}")
            description = field_def.get("description", "")

            # Enforce array constraints strictly
            field_kwargs: dict = {"description": description}
            field_type_str = str(field_def.get("type")) if "type" in field_def else None
            if field_type_str == "array":
                min_items = field_def.get("minItems")
                max_items = field_def.get("maxItems")
                if min_items is not None and (not isinstance(min_items, int) or min_items < 0):
                    raise ValueError(
                        f"minItems must be a non-negative integer for field '{field_name}' in {model_name}"
                    )
                if max_items is not None and (not isinstance(max_items, int) or max_items < 0):
                    raise ValueError(
                        f"maxItems must be a non-negative integer for field '{field_name}' in {model_name}"
                    )
                if isinstance(min_items, int) and isinstance(max_items, int) and max_items < min_items:
                    raise ValueError(
                        f"maxItems ({max_items}) must be >= minItems ({min_items}) for field '{field_name}' in {model_name}"
                    )
                if isinstance(min_items, int):
                    field_kwargs["min_length"] = min_items
                if isinstance(max_items, int):
                    field_kwargs["max_length"] = max_items
            else:
                # If minItems/maxItems are present on non-array fields, that's invalid
                if "minItems" in field_def or "maxItems" in field_def:
                    raise ValueError(
                        f"minItems/maxItems specified on non-array field '{field_name}' in {model_name}"
                    )

            # Required by default; callers can relax later if needed
            fields[field_name] = (field_type, Field(**field_kwargs))

        return create_model(model_name, **fields)  # type: ignore[call-overload]

    @staticmethod
    def _python_type_from_schema(
        field_def: Dict[str, Union[str, int, float, bool, list, dict]],
        model_name_prefix: str,
    ) -> Type:
        """Convert a (sub)schema field definition to a Python/Pydantic type.

        Handles:
        - string, integer, number, boolean
        - array (including arrays of objects)
        - object (nested models constructed recursively)
        """
        field_type_val = field_def.get("type")
        if field_type_val is None:
            raise ValueError(f"Field schema for {model_name_prefix} must include 'type'")
        field_type_str = str(field_type_val)

        if field_type_str == FieldType.STRING:
            return str
        if field_type_str == FieldType.INTEGER:
            return int
        if field_type_str == FieldType.NUMBER:
            return float
        if field_type_str == FieldType.BOOLEAN:
            return bool
        if field_type_str == FieldType.ARRAY:
            items_def = field_def.get("items")
            if not isinstance(items_def, dict) or not items_def:
                raise ValueError(
                    f"Array field {model_name_prefix} must specify a non-empty 'items' object"
                )
            item_type = ModelFactory._python_type_from_schema(items_def, f"{model_name_prefix}_item")
            return List[item_type]  # type: ignore[valid-type]
        if field_type_str == "object":
            # Build a nested model from properties; require non-empty properties
            props = field_def.get("properties")
            if not isinstance(props, dict) or not props:
                raise ValueError(
                    f"Object field {model_name_prefix} must define non-empty 'properties'"
                )
            nested_fields: Dict[str, Union[Type, Tuple[Type, Field]]] = {}
            for nested_name, nested_def in props.items():
                nested_type = ModelFactory._python_type_from_schema(
                    nested_def, f"{model_name_prefix}_{nested_name}"
                )
                description = nested_def.get("description", "")
                nested_fields[nested_name] = (nested_type, Field(description=description))
            nested_model = create_model(model_name_prefix, **nested_fields)  # type: ignore[call-overload]
            return nested_model

        # Unknown/unsupported type: fail fast
        raise ValueError(f"Unsupported field type '{field_type_str}' for {model_name_prefix}")

"""Collection of base CRUD classes for Proxmox."""

from typing import Generic, Type, TypeVar

from pydantic import BaseModel

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBaseProxmox(Generic[ModelType, SchemaType]):
    """CRUD object with basic CRUD methods."""

    def __init__(self, model: Type[ModelType], schema: Type[SchemaType]):
        """Set attributes."""
        self.model = model
        self.schema = schema

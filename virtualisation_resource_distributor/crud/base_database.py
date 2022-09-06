"""Collection of base CRUD classes for database."""

from typing import Any, Generic, List, Optional, Tuple, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session

from virtualisation_resource_distributor.database import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBaseDatabase(Generic[ModelType, SchemaType, CreateSchemaType]):
    """CRUD object with basic CRUD methods."""

    def __init__(self, model: Type[ModelType], schema: Type[SchemaType]):
        """Set attributes."""
        self.model = model
        self.schema = schema

    def create(
        self,
        database_session: Session,
        *,
        obj_in: CreateSchemaType,
    ) -> SchemaType:
        """Create object."""
        db_obj = self.model(**obj_in.dict())

        database_session.add(db_obj)
        database_session.commit()
        database_session.refresh(db_obj)

        return self.schema.from_orm(db_obj)

    def delete(
        self,
        database_session: Session,
        *,
        id: int,
    ) -> None:
        """Delete object."""
        obj = database_session.query(self.model).get(id)

        database_session.delete(obj)
        database_session.commit()

    def get(self, database_session: Session, id: int) -> SchemaType:
        """Get object."""
        return self.schema.from_orm(database_session.query(self.model).get(id))

    def get_multiple(
        self,
        database_session: Session,
        *,
        filter_parameters: Optional[List[Tuple[Any, Any]]] = None,
    ) -> List[SchemaType]:
        """Get objects."""
        query = database_session.query(self.model)

        if filter_parameters:
            for filter_parameter in filter_parameters:
                key, value = filter_parameter

                query = query.filter(
                    or_(cast(self.model.__dict__[key], String) == value)
                )

        return [self.schema.from_orm(i) for i in query]

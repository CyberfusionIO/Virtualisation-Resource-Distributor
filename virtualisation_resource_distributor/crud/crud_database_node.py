"""Collection of object CRUD classes."""

from virtualisation_resource_distributor.crud.base_database import (
    CRUDBaseDatabase,
)
from virtualisation_resource_distributor.models import (
    DatabaseNode as DatabaseNodeOrm,
)
from virtualisation_resource_distributor.schemas import (
    DatabaseNode as DatabaseNodeSchema,
)
from virtualisation_resource_distributor.schemas import DatabaseNodeCreate


class CRUDDatabaseNode(
    CRUDBaseDatabase[DatabaseNodeOrm, DatabaseNodeSchema, DatabaseNodeCreate]
):
    """CRUD methods for object."""

    pass


database_node = CRUDDatabaseNode(DatabaseNodeOrm, DatabaseNodeSchema)

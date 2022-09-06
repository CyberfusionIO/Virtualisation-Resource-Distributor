"""Collection of object CRUD classes."""

from virtualisation_resource_distributor.crud.base_database import (
    CRUDBaseDatabase,
)
from virtualisation_resource_distributor.models import (
    DatabaseZone as DatabaseZoneOrm,
)
from virtualisation_resource_distributor.schemas import (
    DatabaseZone as DatabaseZoneSchema,
)
from virtualisation_resource_distributor.schemas import DatabaseZoneCreate


class CRUDDatabaseZone(
    CRUDBaseDatabase[DatabaseZoneOrm, DatabaseZoneSchema, DatabaseZoneCreate]
):
    """CRUD methods for object."""

    pass


database_zone = CRUDDatabaseZone(DatabaseZoneOrm, DatabaseZoneSchema)

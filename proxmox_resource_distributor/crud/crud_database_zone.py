"""Collection of object CRUD classes."""

from proxmox_resource_distributor.crud.base_database import CRUDBaseDatabase
from proxmox_resource_distributor.models import DatabaseZone as DatabaseZoneOrm
from proxmox_resource_distributor.schemas import (
    DatabaseZone as DatabaseZoneSchema,
)
from proxmox_resource_distributor.schemas import DatabaseZoneCreate


class CRUDDatabaseZone(
    CRUDBaseDatabase[DatabaseZoneOrm, DatabaseZoneSchema, DatabaseZoneCreate]
):
    """CRUD methods for object."""

    pass


database_zone = CRUDDatabaseZone(DatabaseZoneOrm, DatabaseZoneSchema)

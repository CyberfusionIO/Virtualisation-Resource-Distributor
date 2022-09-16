"""Collection of object CRUD classes."""

from typing import List

from proxmoxer import ProxmoxAPI
from sqlalchemy.orm import Session

from virtualisation_resource_distributor import crud
from virtualisation_resource_distributor.crud.base_proxmox import (
    CRUDBaseProxmox,
)
from virtualisation_resource_distributor.models import (
    ProxmoxPool as ProxmoxPoolOrm,
)
from virtualisation_resource_distributor.schemas import (
    DatabaseZone as DatabaseZoneSchema,
)
from virtualisation_resource_distributor.schemas import ProxmoxMemberStatusEnum
from virtualisation_resource_distributor.schemas import (
    ProxmoxPool as ProxmoxPoolSchema,
)


class CRUDProxmoxPool(CRUDBaseProxmox[ProxmoxPoolOrm, ProxmoxPoolSchema]):
    """CRUD methods for object."""

    def get(
        self, proxmox_connection: ProxmoxAPI, name: str
    ) -> ProxmoxPoolSchema:
        """Get object."""
        return self.schema(name=name)

    def get_multiple(
        self, proxmox_connection: ProxmoxAPI
    ) -> List[ProxmoxPoolSchema]:
        """Get objects."""
        results = []

        for pool in proxmox_connection.pools.get():
            results.append(self.get(proxmox_connection, pool["poolid"]))

        return results

    def get_members_zones(
        self,
        database_session: Session,
        proxmox_connection: ProxmoxAPI,
        name: str,
    ) -> List[DatabaseZoneSchema]:
        """Get zones that members are in."""
        zones = []

        members = crud.proxmox_member.get_by_pool(proxmox_connection, name)

        for member in members:
            node = crud.database_node.get_multiple(
                database_session,
                filter_parameters=[("name", member.node_name)],
            )[0]
            zone = crud.database_zone.get_multiple(
                database_session, filter_parameters=[("id", node.zone_id)]
            )[0]

            if zone in zones:
                continue

            zones.append(zone)

        return zones

    def get_has_members_to_migrate(
        self,
        database_session: Session,
        proxmox_connection: ProxmoxAPI,
        name: str,
    ) -> bool:
        """Check if pool has members to migrate (members are not in as many different zones as possible)."""
        members = [
            m
            for m in crud.proxmox_member.get_by_pool(proxmox_connection, name)
            if m.status == ProxmoxMemberStatusEnum.RUNNING
        ]
        used_zones = self.get_members_zones(
            database_session, proxmox_connection, name
        )
        unused_zones = [
            zone
            for zone in crud.database_zone.get_multiple(database_session)
            if zone not in used_zones
        ]

        # More members than used zones are only allowed when there are no unused
        # zones

        if len(members) > len(used_zones):
            return bool(unused_zones)

        # There are not more members than used zones

        return False


proxmox_pool = CRUDProxmoxPool(ProxmoxPoolOrm, ProxmoxPoolSchema)

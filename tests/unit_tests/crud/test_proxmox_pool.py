from typing import List

from proxmoxer import ProxmoxAPI

from virtualisation_resource_distributor.crud import proxmox_pool
from virtualisation_resource_distributor.database import DatabaseSession
from virtualisation_resource_distributor.schemas import (
    DatabaseZone,
    ProxmoxMember,
    ProxmoxPool,
)


def test_proxmox_pool_get_multiple(
    proxmox_connection: ProxmoxAPI, proxmox_pools: List[ProxmoxPool]
) -> None:
    result = proxmox_pool.get_multiple(proxmox_connection)

    assert len(result) == 2


def test_proxmox_pool_get(
    proxmox_connection: ProxmoxAPI, proxmox_pools: List[ProxmoxPool]
) -> None:
    result = proxmox_pool.get(proxmox_connection, name=proxmox_pools[0].name)

    assert result.name == proxmox_pools[0].name


def test_proxmox_pool_get_members_zones(
    proxmox_connection: ProxmoxAPI,
    database_session: DatabaseSession,
    proxmox_pools: List[ProxmoxPool],
    proxmox_members: List[ProxmoxMember],
    database_zones: List[DatabaseZone],
) -> None:
    result = proxmox_pool.get_members_zones(
        database_session, proxmox_connection, name=proxmox_pools[0].name
    )

    assert len(result) == 1

    assert result[0].id == database_zones[0].id


def test_proxmox_pool_get_has_members_to_migrate_true(
    proxmox_connection: ProxmoxAPI,
    database_session: DatabaseSession,
    proxmox_pools: List[ProxmoxPool],
    proxmox_members: List[ProxmoxMember],
    database_zones: List[DatabaseZone],
) -> None:
    # Used zones = 1
    # Unused zones = 2
    # Amount of members = 2
    # = 1 zone to be used

    assert (
        proxmox_pool.get_has_members_to_migrate(
            database_session, proxmox_connection, name=proxmox_pools[0].name
        )
        is True
    )


def test_proxmox_pool_get_has_members_to_migrate_false(
    proxmox_connection: ProxmoxAPI,
    database_session: DatabaseSession,
    proxmox_pools: List[ProxmoxPool],
    proxmox_members: List[ProxmoxMember],
    database_zones: List[DatabaseZone],
) -> None:
    # Used zones = 1
    # Unused zones = 2
    # Amount of members = 2 (both are in the same zone, but only 1 is taken into account, as 1 is stopped)
    # = 0 zones to be used

    assert (
        proxmox_pool.get_has_members_to_migrate(
            database_session, proxmox_connection, name=proxmox_pools[1].name
        )
        is False
    )

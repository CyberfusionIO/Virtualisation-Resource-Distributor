import os
import shutil
from typing import Generator, List

import pytest
import requests_mock
from proxmoxer import ProxmoxAPI
from requests_mock.mocker import Mocker

from virtualisation_resource_distributor.config import settings
from virtualisation_resource_distributor.crud import (
    database_node,
    database_zone,
)
from virtualisation_resource_distributor.database import DatabaseSession
from virtualisation_resource_distributor.proxmox import API
from virtualisation_resource_distributor.schemas import (
    DatabaseNode,
    DatabaseNodeCreate,
    DatabaseZone,
    DatabaseZoneCreate,
    ProxmoxMember,
    ProxmoxMemberStatusEnum,
    ProxmoxPool,
)


@pytest.fixture(autouse=True)
def database() -> Generator[None, None, None]:
    """Create database and override database path in settings."""
    shutil.copyfile(
        "virtualisation-resource-distributor.sqlite3",
        os.environ[
            "DATABASE_PATH"
        ],  # Must be run from project root, where source file is located
    )

    yield

    os.unlink(os.environ["DATABASE_PATH"])


@pytest.fixture
def database_session() -> DatabaseSession:
    return DatabaseSession()


@pytest.fixture
def proxmox_connection() -> ProxmoxAPI:
    return API()


@pytest.fixture
def database_zones(database_session: DatabaseSession) -> List[DatabaseZone]:
    results = []

    results.append(
        database_zone.create(
            database_session, obj_in=DatabaseZoneCreate(name="BIT-1")
        )
    )
    results.append(
        database_zone.create(
            database_session, obj_in=DatabaseZoneCreate(name="BIT-2A")
        )
    )
    results.append(
        database_zone.create(
            database_session, obj_in=DatabaseZoneCreate(name="BIT-2C")
        )
    )

    return results


@pytest.fixture
def database_nodes(
    database_session: DatabaseSession, database_zones: List[DatabaseZone]
) -> List[DatabaseNode]:
    results = []

    results.append(
        database_node.create(
            database_session,
            obj_in=DatabaseNodeCreate(
                name="proxmox01", zone_id=database_zones[0].id
            ),
        )
    )
    results.append(
        database_node.create(
            database_session,
            obj_in=DatabaseNodeCreate(
                name="proxmox02", zone_id=database_zones[1].id
            ),
        )
    )
    results.append(
        database_node.create(
            database_session,
            obj_in=DatabaseNodeCreate(
                name="proxmox03", zone_id=database_zones[2].id
            ),
        )
    )

    return results


@pytest.fixture(autouse=True)
def proxmox_api_mock(requests_mock: Mocker) -> str:
    """Mock Proxmox API by using requests_mock (requests is used by the https backend)."""
    base_url = (
        "https://" + settings.PROXMOX_HOST + "/api2/json"
    )  # PROXMOX_HOST must include port, otherwise request doesn't match as port is missing

    requests_mock.post(
        f"{base_url}/access/ticket",
        json={
            "data": {
                "ticket": "ticket",
                "CSRFPreventionToken": "CSRFPreventionToken",
                "username": "username",
            }
        },
    )

    return base_url


@pytest.fixture
def proxmox_pools(
    requests_mock: Mocker, proxmox_api_mock: str
) -> List[ProxmoxPool]:
    results = []

    results.append(
        ProxmoxPool(name="important"),
    )
    results.append(
        ProxmoxPool(name="critical"),
    )

    requests_mock.get(
        f"{proxmox_api_mock}/pools",
        json={"data": [{"poolid": "important"}, {"poolid": "critical"}]},
    )
    requests_mock.get(
        f"{proxmox_api_mock}/pools/important",
        json={"data": {"members": []}},
    )
    requests_mock.get(
        f"{proxmox_api_mock}/pools/critical",
        json={"data": {"members": []}},
    )

    return results


@pytest.fixture
def proxmox_members(
    requests_mock: Mocker,
    proxmox_api_mock: str,
    proxmox_pools: List[ProxmoxPool],
    database_nodes: List[DatabaseZone],
) -> List[ProxmoxPool]:
    results = []

    pool0_data = []
    pool1_data = []

    # Pool 0

    member = ProxmoxMember(
        node_name=database_nodes[0].name,
        name="vm01.example.com",
        vm_id=100,
        pool_name=proxmox_pools[0].name,
        status=ProxmoxMemberStatusEnum.RUNNING,
    )
    results.append(
        member,
    )
    pool0_data.append(
        {
            "cpu": 0.0377830136013874,
            "disk": 0,
            "diskread": 562901818520,
            "diskwrite": 891997212672,
            "id": f"qemu/{member.vm_id}",
            "maxcpu": 16,
            "maxdisk": 37580963840,
            "maxmem": 17179869184,
            "mem": 14203925388,
            "name": member.name,
            "netin": 198024469241,
            "netout": 278348107239,
            "node": member.node_name,
            "status": "running",
            "template": 0,
            "type": "qemu",
            "uptime": 4115150,
            "vmid": member.vm_id,
        }
    )

    member = ProxmoxMember(
        node_name=database_nodes[0].name,
        name="vm02.example.com",
        vm_id=101,
        pool_name=proxmox_pools[0].name,
        status=ProxmoxMemberStatusEnum.RUNNING,
    )
    results.append(
        member,
    )
    pool0_data.append(
        {
            "cpu": 0.0377830136013874,
            "disk": 0,
            "diskread": 562901818520,
            "diskwrite": 891997212672,
            "id": f"qemu/{member.vm_id}",
            "maxcpu": 16,
            "maxdisk": 37580963840,
            "maxmem": 17179869184,
            "mem": 14203925388,
            "name": member.name,
            "netin": 198024469241,
            "netout": 278348107239,
            "node": member.node_name,
            "status": "running",
            "template": 0,
            "type": "qemu",
            "uptime": 4115150,
            "vmid": member.vm_id,
        }
    )

    requests_mock.get(
        f"{proxmox_api_mock}/pools/{proxmox_pools[0].name}",
        json={"data": {"members": pool0_data}},
    )

    # Pool 1

    member = ProxmoxMember(
        node_name=database_nodes[1].name,
        name="vm03.example.com",
        vm_id=102,
        pool_name=proxmox_pools[1].name,
        status=ProxmoxMemberStatusEnum.RUNNING,
    )
    results.append(
        member,
    )
    pool1_data.append(
        {
            "cpu": 0.0377830136013874,
            "disk": 0,
            "diskread": 562901818520,
            "diskwrite": 891997212672,
            "id": f"qemu/{member.vm_id}",
            "maxcpu": 16,
            "maxdisk": 37580963840,
            "maxmem": 17179869184,
            "mem": 14203925388,
            "name": member.name,
            "netin": 198024469241,
            "netout": 278348107239,
            "node": member.node_name,
            "status": "running",
            "template": 0,
            "type": "qemu",
            "uptime": 4115150,
            "vmid": member.vm_id,
        }
    )

    member = ProxmoxMember(
        node_name=database_nodes[1].name,
        name="vm04.example.com",
        vm_id=103,
        pool_name=proxmox_pools[1].name,
        status=ProxmoxMemberStatusEnum.STOPPED,
    )
    results.append(
        member,
    )
    pool1_data.append(
        {
            "cpu": 0.0377830136013874,
            "disk": 0,
            "diskread": 562901818520,
            "diskwrite": 891997212672,
            "id": f"qemu/{member.vm_id}",
            "maxcpu": 16,
            "maxdisk": 37580963840,
            "maxmem": 17179869184,
            "mem": 14203925388,
            "name": member.name,
            "netin": 198024469241,
            "netout": 278348107239,
            "node": member.node_name,
            "status": "stopped",
            "template": 0,
            "type": "qemu",
            "uptime": 4115150,
            "vmid": member.vm_id,
        }
    )

    requests_mock.get(
        f"{proxmox_api_mock}/pools/{proxmox_pools[1].name}",
        json={"data": {"members": pool1_data}},
    )

    return results

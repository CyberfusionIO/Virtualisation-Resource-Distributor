from typing import List

from proxmoxer import ProxmoxAPI

from proxmox_resource_distributor.crud import proxmox_member
from proxmox_resource_distributor.schemas import ProxmoxMember, ProxmoxPool


def test_proxmox_member_get_by_pool(
    proxmox_connection: ProxmoxAPI,
    proxmox_pools: List[ProxmoxPool],
    proxmox_members: List[ProxmoxMember],
) -> None:
    result = proxmox_member.get_by_pool(
        proxmox_connection, proxmox_pools[0].name
    )

    assert len(result) == 2

    assert result[0].name == proxmox_members[0].name

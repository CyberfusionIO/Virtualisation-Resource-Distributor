from typing import List

import docopt
import pytest
from _pytest.capture import CaptureFixture
from pytest_mock import MockerFixture  # type: ignore[attr-defined]

from proxmox_resource_distributor import CLI
from proxmox_resource_distributor.crud import database_node, database_zone
from proxmox_resource_distributor.database import DatabaseSession
from proxmox_resource_distributor.schemas import (
    DatabaseNode,
    DatabaseZone,
    ProxmoxMember,
    ProxmoxPool,
)


def test_cli_get_args():
    with pytest.raises(SystemExit):
        CLI.get_args()


# Run


def test_cli_run_has_no_members_to_migrate_without_exclude_pools(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    proxmox_pools: List[ProxmoxPool],
):
    mocker.patch(
        "proxmox_resource_distributor.CLI.get_args",
        return_value=docopt.docopt(CLI.__doc__, ["run"]),
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        CLI.main()

    assert pytest_wrapped_e.value.code == 0

    assert capsys.readouterr().out == ""


def test_cli_run_has_members_to_migrate_without_exclude_pools(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    proxmox_pools: List[ProxmoxPool],
    proxmox_members: List[ProxmoxMember],
):
    mocker.patch(
        "proxmox_resource_distributor.CLI.get_args",
        return_value=docopt.docopt(CLI.__doc__, ["run"]),
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        CLI.main()

    assert pytest_wrapped_e.value.code == 78

    assert (
        capsys.readouterr().out
        == f"Pool '{proxmox_pools[0].name}' has members to migrate\n"
    )


def test_cli_run_has_members_to_migrate_with_exclude_pools(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    proxmox_pools: List[ProxmoxPool],
):
    mocker.patch(
        "proxmox_resource_distributor.CLI.get_args",
        return_value=docopt.docopt(CLI.__doc__, ["run"]),
    )

    mocker.patch(
        "proxmox_resource_distributor.CLI.get_exclude_pools_names",
        return_value=[proxmox_pools[0].name],
    )

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        CLI.main()

    assert pytest_wrapped_e.value.code == 0

    assert (
        capsys.readouterr().out
        == f"Pool '{proxmox_pools[0].name}' has members to migrate, but is excluded\n"
    )


def test_cli_nodes_delete(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    database_session: DatabaseSession,
    database_nodes: List[DatabaseNode],
):
    mocker.patch(
        "proxmox_resource_distributor.CLI.get_args",
        return_value=docopt.docopt(
            CLI.__doc__, ["nodes", "delete", "--name", database_nodes[0].name]
        ),
    )

    assert len(database_node.get_multiple(database_session)) == 3

    CLI.main()

    assert capsys.readouterr().out == ""

    assert len(database_node.get_multiple(database_session)) == 2


# Nodes


def test_cli_nodes_list(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    database_nodes: List[DatabaseNode],
):
    mocker.patch(
        "proxmox_resource_distributor.CLI.get_args",
        return_value=docopt.docopt(CLI.__doc__, ["nodes", "list"]),
    )

    CLI.main()

    assert capsys.readouterr().out.splitlines() == [
        "- proxmox01 (ID 1)",
        "\tZone: BIT-1 (ID 1)",
        "",
        "- proxmox02 (ID 2)",
        "\tZone: BIT-2A (ID 2)",
        "",
        "- proxmox03 (ID 3)",
        "\tZone: BIT-2C (ID 3)",
        "",
    ]


def test_cli_nodes_delete(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    database_session: DatabaseSession,
    database_nodes: List[DatabaseNode],
):
    mocker.patch(
        "proxmox_resource_distributor.CLI.get_args",
        return_value=docopt.docopt(
            CLI.__doc__, ["nodes", "delete", "--name", database_nodes[0].name]
        ),
    )

    assert len(database_node.get_multiple(database_session)) == 3

    CLI.main()

    assert capsys.readouterr().out == ""

    assert len(database_node.get_multiple(database_session)) == 2


def test_cli_nodes_create(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    database_session: DatabaseSession,
    database_zones: List[DatabaseZone],
):
    mocker.patch(
        "proxmox_resource_distributor.CLI.get_args",
        return_value=docopt.docopt(
            CLI.__doc__,
            [
                "nodes",
                "create",
                "--name",
                "proxmox01",
                "--zone-name",
                database_zones[0].name,
            ],
        ),
    )

    assert len(database_node.get_multiple(database_session)) == 0

    CLI.main()

    assert capsys.readouterr().out == ""

    assert len(database_node.get_multiple(database_session)) == 1


# Zones


def test_cli_zones_list(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    database_zones: List[DatabaseZone],
    database_nodes: List[DatabaseNode],
):
    mocker.patch(
        "proxmox_resource_distributor.CLI.get_args",
        return_value=docopt.docopt(CLI.__doc__, ["zones", "list"]),
    )

    CLI.main()

    assert capsys.readouterr().out.splitlines() == [
        "- BIT-1 (ID 1)",
        "\tNodes:",
        "\tproxmox01 (ID 1)",
        "",
        "- BIT-2A (ID 2)",
        "\tNodes:",
        "\tproxmox02 (ID 2)",
        "",
        "- BIT-2C (ID 3)",
        "\tNodes:",
        "\tproxmox03 (ID 3)",
        "",
    ]


def test_cli_zones_delete(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    database_session: DatabaseSession,
    database_zones: List[DatabaseZone],
):
    mocker.patch(
        "proxmox_resource_distributor.CLI.get_args",
        return_value=docopt.docopt(
            CLI.__doc__, ["zones", "delete", "--name", database_zones[0].name]
        ),
    )

    assert len(database_zone.get_multiple(database_session)) == 3

    CLI.main()

    assert capsys.readouterr().out == ""

    assert len(database_zone.get_multiple(database_session)) == 2


def test_cli_zones_create(
    mocker: MockerFixture,
    capsys: CaptureFixture,
    database_session: DatabaseSession,
):
    mocker.patch(
        "proxmox_resource_distributor.CLI.get_args",
        return_value=docopt.docopt(
            CLI.__doc__, ["zones", "create", "--name", "BIT-1"]
        ),
    )

    assert len(database_zone.get_multiple(database_session)) == 0

    CLI.main()

    assert capsys.readouterr().out == ""

    assert len(database_zone.get_multiple(database_session)) == 1

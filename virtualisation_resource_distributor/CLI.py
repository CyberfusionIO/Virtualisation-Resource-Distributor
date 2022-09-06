"""Virtualisation Resource Distributor.

Usage:
   virtualisation-resource-distributor run
   virtualisation-resource-distributor nodes list
   virtualisation-resource-distributor nodes create --name=<name> --zone-name=<zone-name>
   virtualisation-resource-distributor nodes delete --name=<name>
   virtualisation-resource-distributor zones list
   virtualisation-resource-distributor zones create --name=<name>
   virtualisation-resource-distributor zones delete --name=<name>

Options:
  -h --help     Show this screen.
"""

import sys

import docopt
from schema import Or, Schema

from virtualisation_resource_distributor import crud, proxmox
from virtualisation_resource_distributor.config import get_exclude_pools_names
from virtualisation_resource_distributor.database import DatabaseSession
from virtualisation_resource_distributor.schemas import (
    DatabaseNodeCreate,
    DatabaseZoneCreate,
)

"""Program to distribute Virtual Machines and Containers over Proxmox zones."""


def get_args() -> docopt.Dict:
    """Get docopt args."""
    return docopt.docopt(__doc__)


def main() -> None:
    """Spawn relevant class for CLI function."""

    # Validate input

    args = get_args()
    schema = Schema(
        {
            "run": bool,
            "nodes": bool,
            "zones": bool,
            "list": bool,
            "create": bool,
            "delete": bool,
            "--name": Or(str, None),
            "--zone-name": Or(str, None),
        }
    )
    args = schema.validate(args)

    # Run classes

    database_session = DatabaseSession()

    if args["run"]:
        proxmox_api = proxmox.API()

        pools = crud.proxmox_pool.get_multiple(proxmox_api)
        pools_names_with_members_to_migrate = []

        for pool in pools:
            if pool.name in get_exclude_pools_names():
                print(
                    f"Pool '{pool.name}' has members to migrate, but is excluded"
                )

                continue

            if not crud.proxmox_pool.get_has_members_to_migrate(
                database_session, proxmox_api, pool.name
            ):
                continue

            pools_names_with_members_to_migrate.append(pool.name)

        if not pools_names_with_members_to_migrate:
            sys.exit(0)

        for pool_name in pools_names_with_members_to_migrate:
            print(f"Pool '{pool_name}' has members to migrate")

        sys.exit(78)

    if args["nodes"]:
        if args["list"]:
            nodes = crud.database_node.get_multiple(database_session)

            for node in nodes:
                zone = crud.database_zone.get(
                    database_session, id=node.zone_id
                )

                print(f"- {node.name} (ID {node.id})")
                print(f"\tZone: {zone.name} (ID {zone.id})")

                print("")

        if args["create"]:
            name = args["--name"]
            zone_name = args["--zone-name"]

            zone = crud.database_zone.get_multiple(
                database_session, filter_parameters=[("name", zone_name)]
            )[0]

            crud.database_node.create(
                database_session,
                obj_in=DatabaseNodeCreate(name=name, zone_id=zone.id),
            )

        if args["delete"]:
            name = args["--name"]

            crud.database_node.delete(
                database_session,
                id=crud.database_node.get_multiple(
                    database_session, filter_parameters=[("name", name)]
                )[0].id,
            )

    if args["zones"]:
        if args["list"]:
            zones = crud.database_zone.get_multiple(database_session)

            for zone in zones:
                nodes = crud.database_node.get_multiple(
                    database_session, filter_parameters=[("zone_id", zone.id)]
                )

                print(f"- {zone.name} (ID {zone.id})")
                print("\tNodes:")

                for node in nodes:
                    print(f"\t{node.name} (ID {node.id})")

                print("")

        if args["create"]:
            name = args["--name"]

            crud.database_zone.create(
                database_session, obj_in=DatabaseZoneCreate(name=name)
            )

        if args["delete"]:
            name = args["--name"]

            crud.database_zone.delete(
                database_session,
                id=crud.database_zone.get_multiple(
                    database_session, filter_parameters=[("name", name)]
                )[0].id,
            )

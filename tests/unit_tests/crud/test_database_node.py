from typing import List

from virtualisation_resource_distributor.crud import database_node
from virtualisation_resource_distributor.database import DatabaseSession
from virtualisation_resource_distributor.schemas import (
    DatabaseNode,
    DatabaseNodeCreate,
    DatabaseZone,
)


def test_database_node_get_multiple_without_filter_parameters(
    database_session: DatabaseSession, database_nodes: List[DatabaseNode]
) -> None:
    result = database_node.get_multiple(database_session)

    assert len(result) == 3


def test_database_node_get_multiple_with_filter_parameters(
    database_session: DatabaseSession, database_nodes: List[DatabaseNode]
) -> None:
    result = database_node.get_multiple(
        database_session, filter_parameters=[("id", database_nodes[0].id)]
    )

    assert len(result) == 1


def test_database_node_get(
    database_session: DatabaseSession, database_nodes: List[DatabaseNode]
) -> None:
    result = database_node.get(database_session, id=database_nodes[0].id)

    assert result.id == database_nodes[0].id
    assert result.name == database_nodes[0].name
    assert result.zone_id == database_nodes[0].zone_id
    assert result.created_at == database_nodes[0].created_at
    assert result.updated_at == database_nodes[0].updated_at


def test_database_node_delete(
    database_session: DatabaseSession, database_nodes: List[DatabaseNode]
) -> None:
    result = database_node.get_multiple(database_session)
    assert len(result) == 3

    database_node.delete(database_session, id=database_nodes[0].id)

    result = database_node.get_multiple(database_session)
    assert len(result) == 2


def test_database_node_create(
    database_session: DatabaseSession, database_zones: List[DatabaseZone]
) -> None:
    result = database_node.get_multiple(database_session)
    assert len(result) == 0

    database_node.create(
        database_session,
        obj_in=DatabaseNodeCreate(
            name="proxmox01", zone_id=database_zones[0].id
        ),
    )

    result = database_node.get_multiple(database_session)
    assert len(result) == 1

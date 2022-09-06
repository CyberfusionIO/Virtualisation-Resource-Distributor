from typing import List

from virtualisation_resource_distributor.crud import database_zone
from virtualisation_resource_distributor.database import DatabaseSession
from virtualisation_resource_distributor.schemas import (
    DatabaseZone,
    DatabaseZoneCreate,
)


def test_database_zone_get_multiple_without_filter_parameters(
    database_session: DatabaseSession, database_zones: List[DatabaseZone]
) -> None:
    result = database_zone.get_multiple(database_session)

    assert len(result) == 3


def test_database_zone_get_multiple_with_filter_parameters(
    database_session: DatabaseSession, database_zones: List[DatabaseZone]
) -> None:
    result = database_zone.get_multiple(
        database_session, filter_parameters=[("id", database_zones[0].id)]
    )

    assert len(result) == 1


def test_database_zone_get(
    database_session: DatabaseSession, database_zones: List[DatabaseZone]
) -> None:
    result = database_zone.get(database_session, id=database_zones[0].id)

    assert result.id == database_zones[0].id
    assert result.name == database_zones[0].name
    assert result.created_at == database_zones[0].created_at
    assert result.updated_at == database_zones[0].updated_at


def test_database_zone_delete(
    database_session: DatabaseSession, database_zones: List[DatabaseZone]
) -> None:
    result = database_zone.get_multiple(database_session)
    assert len(result) == 3

    database_zone.delete(database_session, id=database_zones[0].id)

    result = database_zone.get_multiple(database_session)
    assert len(result) == 2


def test_database_zone_create(database_session: DatabaseSession) -> None:
    result = database_zone.get_multiple(database_session)
    assert len(result) == 0

    database_zone.create(
        database_session, obj_in=DatabaseZoneCreate(name="BIT-1")
    )

    result = database_zone.get_multiple(database_session)
    assert len(result) == 1

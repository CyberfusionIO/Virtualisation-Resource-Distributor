"""Database models."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP

from virtualisation_resource_distributor.database import Base

# Database


class AuditBaseInDatabase(Base):
    """Base model for basic columns."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)

    created_at = Column(
        TIMESTAMP(timezone=False),
        server_default=func.current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        TIMESTAMP(timezone=False),
        server_default=func.current_timestamp(),
        nullable=False,
        onupdate=func.current_timestamp(),
    )


class DatabaseZone(AuditBaseInDatabase):
    """SQLAlchemy table."""

    __tablename__ = "zones"

    name = Column(String(255), nullable=False, unique=True)


class DatabaseNode(AuditBaseInDatabase):
    """SQLAlchemy table."""

    __tablename__ = "nodes"

    name = Column(String(255), nullable=False, unique=True)
    zone_id = Column(
        Integer,
        ForeignKey("zones.id", ondelete="CASCADE"),
        nullable=False,
        unique=False,
    )


# Proxmox


class ProxmoxPool:
    """Proxmox API model."""

    name: str


class ProxmoxMember:
    """Proxmox API model."""

    node_name: str
    name: str
    vm_id: int
    pool_name: str

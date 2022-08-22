"""Pydantic schemas."""

from datetime import datetime

from pydantic import BaseModel

# Database


class DatabaseZone(BaseModel):
    """Shared properties."""

    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class DatabaseZoneCreate(BaseModel):
    """Properties to receive on creation."""

    name: str


class DatabaseNode(BaseModel):
    """Shared properties."""

    id: int
    name: str
    zone_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class DatabaseNodeCreate(BaseModel):
    """Properties to receive on creation."""

    name: str
    zone_id: int


# Proxmox


class ProxmoxMember(BaseModel):
    """Shared properties."""

    node_name: str
    name: str
    vm_id: int
    pool_name: str


class ProxmoxPool(BaseModel):
    """Shared properties."""

    name: str

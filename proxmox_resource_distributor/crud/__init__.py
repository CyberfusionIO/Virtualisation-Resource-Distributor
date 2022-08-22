"""Import all CRUD objects and override __all__ for easy imports."""

from .crud_database_node import database_node
from .crud_database_zone import database_zone
from .crud_proxmox_member import proxmox_member
from .crud_proxmox_pool import proxmox_pool

__all__ = ["database_node", "database_zone", "proxmox_pool", "proxmox_member"]

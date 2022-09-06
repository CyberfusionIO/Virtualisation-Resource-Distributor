"""App configuration."""

import os
from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings."""

    DATABASE_PATH: str = "/var/lib/virtualisation-resource-distributor.sqlite3"

    PROXMOX_HOST: str = "pve-test:8006"
    PROXMOX_USERNAME: str = "guest"
    PROXMOX_REALM: str = "pve"
    PROXMOX_PASSWORD: str = "guest"
    PROXMOX_VERIFY_SSL: bool = True

    EXCLUDE_POOLS_NAMES: List[str] = []

    class Config:
        """Pydantic configuration."""

        env_file = ".env"


settings = Settings(
    _secrets_dir=os.path.join(
        os.path.sep, "etc", "virtualisation-resource-distributor"
    )
)


def get_exclude_pools_names() -> List[str]:
    """Get exclude pools names."""
    return settings.EXCLUDE_POOLS_NAMES

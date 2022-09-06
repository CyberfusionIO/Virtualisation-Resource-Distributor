"""Proxmox API helpers."""

import functools

from proxmoxer import ProxmoxAPI

from virtualisation_resource_distributor.config import settings

API = functools.partial(
    ProxmoxAPI,
    settings.PROXMOX_HOST,
    user=settings.PROXMOX_USERNAME + "@" + settings.PROXMOX_REALM,
    password=settings.PROXMOX_PASSWORD,
    verify_ssl=settings.PROXMOX_VERIFY_SSL,
)

# Virtualisation Resource Distributor

Virtualisation Resource Distributor ensures that virtual machines and resources in pools are spread as much as possible.

Spread as much as possible means:

* On as many different nodes as possible.
* In as many different zones as possible.

## Supported hypervisors

* Proxmox VE 7.x
* Proxmox VE 6.x

# Install

Install the package from PyPI:

    pip3 install virtualisation-resource-distributor

# Configure

## Environment

Add the following settings to the `.env` file. This file is relative to your working directory.

* `DATABASE_PATH`. Type: string. Default: `/var/lib/virtualisation-resource-distributor.sqlite3`
* `PROXMOX_HOST`. Type: string. Default: `pve-test:8006`. If the port is omitted, it defaults to 8006. The port must be set to run the tests.
* `PROXMOX_USERNAME`. Type: string. Default: `guest`
* `PROXMOX_REALM`. Tyoe: string. Default: `pve`
* `PROXMOX_VERIFY_SSL`. Type: boolean. Default: `True`
* `EXCLUDE_POOLS_NAMES`. Type: JSON (e.g. `'["pool1", "pool2"]'`). Default: empty list, all pools are included.

These settings can be overridden by specifying them as environment variables.

## Secrets

* Create the directory `/etc/virtualisation-resource-distributor` with secure permissions.
* Create the file `proxmox_password` with secure permissions.
* Place the password for the Proxmox user in it.

## Permissions

The Proxmox user specified in the configuration should have the following privileges:

* `Pool.Allocate` on path `/pool`

## Create database

* Create the file specified in `DATABASE_PATH` with secure permissions.
* Copy `virtualisation-resource-distributor.sqlite3` (can be found in the Git repository) to the path specified in `DATABASE_PATH`.

# Usage

## Manage zones and nodes

Add zones with:

    virtualisation-resource-distributor create-zone --name=<name>

Add nodes with:

    virtualisation-resource-distributor create-node --name=<name> --zone-name=<zone-name>

Delete nodes with:

    virtualisation-resource-distributor delete-node --name=<name>

Delete zones with:

    virtualisation-resource-distributor delete-zone --name=<name>

## Run

Check if virtual machines and resources in pools are spread as much as possible:

```
# Not spread as much as possible

$ virtualisation-resource-distributor run
Pool 'db.dmz.cyberfusion.cloud' has members to migrate
$ echo $?
78

# Spread as much as possible

$ virtualisation-resource-distributor run
$ echo $?
0
```

# Tests

Run tests with pytest:

    pytest tests/

Note:

- The tests must be run from the project root.
- The database (at `DATABASE_PATH`) is removed after the tests were run. Set it to a volatile file.

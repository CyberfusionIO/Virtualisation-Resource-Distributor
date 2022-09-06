# Virtualisation Resource Distributor

Cyberfusion provides services such as IMAP, DNS and web hosting. These services run on multiple virtual machines. Therefore, services stay available when a virtual machine is out of service. Virtualisation Resource Distributor spreads virtual machines belonging to specific services over multiple zones.

The hypervisor Proxmox VE is supported.

# Solution

Virtualisation Resource Distributor expects three things to be done:

* Group Proxmox VE cluster nodes into zones. Zones are failure domains (e.g. a datacenter).
* Group service resources into pools. E.g. in case of a DNS cluster consisting of virtual machines `dns0`, `dns1` and `dns2`, add these virtual machines to the pool `dns`. Pools may be named anything.
* Add zones and pools to database (more information below).

Virtualisation Resource Distributor makes sure resources in a pool run:

* On as many different nodes as possible.
* In as many different zones as possible.

... depending on the amount of nodes, resources and zones.

# What it does and does not do

## What it does

When Virtualisation Resource Distributor determines resources should be migrated, two things happen:

* The program exits with [status code 78](https://www.freebsd.org/cgi/man.cgi?query=sysexits).
* The program outputs the names of pools with resources to migrate.

### Running in cron

Running Virtualisation Resource Distributor in cron yields the following results:

* If no resources have to be migrated, nothing happens.
* If resources have to be migrated, `cron` should send mail.

## What it does not do

Virtualisation Resource Distributor does not migrate resources automatically. Migrating resources automatically causes more problems than it solves. When running in cron, the administrator should monitor mail sent by `cron` and migrate resources manually.

# Usage

## Install

Install the package from PyPI:

    pip3 install virtualisation-resource-distributor

## Configuration

### Environment

Add the following settings to the `.env` file. This file is relative to your working directory.

* `DATABASE_PATH`. Type: string. Default: `/var/lib/virtualisation-resource-distributor.sqlite3`
* `PROXMOX_HOST`. Type: string. Default: `pve-test:8006`. If the port is omitted, it defaults to 8006. The port must be set to run the tests.
* `PROXMOX_USERNAME`. Type: string. Default: `guest`
* `PROXMOX_REALM`. Tyoe: string. Default: `pve`
* `PROXMOX_VERIFY_SSL`. Type: boolean. Default: `True`
* `EXCLUDE_POOLS_NAMES`. Type: JSON (e.g. `'["pool1", "pool2"]'`). Default: empty list, all pools are included.

These settings can be overridden by specifying them as environment variables.

### Secrets

* Create the directory `/etc/virtualisation-resource-distributor` with secure permissions.
* Create the file `proxmox_password` with secure permissions.
* Place the password for the Proxmox user in it.

#### Permissions

The Proxmox user specified in the configuration should have the following privileges:

* `Pool.Allocate` on path `/pool`

## Create database

* Create the file specified in `DATABASE_PATH` with secure permissions.
* Copy `virtualisation-resource-distributor.sqlite3` (can be found in the Git repository) to the path specified in `DATABASE_PATH`.

## Manage zones and nodes

Add zones with:

    virtualisation-resource-distributor create-zone --name=<name>

Add nodes with:

    virtualisation-resource-distributor create-node --name=<name> --zone-name=<zone-name>

Delete nodes with:

    virtualisation-resource-distributor delete-node --name=<name>

Delete zones with:

    virtualisation-resource-distributor delete-zone --name=<name>

# Tests

Unit tests are located in `tests/unit_tests`. Run them with pytest. The tests must be run from the project root.

**The database (at `DATABASE_PATH`) is removed after the tests were run. Set it to a volatile file.**

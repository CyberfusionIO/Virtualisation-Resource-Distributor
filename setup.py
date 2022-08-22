"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="proxmox-resource-distributor",
    version="2.0",
    description="Program to distribute resources over Proxmox nodes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    author="William Edwards",
    author_email="opensource@cyberfusion.nl",
    url="https://github.com/CyberfusionNL/Proxmox-Resource-Distributor",
    platforms=["linux"],
    packages=find_packages(
        include=[
            "proxmox_resource_distributor",
            "proxmox_resource_distributor.*",
        ]
    ),
    data_files=[],
    entry_points={
        "console_scripts": [
            "proxmox-resource-distributor=proxmox_resource_distributor.CLI:main"
        ]
    },
    install_requires=[
        "pydantic[dotenv]==1.9.0",
        "SQLAlchemy==1.3.16",
        "proxmoxer==1.1.1",
        "docopt==0.6.2",
        "schema==0.7.2",
        "requests==2.28.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["cyberfusion", "proxmox"],
    license="MIT",
)

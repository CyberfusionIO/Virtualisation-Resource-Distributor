"""A setuptools based setup module."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="virtualisation-resource-distributor",
    version="3.1",
    description="Program to distribute Virtual Machines and Containers over Proxmox zones",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    author="William Edwards",
    author_email="opensource@cyberfusion.nl",
    url="https://github.com/CyberfusionNL/Virtualisation-Resource-Distributor",
    platforms=["linux"],
    packages=find_packages(
        include=[
            "virtualisation_resource_distributor",
            "virtualisation_resource_distributor.*",
        ]
    ),
    data_files=[],
    entry_points={
        "console_scripts": [
            "virtualisation-resource-distributor=virtualisation_resource_distributor.CLI:main"
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
    keywords=["cyberfusion", "proxmox", "virtualisation"],
    license="MIT",
)

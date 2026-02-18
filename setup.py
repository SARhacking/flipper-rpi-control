#!/usr/bin/env python3
"""
Setup script for flipper-rpi-control - Kali Linux application for FlipperHTTP
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flipper-rpi-control",
    version="1.0.0",
    author="Security Researcher",
    description="Kali Linux application for FlipperHTTP integration and management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SARhacking/flipper-rpi-control",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
        "Environment :: Console",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
        "flask>=2.3.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "flipper-rpi=flipper_rpi.cli:main",
            "flipper-rpi-web=flipper_rpi.web:main",
        ],
    },
    include_package_data=True,
)

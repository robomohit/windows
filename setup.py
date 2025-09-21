"""
Setup script for GameBoost Pro
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gameBoostPro",
    version="1.0.0",
    author="GameBoost Pro Team",
    author_email="support@gameboostpro.com",
    description="Advanced System Monitor and Gaming Optimizer for Windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gameboostpro/gameboostpro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Monitoring",
        "Topic :: Games/Entertainment",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gameBoostPro=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*", "*.ico", "*.png"],
    },
    zip_safe=False,
)
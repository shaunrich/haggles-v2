#!/usr/bin/env python3
"""
Setup script for Hagglz AI Negotiation Agent
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hagglz-negotiation-agent",
    version="2.0.0",
    author="Hagglz Team",
    author_email="team@hagglz.ai",
    description="AI-powered bill negotiation system with specialised agents for different bill types",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/shaunrich/haggles-v2",
    project_urls={
        "Bug Tracker": "https://github.com/shaunrich/haggles-v2/issues",
        "Documentation": "https://github.com/shaunrich/haggles-v2#readme",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.11",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "httpx>=0.25.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "tracing": [
            "langsmith>=0.1.0",
        ],
        "production": [
            "redis>=5.0.0",
            "psycopg2-binary>=2.9.0",
            "sqlalchemy>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "hagglz-api=src.hagglz.api.run_api:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yaml", "*.yml", "*.json"],
    },
    zip_safe=False,
)

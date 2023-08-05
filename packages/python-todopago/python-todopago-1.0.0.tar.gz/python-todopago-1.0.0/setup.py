#!/usr/bin/env python3
from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    version='1.0.0',
    name="python-todopago",
    description="TodoPago modern SDK for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Juan Pablo Senn",
    author_email="juanpsenn@gmail.com",
    url="https://github.com/juanpsenn/python-todopago",
    project_urls={
        "Issue Tracker": "https://github.com/juanpsenn/python-todopago/issues",
    },
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0",
        "zeep>=4.0.0,<5.0.0",
    ],
    extra_requires={
        "testing": [
            "pytest",
            "pytest-cov",
            "requests-mock",
            "tox",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

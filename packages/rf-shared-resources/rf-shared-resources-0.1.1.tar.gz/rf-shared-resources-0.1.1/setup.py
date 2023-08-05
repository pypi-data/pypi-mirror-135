#!/usr/bin/env python3

import re
import setuptools

with open("SharedResources/_version.py", "r") as f:
    try:
        version = re.search(
            r"__version__\s*=\s*[\"']([^\"']+)[\"']",f.read()).group(1)
    except:
        raise RuntimeError('Version info not available')

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="rf-shared-resources",
    version=version,
    author="Toni Kangas",
    description="Utility to share Robot Framework resource files in Python packages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kangasta/rf-shared-resources",
    packages=setuptools.find_packages(),
    install_requires=[
        "importlib_resources; python_version<'3.7'",
        "robotframework-pythonlibcore"
    ],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

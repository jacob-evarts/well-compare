#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 16:17:33 2020

@author: jacob
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Grabs the requirements from requirements.txt
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setuptools.setup(
    name="wellcompare",
    version="1.0.2.dev1",
    author="Jacob Evarts",
    author_email="jevarts@uoregon.edu",
    description="A package for doing a well to well analysis of 96 well plates run in an Epoch2 microplate reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacobian0208/well_compare_96",
    packages=setuptools.find_packages(exclude=["tests", "Screens", "Screens.*", "pkgTestEnv", "pkgTestEnv.*"]),
    install_requires=REQUIREMENTS,  # for more serious requirements then requirements.txt
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
            'Bug Reports': 'https://github.com/jacobian0208/well_compare_96/issus'
            }
)

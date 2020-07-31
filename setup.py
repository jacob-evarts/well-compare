#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 16:17:33 2020

@author: jacob
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="96-well-compare-jevarts", # Replace with your own username
    version="0.0.1",
    author="Jacob Evarts",
    author_email="jevarts@uoregon.edu",
    description="A package for doing a well to well analysis of two 96 well plates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacobian0208/well_compare.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
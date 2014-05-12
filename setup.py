#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

# dependencies
with open('requirements.txt') as f:
    deps = f.read().splitlines()

setup(
    name="mtbf-driver",
    version="0.1.0",
    packages = find_packages(),
    
    description="mtbf package",
    author="Mozilla Taiwan",
    author_email="tw-qa@mozilla.com",
    entry_points={'console_scripts': [
        'mtbf = mtbf_driver.mtbf:main']},
    install_requires=deps 
)


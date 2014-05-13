#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from distutils.sysconfig import get_python_lib
from setuptools import setup, find_packages

# dependencies
with open('requirements.txt') as f:
    deps = f.read().splitlines()

version="0.1.0"
# main setup script
setup(
    name="mtbf-driver",
    version=version,
    packages = find_packages(),
    
    description="mtbf package",
    author="Mozilla Taiwan",
    author_email="tw-qa@mozilla.com",
    entry_points={'console_scripts': [
        'mtbf = mtbf_driver.mtbf:main']},
    install_requires=deps,

    package_data={'': ['conf/*.json', 'runlist/*.list']},
    include_package_data = True
)


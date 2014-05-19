#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import shutil
from subprocess import Popen, PIPE
#from distutils.sysconfig import get_python_lib
from setuptools import setup, find_packages

# dependencies
with open('requirements.txt') as f:
    deps = f.read().splitlines()

version = "0.1.0"

# copy check_version script
check_version_script = os.path.join(os.path.dirname(__file__), "bin", "check_versions.sh")
virdir = os.getenv("VIRTUAL_ENV")
bindir = os.path.join(virdir, 'bin')
shutil.copy2(check_version_script, bindir)

# branch name and revision info
info = open(os.path.join(virdir, "info"), 'w')
gitinfo = Popen(["git log HEAD -1 | grep commit"], stdout=PIPE, shell=True).communicate()[0]
revinfo = Popen(["check_versions.sh"], stdout=PIPE, shell=True).communicate()[0]
info.write("MTBF Revision:\n" + gitinfo + "\nFirefox os Revision:\n" + revinfo)
info.close()
# main setup script
setup(
    name="mtbf-driver",
    version=version,
    packages=find_packages(),
    description="mtbf package",
    author="Mozilla Taiwan",
    author_email="tw-qa@mozilla.com",
    entry_points={'console_scripts': [
        'mtbf = mtbf_driver.mtbf:main']},
    install_requires=deps,

    package_data={'': ['conf/*.json', 'runlist/*.list', 'bin/*']},
    include_package_data=True
)

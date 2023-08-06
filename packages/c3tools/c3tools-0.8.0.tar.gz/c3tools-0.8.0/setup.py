# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, 'requirements.txt'), "r", encoding="utf-8") as fobj:
    requires = fobj.readlines()

if os.sys.version_info.major == 2:
    with open(os.path.join(here, 'requirements_py2.txt'), "r", encoding="utf-8") as fobj:
        requires += fobj.readlines()
else:
    with open(os.path.join(here, 'requirements_py3.txt'), "r", encoding="utf-8") as fobj:
        requires += fobj.readlines()
requires = [x.strip() for x in requires]

setup(
    name="c3tools",
    version="0.8.0",
    description="Collections of simple commands.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    license_files=("LICENSE",),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['c3tools', 'cmdtools'],
    install_requires=requires,
    packages=find_packages("."),
)
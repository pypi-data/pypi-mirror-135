#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import setuptools
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines() or []

with open('README.md') as f:
    readme = f.read() or ''

version = ''
with open('aiokubemq/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Version is not set!')


setup(
    name='aiokubemq',
    version=version,
    description='Asynchronous KubeMQ Client',
    author='Technofab',
    author_email='aiokubemq.git@technofab.de',
    url='https://gitlab.com/TECHNOFAB/aiokubemq',
    license='GPL-3.0',
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires='>=3.6',
)

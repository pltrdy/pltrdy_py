#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pltrdy_py',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.0',
    packages=find_packages(),
    project_urls={
    },
    install_requires=[
        "pytz",
    ],
    entry_points={
        "console_scripts": [
            "gen_py=pltrdy.gen_script:main"
        ],
    }
)

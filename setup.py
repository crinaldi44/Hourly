# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "openapi_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
]

setup(
    name=NAME,
    version=VERSION,
    description="Hourly API",
    author_email="test@test.com",
    url="",
    keywords=["OpenAPI", "Hourly API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['start_server=domains.__main__:main']},
    long_description="""\
    Provides interaction with Hourly web app.
    """
)


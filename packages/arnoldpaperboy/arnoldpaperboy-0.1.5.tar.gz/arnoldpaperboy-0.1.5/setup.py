# -*- coding: utf-8 -*-
# (c) Satelligence, see LICENSE.
# pylint: skip-file
from setuptools import setup, find_packages

version = '0.1.5'

long_description = open('README.rst').read()

requirements = [
    'dealer>=2.0.0,<3.0.0',
    'google-api-core>=2.0.0,<3.0.0',
    'google-auth>=2.0.0,<3.0.0',
    'google-cloud-core>=2.0.0,<3.0.0',
    'google-cloud-logging>=2.0.0,<3.0.0',
    'google-cloud-monitoring>=2.0.0,<3.0.0',
    'googleapis-common-protos>=1.50.0,<2.0.0',
    'grpc-google-iam-v1>=0.12.0,<1.0.0',
    'grpcio>=1.30.0,<2.0.0',
]

test_requirements = [
    'pytest',
]

setup(
    name='arnoldpaperboy',
    version=version,
    description="Deliver to stackdriver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Satelligence",
    author_email='schut@satelligence.com',
    url='https://gitlab.com/satelligence/arnoldpaperboy',
    packages=find_packages(),
    include_package_data=True,
    license="Apache-2.0",
    zip_safe=False,
    python_requires='>=3.5',
    install_requires=requirements,
)

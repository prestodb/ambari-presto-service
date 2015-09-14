#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

test_requirements = [
    'tox==1.9.2',
    'nose==1.3.7',
    'mock==1.0.1',
]


setup(
    name='ambari-presto',
    version='0.1.0',
    description='This project contains the integration code for integrating \
Presto as a service in Ambari.',
    long_description=readme + '\n\n' + history,
    author='Teradata Coporation',
    author_email='anton.petrov@teradata.com',
    url='https://github.com/TeradataCenterForHadoop/ambari-presto-service',
    packages=['package.scripts'],
    data_files=[('', ['metainfo.xml']),
                ('configuration', ['configuration/config.properties.xml',
                                    'configuration/jvm.config.xml',
                                    'configuration/node.properties.xml']),
                ('themes', ['themes/theme.json'])
    ],
    include_package_data=True,
    license='APLv2',
    zip_safe=False,
    keywords=['presto', 'ambari', 'hadoop'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: APLv2 License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    tests_require=test_requirements,
)

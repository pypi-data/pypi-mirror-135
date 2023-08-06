# -*- coding: utf-8 -*-
"""Installer for the dsgov.migration package."""

from setuptools import find_packages, setup

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='dsgov.migration',
    version='1.0b3',
    description="A add-on to import json content to plone",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone CMS',
    author='handryks@gmail.com',
    author_email='handryks@gmail.com',
    url='https://github.com/collective/dsgov.migration',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/dsgov.migration',
        'Source': 'https://github.com/collective/dsgov.migration',
        'Tracker': 'https://github.com/collective/dsgov.migration/issues',
        # 'Documentation': 'https://dsgov.migration.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['dsgov'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'z3c.jbot',
        'plone.api>=1.8.4',
        'plone.app.dexterity',
        'collective.transmogrifier>=2.0.0',
        'plone.app.transmogrifier>=2.0.0',
        'collective.jsonmigrator>=2.0.0',
        'transmogrify.dexterity>=2.0.0',
        'pandas==1.3.5',
        'openpyxl==3.0.9',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.testing>=5.0.0',
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = dsgov.migration.locales.update:update_locale
    """,
)

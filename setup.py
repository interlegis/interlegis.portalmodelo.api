# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0b3'
description = 'Portal Modelo: API'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='interlegis.portalmodelo.api',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='interlegis api plone portalmodelo',
    author='Programa Interlegis',
    author_email='ti@interlegis.leg.br',
    url='https://github.com/interlegis/interlegis.portalmodelo.api',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['interlegis', 'interlegis.portalmodelo'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'five.grok',
        'plone.api',
        'plone.app.registry',
        'plone.app.upgrade',
        'plone.directives.form',
        'plone.namedfile',
        'plone.registry',
        'Products.BrFieldsAndWidgets',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'z3c.relationfield',
        'zope.component',
        'zope.globalrequest',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'AccessControl',
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'robotsuite',
        ],
    },
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)

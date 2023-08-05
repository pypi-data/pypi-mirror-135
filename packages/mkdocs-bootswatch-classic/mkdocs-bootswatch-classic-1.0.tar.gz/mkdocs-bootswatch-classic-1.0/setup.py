from setuptools import setup, find_packages
from distutils.core import Command
import os

VERSION = '1.0'


setup(
    name="mkdocs-bootswatch-classic",
    version=VERSION,
    url='http://www.mkdocs.org',
    license='BSD',
    description='Bootswatch themes for MkDocs',
    author='Dougal Matthews',
    author_email='dougal@dougalmatthews.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['mkdocs>=1.0'],
    python_requires='>=2.7.9,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    entry_points={
        'mkdocs.themes': [
            # Amelia and Readable don't have Bootswatch 4 versions, so we can
            # keep these around without the `-classic` suffix for compatibility.
            'amelia = mkdocs_bootswatch_classic.amelia',
            'readable = mkdocs_bootswatch_classic.readable',

            'mkdocs-classic = mkdocs_bootswatch_classic.mkdocs',
            'amelia-classic = mkdocs_bootswatch_classic.amelia',
            'bootstrap-classic = mkdocs_bootswatch_classic.bootstrap',
            'cerulean-classic = mkdocs_bootswatch_classic.cerulean',
            'cosmo-classic = mkdocs_bootswatch_classic.cosmo',
            'cyborg-classic = mkdocs_bootswatch_classic.cyborg',
            'flatly-classic = mkdocs_bootswatch_classic.flatly',
            'journal-classic = mkdocs_bootswatch_classic.journal',
            'readable-classic = mkdocs_bootswatch_classic.readable',
            'simplex-classic = mkdocs_bootswatch_classic.simplex',
            'slate-classic = mkdocs_bootswatch_classic.slate',
            'spacelab-classic = mkdocs_bootswatch_classic.spacelab',
            'united-classic = mkdocs_bootswatch_classic.united',
            'yeti-classic = mkdocs_bootswatch_classic.yeti',
        ]
    },
    zip_safe=False
)

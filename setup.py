#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Mu Yang <http://muyang.pro>"
__copyright__ = "2018-2021 CKIP Lab"
__license__ = "GPL-3.0"

from setuptools import setup, find_namespace_packages
import ehn as about

################################################################################


def main():

    with open("README.rst") as fin:
        readme = fin.read()

    setup(
        name="ehownet",
        version=about.__version__,
        author=about.__author_name__,
        author_email=about.__author_email__,
        description=about.__description__,
        long_description=readme,
        long_description_content_type="text/x-rst",
        url=about.__url__,
        download_url=about.__download_url__,
        platforms=["linux_x86_64"],
        license=about.__license__,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3 :: Only",
            "License :: Free for non-commercial use",
            "Natural Language :: Chinese (Traditional)",
        ],
        packages=find_namespace_packages(
            include=[
                "ehn",
                "ehn.*",
            ]
        ),
        install_requires=[
            "ply>=3.11",
            "treelib>=1.6.0",
            "wcwidth>=0.2.5",
            'dataclasses; python_version < "3.7"',
        ],
        entry_points={
            "console_scripts": [
                "ehn-parser = ehn._bin.parser:main",
            ],
        },
    )


################################################################################

if __name__ == "__main__":
    main()

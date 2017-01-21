"""
clover-config - A clover efi bootloader configuration utility.
Copyright (C) 2017  Fin Christensen <christensen.fin@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath (path.dirname (__file__))

# Get the long description from the README.rst file
with open (path.join (here, "README.rst"), encoding = "utf-8") as readme:
    long_description = readme.read ()

setup (
    name = "clover-config",
    version = "0.0.1",
    description = "A clover efi bootloader configuration utility.",
    long_description = long_description,
    url = "",
    author = "Fin Christensen",
    author_email = "christensen.fin@gmail.com",
    license = "GPLv3+",
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Boot",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords = "clover efi uefi config configuration bootloader boot",
    packages = find_packages (),
    install_requires = ["colorlog"],
    extras_require = {},
    package_data = {
        "music_sync": [],
    },
    data_files = [],
    entry_points = {
        "console_scripts": [
            "clover-config=clover_config:main"
        ],
    },
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  i-Parapheur Utils
#  Copyright (C) 2017-2022 Libriciel-SCOP
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

import parapheur

setup(
    name='iparapheur-utils3.beta',
    version=parapheur.__version__,
    packages=find_packages(),
    author="Libriciel SCOP",
    author_email="contact@libriciel.fr",
    description="Client python pour i-Parapheur",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'suds-py3 == 1.4.4.1',
        'requests == 2.26.0',
        'PyMySql == 1.0.2',
        'progress == 1.6',
        'distro == 1.6.0'
        # TODO : Check those Python2 leftovers
        # 'importlib',
        # 'Unidecode',
        # 'pandas',
        # 'lxml'
    ],
    include_package_data=True,
    url='https://gitlab.libriciel.fr/i-parapheur/client-python',
    entry_points={
        'console_scripts': [
            'ph-echo = parapheur.core:echo',
            'ph-check = parapheur.core:check',
            'ph-init = parapheur.core:init',
            'ph-recupArchives = parapheur.core:recuparchives',
            'ph-properties-merger = parapheur.core:properties_merger',
            'ph-export = parapheur.core:export_data',
            'ph-import = parapheur.core:import_data',
            'ph-rename = parapheur.core:rename',
            'ph-removeldap = parapheur.core:remove_ldap',
            'ph-pushdoc = parapheur.core:pushdoc',
            'ph-ipclean = parapheur.core:ipclean',
            'ph-ldapsearch = parapheur.core:ldapsearch',
            'ph-count_files = parapheur.core:count_files',
            'ph-reset_admin_password = parapheur.core:reset_admin_password',
            'ph-patch = parapheur.core:patch',
            'ph-recupfull = parapheur.core:recupfull',
            'ph-template = parapheur.core:template',
            'ph-orphan = parapheur.core:orphan',
        ],
    },
    Classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3'
    ],
    license="AGPLv3",
)

#!/usr/bin/env python
# coding=utf-8

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

from parapheur.parapheur import pprint  # Colored printer
import sys

req_version = (3, 0)
cur_version = sys.version_info
isp3 = cur_version >= req_version
if isp3:
    # noinspection PyCompatibility,PyUnresolvedReferences
    import configparser as ConfigParser
else:
    # noinspection PyCompatibility
    import ConfigParser
import file_utils
import io

defaut_iparapheur_root = "/opt/iParapheur"


def alfresco_global_exists():
    # Alfresco-global.properties
    file_utils.directory_exists(defaut_iparapheur_root)
    file_utils.subdir_exists(defaut_iparapheur_root, "tomcat/shared/classes")
    return file_utils.file_exists("{0}/tomcat/shared/classes"
                                .format(defaut_iparapheur_root),
                                 "alfresco-global.properties")


def parse(conf):
    if not alfresco_global_exists():
        pprint.error("BAD")
        sys.exit()
    CONFIG_PATH = conf.format(defaut_iparapheur_root)
    with open(CONFIG_PATH, 'r') as f:
        config_string = '[Parapheur]\n' + f.read()
    config_fp = io.BytesIO(config_string)
    config = ConfigParser.RawConfigParser()
    config.readfp(config_fp)

    return config

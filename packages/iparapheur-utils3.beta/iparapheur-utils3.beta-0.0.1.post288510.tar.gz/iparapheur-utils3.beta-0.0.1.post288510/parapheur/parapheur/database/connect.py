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

# module Database
from urlparse import urlparse
import pymysql.cursors


def connect(varconf):
    mysqldburl = varconf.get("Parapheur", "db.url")
    urlparsed = urlparse(mysqldburl[5:])
    mysqlserver = urlparsed.hostname
    mysqlport = 3306
    mysqluser = "null"
    mysqlpwd = "null"
    mysqlbase = "null"
    if urlparsed.port is not None:
        mysqlport = urlparsed.port
        mysqluser = varconf.get("Parapheur", "db.username")
        mysqlpwd = varconf.get("Parapheur", "db.password")
        mysqlbase = varconf.get("Parapheur", "db.name")
    cnx = pymysql.connect(user=mysqluser, password=mysqlpwd, host=mysqlserver, port=mysqlport, database=mysqlbase)
    return cnx

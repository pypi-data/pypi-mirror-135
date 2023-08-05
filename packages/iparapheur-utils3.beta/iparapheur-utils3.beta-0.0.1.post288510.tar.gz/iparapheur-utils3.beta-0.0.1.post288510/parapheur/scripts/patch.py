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

from parapheur.parapheur import config
import os
from os import path as os_path

server = config.get("Parapheur", "server")
folder = config.get("Parapheur", "folder")
PATH = os_path.abspath(os_path.split(__file__)[0])
script = PATH + "/script/patch.sh"
print(script)

os.chmod(script, 0o0755)
script2 = script + " " + folder + " " + server
os.system(script2)

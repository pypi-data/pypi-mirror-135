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

import os
import sys
from subprocess import check_call, CalledProcessError


def checkinstallation():
    from . import checkInstallationIP


def recuparchives():
    from . import recupArchives


def importdata():
    from . import import_data


def exportdata():
    from . import export_data


def rename():
    from . import change_name


def removeldap():
    from . import remove_ldap


def push_doc():
    from . import pushdoc


def ip_clean():
    from . import ipclean


def ldap_search():
    from . import ldapsearch


def countfiles():
    from . import count_files


def reset_admin():
    from . import reset_admin_password


def dopatch():
    from . import patch


def recupfull():
    from . import recupfull


def template():
    from . import template


def orphan():
    from . import orphan


def properties_merger():
    args = sys.argv[1:]
    args.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/shell/properties-merger/properties-merger.sh")
    try:
        check_call(args)
    except CalledProcessError:
        pass

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

# module Parapheur
import os
from parapheur.parapheur import pprint


def directory_exists(repertoire, verbose=False):
    if os.path.exists(repertoire):
        if verbose:
            pprint.header("#", False, ' ')
            pprint.info("Répertoire", False, ' ')
            pprint.info(repertoire.ljust(35), True, ' ')
            pprint.success('{:>10s}'.format("OK"), True)
        return True
    else:
        pprint.header("#", False, ' ')
        pprint.info("Répertoire", False, ' ')
        pprint.info(repertoire.ljust(35), True, ' ')
        pprint.warning('{:>10s}'.format("absent"))
        return False


def subdir_exists(repertoire, sousrep, verbose=False):
    if os.path.exists("{0}/{1}".format(repertoire, sousrep)):
        if verbose:
            pprint.header("#", False, ' ')
            pprint.info("  subdir", False, ' ')
            pprint.info(sousrep.ljust(37), True, ' ')
            pprint.success('{:>10s}'.format("OK"), True)
        return True
    else:
        pprint.header("#", False, ' ')
        pprint.info("  subdir", False, ' ')
        pprint.info(sousrep.ljust(37), True, ' ')
        pprint.warning('{:>10s}'.format("absent"))
        return False


def file_exists(repertoire, fichier, verbose=False):
    if os.path.exists("{0}/{1}".format(repertoire, fichier)):
        if verbose:
            pprint.header("#", False, ' ')
            pprint.info(" fichier", False, ' ')
            pprint.info(fichier.ljust(37), True, ' ')
            pprint.success('{:>10s}'.format("OK"))
        return True
    else:
        pprint.header("#", False, ' ')
        pprint.info(" fichier", False, ' ')
        pprint.info(fichier.ljust(37), True, ' ')
        pprint.warning('{:>10s}'.format("absent"))
        return False

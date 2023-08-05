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

# module ParapheurModule
"""
CeCILL Copyright (c) 2006-2015, ADULLACT-projet
Initiated by ADULLACT-projet S.A.
Developped by ADULLACT-projet S.A.

contact@adullact-projet.coop

Ce logiciel est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA
sur le site "http://www.cecill.info".

En contrepartie de l'accessibilité au code source et des droits de copie,
de modification et de redistribution accordés par cette licence, il n'est
offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
seule une responsabilité restreinte pèse sur l'auteur du programme,  le
titulaire des droits patrimoniaux et les concédants successifs.

A cet égard  l'attention de l'utilisateur est attirée sur les risques
associés au chargement,  à l'utilisation,  à la modification et/ou au
développement et à la reproduction du logiciel par l'utilisateur étant
donné sa spécificité de logiciel libre, qui peut le rendre complexe à
manipuler et qui le réserve donc à des développeurs et des professionnels
avertis possédant  des  connaissances  informatiques approfondies.  Les
utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
logiciel à leurs besoins dans des conditions permettant d'assurer la
sécurité de leurs systèmes et ou de leurs données et, plus généralement,
à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.

Le fait que vous puissiez accéder à cet en-tête signifie que vous avez
pris connaissance de la licence CeCILL, et que vous en avez accepté les
termes.
"""
import os
from shutil import copyfile
from .Client import Client
from .Webservice import Webservice

import requests
from configparser import ConfigParser

from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

__author__ = 'lhameury'

# Récuperation du fichier de propriétés
config = ConfigParser()
real_config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'script.cfg')
if os.path.isfile("./iparapheur-utils.cfg"):
    real_config_path = "./iparapheur-utils.cfg"
config.read(real_config_path)


def copyconfig(filename, path):
    configpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../configs', filename + '.cfg')
    copyfile(configpath, os.path.join(path, "iparapheur-utils.cfg"))


def setconfig(path):
    global config, real_config_path
    # Récuperation du fichier de propriétés
    config = ConfigParser()
    config.read([real_config_path, path])


def setconfigproperty(section, propertyname, value):
    config.set(section, propertyname, value)


def getrestclient():
    return Client(config)


def getsoapclient(user=None, password=None):
    if user is not None and password is not None:
        return Webservice(config, user, password)
    else:
        return Webservice(config)

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
from parapheur.parapheur import pprint


def clean(_str_):
    _str_ = _str_.replace('\n', '')
    _str_ = _str_.replace('\r', '')
    _str_ = _str_.split("=", 1)
    return _str_[1]


def get_conf():
    global conf, active, url, security_principal, credentials, groupSearchBase, personDifferentialQuery
    pprint.header("----------- Récupération des sources")
    try:
        conf = config.get("Ldapsearch", "conf_file")
    except:
        pprint.error("Fichier de conf requis: ph-init ldapsearch")

    try:
        file = open(conf, "r")
        pprint.success("OK")
    except:
        pprint.error("ERREUR : Le fichier de conf " + conf + " n'existe pas")
        exit(0)

    # noinspection PyUnboundLocalVariable
    for line in file:
        if line.startswith("ldap.authentication.active"):
            active = clean(line)
        if line.startswith("ldap.authentication.java.naming.provider.url"):
            url = clean(line)
        if line.startswith("ldap.synchronization.java.naming.security.principal"):
            security_principal = clean(line)
        if line.startswith("ldap.synchronization.java.naming.security.credentials"):
            credentials = clean(line)
        if line.startswith("ldap.synchronization.groupSearchBase"):
            groupSearchBase = clean(line)
        if line.startswith("ldap.synchronization.personDifferentialQuery"):
            personDifferentialQuery = clean(line)
    file.close()
    return active, url, security_principal, credentials, groupSearchBase, personDifferentialQuery


def isSynchoEnable(authentication_active):
    pprint.header("----------- Synchronisation demandée ?")

    if authentication_active == "true":
        pprint.success("Synchronisation activée")
    else:
        pprint.error("ERREUR : Synchronisation désactivée")


def accessUrl(authentication_url):
    pprint.header("----------- URL accessible ?")
    url1 = authentication_url.split("//")
    url2 = url1[1].split(":")
    try:
        response = os.system("ping -c 1 " + url2[0] + " -p " + url2[1])
    except:
        response = os.system("ping -c 1 " + url2[0])

    if response == 0:
        pprint.success('Le serveur LDAP est accessible')
    else:
        pprint.error('ERREUR : Le serveur LDAP  n\'est pas accessible ' + authentication_url)


def ldapRequest(url, security_principal, credentials, groupSearchBase, personDifferentialQuery):
    global query
    pprint.header("----------- Requête LDAP")
    query = "ldapsearch -LLL -H " + url + " -x -D " + security_principal + " -w '" + credentials + "' -b '" \
            + groupSearchBase + "' '" + personDifferentialQuery + "' | grep displayName "
    pprint.info(query)
    return query


def ldapSearchGrepDisplayname():
    pprint.header("----------- Liste des utilisateurs")
    os.system(query.replace('\\', ''))


get_conf()
isSynchoEnable(active)
accessUrl(url)
ldapRequest(url, security_principal, credentials, groupSearchBase, personDifferentialQuery)
ldapSearchGrepDisplayname()

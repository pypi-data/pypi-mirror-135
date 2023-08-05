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

import parapheur
from progress.bar import IncrementalBar

client = parapheur.getrestclient()

if client.islogged:
    utilisateurs = client.doget("/parapheur/utilisateurs")
    bar = IncrementalBar('Analyse des utilisateurs', max=len(utilisateurs), suffix='%(index)d/%(max)d - %(eta)ds')

    to_delete = []

    for user in utilisateurs:
        if user["isFromLdap"]:
            bureaux = client.doget("/parapheur/utilisateurs/%s/bureaux" % user["id"], {"administres": "false"})
            if len(bureaux) == 0:
                to_delete.append(user)
                client.dodelete("/parapheur/utilisateurs/%s" % user["id"])

        bar.next()

    bar.finish()

    bar = IncrementalBar('Suppression des utilisateurs LDAP inutiles',
                         max=len(to_delete),
                         suffix='%(index)d/%(max)d - %(eta)ds')

    for user in to_delete:
        client.dodelete("/parapheur/utilisateurs/%s" % user["id"])
        bar.next()

    bar.finish()

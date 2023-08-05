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

import pymysql
import os
from parapheur.parapheur import config
from parapheur.parapheur import pprint  # Colored printer


# Init database connexion
cnx = pymysql.connect(user=config.get("Database", "username"), password=config.get("Database", "password"),
                      host=config.get("Database", "server"), database=config.get("Database", "database"))

pprint.header("\nRéinitialisation du mot de passe admin")

cursor = cnx.cursor()

# On récupère les 2 identifiants
query1 = "SELECT anp1.node_id, anp1.qname_id, anp1.string_value " \
         "FROM alf_node_properties anp1 " \
         "INNER JOIN alf_qname aq1 ON aq1.id = anp1.qname_id " \
         "INNER JOIN alf_node_properties anp2 ON anp2.node_id = anp1.node_id " \
         "INNER JOIN alf_qname aq2 ON aq2.id = anp2.qname_id " \
         "WHERE aq1.local_name = 'password' " \
         "AND aq2.local_name = 'username' " \
         "AND anp2.string_value = 'admin';"
cursor.execute(query1)
x = cursor.fetchall()
node_id = x[0][0]
qname_id = x[0][1]

# On modifie le mot de passe
query2 = "UPDATE alf_node_properties " \
         "SET string_value='209c6174da490caeb422f3fa5a7ae634' " \
         "WHERE node_id={0} and qname_id={1};".format(str(node_id), str(qname_id))
cursor.execute(query2)
cnx.commit()
cnx.close()

# On relance l'application
os.system("/etc/init.d/alfresco restart")

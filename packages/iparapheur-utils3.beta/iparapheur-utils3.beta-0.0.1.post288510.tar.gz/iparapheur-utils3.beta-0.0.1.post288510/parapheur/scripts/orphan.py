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


from parapheur.parapheur import parse, file_utils
from parapheur.parapheur.database import connect, execute
import os

default_iparapheur_root = "/opt/iParapheur/"
tomcat_conf_subdir = "tomcat/shared/classes/"
alfresco_conf_file = "alfresco-global.properties"
queries = []
query_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "parapheur/database/queries/orphans/"))
exit_code = 0

# Get data from alfresco-global.properties for connecting database
file_utils.directory_exists(default_iparapheur_root, False)
file_utils.subdir_exists(default_iparapheur_root, tomcat_conf_subdir, False)
file_utils.file_exists(default_iparapheur_root + tomcat_conf_subdir, alfresco_conf_file, False)
alfresco_conf = parse.parse(default_iparapheur_root + tomcat_conf_subdir + alfresco_conf_file)

# Get the dabatase connexion
cnx = connect.connect(alfresco_conf)

# Execute queries
query_files = os.listdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', query_root)))
for file in query_files:
    if file.endswith("sql"):
        f = open(query_root + '/' + file, "r")
        query = f.readline()
        queries.append(query)
queries_responses = execute.execute(cnx, queries)

# Return exit code for both queries
for response in queries_responses:
    if response != 0:
        exit_code = 1

if exit_code == 1:
    print(
        "Il y a des noeuds orphelins en base de données. Vous pouvez utilisez la commande 'ph-ipclean' pour les "
        "supprimer et générer les index")
else:
    print("Il n'y a pas de noeud orphelin en base de données.")

exit(exit_code)

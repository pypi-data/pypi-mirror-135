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

from parapheur.parapheur import config  # Configuration
from parapheur.parapheur import pprint  # Colored printer

current_host = config.get("Parapheur", "old_url")
new_host = config.get("Parapheur", "new_url")


def replace_hostname_in_file(file_to_handle):
    # Read in the file
    with open(file_to_handle, 'r') as f_read:
        filedata = f_read.read()

    # Replace the target string
    filedata = filedata.replace(current_host, new_host)

    # Write the file out again
    with open(file_to_handle, 'w') as f_write:
        f_write.write(filedata)


# NginX
replace_hostname_in_file("/etc/nginx/conf.d/parapheur.conf")
replace_hostname_in_file("/etc/nginx/conf.d/parapheur_ssl.conf")
# Tomcat
replace_hostname_in_file("/opt/iParapheur/tomcat/scripts/ctl.sh")
replace_hostname_in_file("/opt/iParapheur/tomcat/conf/Catalina/localhost/alfresco.xml")
replace_hostname_in_file("/opt/iParapheur/tomcat/shared/classes/alfresco-global.properties")
replace_hostname_in_file("/opt/iParapheur/tomcat/shared/classes/iparapheur-global.properties")
# WSDL
replace_hostname_in_file("/var/www/parapheur/alfresco/iparapheur.wsdl")

pprint.warning("ATTENTION ! Le certificat serveur configuré dans le fichier /etc/nginx/conf.d/parapheur_ssl.conf "
               "ne correspond potentiellement plus avec le nouveau nom du parapheur.\nIl convient de remplacer "
               "ce certificat (localisé dans le dossier /etc/nginx/ssl/) pour que le parapheur soit totalement "
               "fonctionnel.\n", True)

pprint.success("Propriétés à modifier dans le fichier de configuration /etc/nginx/conf.d/parapheur_ssl.conf :")
pprint.header("- ssl_certficiate /etc/nginx/ssl/certificat.pem;     # Partie publique")
pprint.header("- ssl_certficiate_key /etc/nginx/ssl/certificat.key; # Partie privée\n")

pprint.info("Une fois les modifications de certificat effectuées, relancer le service NginX :")
pprint.header("service nginx restart\n\n")

pprint.success("Modification de nom terminée.")

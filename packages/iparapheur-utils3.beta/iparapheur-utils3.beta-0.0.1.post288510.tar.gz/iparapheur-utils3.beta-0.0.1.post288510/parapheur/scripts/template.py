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

import parapheur
import os
import time
import zipfile
import filecmp
from parapheur.parapheur import config  # Configuration

# Configuration
# Init REST API client
client = parapheur.getrestclient()
models = client.doget("/parapheur/modeles")
template_names = ["parapheur-signataires.ftl", "parapheur-owner-archivage.ftl", "parapheur-mail-reject.ftl",
                   "parapheur-digest-mail.ftl", "parapheur-secretariat-relecture.ftl", "parapheur-dossier-email.ftl",
                   "parapheur-current-reception.ftl", "parapheur-mail-retard.ftl", "parapheur-diffusion-tdt-ok.ftl",
                   "parapheur-mail-moveAdmin.ftl", "parapheur-mail-reviewing.ftl", "parapheur-next-reprise.ftl",
                   "parapheur-secretariat-retour.ftl", "parapheur-tiers-tdt-ok-archivage.ftl",
                   "parapheur-admin-suppression.ftl", "parapheur-mailsec-template.ftl", "parapheur-owner-retour.ftl",
                   "parapheur-owner-reception.ftl", "parapheur-diffusion-archive.ftl", "parapheur-tiers-visa.ftl",
                   "parapheur-current-retard.ftl", "parapheur-tiers.ftl", "parapheur-diffusion-visa.ftl",
                   "parapheur-diffusion-retour.ftl", "parapheur-admin-transfert.ftl", "parapheur-tiers-retour.ftl",
                   "parapheur-mail-approve.ftl", "parapheur-mail-tiers.ftl", "parapheur-current-tdt-ok-archivage.ftl",
                   "parapheur-mail-resetpassword.ftl", "parapheur-mail-remord.ftl", "parapheur-diffusion-emission.ftl",
                   "parapheur-mail-archive.ftl", "parapheur-mail-deleteAdmin.ftl", "parapheur-mail-delegation.ftl",
                   "parapheur-secretariat-signature.ftl", "parapheur-mail-print.ftl"]
template_root = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "files/templates/"))
reload_template = config.getboolean("Parapheur", "reload")
zip = zipfile.ZipFile('models' + time.strftime('%d%m%Y_%H%M%S') + ".zip", 'w')

for model in models:
    # Get template data
    model_response = client.doget("/parapheur/modeles/%s" % model['id'])
    model_name = model_response['name']
    model_content = model_response['content']
    # Check if the template has been changed
    g = open(template_root + '/' + str(model_name), "r")
    g_text = g.read()
    f = open(model['name'], "w")
    if g_text != model_content.encode('utf-8'):
        print(str(model_name) + ": Ce modèle n'est pas à jour et/ou a été modifié")
    # Save the template
    f.write(model_content.encode("utf-8"))
    f.close()
    zip.write(model_name)
    os.remove(model_name)

zip.close()

if reload_template:
    print("RELOAD des modèles")
    client.doget("/parapheur/modeles/reload")

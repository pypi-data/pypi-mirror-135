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

import os
import sys, traceback
import re
import time
import json
import pandas
from datetime import datetime, timedelta
from collections import Counter
from progress.bar import IncrementalBar
from lxml import etree
import ast
import parapheur  # Configuration
from parapheur.parapheur import config
from parapheur.parapheur import pprint  # Colored printer
from unidecode import unidecode

__config_section__ = "RecupArchives"

# Init REST API client
client = parapheur.getrestclient()

# Params
recup_folder = config.get(__config_section__, "folder")
# recup_folder = "/tmp/getdoc/"
page_size = config.get(__config_section__, "page_size")
# page_size = "500"

purge = config.get(__config_section__, "purge") == "true"
# purge = False
download = config.get(__config_section__, "download") == "true"
# download = True
metadata_xml = config.get(__config_section__, "metadata_xml") == "true"
type_filter = config.get(__config_section__, "type_filter")
# type_filter = "*"
subtype_filter = config.get(__config_section__, "subtype_filter")
# subtype_filter = "*"
waiting_days = int(config.get(__config_section__, "waiting_days"))
# waiting_days = 0

__special_section__ = "Special"
metas_list = None
if config.has_option(__special_section__, "metas_list"):
    metas_list = config.get(__special_section__, "metas_list")
    metas_list = metas_list.strip().split(',')
metas_tree = None
if config.has_option(__special_section__, "metas_tree"):
    metas_tree = config.get(__special_section__, "metas_tree")
    metas_tree = metas_tree.strip().split(',')
    if (len(metas_tree) == 1) & (metas_tree[0] == ""):
        metas_tree = ['PH_type', 'PH_soustype']
metas_default_values = None
if config.has_option(__special_section__, "metas_default_values"):
    metas_default_values = config.get(__special_section__, "metas_default_values")
    metas_default_values = metas_default_values.strip().split(',')
csv_daily_report = False
if config.has_option(__special_section__, "csv_daily_report"):
    csv_daily_report = config.get(__special_section__, "csv_daily_report") == "true"
csv_log_report = False
if config.has_option(__special_section__, "csv_log_report"):
    csv_log_report = config.get(__special_section__, "csv_log_report") == "true"

## On vérifie qu'il y a bien des métadonnées à traiter
if metas_list[0] == "":
    print("Aucune métadonnée définie dans iparapheur-utils.cfg \tVeuillez renseigner au moins une métadonnée et sa valeur par défaut")
    exit(0)
## On vérifie que metas_list et metas_default_values ont la même taille
if len(metas_list) != len(metas_default_values):
    print("metas_list et metas_default_values n'ont pas la même taille")
    exit(0)
path_list = []


# region Private methods
def parse_meta_tree(metas_tree):
    # split by coma
    metas_tree_path = []
    # trouver les caractères réservés
    for meta in metas_tree:
        meta = meta.replace(" ", "")
        if meta == "PH_type":
            metas_tree_path.append(meta)
        elif meta == "PH_soustype":
            metas_tree_path.append(meta)
        else:
            metas_tree_path.append("___REMPLACE___" + meta)
    return metas_tree_path


def parse_meta(metas_list, metas_default_values):
    list = []
    meta_list_data = metas_list
    if len(meta_list_data) != len(metas_default_values):
        print("Erreur : {0} metadonnées définies, {1} valeurs par défaut trouvées".format(len(meta_list_data),
                                                                                          len(metas_default_values)))
        print("Métadonnées = " + metas_list)
        print("Valeurs par défaut = " + metas_default_values)
        exit(0)
    i = 0
    for meta in meta_list_data:
        element = []
        meta = meta.replace(" ", "")
        element.append(meta)
        # element.append(metas_default_values[i].replace(" ", ""))
        element.append(metas_default_values[i])
        list.append(element)
        i += 1
    return list


def cleanup_special_chars(string):
    # Windows Forbidden punctuation
    cleaned = re.sub(u"<", "(", string)
    cleaned = re.sub(u">", ")", cleaned)
    cleaned = re.sub(u":", "=", cleaned)
    cleaned = re.sub(u"\"", "''", cleaned)
    cleaned = re.sub(u"[\\/\|]", "-", cleaned)
    cleaned = re.sub(u"\n", " ", cleaned)
    cleaned = re.sub(u"[\*\?%€&£$§#°]", "_", cleaned)

    # Special chars
    cleaned = re.sub(u'[ÀÁÂÄ]', 'A', cleaned)
    cleaned = re.sub(u'[ÈÉÊË]', 'E', cleaned)
    cleaned = re.sub(u'[ÍÌÎÏ]', 'I', cleaned)
    cleaned = re.sub(u'[ÒÓÔÖ]', 'O', cleaned)
    cleaned = re.sub(u'[ÙÚÛÜ]', 'U', cleaned)
    cleaned = re.sub(u'[áàâä]', 'a', cleaned)
    cleaned = re.sub(u'[éèêë]', 'e', cleaned)
    cleaned = re.sub(u'[íìîï]', 'i', cleaned)
    cleaned = re.sub(u'[óòôö]', 'o', cleaned)
    cleaned = re.sub(u'[úùûü]', 'u', cleaned)
    cleaned = re.sub(u'Æ', 'AE', cleaned)
    cleaned = re.sub(u'æ', 'ae', cleaned)
    cleaned = re.sub(u'Œ', 'OE', cleaned)
    cleaned = re.sub(u'œ', 'oe', cleaned)
    cleaned = re.sub(u'Ç', 'C', cleaned)
    cleaned = re.sub(u'ç', 'c', cleaned)

    # Fix for Lille Metropole and Ville Lille
    # cleaned = re.sub(r'[^\w\d\.\-_\(\)]', '_', cleaned)

    cleaned = cleaned.replace(u'\xb0', ".")
    cleaned = cleaned.replace(u'\xa0', ".")
    cleaned = cleaned.replace(u'\xa1', ".")
    cleaned = cleaned.replace(u'\xa8', ".")
    cleaned = cleaned.replace(u'\xab', ".")
    cleaned = cleaned.replace(u'\xa9', "c")
    cleaned = cleaned.replace(u'\xbb', ".")
    cleaned = cleaned.replace(u'\xb2', "2")
    cleaned = cleaned.replace(u'\xe7', "c")
    cleaned = cleaned.replace(u'\xe8', "e")
    cleaned = cleaned.replace(u'\xe9', "e")
    cleaned = cleaned.replace(u'\xea', "e")
    cleaned = cleaned.replace(u'\u2013', "-")
    cleaned = cleaned.replace(u'\u2018', "'")
    cleaned = cleaned.replace(u'\u2019', "'")
    cleaned = cleaned.replace(u'\u0009', " ")

    if len(cleaned) == 0:
        cleaned = "dossier_sans_nom"

    # Cas du fs ext4 - réduction du nombre de caractère à 200 (titre + id ~ 250)
    cleaned = cleaned[0:200]

    return cleaned


def get_full_folder_path_with_meta():
    full_path = recup_folder
    for meta in metas_tree:
        if meta.startswith("___REMPLACE___"):
            meta = meta.replace("___REMPLACE___", "")
            meta_replace = dossier["cu:" + meta]
            try:
                meta_replace = str(meta_replace)
                meta_replace = cleanup_special_chars(meta_replace)
            except:
                try:
                    meta_replace = unidecode(meta_replace, errors='ignore')
                except:
                    meta_replace = cleanup_special_chars(meta_replace.decode('utf-8'))
            meta = meta_replace.replace("/", "_")
        elif meta == "PH_type":
            meta = dossier["type"]
            meta = cleanup_special_chars(meta)
        elif meta == "PH_soustype":
            meta = dossier["sousType"]
            meta = cleanup_special_chars(meta)
        try:
            full_path = full_path + "/" + meta.encode("utf-8")
        except:
            full_path = full_path + "/" + meta.decode("utf-8")
    full_path = full_path + "/"
    full_path = full_path + title_clean.encode('utf-8').replace(".","_")
    full_path = full_path + '_'
    full_path = full_path + str(dossier['id'])
    if not os.path.exists(full_path):
        os.makedirs(full_path, 0755)
    return full_path


def move_incomplete_download_to_temp(path):
    temp_version = 1
    while os.path.exists("{0}_temp{1}".format(path, temp_version)):
        temp_version += 1
    os.rename("{0}".format(path), "{0}_temp{1}".format(path, temp_version))


def generate_xml_archive():
    archive = etree.Element("Archive")
    archive.attrib["id"] = dossier['title_id']
    type2 = etree.SubElement(archive, "Type")
    type2.attrib["id"] = dossier["type"]
    sousType = etree.SubElement(archive, "SousType")
    sousType.attrib["id"] = dossier["sousType"]
    title = etree.SubElement(archive, "Titre")
    title.attrib["valeur"] = dossier["title_clean"]
    originalName = etree.SubElement(archive, "originalName")
    originalName.attrib["nom"] = dossier["originalName"]
    MetaDonnees = etree.SubElement(archive, "MetaDonnees")
    # On boucle sur la liste des métadonnées définies "metas_list"
    i = 0
    for meta in liste_metas:
        meta = meta.replace(" ", "")
        MetaDonnee = etree.SubElement(MetaDonnees, "MetaDonnee")
        id_meta = "cu:" + str(meta)
        MetaDonnee.attrib["id"] = id_meta
        MetaDonnee.attrib["nom"] = str(meta)
        try:
            x = unidecode(dossier[id_meta])
        except:
            x = dossier[id_meta]
        MetaDonnee.attrib["valeur"] = str(x).decode('utf-8')
        i += 1
    circuit = etree.SubElement(archive, "circuit")
    etape = etree.SubElement(circuit, "etape")
    etape.attrib["horodatage"] = datetime.fromtimestamp(dossier["created"] / 1000).isoformat()
    etape.attrib["iParapheurStatus"] = u"Archivé"
    etape.attrib["nom"] = dossier["creator"]
    etree.SubElement(etape, "annotation").text = u"Dossier archivé"
    f = open(download_folder_path + "/iParapheur_proprietes.xml", "w")
    f.write(etree.tostring(archive, encoding='UTF-8', xml_declaration=True, pretty_print=True))
    f.close()


def get_csv_report(dossier):
    full_path = recup_folder + "/PH_report"
    if not os.path.exists(full_path):
        os.makedirs(full_path, 0755)
    full_path = full_path + "/report_archives.csv"
    dossier_dump = "[" + json.dumps(dossier) + "]"
    jsonData = json.loads(dossier_dump)
    df = pandas.DataFrame(jsonData, index=None)
    columns = []
    for meta in metas_tree:
        if meta == "PH_type":
            meta = "type"
            columns.append(meta)
        elif meta == "PH_soustype":
            meta = "sousType"
            columns.append(meta)
        elif meta.startswith("___REMPLACE___"):
            meta = meta.replace("___REMPLACE___", "cu:")
            columns.append(meta)
        else:
            columns.append(meta)
    columns.append("title_id")
    columns.append("title")
    columns.append("creator")
    columns.append("created_clean")
    for meta in metas_list:
        meta = "cu:" + meta
        columns.append(meta)
    columns.append("originalName")
    df.to_csv(full_path, header=False, mode="a",
              columns=columns, encoding='utf-8',
              index=False)


def get_daily_txt_report(path_list, len_metas_tree):
    full_path = recup_folder + "/PH_report/daily"
    if not os.path.exists(full_path):
        os.makedirs(full_path, 0755)
    list_path_to_exploit = []
    for path in path_list:
        path = path.replace(recup_folder, "")
        path_data = path.strip().split('/')
        i = 1
        path_to_exploit = path_data[1]
        while i < len_metas_tree:
            path_to_exploit = path_to_exploit + "," + path_data[i + 1]
            i += 1
        list_path_to_exploit.append(path_to_exploit)
    # On récupère la liste des path nettoyés rangés alphabétiquement
    list_path_to_exploit.sort()
    count = Counter(list_path_to_exploit)
    x = datetime.now()
    f = open(full_path + "/ph-recupfull-" + x.strftime("%Y%m%d_%H%M%S") + ".csv", "a")
    meta_tree_list = []
    for meta in metas_tree:
        if meta == "PH_type":
            meta = "type"
            meta_tree_list.append(meta)
        elif meta == "PH_soustype":
            meta = "soustype"
            meta_tree_list.append(meta)
        elif meta.startswith("___REMPLACE___"):
            meta = meta.replace("___REMPLACE___", "")
            meta_tree_list.append(meta)
        else:
            meta_tree_list.append(meta)
    meta_tree_list_text = ""
    for meta in meta_tree_list:
        meta_tree_list_text = meta_tree_list_text + "," + meta
    meta_tree_list_text = meta_tree_list_text[1:]
    f.write(str(meta_tree_list_text) + ",TOTAL\n")
    for path, countt in count.most_common():
        f.write('%s,%d\n' % (path, countt))
    f.close()


type_filter = type_filter.replace(" ", "%20")
subtype_filter = subtype_filter.replace(" ", "%20")
download_folder_path = None

liste_metas = metas_list
if len(liste_metas) > 0:
    str_meta = '{"metas":['
    for i in range(len(liste_metas)):
        str_meta = str_meta + '"cu:' + liste_metas[i] + '"'
        if i < (len(liste_metas) - 1):
            str_meta = str_meta + ','
    str_meta = str_meta + ']}'
str_meta = str_meta.replace(" ", "")

metas_tree = parse_meta_tree(metas_tree)
list_meta = parse_meta(metas_list, metas_default_values)

if client.islogged:

    # Fetch folders

    # Get maxdate for filtering. -1 because we don't count today as a day !
    newdate = datetime.today() - timedelta(days=waiting_days - 1)
    datefilterstr = "%s-%s-%s" % (newdate.year, '%02d' % newdate.month, '%02d' % newdate.day)

    page = 0
    dossiers_archive = []
    # skipy = int(page_size)
    dossiers_fetched = [1]
    skipped = "0"

    while len(dossiers_fetched) > 0:

        dossiers_fetched = client.doget("/parapheur/archives",
                                        dict(
                                            # asc="false",
                                            page=str(page),
                                            filter='{"and":[{"or":[{"ph:typeMetier":"%s"}]},{"or":[{"ph:soustypeMetier":"%s"}]}]}' % (
                                                type_filter, subtype_filter),
                                            metas=str_meta,
                                            pageSize=page_size,
                                            skipped=skipped
                                        )
                                        )

        if dossiers_fetched is not False:
            dossiers_archive += dossiers_fetched
            pprint.log("Page {0} : {1} dossiers".format(page, len(dossiers_fetched)))
            if len(dossiers_fetched) > 0:
                skipped = str(dossiers_fetched[0]["skipped"])
        else:
            pprint.error("Page {0} : Erreur de récupération".format(page))
            dossiers_fetched = [1]

            # STV DBG
            sys.exit(1)

        page += 1

    pprint.log("{0} dossier(s) trouvé(s)".format(len(dossiers_archive)))

    if waiting_days > 0:
        timestamp = (int(time.time()) - 60 * 60 * 24 * waiting_days) * 1000
        dossiers_archive = [d for d in dossiers_archive if d['created'] < timestamp]
        pprint.log("{0} dossier(s) apres le delai de carence".format(len(dossiers_archive)))

    bar = IncrementalBar('Recuperation des archives', max=len(dossiers_archive), suffix='%(index)d/%(max)d - %(eta)ds')

    # Download
    import itertools

    for dossier_index in range(0, len(dossiers_archive)):

        try:
            dossier = dossiers_archive[dossier_index]
            ## On ajout le titre_id et on remplace les métadonnées avec les valeurs par défaut si besoin
            dossier['title_id'] = cleanup_special_chars(dossier['title']) + "_" + dossier['id']
            dossier['title_clean'] = cleanup_special_chars(dossier['title'])
            dossier['created_clean'] = datetime.fromtimestamp(dossier["created"] / 1000).isoformat()
            for meta, meta_default in itertools.izip(metas_list, metas_default_values):
                meta_value = dossier["cu:" + meta]
                if meta_value is None or (meta_value == ""):
                    if meta_default is None:
                        meta_default = ""
                    dossier["cu:" + meta] = meta_default
                meta_value = dossier["cu:" + meta]
                try:
                    dossier["cu:" + meta] = meta_value.replace('&', '_')
                except:
                    dossier["cu:" + meta] = meta_value
            # for meta in metas_list:
            # print(type(dossier["cu:" + meta]))
            # dossier["cu:" + meta] = cleanup_special_chars(dossier["cu:" + meta])
            title_clean = cleanup_special_chars(dossier['title'])
            type_clean = cleanup_special_chars(dossier['type'])
            subtype_clean = cleanup_special_chars(dossier['sousType'])

            if download:
                # Create folders
                # On récupère la liste des subdir
                download_folder_path = get_full_folder_path_with_meta()
                try:
                    download_folder_path = str(download_folder_path)
                except:
                    print(download_folder_path)
                download_folder_path = download_folder_path.encode('utf-8')
                is_already_downloaded = os.path.exists("{0}/.done".format(download_folder_path))

                folder_already_contains_data = len(os.listdir(download_folder_path)) > 0

                if folder_already_contains_data and not is_already_downloaded:
                    move_incomplete_download_to_temp(download_folder_path)
                    download_folder_path = get_full_folder_path(type_clean, subtype_clean, title_clean,
                                                                dossier['id'])

                # Download content

                if not is_already_downloaded:

                    content_url = "/api/node/content/workspace/SpacesStore/{0}/{1}".format(dossier['id'], title_clean)
                    content_url = content_url.replace(" ", "%20")
                    client.dodownload(content_url, "{0}/{1}".format(download_folder_path, title_clean))
                    multidoc = False
                    if dossier['original'] == "true":

                        if dossier['isXemEnabled']:
                            dossier_distant_original_name = title_clean
                            dossier_local_original_name = "{0}_original.xml".format(title_clean)
                        elif dossier['originalName'] is not None:
                            dossier_distant_original_name = cleanup_special_chars(dossier['originalName'])
                            ## Le cas d'un multidoc
                            if dossier_distant_original_name.endswith(".zip"):
                                multidoc = True
                                dossier_distant_original_name = dossier_distant_original_name.replace(".",
                                                                                                      "_")
                                dossier_distant_original_name = dossier_distant_original_name.replace("_zip",
                                                                                                      ".zip")
                            dossier_local_original_name = "original_" + dossier_distant_original_name
                        else:
                            dossier_distant_original_name = title_clean
                            dossier_local_original_name = "original_" + title_clean

                        original_url = "/api/node/content%3bph%3aoriginal/workspace/SpacesStore/{0}/{1}".format(
                            dossier['id'], dossier_distant_original_name)
                        original_url = original_url.replace(" ", "%20")
                        client.dodownload(original_url,
                                          "{0}/{1}".format(download_folder_path, dossier_local_original_name))

                    if dossier['sig'] == "true":
                        sign_url = "/api/node/content%3bph%3asig/workspace/SpacesStore/{0}/{1}_sig.zip".format(
                            dossier['id'], title_clean)
                        sign_url = sign_url.replace(" ", "%20")
                        client.dodownload(sign_url, "{0}/{1}_sig.zip".format(download_folder_path, title_clean))

                    ## Cas multidoc: on dezip
                    # if multidoc:
                    #     download_folder_path2 = download_folder_path.replace(" ", "\ ")
                    #     os.system("cd " + download_folder_path2 + "; mkdir multidoc")
                    #     multidoc_path = download_folder_path2 + "/multidoc"
                    #     os.system("unzip -q " + download_folder_path2 + "/" + dossier_local_original_name.replace(" ",
                    #                                                                                               "\ ") + " -d " + multidoc_path)
                    os.mknod("{0}/.done".format(download_folder_path))

            if purge:
                if download:
                    if os.path.exists("{0}/.done".format(download_folder_path)) or use_only_print_pdfs:
                        client.executescript("removeNode.js", format=(dossier['id'],))
                else:
                    client.executescript("removeNode.js", format=(dossier['id'],))
                    #  pprint.success("Deleted : {0} ({1}/{2})".format(dossier['id'], dossier_index + 1, len(dossiers_archive)))

            bar.next()
            if metadata_xml:
                generate_xml_archive()
            if csv_log_report:
                get_csv_report(dossier)
            path_list.append(download_folder_path)

        except TypeError as exception:
            # STV
            print("STV DBG   Unexpected error: %s" % (exception))
            traceback.print_exc()
            exit(1)
        except:
            pprint.log("Erreur de récupération d'une archive")
            # STV
            # print("DBG   Unexpected error: %s" % (exception))
            traceback.print_exc()
            if csv_daily_report:
                get_daily_txt_report(path_list, len(metas_tree))
            exit(1)
    bar.finish()
    if csv_daily_report:
        get_daily_txt_report(path_list, len(metas_tree))
pprint.success("Done", True)

# -*-coding:Latin-1 -*
import requests
import sys
import os
from requests.auth import HTTPDigestAuth
import json
import datetime

#choisir ici les versions à récolter
versionA = "49.0"
versionB = "49.0.1"

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&version=' + versionA + '&version=' + versionB + '&_facets=signature'
data = ''
try:
    response = requests.get(url, data=data)
except requests.exceptions.RequestException as e:
    print e
    sys.exit(1)
parsed = json.loads(response.content)
facets = parsed['facets']
signatures = facets['signature']
terms = []

directoryVersion = str(versionA + '-' + versionB)
if not os.path.exists(directoryVersion):
    os.makedirs(directoryVersion)

queryRange = "date -7 days"
now = datetime.datetime.now()
queryDate = str(now)
queryUrl = url
versions = []
versions.append(versionA)
versions.append(versionB)
buckets = {}


#récupération des différentes types de signature
#création d'un dossier pour chaque signature
for signature in signatures:
    terms.append(signature['term'])
    directory = directoryVersion + "/" + str(terms.index(signature['term']))
    buckets[terms.index(signature['term'])]= signature['term']
    if not os.path.exists(directory):
        os.makedirs(directory)
print("nombre de dossiers : " + str(len(terms)))

metadata = {}
metadata["queryDate"] = queryDate
metadata["queryRange"]= queryRange
metadata["queryUrl"]= queryUrl
metadata["versions"]= versions
metadata["buckets"]= buckets
with open(directoryVersion + "/metadata.json", 'wb') as outfile:
    json.dump(metadata, outfile)

#pour chaque signature, on garde les id des crash reports à l'intérieur
for term in terms:
    print("Traitement du dossier : " + str(terms.index(term)))

    #term = 'OOM | large | NS_ABORT_OOM | nsACString_internal::Replace'
    offset = 0
    uuids = []
    rester = True

    while rester:
        url = 'https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&version=' + versionA + '&version=' + versionB + '&signature==' + term + "&_columns=uuid&_results_offset=" + str(offset) + "&_results_number=1000"
        try:
            response = requests.get(url, data=data)
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)
        parsed = json.loads(response.content)
        #print(parsed)
        if parsed['total'] > (offset + 1000):
            offset = offset + 1000
        else:
            rester = False
        for hit in parsed['hits']:
            uuids.append(hit['uuid'])


    #print(uuids)
    tailleServ = len(uuids)
    DIR = directoryVersion + "/" + str(terms.index(term))
    tailleLocal = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

    if(tailleLocal >= tailleServ):
        print("Dossier " + str(terms.index(term)) + " déja importé.")
        continue
    if(tailleLocal > 0):
        print("Dossier " + str(terms.index(term)) + " partiellement importé.")
    print("Réécriture du dossier " + str(terms.index(term)))

    compteur = 0
    #récupération du rapport de crash
    #création d'un fichier contenant le rapport de crash
    for uuid in uuids:
        if(tailleLocal - 5 > compteur):
            print("fichier déjà écrit, numéro : " + str(compteur) + " " + uuid)
            compteur = compteur + 1
            continue;
        compteur = compteur + 1
        print("fichier numéro : " + str(compteur) + " " + uuid)
        url = "https://crash-stats.mozilla.com/api/ProcessedCrash/?crash_id=" + uuid
        try:
            response = requests.get(url, data=data)
        except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)
        parsed = json.loads(response.content)
        if not os.path.exists(directoryVersion + "/" + str(terms.index(term)) + "/"+ uuid):
            print("écriture ... : ")
            with open(directoryVersion + "/" + str(terms.index(term)) + "/"+ uuid, 'w') as outfile:
                json.dump(parsed, outfile)

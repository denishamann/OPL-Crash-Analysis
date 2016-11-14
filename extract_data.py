# -*-coding:Latin-1 -*
import requests
import sys
import os
from requests.auth import HTTPDigestAuth
import json

#choisir ici les versions à récolter
versionA = "49.0"
versionB = "49.0.1"

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&version=' + versionA + "&version=" + versionB + '&_facets=signature'
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

#récupération des différentes types de signature
#création d'un dossier pour chaque signature
for signature in signatures:
    terms.append(signature['term'])
    directory = signature['term']
    if not os.path.exists(directory):
		os.makedirs(directory)
#print(terms)
print("nombre de dossiers : " + str(len(terms)))

cpt = 1;
#pour chaque signature, on garde les id des crash reports à l'intérieur
for term in terms:
	print("Traitement du dossier : " + str(cpt))
	cpt = cpt + 1

	#term = 'OOM | large | NS_ABORT_OOM | nsACString_internal::Replace'
	offset = 0
	uuids = []
	rester = True

	while rester:
		url = "https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&version=49.0&version=49.0.1&signature==" + term + "&_columns=uuid&_results_offset=" + str(offset) + "&_results_number=1000"
		try:
			response = requests.get(url, data=data)
		except requests.exceptions.RequestException as e:
			print e
			sys.exit(1)
		print(response)
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
	DIR = term
	tailleLocal = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])

	if(tailleLocal >= tailleServ):
		print("Dossier " + term + " déja importé.")
		continue
	if(tailleLocal > 0):
		print("Dossier " + term + " partiellement importé.")
	print("écriture dans le dossier " + term)

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
		if not os.path.exists(term + "/"+ uuid):
			print("écriture ... : " + str(compteur) + " " + uuid)
			with open(term + "/"+ uuid, 'w') as outfile:
				json.dump(parsed, outfile)

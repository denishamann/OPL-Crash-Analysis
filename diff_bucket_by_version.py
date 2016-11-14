import requests
from requests.auth import HTTPDigestAuth
from collections import defaultdict
import json
import sys
"""all the versions to compare should be ordered"""
versions = ["45.0","45.0.1","45.0.2","45.1.1","45.2.0","45.3.0","45.4.0","46.0","46.0.1","47.0","47.0.1","48.0","48.0.1","49.0","49.0.1"]
versions_signatures = defaultdict(list)
url = 'https://crash-stats.mozilla.com/api/SuperSearch/?product=Firefox&_facets=signature'

""" should absolutly end with a '/' """
destination_directory = '/home/m2iagl/bacquet/Documents/tmp/Firefox_buckets_comparison/'

data = ''




def extractSignatures(version):
    # print(response.json())
    allRequests = []
    offset = 0
    rester = True
    while rester:
        current_url = url + "&version=" + version+"&_results_offset=" + str(
            offset) + "&_results_number=1000"
        try:
            response = requests.get(current_url, data=data)
        except requests.exceptions.RequestException as e:
            print (e)
            sys.exit(1)
        print(response)
        parsed = json.loads(response.text)
        # print(parsed)
        allRequests.append(parsed)

        if parsed['total'] > (offset + 1000):
            offset = offset + 1000
        else:
            rester = False
    terms = []
    for parsed in allRequests :
        facets = parsed['facets']
        signatures = facets['signature']
        for signature in signatures:
            terms.append(signature['term'])
    return terms


def determineChanges(signatures1, signatures2):
    result = defaultdict(list)
    for signature in signatures1:
        if signature not in signatures2 and signature not in result['corrected']:
            result['corrected'].append(signature)
    for signature in signatures2:
        if signature not in signatures1 and signature not in result['introduced'] and signature not in result['corrected']:
            result['introduced'].append(signature)
        elif signature not in result['remaining'] and signature not in result['introduced'] and signature not in result['corrected']:
            result['remaining'].append(signature)
        else :
            result['doubles'].append(signature)
    return result

def generate_report(analyse_result):
    report_file = open(destination_directory+analyse_result['version1']+'_'+analyse_result['version2']+'_buckets_presence_comparison','w')
    report_file.write("versions : " + analyse_result['version1'] + " & " + analyse_result['version2'] + "\n\n")
    report_file.write("quantity of buckets corrected between the two versions : "+ str(len(analyse_result['corrected'])) + "\n")
    report_file.write("quantity of buckets introduced between the two versions : "+ str(len(analyse_result['introduced'])) + "\n")
    report_file.write("quantity of buckets remaining between the two versions: "+ str(len(analyse_result['remaining']))+ "\n\n\n")

    report_file.write("buckets corrected : \n")
    for signature in analyse_result['corrected'] :
        report_file.write("\t-"+signature+"\n")

    report_file.write("\n\nbuckets introduced: \n")
    for signature in analyse_result['introduced'] :
        report_file.write("\t-"+signature+"\n")

    report_file.write("\n\nbuckets remaining: \n")
    for signature in analyse_result['remaining'] :
        report_file.write("\t-"+signature+"\n")

    report_file.write("\n\nbuckets removed because they are considered as doubles: \n")
    for signature in analyse_result['doubles'] :
        report_file.write("\t-"+signature+"\n")
    report_file.close()

def extract_all_versions_signatures() :

    for version in versions :
        print version
        versions_signatures[version] = extractSignatures(version)

def diff_between_two_versions( version1 , version2):

    signatures1 = versions_signatures[version1]
    signatures2 = versions_signatures[version2]

    analyse_result = determineChanges(signatures1, signatures2)
    analyse_result['version1'] = version1
    analyse_result['version2'] = version2

    return analyse_result

def generate_html_array(versions_comparison_stats):
    i = 0
    html_file = open(destination_directory+'bucket_presence_stats_between_versions.html','w')
    html_file.write('<html><title>bucket presence stats between versions</title><head><style>table{border: 3px solid black;}th,td{border: 1px solid black;}</style></head><body><table >')
    html_file.write('<th> &nbsp; &nbsp; &nbsp; &nbsp;</th>');
    for version in versions :
        html_file.write('<th>'+version+'</th>')
    for version1 in versions:
        html_file.write('<tr><td>'+version1+'</td>')
        for version2 in versions:
            if version1 < version2:
                html_file.write('<td>'+str(versions_comparison_stats[i]['corrected'])+'|'+str(versions_comparison_stats[i]['introduced'])+'|'+str(versions_comparison_stats[i]['remaining'])+'</td>')
                i += 1
            else:
                html_file.write('<td> &nbsp; &nbsp; &nbsp; &nbsp;</td>')
    html_file.write('</tr>');

    html_file.write('</table></body></html>')
    html_file.close()

extract_all_versions_signatures()
versions_comparison_stats = []
for version1 in versions :
    for version2 in versions :
        if version1 < version2 :
            analyse_result = diff_between_two_versions(version1,version2)
            nb_corrected = len(analyse_result['corrected'])
            nb_introduced =len(analyse_result['introduced'])
            nb_remaining =len(analyse_result['remaining'])
            versions_comparison_stats.append({'version1':version1,'version2':version2,'corrected':nb_corrected,'introduced':nb_introduced,'remaining':nb_remaining})
            print (versions_comparison_stats)
            generate_report(analyse_result)
generate_html_array(versions_comparison_stats)
# print (len(extractSignatures("49.0")))
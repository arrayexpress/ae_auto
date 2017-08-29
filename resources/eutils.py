import json
import requests
import time

__author__ = 'Ahmed G. Ali'

BASE_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'


def esearch(db, term, history=False):
    url = BASE_URL + 'esearch.fcgi'
    data = {'db': db, 'term': term, 'retmode': 'json'}
    if history:
        data['usehistory'] = 'y'
    r = requests.get(url, params=data)
    if 'Error 503' in r.text:
        print 'eutils gave Error 503. Waiting 20 secs then trying again'
        time.sleep(20)
        return esearch(db, term)
    return json.loads(r.text)


def efetch(db, ids):
    url = BASE_URL + 'efetch.fcgi'
    data = {'db': db, 'id': ','.join(ids)}
    r = requests.get(url, params=data)
    if 'Error 503' in r.text:
        print 'eutils gave Error 503. Waiting 20 secs then trying again'
        time.sleep(20)

    return json.loads(r.text)


def esummary(db, query_id, web_env, ret_start=0, ret_max=500):
    url = BASE_URL + 'esummary.fcgi'
    data = {'db': db, 'query_key': query_id, 'WebEnv': web_env, 'retmode': 'json', 'retstart': ret_start,
            'retmax': ret_max}
    r = requests.get(url, params=data)
    if 'Error 503' in r.text:
        print 'eutils gave Error 503. Waiting 20 secs then trying again'
        time.sleep(20)
        return esummary(db, query_id, web_env, ret_start, ret_max)
    return json.loads(r.text)


if __name__ == '__main__':
    a = esearch(db='gds', term='GPL[ETYP]', history=True)
    print a
    print esummary(
        db='gds',
        query_id=a['esearchresult']['querykey'],
        web_env=a['esearchresult']['webenv']
    )

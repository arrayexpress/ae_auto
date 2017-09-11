import json
import requests
import time

from settings import PMC_BASE_URL

__author__ = 'Ahmed G. Ali'


def search(query,  page=1, result_format='JSON', iteration=0):
    """
    Send get request to Europe PMC rest API ``http://www.ebi.ac.uk/europepmc/webservices/rest/`` using the
    ``search`` endpoint with given parameters.

    :param query: Query send to rest API.
    :type query: str
    :param page: Page number of the results.
    :type page: int
    :param result_format: results return format. Default: 'JSON'
    :type result_format: str
    :param iteration: Number indicating how many times the same request was called. Terminating the execution
        after 10 times with 30 sec sleep between each attempt.
    :type iteration: int
    :return: List of JSON objects as returned from Europe PMC.
    :rtype: :obj:`list` of :obj:`dict`
    """
    _articles = []
    if iteration == 10:
        return _articles
    url = PMC_BASE_URL + 'search/query=' + query + '&format=' + result_format + '&page=' + str(
        page) + '&sort_date:y&resulttype=core'
    # print url
    # exit
    r = requests.get(url)
    res = json.loads(r.text)
    if "errCode" in res.keys() and res["errCode"] == 404:
        time.sleep(30)
        iteration+=1
        return search(query,  page=1, result_format='JSON', iteration=iteration)

    if not 'resultList' in res.keys():
        time.sleep(30)
        iteration += 1
        return search(query, page=1, result_format='JSON', iteration=iteration)
    articles_json = res['resultList']['result']

    # total_count = json.loads(r.text)['hitCount']
    # print '%d: %d articles collected out of total: %d' % (iteration, len(initial_articles), total_count)
    if not articles_json:
        return _articles
    _articles += [article for article in articles_json if
                  article['hasTMAccessionNumbers'] == 'Y' and article['hasTextMinedTerms'] == 'Y']
    return _articles
#
# def search(query, initial_articles, page=1, result_format='JSON', iteration=0):
#     while True:
#         url = PMC_BASE_URL + 'search/query=' + query + '&format=' + result_format + '&page=' + str(
#             page) + '&sort_date:y&resulttype=core'
#         # print url
#         # exit
#         r = requests.get(url)
#         res = json.loads(r.text)
#         if "errCode" in res.keys() and res["errCode"] == 404:
#             time.sleep(30)
#             continue
#
#         if not 'resultList' in res.keys():
#             time.sleep(30)
#             continue
#         articles_json = res['resultList']['result']
#
#         total_count = json.loads(r.text)['hitCount']
#         # print '%d: %d articles collected out of total: %d' % (iteration, len(initial_articles), total_count)
#         if not articles_json:
#             break
#         if iteration == 20000:
#             break
#         initial_articles += [article for article in articles_json if
#                              article['hasTMAccessionNumbers'] == 'Y' and article['hasTextMinedTerms'] == 'Y']
#         page += 1
#
#         iteration += 1
#         break
#     return initial_articles


def search_textmined(articles):
    """
    Send get request to Europe PMC rest API ``http://www.ebi.ac.uk/europepmc/webservices/rest/`` using the
    ``PMC/*PMC_ID*/textMinedTerms/ACCESSION/1/json`` endpoint with given parameters.

    :param articles: List of articles as collected from Europe PMC
    :type articles: :obj:`list` of :obj:`dict`

    :return: List of articles having one or more ArrayExpress Accession in their text-mined terms.
    :rtype: :obj:`list` of :obj:`dict`
    """
    url = PMC_BASE_URL + 'PMC/%s/textMinedTerms/ACCESSION/1/json'
    return_articles = []
    for article in articles:
        # print url % article['pmcid']
        res = requests.get(url % article['pmcid'])
        try:
            res = json.loads(res.text)
        except:

            # print
            # print res
            # print res.text
            raise Exception(url % article['pmcid'])

        article['accessions'] = []
        if 'semanticTypeList' in res.keys() and 'semanticType' in res['semanticTypeList'].keys():
            for acc in res['semanticTypeList']['semanticType']:
                if acc['tmSummary']:
                    for t in acc['tmSummary']:
                        if t['dbName'] == 'arrayexpress':
                            article['accessions'].append(t['term'])
        return_articles.append(article)
    return return_articles


if __name__ == '__main__':
    a = search('arrayexpress')
    print a
# from mock import Mock
#     search=Mock(return_value="mocked stuff")
#     r= search('arrayExpress')
#     print r

import json as json_lib
import random

__author__ = 'Ahmed G. Ali'


def generate_articles(count=0, with_accession_count=0):
    articles = []
    has_accessions = u'Y'
    for i in range(count):
        if with_accession_count <= 0:
            has_accessions = u'N'
        author_count = random.randint(1, 9)
        authors = []
        article_id = random.randint(1111, 99999)
        for j in range(author_count):
            authors.append(u'Author%d' % (j + 1))
        articles.append(
            {
                u'pubYear': u'2015',
                u'authorString': ', '.join(authors),
                u'journalIssn': u'%d-%d' % (random.randint(1111, 9999), random.randint(1111, 9999)),
                u'pubType': u"Some type %d" % i,
                u'id': u'%d' % article_id,
                u'inEPMC': u'Y',
                u'journalVolume': u'%d' % random.randint(100, 1000),
                u'title': u'Some title with ArrayExpress %d ' % (i + 1),
                u'citedByCount': random.randint(0, 100),
                u'source': u'MED',
                u'pmid': u'%d' % article_id,
                u'hasLabsLinks': u'N',
                u'issue': u'database issue',
                u'hasTextMinedTerms': u'Y',
                u'luceneScore': u'578.4927',
                u'inPMC': u'N',
                u'hasTMAccessionNumbers': has_accessions,
                u'hasReferences': u'Y',
                u'isOpenAccess': u'Y',
                u'pageInfo': u'd1113-6',
                u'pmcid': u'PMC%d' % random.randint(111111, 9999999),
                u'hasDbCrossReferences': u'N',
                u'doi': u'10.1093/nar/gku1057',
                u'journalTitle': u'Journal Title %d' % i
            }
        )
        with_accession_count -= 1
    return articles


def generate_textmined_response(accession_num=1):
    accessions = []
    for i in range(accession_num+1):
        term = u"E-MTAB-%d" % random.randint(1111, 99999)
        accessions.append(
            {
                u"term": term,
                u"count": 1,
                u"altNameList": {u"altName": []},
                u"dbName": u"arrayexpress",
                u"dbIdList": {u"dbId": [term]}
            }
        )
    return {
        u"version": u"4.1",
        u"hitCount": 27,
        u"request": {
            u"id": u"PMC_id",
            u"source": u"PMC",
            u"email": u"",
            u"page": 1
        },
        u"semanticTypeCountList": {
            u"semanticType": [{u"name": u"accession", u"count": accession_num}]
        },
        u"semanticTypeList": {
            u"semanticType": [
                {
                    u"name": u"accession",
                    u"total": accession_num,
                    u"tmSummary": accessions
                },
            ]
        }
    }


class MockResponse(object):
    def __init__(self, res_dict={}):
        self.json = res_dict
        self.text = json_lib.dumps(res_dict)


class RequestSideEffect(object):
    def __init__(self, conditions={}):
        self.conditions = conditions

    def my_side_effect(self, *args):
        for k, v in self.conditions.items():
            if k in args[0]:
                return v
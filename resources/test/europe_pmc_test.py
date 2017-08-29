import copy
import random
import unittest

import mock

from resources import europe_pmc
from test_resources.common import generate_articles, generate_textmined_response, MockResponse, RequestSideEffect

__author__ = 'Ahmed G. Ali'


class EuropePMCTest(unittest.TestCase):
    def setUp(self):
        self.query = 'arrayexpress'
        self.response_dict = {
            "version": "4.1",
            "hitCount": 0,
            "request": {"resultType": "LITE",
                        "synonym": False,
                        "query": self.query,
                        "page": 1
                        },
            "resultList": {"result": []}
        }

    def test_return_empty_list(self):
        side_effects = {
            'page=1': MockResponse(copy.deepcopy(self.response_dict))
        }
        europe_pmc.requests.get = mock.Mock(side_effect=RequestSideEffect(side_effects).my_side_effect)
        res = europe_pmc.search(query=self.query)
        self.assertEqual(res, [])
        articles = europe_pmc.search_textmined(res)
        self.assertEqual(articles, [])

    def test_a_articles_without_accessions(self):
        articles = generate_articles(count=100, with_accession_count=0)
        expected_dict = copy.deepcopy(self.response_dict)
        expected_dict['hitCount'] = len(articles)
        expected_dict["resultList"]["result"] = articles
        empty_dict = copy.deepcopy(self.response_dict)
        empty_dict['request']['page'] = 2
        side_effects = {
            'page=1': MockResponse(expected_dict),
            'page=2': MockResponse(empty_dict)
        }
        europe_pmc.requests.get = mock.Mock(side_effect=RequestSideEffect(side_effects).my_side_effect)
        res = europe_pmc.search(query=self.query)
        self.assertEqual(res, [])
        articles = europe_pmc.search_textmined(res)
        self.assertEqual(articles, [])

    def test_articles_with_accessions(self):
        articles = generate_articles(count=100, with_accession_count=50)
        expected_dict = copy.deepcopy(self.response_dict)
        expected_dict['hitCount'] = len(articles)
        expected_dict["resultList"]["result"] = articles

        empty_dict = copy.deepcopy(self.response_dict)
        empty_dict['request']['page'] = 2
        side_effects = {
            'page=1': MockResponse(expected_dict),
            'page=2': MockResponse(empty_dict),
            'textMinedTerms': MockResponse(generate_textmined_response(accession_num=random.randint(1, 9)))
        }
        europe_pmc.requests.get = mock.Mock(side_effect=RequestSideEffect(side_effects).my_side_effect)
        res = europe_pmc.search(query=self.query)
        self.assertEqual(len(res), 50)
        annotated_articles = europe_pmc.search_textmined(res)
        self.assertEqual(len(annotated_articles), 50)
        for article in annotated_articles:
            self.assertIn('accessions', article.keys())
            self.assertGreaterEqual(len(article['accessions']), 0)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()

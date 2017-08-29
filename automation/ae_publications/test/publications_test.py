import copy
import random
import unittest
import datetime

import mock

from automation.ae_publications import publications_experiments as publications
# from dal.oracle.ae2 import view_publications, ae2_transaction, study, study_publication
from resources import europe_pmc
from test_resources.common import MockResponse, RequestSideEffect, generate_articles, generate_textmined_response

__author__ = 'Ahmed G. Ali'


class PublicationTest(unittest.TestCase):
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

    def test_no_publications_collected(self):
        side_effects = {
            'page=1': MockResponse(copy.deepcopy(self.response_dict))
        }
        europe_pmc.requests.get = mock.Mock(side_effect=RequestSideEffect(side_effects).my_side_effect)
        publications.main(self.query)
        publications.retrieve_permission_for_accession = mock.Mock()
        self.assertFalse(publications.retrieve_permission_for_accession.called)

    def test_no_publications_found_for_accession_for_existing_publication(self):
        articles = generate_articles(count=1, with_accession_count=1)
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
        publications.retrieve_permission_for_accession = \
            mock.Mock(return_value=[
                dict(releasedate=datetime.datetime.now(), sc_user_id=1)
            ])
        publications.retrieve_existing_publications_by_accession = \
            mock.Mock(return_value=[])
        publications.retrieve_pub_id_by_doi = \
            mock.Mock(return_value=[articles[0]['pmid']])
        publications.retrieve_study_id_by_acc = \
            mock.Mock(return_value=[{'id': 12345}])
        publications.insert_study_publication = mock.Mock()
        experiment = type('', (object,), {"description": "Description", 'title': 'Title'})()

        publications.retrieve_study_by_acc = mock.Mock(return_value=[experiment])
        publications.main(self.query)
        for article in articles:
            # for acc in article['accessions']:
            self.assertTrue(publications.retrieve_permission_for_accession.called)
            self.assertTrue(publications.retrieve_existing_publications_by_accession.called)
            self.assertTrue(publications.retrieve_pub_id_by_doi.called)
            publications.retrieve_pub_id_by_doi.assert_called_with(article['doi'])
            self.assertTrue(publications.retrieve_study_id_by_acc.called)
            self.assertTrue(publications.insert_study_publication.called)
            publications.insert_study_publication.assert_called_with(12345, articles[0]['pmid'])

    def test_no_publications_found_for_accession_for_non_existing_publication(self):
        articles = generate_articles(count=1, with_accession_count=1)
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
        publications.retrieve_permission_for_accession = \
            mock.Mock(return_value=[
                dict(releasedate=datetime.datetime.now(), sc_user_id=1)
            ])
        publications.retrieve_existing_publications_by_accession = \
            mock.Mock(return_value=[])
        publications.retrieve_pub_id_by_doi = \
            mock.Mock(return_value=[])

        publications.insert_publication_view = mock.Mock()
        experiment =  type('',(object,),{"description": "Description", 'title': 'Title'})()

        publications.retrieve_study_by_acc = mock.Mock(return_value=[experiment])
        publications.main(self.query)
        for article in articles:
            # for acc in article['accessions']:
            self.assertTrue(publications.retrieve_permission_for_accession.called)
            self.assertTrue(publications.retrieve_existing_publications_by_accession.called)
            self.assertTrue(publications.retrieve_pub_id_by_doi.called)
            publications.retrieve_pub_id_by_doi.assert_called_with(article['doi'])
            self.assertFalse(publications.retrieve_study_id_by_acc.called)
            self.assertFalse(publications.insert_study_publication.called)
            self.assertTrue(publications.insert_publication_view.called)

    def tearDown(self):
        mocks = [
            publications.retrieve_permission_for_accession,
            publications.retrieve_existing_publications_by_accession,
            # publications.retrieve_pub_id_by_doi,
            publications.retrieve_study_id_by_acc,
            publications.insert_study_publication,
            # publications.insert_publication_view
        ]
        for m in mocks:
            try:
                m.reset_mock()
            except Exception, e:
                pass

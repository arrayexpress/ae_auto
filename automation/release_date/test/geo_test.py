import os
import unittest

import mock

import settings
from automation.release_date import geo
from dal.mysql.ae_autosubs import db as ae_autosubs_db
from dal.mysql.ae_autosubs.experiments import retrieve_experiment_status
from dal.mysql.comon import execute_insert
from settings import GEO_ACCESSIONS_PATH

__author__ = 'Ahmed G. Ali'


class GEOToPrivateTest(unittest.TestCase):
    def setUp(self):
        self.geo_id = 'GSE7410258963'
        self.ae_id = 'E-GEOD-7410258963'
        self.geo_ids = ['GDS12345678910', 'GSE0987654321']
        self.ae_ids = ['E-GEOD-12345678910', 'E-GEOD-0987654321']
        self.email_body = """

        Dear ArrayExpress Team,

        The Series %s was returned to private status.

        Regards,
        The GEO Team
        """ % self.geo_id

        self.email_body_multiple_series = """
        Dear ArrayExpress Team,

        The Series %s and %s were returned to private status.

        Regards,
        The GEO Team
        *************""" % tuple(self.geo_ids)

    def test_change_to_private_non_loaded_experiment(self):
        try:
            geo.change_to_private(self.email_body, settings.CONAN_LOGIN_EMAIL)
        except Exception, e:
            # print e
            self.fail(e.message)

    def test_change_to_private(self):

        # adding the accession to yml file
        with open(GEO_ACCESSIONS_PATH, "a") as my_file:
            my_file.write("\n  - %s" % self.geo_id)

        sql_stmt = """INSERT INTO experiments (accession, status, is_deleted)
                      VALUES ('%s', 'AE2 Export Complete', 0);""" % self.ae_id
        execute_insert(sql_stmt, ae_autosubs_db)
        geo.retrieve_study_id_by_acc = mock.Mock(return_value=[{'ID': 12345}])
        geo.ConanPage= mock.Mock()
        geo.wait_execution = mock.Mock()
        geo.retrieve_plantain_connection= mock.Mock(return_value=(mock.Mock(), mock.Mock()))
        geo.change_to_private(self.email_body, settings.CONAN_LOGIN_EMAIL)
        # self.assertTrue(geo.ConanPage.unload_experiment.called)
        self.assertTrue(geo.retrieve_plantain_connection.called)
        self.assertEqual(retrieve_experiment_status(self.ae_id), 'Checking failed')
        f = open(GEO_ACCESSIONS_PATH, 'r')
        txt = f.read()
        f.close()
        self.assertNotIn(self.geo_id, txt)
        # Need to add assertion for unload process call

    def test_change_to_private_multiple_ids(self):

        # adding the accession to yml file
        with open(GEO_ACCESSIONS_PATH, "a") as my_file:
            my_file.write("\n  - %s%s" % (self.geo_ids[0], os.linesep))
            my_file.write("\n  - %s%s" % (self.geo_ids[1], os.linesep))

        sql_stmt = """INSERT INTO experiments (accession, status, is_deleted)
                      VALUES ('%s', 'AE2 Export Complete', 0),
                             ('%s', 'AE2 Export Complete', 0);""" % tuple(self.ae_ids)
        execute_insert(sql_stmt, ae_autosubs_db)
        geo.retrieve_study_id_by_acc = mock.Mock(return_value=[{'ID': 12345}])
        geo.ConanPage= mock.Mock()
        geo.retrieve_plantain_connection = mock.Mock(return_value=(mock.Mock(), mock.Mock()))
        geo.change_to_private(self.email_body_multiple_series, settings.CONAN_LOGIN_EMAIL)
        geo.wait_execution = mock.Mock()
        # self.assertTrue(geo.ConanPage.unload_experiment.called)
        self.assertTrue(geo.retrieve_plantain_connection.called)
        self.assertEqual(retrieve_experiment_status(self.ae_ids[0]), 'Checking failed')
        self.assertEqual(retrieve_experiment_status(self.ae_ids[1]), 'Checking failed')
        f = open(GEO_ACCESSIONS_PATH, 'r')
        txt = f.read()
        f.close()
        self.assertNotIn(self.geo_ids[0], txt)
        self.assertNotIn(self.geo_ids[1], txt)
        # Need to add assertion for unload process call

    def tearDown(self):
        execute_insert("DELETE FROM experiments where accession in %s;" % str(tuple([self.ae_id] + self.ae_ids)),
                       ae_autosubs_db)

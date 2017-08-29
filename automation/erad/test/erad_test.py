import unittest
import mock
from automation.erad import erad_submission as erad

__author__ = 'Ahmed G. Ali'


class DummyObject:
    pass


class ERADTest(unittest.TestCase):
    def setUp(self):
        self.accessions = ['ERAD-1', 'ERAD-2', 'ERAD-3']
        erad.ConanPage.__init__ = mock.Mock(return_value=None)
        erad.ConanPage.login = mock.Mock(return_value=True)
        erad.ConanPage.unload_experiment = mock.Mock()
        erad.ConanPage.load_experiment = mock.Mock()

    def test_new_experiments(self):
        task = DummyObject()
        task.id = 1234
        task.state = 'COMPLETED'
        erad.retrieve_task = mock.Mock(return_value=task)
        erad.retrieve_experiment_status = mock.Mock(return_value='AE2 Export Complete')

        erad.manage_threads(self.accessions)
        self.assertTrue(len(erad.REPORT) == len(self.accessions))
        self.assertTrue(erad.REPORT.values() == ['Reloaded successfully' for i in self.accessions])

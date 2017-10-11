from clint.textui import colored

from dal.oracle.era.era_transaction import retrieve_runs_by_study_id, retrieve_samples_by_study_id, \
    retrieve_files_by_study_id
from dal.oracle.era.experiment import retrieve_experiment_by_acc, retrieve_experiments_by_submission_acc, \
    retrieve_experiments_by_study_acc
from dal.oracle.era.experiment_sample import retrieve_sample_acc_by_exp_acc
from dal.oracle.era.run import retrieve_run_by_acc, retrieve_runs_by_submission_acc, retrieve_runs_by_experiment_acc
from dal.oracle.era.sample import retrieve_sample_by_acc
from dal.oracle.era.webin_file import retrieve_files_by_run_owner
from dal.oracle.era.wh_run import retrieve_ena_nodes_relations, retrieve_runs_by_experiment

__author__ = 'Ahmed G. Ali'

EXPERIMENTS = None
RUNS = None
SAMPLES = None
FILES = None


class ENASample:
    def __init__(self, sample_record):
        """Creates a mapping object for an existing ENA SAMPLE from a db record

        :param sample_record: Sample database record
        :type sample_record: Record <`dal.oracle.dbms.cursors.Record`>

        """
        self.sample_acc = sample_record.sample_id
        # print colored.magenta('retrieving the sample ' + self.sample_acc)
        # db_record = retrieve_sample_by_acc(self.sample_acc)[0]

        self.name = sample_record.sample_title
        self.bio_sample = sample_record.biosample_id

    def __str__(self):
        return """Sample: %s, %s""" % (self.sample_acc, self.name)


class ENARun:
    """Creates a mapping object for an existing ENA RUN with its DATA FILES and connected Sample objects from a db record
            and filters of global variable containing ``FILES``

            :param run_record: Run database record
            :type run_record: Record <`dal.oracle.dbms.cursors.Record`>
            :param sample_record: Sample database record
            :type sample_record: Record <`dal.oracle.dbms.cursors.Record`>
            """

    def __init__(self, run_record, sample_record):
        global FILES
        self.run_acc = run_record.run_id
        # print colored.magenta('retrieving the run ' + self.run_acc)
        # db_record = retrieve_run_by_acc(self.run_acc)[0]
        self.name = run_record.run_alias
        if self.name is None:
            self.name = self.run_acc
        self.layout = run_record.process_library_layout
        self.sample = ENASample(sample_record)
        self.files = []
        files = [f for f in FILES if f.data_file_owner_id == self.run_acc]
        if files:
            for f in files:
                self.files.append(f.upload_file_path)

    def __str__(self):
        return """Run: %s, %s\n Files: %s\n %s""" % (self.run_acc, self.layout, ', '.join(self.files), str(self.sample))


class ENAExperiment:
    """Creates a mapping object for an existing ENA Experiment with its runs and samples objects from a db record
    and filters of global variables containing ``RUNS`` and ``SAMPLES``

    :param record: Experiment database record
    :type record: Record <`dal.oracle.dbms.cursors.Record`>
    """

    def __init__(self, record):
        global RUNS
        global SAMPLES

        self.exp_acc = record.experiment_id

        self.runs = []
        # db_record = retrieve_experiment_by_acc(self.exp_acc)[0]
        self.name = record.library_name
        # print colored.magenta('retrieving runs for ' + self.exp_acc)
        # record = retrieve_runs_by_experiment_acc(exp_acc)
        # sample = retrieve_sample_acc_by_exp_acc(exp_acc)[0].sample_id
        # print self.exp_acc
        sample = [s for s in SAMPLES if s.experiment_id == self.exp_acc][0]
        runs = [r for r in RUNS if r.experiment_id == self.exp_acc]
        if runs:
            for r in runs:
                self.runs.append(ENARun(r, sample))

    def get_run_by_file_name(self, data_file):
        """
        Retrieve Run object containing certain data file name

        :param data_file: Data file name.
        :type data_file: str
        :return: Run object containing the data file
        :rtype: ENARun
        """
        for r in self.runs:
            if data_file in r.files:
                return r

    def has_data_file(self, data_file):
        """
        Check if an experiment object has a certain datafile in one of its runs objects

        :param data_file: Data file name.
        :return: ``True`` if file exists, ``False`` otherwise.
        :rtype: bool
        """
        for r in self.runs:
            if data_file in r.files:
                return True
        return False

    def __str__(self):
        runs = '\n'.join([str(e) for e in self.runs])
        return """Exp: %s, Name: %s\n %s""" % (self.exp_acc, self.name, runs)


class ENAStudy:
    """
    Creates a mapping object for an existing ENA study by retrieving the study and its connecting nodes from
    ENA database.
    Populates the following global variables:
        - ``EXPERIMENTS``: list of all ENA Experiment database record associated with the study
        - ``RUNS``: list of all ENA RUNS database record associated with the study
        - ``SAMPLES``: list of all ENA SAMPLES database record associated with the study
        - ``FILES``: list of all ENA FILES database record associated with the study


    :param study_acc: ENA Study Accession Number
    :type study_acc: str
    """

    def __init__(self, study_acc):
        global EXPERIMENTS
        global RUNS
        global SAMPLES
        global FILES

        self.study_acc = study_acc
        # self.submission_acc = submission_acc
        self.experiments = []
        # print colored.magenta('retrieving experiments for ' + self.study_acc)
        EXPERIMENTS = retrieve_experiments_by_study_acc(self.study_acc)
        RUNS = retrieve_runs_by_study_id(self.study_acc)
        SAMPLES = retrieve_samples_by_study_id(self.study_acc)
        FILES = retrieve_files_by_study_id(self.study_acc)
        # print records
        if EXPERIMENTS:
            for r in EXPERIMENTS:
                e = ENAExperiment(r)
                self.experiments.append(e)
                # print '\t'.join([e.runs[0].sample.name, e.runs[0].sample.sample_acc, e.runs[0].run_acc, e.exp_acc])

    def __str__(self):
        experiments = '\n\n'.join([str(e) for e in self.experiments])
        return '''ENA Study: %s\n%s''' % (self.study_acc, experiments)

    def get_exp_by_file_name(self, data_file):
        """
        Retrieves ``ENAExperiment`` object containing given data file name.

        :param data_file: Raw data file name as submitted to ENA.
        :type data_file: str
        :return: ``ENAExperiment`` Object containing the file.
        :rtype: ``ENAExperiment``, None
        """
        for e in self.experiments:
            if e.has_data_file(data_file):
                return e
        return None


if __name__ == '__main__':
    study = ENAStudy('ERP022169')
    print study
    # print 'Sample\tsample acc\tRun\tExperiment'

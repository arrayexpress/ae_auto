from clint.textui import colored

from dal.oracle.era.experiment import retrieve_experiment_by_acc, retrieve_experiments_by_submission_acc, \
    retrieve_experiments_by_study_acc
from dal.oracle.era.experiment_sample import retrieve_sample_acc_by_exp_acc
from dal.oracle.era.run import retrieve_run_by_acc, retrieve_runs_by_submission_acc, retrieve_runs_by_experiment_acc
from dal.oracle.era.sample import retrieve_sample_by_acc
from dal.oracle.era.webin_file import retrieve_files_by_run_owner
from dal.oracle.era.wh_run import retrieve_ena_nodes_relations, retrieve_runs_by_experiment


__author__ = 'Ahmed G. Ali'


class ENASample:
    def __init__(self, sample_acc):
        self.sample_acc = sample_acc
        # print colored.magenta('retrieving the sample ' + self.sample_acc)
        db_record = retrieve_sample_by_acc(self.sample_acc)[0]

        self.name = db_record.sample_title
        self.bio_sample = db_record.biosample_id

    def __str__(self):
        return """Sample: %s, %s""" % (self.sample_acc, self.name)


class ENARun:
    def __init__(self, run_acc, sample_acc):
        self.run_acc = run_acc
        # print colored.magenta('retrieving the run ' + self.run_acc)
        db_record = retrieve_run_by_acc(self.run_acc)[0]
        self.layout = db_record.process_library_layout
        self.sample = ENASample(sample_acc)
        self.files = []
        files = retrieve_files_by_run_owner(self.run_acc)
        if files:
            for f in files:
                self.files.append(f.upload_file_path)

    def __str__(self):
        return """Run: %s, %s\n Files: %s\n %s""" % (self.run_acc, self.layout, ', '.join(self.files), str(self.sample))


class ENAExperiment:
    def __init__(self, exp_acc):
        self.exp_acc = exp_acc

        self.runs = []
        db_record = retrieve_experiment_by_acc(self.exp_acc)[0]
        self.name = db_record.library_name
        # print colored.magenta('retrieving runs for ' + self.exp_acc)
        record = retrieve_runs_by_experiment_acc(exp_acc)
        sample = retrieve_sample_acc_by_exp_acc(exp_acc)[0].sample_id
        if record:
            for r in record:
                self.runs.append(ENARun(r.run_id, sample))

    def get_run_by_file_name(self, data_file):
        for r in self.runs:
            if data_file in r.files:
                return r

    def has_data_file(self, data_file):
        for r in self.runs:
            if data_file in r.files:
                return True
        return False

    def __str__(self):
        runs = '\n'.join([str(e) for e in self.runs])
        return """Exp: %s, Name: %s\n %s""" % (self.exp_acc, self.name, runs)


class ENAStudy:
    def __init__(self, study_acc):
        self.study_acc = study_acc
        # self.submission_acc = submission_acc
        self.experiments = []
        # print colored.magenta('retrieving experiments for ' + self.study_acc)
        records = retrieve_experiments_by_study_acc(self.study_acc)
        # print records
        if records:
            for r in records:
                e = ENAExperiment(r.experiment_id)
                self.experiments.append(e)
                print '\t'.join([e.runs[0].sample.name, e.runs[0].sample.sample_acc, e.runs[0].run_acc, e.exp_acc])


    def __str__(self):
        experiments = '\n\n'.join([str(e) for e in self.experiments])
        return '''ENA Study: %s\n%s''' % (self.study_acc, experiments)

    def get_exp_by_file_name(self, data_file):
        for e in self.experiments:
            if e.has_data_file(data_file):
                return e
        return None


if __name__ == '__main__':
    study = ENAStudy('ERP014059', 'ERA559203')
    print study
    # print 'Sample\tsample acc\tRun\tExperiment'


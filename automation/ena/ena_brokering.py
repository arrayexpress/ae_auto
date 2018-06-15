import argparse
import codecs
import datetime
import os
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from glob import glob
import chardet
import requests
from clint.textui import colored
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import settings
from automation.erad.erad_submission import reload_experiment
from dal.mysql.ae_autosubs.experiments import retrieve_experiment_status, retrieve_checker_score

from automation.ena.add_ena_accessions import add_ena_accessions
from dal.mysql.annotare.submission import retrieve_submission_by_accession
from dal.oracle.era.experiment import retrieve_experiments_by_submission_acc
from dal.oracle.era.run import retrieve_runs_by_submission_acc
from dal.oracle.era.sample import retrieve_samples_by_submission_acc
from dal.oracle.era.study import get_ena_acc_and_submission_acc_by_ae_acc
from dal.oracle.era.wh_run import retrieve_ena_nodes_relations
from ena_experiment import ENAExperiment
from models.conan import CONAN_PIPELINES
from models.ena_models import ENAStudy
from models.magetab.idf import IDF
from models.magetab.sdrf import SdrfCollection
from resources.ssh import retrieve_plantain_connection, get_ssh_out, retrieve_ena_connection, wait_execution
from utils.common import execute_command
from utils.conan.conan import submit_conan_task

__author__ = 'Ahmed G. Ali'


def rename_file(file_name):
    parts = file_name.split('.')
    name = parts[0]
    underscore = name.rfind('_')
    new_name = name[:underscore - 2] + name[underscore + 1:] + '_' + name[underscore - 2:underscore]
    return '.'.join([new_name] + parts[1:])


def check_modify_file_names(assay_file):
    file_mapping = {}
    renamed = False
    for assay, files in assay_file.items():
        if len(files) == 1:
            # case single
            file_mapping[files[0]] = files[0]
            continue
        file1 = files[0]
        file2 = files[1]
        if file1[:-1] == file2[:-1]:
            # case no need to rename
            file_mapping[file1] = file1
            file_mapping[file2] = file2
            continue
        renamed = True
        file1_renamed = rename_file(file_name=file1)
        file2_renamed = rename_file(file_name=file2)
        file_mapping[file1] = file1_renamed
        file_mapping[file2] = file2_renamed
    return renamed, file_mapping


def extract_acc_dict(elems):
    print elems
    dct = {}
    for elm in elems:
        dct[':'.join(elm.attrib['alias'].split(':')[1:])] = elm.attrib['accession']
    return dct


def extract_biosamples(elems):
    dct = {}
    for elm in elems:
        biosample = [e for e in elm.findall('EXT_ID') if e.attrib['type'] == 'biosample']
        if biosample:
            biosample = biosample[0]
            dct[':'.join(elm.attrib['alias'].split(':')[1:])] = biosample.attrib['accession']
        else:
            dct[':'.join(elm.attrib['alias'].split(':')[1:])] = ''

    return dct


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def parse_receipt(receipt_path, extract_center=False, study_acc=None):
    tree = ET.parse(receipt_path)
    root = tree.getroot()
    study = root.find('STUDY')
    if not study_acc:
        try:
            study_acc = study.attrib['accession']
        except:
            study_acc = None
    experiments = extract_acc_dict(root.findall('EXPERIMENT'))
    samples = extract_acc_dict(root.findall('SAMPLE'))
    biosamples = extract_biosamples(root.findall('SAMPLE'))
    runs = extract_acc_dict(root.findall('RUN'))
    if extract_center:
        f = open(receipt_path, 'r')
        content = f.read()
        f.close()
        center_name = content.split('center name')[1].split('<')[0].split(' is')[0].replace('=', '').strip()
        return experiments, runs, samples, study_acc, center_name
    return experiments, runs, samples, study_acc, biosamples


def check_submission(accession):
    ena_study = get_ena_acc_and_submission_acc_by_ae_acc(accession)
    study_submitted = False
    runs_submitted = False
    samples_submitted = False
    experiments_submitted = False
    ena_acc = None
    if ena_study and len(ena_study) > 0:
        ena_acc = ena_study[0].study_id
        submission_acc = ena_study[0].submission_id
        study_submitted = True
        runs = retrieve_runs_by_submission_acc(submission_acc)
        if runs and len(runs) > 0:
            runs_submitted = True
        samples = retrieve_samples_by_submission_acc(submission_acc)
        if samples and len(samples) > 0:
            samples_submitted = True
        experiments = retrieve_experiments_by_submission_acc(submission_acc)
        if experiments and len(experiments) > 0:
            experiments_submitted = True
    return ena_acc, study_submitted, runs_submitted, samples_submitted, experiments_submitted


class ENASubmission:
    """

    *Main class for ENA Brokering. It handles all execution options given by user in command line interface*

    :param exp_dir: Full path contining the MAGE-TAB files, e.g. MAGE-TAB_xxxx
    :type exp_dir: str

    :param accession: The Automatic ArrayExpress Accession Number, e.g. E-MTAB-xxxx
    :type accession: str

    :param meta_data_bas_dir: The base directory for the experiment's data.
                              If not given the default value is /ebi/microarray/ma-exp/AutoSubmissions/annotare/
    :type meta_data_bas_dir: str

    :param ena_optional_dir: path/to/fastq/files/directory/
                        The location of fastq files on ENA machine. If not
                        given the default value is /fire/staging/aexpress/
    :type ena_optional_dir: str

    :param combined_mage_tab:  A flag indicating that the IDF and SDRF are in the
                        same file.
    :type combined_mage_tab: bool

    :param combined_file_name:  The
                        name of the file which contians the IDF and SDRF
    :type combined_file_name: bool

    :param conan_email: The email used to submit to Conan. The default is
                        ahmed@ebi.ac.uk
    :type conan_email: str

    :param skip_validation: A flag for skipping validate fastq files.
    :type skip_validation: bool

    :param skip_copy: A flag for skipping copying fastq files.
    :type skip_copy: bool

    :param skip_ena_submission: A flag for skipping submission to ENA.
    :type skip_ena_submission: bool

    :param add_samples: A flag for adding new samples to existing experiment.
    :type add_samples: bool

    :param new_alias: suffix for ENA alias names
    :type new_alias: str


    :param receipt_date: For correction usage only
    :type receipt_date: str, isoformat date

    :param validated_before: A flag if the fastq files where validated before.
    :type validated_before: bool

    :param skip_date: skip changing the release date
    :type skup_date: bool

    :param reuse_samples: A flag indicating that there are samples to be reused.
                        In this case an existing SDRF with the sample names
                        and their ENA accessions must be provided.
    :type reuse_samples: bool

    :param other_experiment_dir: full directory containing the unpacked folder which
                        has the combined MAGE-TAB containing the already
                        submitted samples to be reused. Must have ENA
                        accessions or Biostudies IDs and the same sample
                        names. Required when --reuse_sample option is used.
    :type other_experiment_dir: str

    :param move: A flag for moving files from the root FTP dir.
    :type move: bool

    :param neglect_patterns: List of patterns to be neglected from file names when
                        trying to find pairs
    :type neglect_patterns: :obj:`list` of :obj:`str`

    :param combined_pairs: A flag to tell the system that all the pairs are
                        combined. So that, any similarity would be considered
                        as technical replica
    :type combined_pairs: str

    :param validate_only: A flag to quite after validation.
    :type validate_only: book

    :param mixed_pairs: A flag to tell the system that the pairs are combined
                        and not combined.
    :type mixed_pairs: bool

    :param no_spots:  A flag indicating that the spots have been calculated
                        before.
    :type no_spits: bool

    :param idf: The idf file name.
    :type idf: str

    :param sdrf: The SDRF file_name
    :type sdrf: str

    :param test: A flag for the submission to be submitted to ENA Dev server.
    :type test: bool
    """

    def __init__(self, exp_dir, accession, meta_data_bas_dir=None, ena_optional_dir=None, combined_mage_tab=False,
                 combined_file_name=None, conan_email=None, skip_validation=False, skip_copy=False,
                 skip_ena_submission=False, add_samples=False, new_alias=None, replace_idf=False,
                 receipt_date=None, validated_before=False, skip_date=False, reuse_samples=False,
                 other_experiment_dir=None, move=False, neglect_patterns=[], combined_pairs=False, validate_only=False,
                 mixed_pairs=False, no_spots=False, idf=None, sdrf=None, test=False):

        self.new_alias = ''
        if new_alias:
            self.new_alias = new_alias

        self.idf_file = idf
        self.sdrf_file = sdrf
        self.test = test

        self.no_spots = no_spots
        self.renamed = False
        self.validate_only = validate_only
        if not neglect_patterns:
            neglect_patterns = []
        self.move = move
        if receipt_date:
            self.time_stamp = receipt_date
        else:
            self.time_stamp = datetime.datetime.now().isoformat().split('.')[0].replace('T', '_').replace(':', '_')
        self.reuse_samples = reuse_samples
        self.other_experiment_dir = other_experiment_dir
        # print self.other_experiment_dir
        # exit()
        if self.reuse_samples and not self.other_experiment_dir:
            print colored.red('An old SDRF file name should be provided when reuse samples are requested!', bold=True)
            exit(1)
        self.validated_before = validated_before
        self.exp_dir = exp_dir
        self.skip_validation = skip_validation
        self.skip_copy = skip_copy
        self.skip_ena_submission = skip_ena_submission
        self.combined_mage_tab = combined_mage_tab
        self.add_samples = add_samples
        self.added_samples = []
        self.study_accession = None
        if conan_email:
            settings.CONAN_LOGIN_EMAIL = conan_email
        if meta_data_bas_dir:

            self.exp_path = os.path.join(meta_data_bas_dir, exp_dir)
        else:
            self.exp_path = os.path.join(settings.ANNOTARE_DIR, exp_dir)

        self.ena_optional_dir = ena_optional_dir
        self.accession = accession
        self.plantain, self.plantain_ssh = retrieve_plantain_connection()
        # self.ena, self.ena_ssh = retrieve_ena_connection()
        if not combined_mage_tab:
            if not self.sdrf_file:
                self.sdrf_file = self.extract_sdrf_file_name()
            if not self.idf_file:
                self.idf_file = self.extract_idf_file_name()

        else:
            self.sdrf_file = combined_file_name
            self.idf_file = combined_file_name
        if self.other_experiment_dir and self.other_experiment_dir.startswith('MAGE-TAB_'):
            self.other_experiment_dir = os.path.join(settings.ANNOTARE_DIR, self.other_experiment_dir)

        if self.other_experiment_dir:
            if self.other_experiment_dir.endswith('.idf.txt'):
                self.other_sdrf_name = self.other_experiment_dir.split('/')[-1]
            else:
                self.other_sdrf_name = self.extract_idf_file_name(other=True)
                self.other_experiment_dir = os.path.join(self.other_experiment_dir, self.other_sdrf_name)

        self.ena_dir = self.extract_ena_accession_dir()
        self.ena_full_path = '/fire/staging/aexpress/' + self.ena_dir
        print colored.green('ENA DIR: '+ self.ena_dir)
        # exit()
        if replace_idf:
            os.remove(os.path.join(self.exp_path, self.idf_file + '_original'))
            shutil.copyfile(os.path.join(self.exp_path, self.idf_file + '_without_ena'),
                            os.path.join(self.exp_path, self.idf_file))
        self.local_tmp = os.path.join(settings.TEMP_FOLDER, self.accession)
        self.files_mapping = {}
        self.samples = {}
        self.runs = {}
        self.experiments = {}
        self.biosamples = {}
        if not os.path.exists(self.local_tmp):
            os.makedirs(self.local_tmp)
        if not self.sdrf_file:
            print colored.red('ERROR: No SDRF File')
            exit(1)
        if self.add_samples:
            print colored.green("Retrieving submitted Experiment, this might take few minutes.")
            r = get_ena_acc_and_submission_acc_by_ae_acc(self.accession)[0]
            study_acc = r.study_id

            study = ENAStudy(study_acc=study_acc)
            # print str(study)
            for exp in study.experiments:
                self.experiments[exp.name] = exp.exp_acc
                for run in exp.runs:
                    self.runs[run.name] = run.run_acc
                    self.samples[run.sample.name] = run.sample.sample_acc
                    self.biosamples[run.sample.name] = run.sample.bio_sample
            if not self.study_accession:
                self.study_accession = study_acc

            # receipts = self.copy_receipts()
            #
            # for receipt in receipts:
            #     old_experiments, old_runs, old_samples, study_acc, old_biosamples = parse_receipt(
            #         os.path.join(self.local_tmp, receipt), False)
            #     self.samples = merge_two_dicts(old_samples, self.samples)
            #     self.runs = merge_two_dicts(old_runs, self.runs)
            #     # print self.runs
            #     self.experiments = merge_two_dicts(old_experiments, self.experiments)
            #     if not self.study_accession:
            #         self.study_accession = study_acc
            #     self.biosamples = merge_two_dicts(old_biosamples, self.biosamples)

            # print 'RUNS'
            # print self.runs
            # exit()
            self.added_samples = self.samples.keys()
        # print self.samples
        # exit()
        if combined_mage_tab:
            shutil.copyfile(os.path.join(self.exp_path, self.idf_file),
                            os.path.join(self.local_tmp, self.idf_file))
        else:
            shutil.copyfile(os.path.join(self.exp_path, 'unpacked', self.sdrf_file),
                            os.path.join(self.local_tmp, self.sdrf_file))
            shutil.copyfile(os.path.join(self.exp_path, self.idf_file),
                            os.path.join(self.local_tmp, self.idf_file))
        if self.other_experiment_dir:
            shutil.copyfile(self.other_experiment_dir, os.path.join(self.local_tmp, self.other_sdrf_name))
        self.center_name = None
        self.idf = IDF(idf_path=os.path.join(self.local_tmp, self.idf_file), combined=combined_mage_tab,
                       skip_release_date=skip_date)
        self.sdrf = SdrfCollection(file_path=os.path.join(self.local_tmp, self.sdrf_file), combined=combined_mage_tab,
                                   neglect_patterns=neglect_patterns, combined_pairs=combined_pairs,
                                   mixed_pairs=mixed_pairs)
        if self.other_experiment_dir:
            self.ena_sdrf = SdrfCollection(file_path=os.path.join(self.local_tmp, self.other_sdrf_name), combined=True)

        self.exp = ENAExperiment(accession=self.accession, sdrf=self.sdrf, idf=self.idf, time_stamp=self.time_stamp,
                                 added_samples=self.added_samples, study_accession=self.study_accession,
                                 center_name=self.center_name, new_alias=new_alias)
        if self.other_experiment_dir:
            for row in sorted(self.sdrf.rows, key=lambda x: x.source):
                for other_row in sorted(self.ena_sdrf.rows, key=lambda x: x.source):
                    if row.source == other_row.source:
                        row.bio_sample = other_row.bio_sample
                        row.ena_sample = other_row.ena_sample
                        row.ena_alias = other_row.ena_alias
                        continue
        self.sdrf.generate_file_to_check(
            file_path=os.path.join(self.local_tmp, '%s_files_to_check.txt' % self.accession),
            added_samples=self.added_samples)
        shutil.copyfile(os.path.join(self.local_tmp, '%s_files_to_check.txt' % self.accession),
                        os.path.join(self.exp_path, 'unpacked', '%s_files_to_check.txt' % self.accession))
        try:
            os.chmod(os.path.join(self.local_tmp, '%s_files_to_check.txt' % self.accession), 0o777)
        except:
            pass
        try:
            os.chmod(os.path.join(self.exp_path, 'unpacked', '%s_files_to_check.txt' % self.accession), 0o777)
        except:
            pass

    def extract_sdrf_file_name(self):
        lines = os.listdir(os.path.join(self.exp_path, 'unpacked'))
        sdrf_file_name = [l.strip() for l in lines if self.accession in l and '_v' in l]
        if not sdrf_file_name or sdrf_file_name == []:
            sdrf_file_name = [l.strip() for l in lines if
                              'submission' in l and 'annotare' in l and l.strip().endswith('.sdrf.txt')]
        if sdrf_file_name:
            versions = []
            for i in sdrf_file_name:
                v = i.split('.')[0].split('_')[-1]
                if v.startswith('v'):
                    versions.append(int(v.replace('v', '')))
                else:
                    versions.append(-1)
            max_index = versions.index(max(versions))
            return sdrf_file_name[max_index]
        return None

    def extract_fastq_file_names(self):
        local_file = os.path.join(self.local_tmp, '%s_files_to_check.txt' % self.accession)
        f = open(local_file, 'r')
        lines = f.readlines()
        f.close()
        files = []
        for l in lines[1:]:
            files.append(l.split('\t')[2])
        return files

    def validate_fastq_files(self):
        """
        Calls fastq files validator.

        :return: True if valid, terminates if invalid
        """
        local_file = os.path.join(self.local_tmp, '%s_validation.txt' % self.accession)
        if not self.validated_before:
            memory = ''
            # print [r for r in self.sdrf.rows if r.new_data_file.endswith('.bz2')]
            if len([r for r in self.sdrf.rows if r.new_data_file.endswith('.bz2')]):
                # print 'removing'
                self.remove_validation_tmp_files()
                memory = '65536'
            # self.ena.send(
            #     'gxa_validate_fastq.sh %s_files_to_check.txt  %s > validation_out.txt 2>&1\n' % (
            #         self.accession, memory))
            execute_command(
                "ssh sra-login-2 'source /homes/fg_cur/.bashrc;source /etc/profile; source /home/fg_cur/.bash_profile; echo \$PATH;cd %s;gxa_validate_fastq.sh %s_files_to_check.txt  "
                "%s > validation_out.txt 2>&1'" % (
                    self.ena_full_path, self.accession, memory), 'fg_cur')
            # execute_command(
            #     "ssh sra-login-2  ' source /homes/fg_cur/.bashrc;echo LSF_ENVDIR=; echo \\$LSF_ENVDIR;echo \\$PATH; ' ", 'fg_cur')
            # print 'Validation command sent'
            # wait_execution(self.ena)
            # self.plantain.send(
            #     'scp sra-login-2:/fire/staging/aexpress/%s/validation_out.txt %s\n' % (
            #         self.ena_dir, self.exp_path))
            execute_command(
                'scp sra-login-2:/fire/staging/aexpress/%s/validation_out.txt %s\n' % (
                    self.ena_dir, self.exp_path), 'fg_cur')
            # a = wait_execution(self.plantain)
            # print a
            shutil.copyfile(os.path.join(self.exp_path, 'validation_out.txt'),
                            local_file)
        f = open(local_file, 'r')
        lines = f.readlines()
        f.close()
        check_valid = False
        check_copied = False
        for line in lines:
            line = line.strip()
            if 'error' in line.lower():
                self.rename_back()
                print colored.red(
                    'ERROR: There was an error in validating fastq files. Please check the script output in: ' + local_file)
                exit(1)
            if line == '':
                continue
            if line.startswith('fastq(s)'):
                check_copied = False
                check_valid = True
                continue
            elif line.startswith('Copying'):
                check_copied = True
                check_valid = False
                continue
            elif line.startswith('Time'):
                check_copied = False
                check_valid = False
                continue
            if check_valid and not line.endswith('Valid'):
                self.rename_back()
                print colored.red('Error: There was an invalid fastq files(s). Check the output in ' + local_file)
                exit(1)
            if check_copied and not line.endswith('successfully'):
                self.rename_back()
                print colored.red('Error: Copying fastq files failed. Check the output in ' + local_file)
                exit(1)
        print colored.green('Everything is valid and copied successfully')
        return True

    def remove_validation_tmp_files(self):
        execute_command("ssh sra-login-2 'cd %s;rm *.pipe.*;rm ..*.pipe.*;rm gxa_validate_fastq*.err*;rm "
                        "gxa_validate_fastq*.out*;rm *.uniq'" % self.ena_full_path, 'fg_cur')
        # self.ena.send('rm *.pipe.*\n')
        # a = wait_execution(self.ena)
        # self.ena.send('rm ..*.pipe.*\n')
        # a = wait_execution(self.ena)
        # # print a
        # self.ena.send('rm gxa_validate_fastq*.err*\n')
        # a = wait_execution(self.ena)
        # # print a
        # self.ena.send('rm gxa_validate_fastq*.out*\n')
        # a = wait_execution(self.ena)
        # # print a
        # self.ena.send('rm *.uniq\n')
        # wait_execution(self.ena)

    def check_rename(self):
        missing_files = []
        for row in self.sdrf.rows:
            if row.source in self.added_samples:
                continue
            if row.data_file != row.new_data_file:
                print colored.blue('renaming %s to become %s' % (row.data_file, row.new_data_file))
                # cmd = 'mv %s %s\n' % (row.data_file, row.new_data_file)
                # self.ena.send(cmd)
                cmd = 'ssh sra-login-2 "cd %s; mv %s %s"' % (self.ena_full_path, row.data_file, row.new_data_file)
                out = ' '.join(execute_command(cmd=cmd, user='fg_cur'))
                self.renamed = True
                # out = get_ssh_out(self.ena)
                if 'No such file or directory' in out:
                    # self.ena.send('ls\n')
                    # check = get_ssh_out(self.ena)
                    check = ' '.join(
                        execute_command(cmd="ssh sra-login-2 'cd %s;ls;'" % self.ena_full_path, user='fg_cur'))
                    if row.new_data_file not in check:
                        missing_files.append(row.data_file)
        if missing_files:
            print colored.green('Error: These files do not exit on the FTP:\n' + '\n'.join(missing_files))
            exit(1)

    def move_files_to_local_ena_dir(self):
        missing_files = []
        for row in self.sdrf.rows:
            if row.source in self.added_samples:
                continue
            file_name = row.data_file
            new_file_name = row.new_data_file
            if file_name == new_file_name:
                print 'Moving:  %s' % file_name
            else:
                print 'Moving:  %s to become %s' % (file_name, new_file_name)
            # cmd = 'mv ../%s ./%s\n' % (file_name, new_file_name)
            cmd = "ssh sra-login-2 'cd %s;mv ../%s ./%s;'" % (self.ena_full_path, file_name, new_file_name)
            if self.ena_optional_dir:
                # cmd = 'mv %s ./%s\n' % (os.path.join(self.ena_optional_dir, file_name), new_file_name)
                cmd = "ssh sra-login-2 'cd %s;mv %s ./%s'" % (
                    self.ena_full_path, os.path.join(self.ena_optional_dir, file_name), new_file_name)
            out = ' '.join(execute_command(cmd, 'fg_cur'))
            # out = get_ssh_out(self.ena)
            if 'No such file or directory' in out:
                # self.ena.send('ls\n')
                # check = get_ssh_out(self.ena)
                check = ' '.join(
                    execute_command(
                        cmd="ssh sra-login-2 'cd %s;ls;'" % self.ena_full_path,
                        user='fg_cur'
                    )
                )

                if new_file_name not in check:
                    missing_files.append(file_name)
        if missing_files:
            print colored.green('Error: These files do not exit on the FTP:\n' + '\n'.join(missing_files))
            exit(1)

    def move_files_back(self):
        for row in self.sdrf.rows:
            # self.ena.send('mv %s ../%s\n' % (row.new_data_file, row.data_file))
            execute_command(
                "ssh sra-login-2 'mv %s/%s /fire/staging/aexpress/%s'" %
                (self.ena_full_path, row.new_data_file, row.data_file),
                'fg_cur'
            )
            # wait_execution(self.ena)

    def create_ena_exp_dir(self):
        if self.ena_dir == self.accession:
            execute_command("ssh sra-login-2 'mkdir /fire/staging/aexpress/%s'" % self.accession, 'fg_cur')
        # self.ena.send('aexpress\n')

        # if self.ena_dir == self.accession:
        #     self.ena.send('mkdir %s\n' % self.accession)
        # self.ena.send('cd %s\n' % self.ena_dir)

        execute_command(
            "scp %s/unpacked/%s_files_to_check.txt sra-login-2:/fire/staging/aexpress/%s/%s_files_to_check.txt\n" % (
                self.exp_path, self.accession, self.ena_dir, self.accession),
            'fg_cur'
        )

        # self.plantain.send(
        #     "scp %s/unpacked/%s_files_to_check.txt sra-login-2:/fire/staging/aexpress/%s/%s_files_to_check.txt\n" % (
        #         self.exp_path, self.accession, self.ena_dir, self.accession))
        # a = wait_execution(self.plantain)
        # print a

    def copy_receipts(self):
        old_xml_path = os.path.join(self.exp_path, 'xmls')
        receipts = []
        if os.path.exists(old_xml_path):
            if os.path.isdir(old_xml_path):
                for f in os.listdir(old_xml_path):
                    if 'receipt' in f.strip():
                        shutil.copyfile(os.path.join(old_xml_path, f), os.path.join(self.local_tmp, f))
                        receipts.append(f)
        # std_in, std_out, std_err = self.plantain_ssh.exec_command("ls %s;" % os.path.join(self.exp_path, 'xmls/'))
        # lines1 = std_out.readlines()
        # std_in, std_out, std_err = self.plantain_ssh.exec_command("ls %s;" % os.path.join(self.exp_path, '*receipt*'))
        # lines2 = std_out.readlines()
        # receipts = [l.strip().split('/')[-1] for l in lines2 if 'receipt' in l.strip()] + \
        #            [os.path.join('xmls', l.strip()) for l in lines1 if 'receipt' in l.strip()]
        # sftp = self.plantain_ssh.open_sftp()
        # for r in receipts:
        #     sftp.get(os.path.join(self.exp_path, r),
        #              os.path.join(self.local_tmp, r.replace('xmls/', '')))
        # sftp.close()
        # return [r.replace('xmls/', '') for r in receipts]
        return receipts

    def extract_idf_file_name(self, other=False):
        exp_path = self.exp_path
        if other:
            exp_path = self.other_experiment_dir
        # if other:
        #     lines = os.listdir(self.other_experiment_dir)
        # else:
        #     lines = os.listdir(self.exp_path)
        lines = os.listdir(exp_path)
        f_name = ''
        if self.add_samples:
            idf = [l.strip() for l in lines if 'before_ena' in l.strip()]
            if idf:
                f_name = idf[0]
                for filename in glob("*.csv"):
                    os.remove('%s/%s' % (exp_path, filename))
                shutil.copyfile(os.path.join(exp_path, f_name),
                                os.path.join(exp_path,
                                             f_name.replace('_before_ena', '')))
                lines = [l for l in lines if '_original' not in l]
        idf = [l.strip() for l in lines if
               l.strip().endswith('.idf.txt') and l.strip().startswith(self.accession) and 'backup' not in l]
        if not idf or idf == []:
            idf = [l.strip() for l in lines if l.strip().endswith('.idf.txt') and 'backup' not in l]
        if idf:
            versions = [int(i.split('.')[0].split('_')[-1].replace('v', '')) for i in idf]
            max_index = versions.index(max(versions))
            f_name = idf[max_index]
        if [l.strip() for l in lines if f_name + '_original' in l.strip()] and not other:
            # print colored.green('original idf file found')
            shutil.copyfile(os.path.join(exp_path, f_name + '_original'), os.path.join(exp_path, f_name))
        else:
            # print colored.green('saving original idf')
            shutil.copyfile(os.path.join(exp_path, f_name), os.path.join(exp_path, f_name + '_original'))
        # if other:
        #     print f_name
        #     exit()
        return f_name

    def submit_xmls(self, nodes_only=False):
        """
        Submits prepared ENA project xml files to ENA

        :param nodes_only: flag for skipping submission of study.xml
        :type nodes_only: bool

        :return: None
        """
        url = settings.ENA_SRA_URL
        if self.test:
            url = settings.ENA_SRA_DEV_URL
            print colored.magenta('This submission is going to ENA Dev Server')
        files = {}
        keys = ['EXPERIMENT', 'RUN', 'SAMPLE', 'STUDY', 'SUBMISSION']
        if self.add_samples or nodes_only:
            keys = ['EXPERIMENT', 'RUN', 'SAMPLE', 'SUBMISSION']

        for k in keys:
            files[k] = open(os.path.join(self.local_tmp, '%s_%s_%s.xml' % (self.accession, self.time_stamp, k.lower())),
                            'rb')
        # print colored.blue(str(files))
        # exit()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        r = requests.post(url, files=files, verify=False, timeout=1000)
        content = r.content
        if '<html>' in content:
            print colored.yellow('ENA Service is not available now, will try again in 20 seconds.')
            time.sleep(20)
            self.submit_xmls()
            return
        f = open(os.path.join(self.local_tmp, '%s_%s_receipt.xml' % (self.accession, self.time_stamp)), 'w')
        f.write(content)
        f.close()
        if 'success="true' not in content:
            print colored.cyan('FAILURE: Failed submission to ENA. Please check the receipt: ' +
                               os.path.join(self.local_tmp, '%s_%s_receipt.xml' % (self.accession, self.time_stamp)))
            print colored.red(content.split('<ERROR>')[1].split('</ERROR>')[0])
            # exit(1)

    def add_ena_accession(self):
        receipt_path = os.path.join(self.local_tmp, '%s_%s_receipt.xml' % (self.accession, self.time_stamp))
        experiments, runs, samples, study_acc, biosamples = parse_receipt(receipt_path=receipt_path,
                                                                          study_acc=self.study_accession)
        self.samples = merge_two_dicts(samples, self.samples)
        self.biosamples = merge_two_dicts(biosamples, self.biosamples)

        self.experiments = merge_two_dicts(experiments, self.experiments)
        if self.add_samples:
            self.idf.lines.append(
                "Comment[SequenceDataURI]\thttp://www.ebi.ac.uk/ena/data/view/%s-%s\thttp://www.ebi.ac.uk/ena/data/view/%s-%s" %
                (min(self.runs.values()), max(self.runs.values()), min(runs.values()), max(runs.values()))
            )
            self.runs = merge_two_dicts(runs, self.runs)

        else:
            self.runs = merge_two_dicts(runs, self.runs)
            self.idf.lines.append(
                "Comment[SequenceDataURI]\thttp://www.ebi.ac.uk/ena/data/view/%s-%s" %
                (min(self.runs.values()), max(self.runs.values()))
            )
        self.idf.lines.append('Comment[SecondaryAccession]\t' + study_acc)
        self.sdrf.add_ena_accessions(self.samples, self.experiments, self.runs, self.biosamples)

        f = codecs.open(os.path.join(self.local_tmp, 'combined.txt'), 'w', 'UTF8')
        combined = ['[IDF]'] + self.idf.lines + ['[SDRF]'] + self.sdrf.get_lines_with_ena()

        try:
            write_string = (u'%s' % os.linesep).join([i.encode('utf8') for i in combined])
        except Exception, e:

            write_string = (u'%s' % os.linesep).join([i.decode('utf8') for i in combined])
        f.write(write_string)
        f.close()

    def reset_experiment(self):
        subprocess.call('dos2unix %s\n' % os.path.join(self.exp_path, self.idf_file), shell=True,
                        env=dict(ENV=settings.BASH_PATH))
        subprocess.call('source %s; reset_experiment.pl -c %s' % (settings.BASH_PATH, self.exp_dir), shell=True,
                        env=dict(ENV=settings.BASH_PATH))

    def validate_xml(self, extract_num=0, assay_num=0, sample_num=0):
        """
        Validates generated ENA xmls before submission.
        Terminate on wrong xml files content.

        :param extract_num: number of expected extract names
        :param assay_num: number of expected assay names
        :param sample_num: number of expected samples
        :type extract_num: int
        :type assay_num: int
        :type sample_num: int

        :return: None
        """
        self.check_utf8(f_type='submission')
        self.check_utf8(f_type='experiment')

        tree = ET.parse(os.path.join(self.local_tmp, '%s_%s_experiment.xml' % (self.accession, self.time_stamp)))
        root = tree.getroot()
        experiments = root.findall('EXPERIMENT')
        if len(experiments) != extract_num:
            print colored.red('''Error: Invalid Experiment.xml file.
            Number of experiment aliases is not correct.
            Please check the file: ''' + os.path.join(self.local_tmp,
                                                      '%s_%s_experiment.xml' % (self.accession, self.time_stamp)))
            exit(1)

        self.check_utf8(f_type='sample')
        tree = ET.parse(os.path.join(self.local_tmp, '%s_%s_sample.xml' % (self.accession, self.time_stamp)))
        root = tree.getroot()
        samples = root.findall('SAMPLE')
        if len(samples) != sample_num:
            print colored.red('''Error: Invalid Samples.xml file.
            Number of samples is not correct.
            No of samples: %s
            No of expected samples: %s
            Please check the file: ''' % (str(len(samples)), str(sample_num)) +
                              os.path.join(self.local_tmp,
                                           '%s_%s_sample.xml' % (
                                               self.accession,
                                               self.time_stamp)))
            exit(1)
        self.check_utf8(f_type='run')
        tree = ET.parse(os.path.join(self.local_tmp, '%s_%s_run.xml' % (self.accession, self.time_stamp)))
        root = tree.getroot()
        runs = root.findall('RUN')
        if not self.sdrf.combined_pairs:
            if len(runs) != assay_num:
                print colored.red('''Error: Invalid Run.xml file.
                Number of runs is not correct.
                No of runs: %s
                No of expected runs: %s
                Please check the file: ''' % (str(len(runs)), str(assay_num)) +
                                  os.path.join(self.local_tmp,
                                               '%s_%s_run.xml' % (
                                                   self.accession,
                                                   self.time_stamp)))
                exit(1)
        f = open(os.path.join(self.local_tmp, '%s_%s_run.xml' % (self.accession, self.time_stamp)), 'r')
        runs = f.read()
        f.close()
        files_not_found = []
        for row in self.sdrf.rows:
            if row.source in self.added_samples:
                continue
            if row.new_data_file.decode('utf8') not in runs.decode('utf8'):
                files_not_found.append(row.new_data_file)
        if len(files_not_found) > 0:
            print colored.red(
                """Error: Invalid Run.xml files\nThe following files didn't appear\n""" + '\n'.join(files_not_found) +
                """Please check the file : """ + os.path.join(self.local_tmp, '%s_run.xml' % self.accession))
            exit(1)

    def check_utf8(self, f_type):
        f = open(os.path.join(self.local_tmp, '%s_%s_%s.xml' % (self.accession, self.time_stamp, f_type)), 'r')
        f_content = f.read()
        f.close()
        encoding = chardet.detect(f_content)
        char_set = encoding['encoding']
        if char_set.replace('-', '').replace('_', '').lower() != 'utf8':
            # print colored.cyan('Warning: %s xml file is not UTF8. Converting!!!' % f_type)
            f_content = f_content.decode(char_set)
            f_content = f_content.encode('utf-8')
            f = open(os.path.join(self.local_tmp, '%s_%s_%s.xml' % (self.accession, self.time_stamp, f_type)), 'w')
            f.write(f_content)
            f.close()

    def add_sdrf_spot_length_from_validation_output(self):
        f = open(os.path.join(self.local_tmp, '%s_validation.txt' % self.accession), 'r')
        lines = f.readlines()
        f.close()
        results = []
        add_line = False
        for line in lines:
            if line.startswith('fastq(s)'):
                add_line = True
                continue
            if add_line:

                if line.strip() == '' or line.strip().startswith('Time'):
                    break
                results.append(line)

        files = {}
        for l in results:
            l = l.strip().split('\t')
            f_names = l[0]
            print l

            val = l[2]
            try:
                val = int(val)
            except:
                val = None

            if ' ' in l[0]:
                for name in f_names.split(' '):
                    files[name] = val
            else:
                files[f_names] = val
        bam_files = [row.new_data_file for row in self.sdrf.rows if '.bam' in row.new_data_file]
        for f in bam_files:
            files[f] = None
        # print 'Validation out files: '
        # print files
        self.sdrf.add_spot_length(files=files)
        return

    def submit_experiment(self, ):

        self.create_ena_exp_dir()
        if self.move:
            self.move_files_to_local_ena_dir()

        # self.check_rename()
        if self.sdrf.combined_pairs or self.skip_validation:
            if not self.skip_copy:
                print colored.green('Copying to ENA dropbox')
                self.copy_to_ena_dropbox()
            files = self.get_spot_length()
            print colored.green('Adding spot length to SDRF')
            self.sdrf.add_spot_length(files)

        else:
            print colored.green('Validating fastq files')
            self.validate_fastq_files()
            self.copy_to_ena_dropbox(extra=True)
            print colored.green('Adding extra columns to SDRF')
            self.add_sdrf_spot_length_from_validation_output()
        if self.add_samples:
            print colored.green('Adding Samples mode')
            files = self.get_spot_length()

            self.sdrf.add_spot_length(files)
        if self.validate_only:
            print colored.green(
                'The running mode was validate only!\n Please next time use -vb not to waste time in validating again!')
            exit(0)
        print colored.green('Generating ENA-RSA XML files')
        self.exp.generate_xmls(save_dir=self.local_tmp)
        print colored.green('Validating XML files')
        assay_num = len(list(set([r.new_data_file for r in self.sdrf.rows if
                                  not r.is_paired and
                                  r.source not in self.added_samples and
                                  '.qual' not in r.new_data_file]))) + len(
            list(set([r.assay_name for r in self.sdrf.rows if
                      r.is_paired and r.source not in self.added_samples and '.qual' not in r.new_data_file])))

        self.validate_xml(
            assay_num=assay_num,
            sample_num=len(list(
                set([r.source for r in self.sdrf.rows if not r.ena_sample and r.source not in self.added_samples]))),
            extract_num=len(list(set([r.extract_detailed for r in self.sdrf.rows if
                                      r.source not in self.added_samples])))
        )

        if not self.skip_ena_submission:
            print colored.green('submitting XML files to ENA')
            self.submit_xmls()
        if not os.path.exists(os.path.join(self.exp_path, 'xmls')):
            os.mkdir(os.path.join(self.exp_path, 'xmls'))
            os.chmod(os.path.join(self.exp_path, 'xmls'), 0o777)

        for f in os.listdir(self.local_tmp):
            if self.time_stamp in f and self.accession in f and f.endswith('.xml'):
                # print os.path.join(self.local_tmp, f), os.path.join(self.exp_path, 'xmls', f)
                shutil.copyfile(os.path.join(self.local_tmp, f), os.path.join(self.exp_path, 'xmls', f))
        ena_acc, study_submitted, runs_submitted, samples_submitted, experiments_submitted = check_submission(
            self.accession)
        if not study_submitted:
            print colored.red('Error while submitting the study, retrying!')
            self.submit_xmls()

        if not (runs_submitted or samples_submitted or experiments_submitted):
            print colored.red('Study added but not other nodes. Retrying to fix this')
            self.exp.study_accession = ena_acc
            self.exp.generate_xmls(save_dir=self.local_tmp)
            self.submit_xmls(nodes_only=True)

        print colored.green('Adding ENA accessions')
        shutil.copyfile(os.path.join(self.local_tmp, self.idf_file),
                        os.path.join(self.exp_path, self.idf_file + '_before_ena'))
        if self.test:
            self.add_ena_accession()
        # shutil.copyfile(os.path.join(self.local_tmp, 'combined.txt'),
        #                 os.path.join(self.exp_path, self.idf_file))
        else:
            add_ena_accessions(ae_acc=self.accession, idf=self.idf, sdrf=self.sdrf,
                               out_file=os.path.join(self.exp_path, self.idf_file))
        # shutil.copyfile(os.path.join(self.local_tmp, 'combined.txt'),
        #                 os.path.join(self.exp_path, self.idf_file))

        print colored.green('Reset Experiment')
        self.reset_experiment()
        self.wait_for_ae_export()
        print colored.green('starting conan submission')
        if self.add_samples:
            reload_experiment(self.accession)
        else:

            submit_conan_task(accession=self.accession, pipeline_name=CONAN_PIPELINES.load)
            print colored.green('submitted to conan')
        shutil.move(os.path.join(self.exp_path, self.idf_file + '_original'),
                    os.path.join(self.exp_path, self.idf_file + '_without_ena'))
        # self.plantain_ssh.close()
        # self.ena_ssh.close()

    def wait_for_ae_export(self, exported=False):
        status = retrieve_experiment_status(self.accession)
        while status != 'AE2 Export Complete':
            # print status
            time.sleep(30)
            status = retrieve_experiment_status(self.accession)
            if status in ['Export failed', 'Checking failed', 'Abandoned', '** CHECKER CRASH **',
                          'MAGE-TAB export failed', 'Validation failed']:
                checker_score = retrieve_checker_score(self.accession)
                if not exported and checker_score == 34:
                    print 'Checker score 34. Exporting'
                    self.export_experiment()
                    time.sleep(120)
                    self.wait_for_ae_export(True)
                else:
                    print colored.red('Failure: Experiment Reset Failed')
                    exit(1)
        print colored.green('Export Complete')

    def copy_to_ena_dropbox(self, extra=False):
        new_rows = self.sdrf.rows
        if self.added_samples:
            new_rows = [r for r in self.sdrf.rows if r.source not in self.added_samples]

            print colored.green('Copying new files only. %d files are being copied' % len(new_rows))
        for row in new_rows:
            if extra:
                if '.bam' not in row.data_file:
                    continue
            print colored.green('Copying: ' + row.data_file)
            # self.ena.send('cp ./%s /fire/staging/era/upload/Webin-24/\n' % row.data_file)
            # wait_execution(self.ena)
            execute_command(
                "ssh sra-login-2 'cp %s/%s /fire/staging/era/upload/Webin-24/'" % (
                    self.ena_full_path, row.data_file), 'fg_cur')

    def get_spot_length(self):
        print colored.green('Calculating Spot Length')
        files = {}
        local_file = os.path.join(self.local_tmp, 'spots.txt')
        if not self.no_spots:
            # self.ena.send('rm spots.txt;touch spots.txt\n')
            # wait_execution(self.ena)
            execute_command(
                "ssh sra-login-2 'cd %s;rm spots.txt;touch spots.txt'" % self.ena_full_path,
                'fg_cur'
            )
            crams = [r.new_data_file for r in self.sdrf.rows if
                     r.new_data_file.endswith('.cram')]
            gzs = [
                r.new_data_file for r in self.sdrf.rows if
                r.new_data_file.endswith('.gz')
            ]
            bams = [
                r.new_data_file for r in self.sdrf.rows if
                r.new_data_file.endswith('.bam')
            ]
            sffs = [
                r.new_data_file for r in self.sdrf.rows if
                r.new_data_file.endswith('.sff')
            ]
            commands = []
            if crams:
                # print 'calculating cram spots'
                # self.ena.send(
                #     'for file in *.cram; do echo -e -n "$file\\t" >>spots.txt; cramtools fastq -I "$file" | head -n2 | tail -n1 | wc -c >>spots.txt; echo ''>>spots.txt; done;\n')
                # wait_execution(self.ena)
                commands.append('for file in *.cram; do echo -e -n "$file\\t" >>spots.txt; cramtools '
                                'fastq -I "$file" | head -n2 | tail -n1 | wc -c >>spots.txt; echo ''>>spots.txt; done;' %
                                self.ena_full_path)
                # execute_command(
                #     'ssh sra-login-2 "cd %s;for file in *.cram; do echo -e -n "$file\\t" >>spots.txt; cramtools '
                #     'fastq -I "$file" | head -n2 | tail -n1 | wc -c >>spots.txt; echo ''>>spots.txt; done;"' %
                #     self.ena_full_path,
                #     'fg_cur')
            if sffs:
                # print 'calculating sff spots'
                # self.ena.send(
                #     'for file in *.sff; do echo -e -n "$file\\t" >>spots.txt; sff "$file" | head -n2 | tail -n1 | wc -c >>spots.txt; echo ''>>spots.txt; done;\n')
                # wait_execution(self.ena)
                commands.append(
                    'for file in *.sff; do echo -e -n "$file\\t" >>spots.txt; sff "$file" |'
                    'head -n2 | tail -n1 | wc -c >>spots.txt; echo ''>>spots.txt; done;')
            if gzs:
                # print 'calculating gz spots'
                commands.append('for file in *.gz ; do echo -e -n "$file\\t" >>spots.txt; zcat '
                                '"./$file"  | head -2 | tail -1 | wc -m >>spots.txt; echo ''>>spots.txt; done;')
                # print command

                # self.ena.send(command)
                # wait_execution(self.ena)
                # execute_command(command, 'fg_cur')
            if bams:
                # print 'calculating bam spots'
                commands.append('for file in *.bam ; do echo -e -n "$file\\t" >>spots.txt; '
                                'samtools view "./$file"  | head -2 | tail -1 | wc -m >>spots.txt; echo ''>>spots.txt; ' \
                                'done;')


                # self.ena.send(command)
                # wait_execution(self.ena)
                # execute_command(command, 'fg_cur')
            bzs = [r.new_data_file for r in self.sdrf.rows if r.new_data_file.endswith('.bz2')]
            if bzs:
                # print 'calculating bz2 spots'
                # self.ena.send(
                #     'for file in *.bz2; do echo -e -n "$file\\t" >>spots.txt; bzcat "./$file"  | head -2 | tail -1 | wc -m >>spots.txt; echo ''>>spots.txt; done;  \n')
                # wait_execution(self.ena)
                commands.append(
                    'for file in *.bz2; do echo -e -n "$file\\t" >>spots.txt; bzcat '
                    '"./$file"  | head -2 | tail -1 | wc -m >>spots.txt; echo ''>>spots.txt; done;' )
            print commands
            spot_sh = os.path.join(self.local_tmp, 'spots.sh')
            f = open(spot_sh, 'w')
            f.write('\n'.join(commands))
            f.close()
            # execute_command('scp  sra-login-2:')
            # print 'copying spots'
            # self.plantain.send(
            #     'scp sra-login-2:/fire/staging/aexpress/%s/spots.txt %s\n' % (
            #         self.ena_dir, self.exp_path))
            # wait_execution(self.plantain)
            execute_command(
                'scp %s sra-login-2:/fire/staging/aexpress/%s/' % (
                    spot_sh, self.ena_dir), 'fg_cur')
            execute_command("ssh sra-login-2 'cd %s;sh ./spots.sh'" % self.ena_full_path, 'fg_cur')
            execute_command(
                'scp sra-login-2:/fire/staging/aexpress/%s/spots.txt %s' % (
                     self.ena_dir, self.exp_path), 'fg_cur')
            # print 'retrieving spots local'

            shutil.copyfile(os.path.join(self.exp_path, 'spots.txt'),
                            local_file)
        f = open(local_file, 'r')
        lines = f.readlines()
        f.close()
        print lines
        for line in lines:
            if line.strip() == '':
                continue
            print line.strip().split('\t')
            f, num = line.strip().split('\t')
            files[f] = int(num) - 1

        for row in self.sdrf.rows:

            if not (row.is_paired or '.csfasta' in row.new_data_file or '.qual' in row.new_data_file):
                files[row.data_file] = None
                continue
            if row.data_file not in files.keys():
                if row.spot_length:
                    files[row.data_file] = int(row.spot_length)

        print colored.green('Spot Length Done')
        return files

    def export_experiment(self):
        subprocess.call('source %s; reset_experiment.pl -e %s\n' % (settings.BASH_PATH, self.exp_dir),
                        shell=True, env=dict(ENV=settings.BASH_PATH))

    def extract_ena_accession_dir(self):
        r = retrieve_submission_by_accession(self.accession)
        if r and len(r) > 0:
            return r[0]['ftpSubDirectory']
        # self.ena.send("find /fire/staging/aexpress/E-MTAB-* -name '%s-*'\n" % self.accession)
        # lines = [i for i in wait_execution(self.ena).split('\n') if self.accession in i]
        # out = '\n'.join(
        #     execute_command(
        #         "ssh sra-login-2 'find /fire/staging/aexpress/E-MTAB-* -name \"%s-*\" '" % self.accession,
        #         'fg_cur'
        #     )
        # )
        # lines = [i for i in out.split('\n') if self.accession in i]
        # # print lines
        # if len([l for l in lines if 'find' not in l]) > 0:
        #     dir_name = [l for l in lines if '/fire/staging/aexpress/' in l and 'find' not in l and self.accession in l][
        #         0].strip().split('/')[-1]
        #     print colored.blue(dir_name)
        #     return dir_name
        return self.accession

    def rename_back(self):
        if self.renamed:
            for row in self.sdrf.rows:
                if row.new_data_file != row.data_file:
                    # self.ena.send('mv %s %s\n' % (row.new_data_file, row.data_file))
                    # wait_execution(self.ena)
                    execute_command(
                        "ssh sra-login-2 'cd %s;mv %s %s'" % (self.ena_full_pathrow.new_data_file, row.data_file),
                        'fg_cur'
                    )


def parse_arguments():
    parser = argparse.ArgumentParser(description='submits and loads sequencing experiment to ENA and ArrayExpress')
    parser.add_argument('dir_name', metavar='MAGE-TAB_xxxx', type=str,
                        help='''The directory name where the submission meta-date files exists.
                                If used without the base_dir argument then the default base directory is:
                                 /ebi/microarray/ma-exp/AutoSubmissions/annotare/''')
    parser.add_argument('accession', metavar='E-MTAB-xxxx', type=str,
                        help='''The accession number for the experiment''')
    parser.add_argument('-as', '--add_samples', action='store_true',
                        help='A flag for adding new samples to existing experiment.')
    parser.add_argument('-t', '--test', action='store_true',
                        help='The submission will be submitted to ENA Dev server.')
    parser.add_argument('-cp', '--combined_pairs', action='store_true',
                        help='A flag to tell the system that all the pairs are combined. So that, any similarity would be considered as technical replica')
    parser.add_argument('-mp', '--mixed_pairs', action='store_true',
                        help='A flag to tell the system that the pairs are combined and not combined.')
    parser.add_argument('-m', '--move', action='store_true',
                        help='A flag for moving files from the root FTP dir.')
    parser.add_argument('-bd', '--base_dir', metavar='path/to/experiment/directory/__without__/MAGE-TAB_xxx', type=str,
                        help="""The base directory for the experiment's data.
                       If not given the default value is /ebi/microarray/ma-exp/AutoSubmissions/annotare/""")
    parser.add_argument('-ed', '--ena_dir', metavar='path/to/fastq/files/directory/', type=str,
                        help="""The location of fastq files on ENA machine.
                       If not given the default value is /fire/staging/aexpress/""")
    parser.add_argument('-ic', '--is_combined', action='store_true',
                        help='A flag indicating that the IDF and SDRF are in the same file.')
    parser.add_argument('-sv', '--skip_validation', action='store_true',
                        help='A flag for skipping validate fastq files.')
    parser.add_argument('-sc', '--skip_copy', action='store_true',
                        help='A flag for skipping copying fastq files.')
    parser.add_argument('-ses', '--skip_ena_submission', action='store_true',
                        help='A flag for skipping submission to ENA.')
    parser.add_argument('-vb', '--validated_before', action='store_true',
                        help='A flag if the fastq files where validated before.')
    parser.add_argument('-vo', '--validate_only', action='store_true',
                        help='A flag to quite after validation.')
    parser.add_argument('-cf', '--combined_file_name',
                        help='This is required in case --is_combined is true. The name of the file which contians the IDF and SDRF')
    parser.add_argument('-i', '--idf',
                        help='The idf file name.')
    parser.add_argument('-s', '--sdrf',
                        help='The SDRF file_name')
    parser.add_argument('-ce', '--conan_email',
                        help='The email used to submit to Conan. The default is ahmed@ebi.ac.uk')
    parser.add_argument('-d', '--date',
                        help='For correction usage only')
    parser.add_argument('-na', '--new_alias',
                        help='suffix for ENA alias names')
    parser.add_argument('-sd', '--skip_date',
                        help='skip changing the release date')
    parser.add_argument('-rs', '--reuse_samples', action='store_true',
                        help='''A flag indicating that there are samples to be reused.
                    In this case an existing SDRF with the sample names and their ENA accessions must be provided.''')
    parser.add_argument('-ns', '--no_spots', action='store_true',
                        help='''A flag indicating that the spots have been calculated before.''')
    parser.add_argument('-oed', '--other_experiment_dir',
                        help='''full directory containing the unpacked folder which has the combined MAGE-TAB containing the already submitted samples to be reused.
                        Must have ENA accessions or Biostudies IDs and the same sample names.
                        Required when --reuse_sample option is used.''')
    parser.add_argument('-np', '--neglect_patterns', nargs='+', metavar='patern1 patern2 ...',
                        help='List of patterns to be neglected from file names when trying to find pairs')
    return parser


if __name__ == '__main__':

    parser = parse_arguments()
    args = parser.parse_args()
    if args.is_combined and not args.combined_file_name:
        print '--combined_file_name is required'
        print parser.print_help()
        exit()
    ena = ENASubmission(exp_dir=args.dir_name, accession=args.accession,
                        meta_data_bas_dir=args.base_dir,
                        ena_optional_dir=args.ena_dir, combined_mage_tab=args.is_combined,
                        combined_file_name=args.combined_file_name,
                        conan_email=args.conan_email, skip_validation=args.skip_validation,
                        skip_copy=args.skip_copy, validated_before=args.validated_before,
                        skip_ena_submission=args.skip_ena_submission,
                        add_samples=args.add_samples,
                        receipt_date=args.date, new_alias=args.new_alias,
                        skip_date=args.skip_date,
                        reuse_samples=args.reuse_samples,
                        other_experiment_dir=args.other_experiment_dir,
                        move=args.move,
                        neglect_patterns=args.neglect_patterns,
                        combined_pairs=args.combined_pairs, validate_only=args.validate_only,
                        mixed_pairs=args.mixed_pairs,
                        no_spots=args.no_spots,
                        idf=args.idf,
                        sdrf=args.sdrf,
                        test=args.test)
    ena.submit_experiment()

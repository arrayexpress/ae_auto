import os
import shutil
import time
from collections import OrderedDict

# from automation.ena.ena_brokering import ENASubmission, parse_arguments
from clint.textui import colored

from dal.mysql.ae_autosubs.autosubs_transaction import retrive_expid_username_by_acc
from dal.mysql.annotare.submission import retrieve_submission_by_accession
from models.magetab.sdrf import SdrfCollection
import argparse

from settings import AUTOSUB_DIR, BAM_GENERATOR_PATH, ENA_DIR, TEMP_FOLDER, FTP_GATE
from utils.common import execute_command, exists_remote
from utils.lsf.cluster_job import Job

import itertools as it

__author__ = 'Ahmed G. Ali'


#
# DATA_DIR = ''
# LOCAL_TMP = ''

ERROR = []
def common_start(strings):
    """ Returns the longest common substring
        from the beginning of the `strings`
    """
    print strings

    def _iter():
        for z in zip(*strings):
            print z
            if z.count(z[0]) == len(z):  # check all elements in `z` are the same
                yield z[0]
            else:
                return

    return ''.join(_iter())


def get_command(read1, read2, index1, index2, schema, bam_file, data_dir):
    command = 'cd {data_dir};fastq2bam -b {bam_file} -s {scheme} -1 {read1} '.format(
        bam_file=bam_file, scheme=schema, read1=read1,
        data_dir=os.path.join(ENA_DIR, data_dir))
    counter = 2
    if read1 != read2:
        command += ' -{counter} {read}'.format(counter=counter, read=read2)
        counter += 1
    if index1:
        command += ' -{counter} {read}'.format(counter=counter, read=index1)
        counter += 1
    if index2:
        command += ' -{counter} {read}'.format(counter=counter, read=index2)
        # counter +=1
    # print(command)
    return command


class BAM10X:
    def __init__(self, acc, sdrf_path):
        self.added_files = []
        self.acc = acc
        self.sdrf_path = sdrf_path
        self.data_dir = ''
        self.local_tmp = os.path.join(TEMP_FOLDER, self.acc)
        if not os.path.exists(self.local_tmp):
            os.makedirs(self.local_tmp)
        file_name = sdrf_path.split(os.pathsep)[-1]
        if not os.path.exists(os.path.join(sdrf_path.split(os.pathsep)[:-1], file_name + '_orignial')):
            shutil.copy(sdrf_path, os.path.join(sdrf_path.split(os.pathsep)[:-1], file_name + '_orignial'))
        f = open(sdrf_path, 'r')
        lines = f.readlines()
        f.close()
        self.original_header = lines[0].strip().split('\t')
        header = [i.lower().replace('comment', '').replace('[', '').replace(']', '').replace(' ', '_')
                  for i in lines[0].strip().split('\t')]
        self.read_1 = None
        self.read_2 = None
        self.index_1 = None
        self.index_2 = None
        if 'read1_file' in header:
            self.read_1 = header.index('read1_file')
        if 'read2_file' in header:
            self.read_2 = header.index('read2_file')
        if 'index1_file' in header:
            self.index_1 = header.index('index1_file')
        if 'index2_file' in header:
            self.index_2 = header.index('index2_file')

        self.assay = header.index('assay_name')
        self.schema = header.index('library_construction')
        r = retrieve_submission_by_accession(self.acc)
        self.commands = {}
        self.bams = OrderedDict({})
        self.bams_md5 = {}
        self.data_dir = ''
        if r and len(r) > 0:
            self.data_dir = r[0]['ftpSubDirectory']

        assays = {}
        for l in lines[1:]:
            cells = l.strip().split('\t')
            read1 = cells[self.read_1] if self.read_1 else None
            read2 = cells[self.read_2] if self.read_2 else None
            index1 = cells[self.index_1] if self.index_1 else None
            index2 = cells[self.index_2] if self.index_2 else None
            schema = cells[self.schema]
            assay = cells[self.assay].strip().replace(' ', '_')
            key = (read1, read2, index1, index2)
            self.added_files+=list(key)
            if key in assays.keys():
                continue
            i = 1
            while assay in assays.values():
                assay = '%s_%s' % (assay, str(i))
                i += 1
            assays[key] = assay
            bam_file = assay + '.bam'

            self.bams[bam_file] = cells

            command = get_command(read1=read1, read2=read2, index1=index1,
                                  index2=index2, schema=schema, data_dir=self.data_dir, bam_file=bam_file)
            if 'cell_barcode_offset' in header:
                command += ' -c ' + cells[header.index('cell_barcode_offset')]
            if 'cell_barcode_size' in header:
                command += ' -C ' + cells[header.index('cell_barcode_size')]
            if 'umi_barcode_offset' in header:
                command += ' -u ' + cells[header.index('umi_barcode_offset')]
            if 'umi_barcode_size' in header:
                command += ' -U ' + cells[header.index('umi_barcode_size')]
            if 'sample_barcode_offset' in header:
                command += ' -z ' + cells[header.index('sample_barcode_offset')]
            if 'sample_barcode_size' in header:
                command += ' -Z ' + cells[header.index('sample_barcode_size')]
            self.commands[bam_file] = command
            # print(command)
            # exit()
        self.write_lines = []

        self.converter_bams()
        self.get_md5()
        # print(self.bams_md5)
        self.export_sdrf()

    def export_sdrf(self):
        header = self.original_header[:]
        insert_read1 = False
        if self.read_1:
            index = self.original_header.index('Comment[read1 file]') + 1
            if self.original_header[index] != 'Comment[FASTQ_URI]':
                self.original_header.insert(index, 'Comment[FASTQ_URI]')
                insert_read1 = True
        insert_read2 = False
        if self.read_2:
            index = self.original_header.index('Comment[read2 file]') + 1
            if self.original_header[index] != 'Comment[FASTQ_URI]':
                self.original_header.insert(index, 'Comment[FASTQ_URI]')
                insert_read2 = True
        insert_index1 = False
        if self.index_1:
            index = self.original_header.index('Comment[index1 file]') + 1
            if self.original_header[index] != 'Comment[FASTQ_URI]':
                self.original_header.insert(index, 'Comment[FASTQ_URI]')
                insert_index1 = True
        insert_index2 = False
        if self.index_2:
            index = self.original_header.index('Comment[index2 file]') + 1
            if self.original_header[index] != 'Comment[FASTQ_URI]':
                self.original_header.insert(index, 'Comment[FASTQ_URI]')
                insert_index2 = True
        self.write_lines = []
        insert_md5 = False
        if 'Comment[MD5]' not in self.original_header:
            self.original_header.insert(self.original_header.index('Comment[Array Data File]') + 1, 'Comment[MD5]')
            insert_md5 = True

        for bam, cells in self.bams.items():
            read1 = cells[header.index('Comment[read1 file]')] if 'Comment[read1 file]' in header else None
            read2 = cells[header.index('Comment[read2 file]')] if 'Comment[read2 file]' in header else None
            index1 = cells[header.index('Comment[index1 file]')] if 'Comment[index1 file]' in header else None
            index2 = cells[header.index('Comment[index2 file]')] if 'Comment[index2 file]' in header else None
            # print ([read1, read2, index1, index2])
            # if 'Comment[Array Data File]' in header:
            #     data_file = cells[header.index('Comment[Array Data File]')]
            # elif 'Array Data File' in header:
            #     data_file = cells[header.index('Array Data File')]
            # else:
            #     raise Exception('Cannot find Data file\nHeader: ' + str(header) + '\nCells: ' + str(cells))

            # print(cells)
            # print(data_file)
            cells[header.index('Array Data File')] = bam
            if insert_read1:
                if read1:
                    cells[self.read_1] = cells[self.read_1] \
                                         + '\t' + \
                                         'ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/{acc}/{' \
                                         'f_name}'.format(
                                             acc=self.acc, f_name=read1)
                else:
                    cells[self.read_1] = cells[self.read_1] + '\t'

            if insert_read2:
                if read2:
                    cells[self.read_2] = cells[self.read_2] \
                                         + '\t' + \
                                         'ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/{acc}/{' \
                                         'f_name}'.format(
                                             acc=self.acc, f_name=read2)
                else:
                    cells[self.read_2] = cells[self.read_2] + '\t'
            if insert_index1:
                if index1:
                    cells[self.index_1] = cells[self.index_1] \
                                          + '\t' + \
                                          'ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/{acc}/{' \
                                          'f_name}'.format(
                                              acc=self.acc, f_name=index1)
                else:
                    cells[self.index_1] = cells[self.index_1] + '\t'
            if insert_index2:
                if index2:
                    cells[self.index_2] = cells[self.index_2] \
                                          + '\t' + \
                                          'ftp://ftp.ebi.ac.uk/pub/databases/microarray/data/experiment/MTAB/{acc}/{' \
                                          'f_name}'.format(
                                              acc=self.acc, f_name=index2)
                else:
                    cells[self.index_2] = cells[self.index_2] + '\t'

            if insert_md5:
                cells.insert(cells.index(bam) + 1, self.bams_md5[bam])
            else:
                cells[cells.index(bam) + 1] = self.bams_md5[bam]

            self.write_lines.append('\t'.join(cells))
        self.write_lines = ['\t'.join(self.original_header)] + self.write_lines
        f = open(self.sdrf_path, 'w')
        f.write('\n'.join(self.write_lines))
        f.close()

    def converter_bams(self):
        jobs = []
        completed = []
        error = False
        ena_data_dir = os.path.join(ENA_DIR, self.data_dir)
        for b_name, command in self.commands.items():
            # print(command)
            if not exists_remote(host='sra-login',
                                 path='{data_dir}/{file_name}'.format(file_name=b_name, data_dir=ena_data_dir),
                                 user='fg_cur'):
                j = Job(b_name, command=command, memory=20000, remote_host='sra-login', remote_user='fg_cur')
                j.submit()
                jobs.append(j)
            else:
                print('{} file exists, will not regenerate'.format(b_name))
        # return
        while len(jobs) > 0:
            print('converting {} bam files'.format(str(len(jobs))))
            time.sleep(60)
            for j in jobs:
                try:
                    if not j.is_alive():
                        completed.append(jobs.pop(jobs.index(j)))
                except Exception as e:
                    error = True
                    err_job = jobs.pop(jobs.index(j))
                    ERROR.append("""There was error generating {name}
                    {e}
                    Execution output for Job {id} is:\n{out}\n{err}""".format(name=err_job.name, e=str(e),
                                                                              id=err_job.job_id, out=err_job.out, err=err_job.error))
                    # print colored.red(e, bold=True)
                    # print colored.red('There was error generating {}'.format(err_job.name))
                    # print (
                    #     'Execution output for Job {} is:\n{}\n{}'.format(err_job.job_id, err_job.out, err_job.error))
        if error:
            err_path = os.path.join(TEMP_FOLDER, self.acc+'_10x.err.txt')
            f = open(err_path, 'w')
            f.write("===================================\n".join(ERROR))
            f.close()
            print colored.red('There was errors generating the bam files.\n Please check: %s'%err_path)
            exit(1)

    def get_md5(self):
        jobs = []
        error = False
        command = 'md5sum {data_dir}/{bam_file} > {data_dir}/{bam_file}.md5'
        ena_data_dir = os.path.join(ENA_DIR, self.data_dir)
        for b in self.bams:
            if not exists_remote(host='sra-login',
                                 path='{data_dir}/{file_name}.md5'.format(file_name=b, data_dir=ena_data_dir),
                                 user='fg_cur'):
                job = Job(name=b, command=command.format(data_dir=os.path.join(ENA_DIR, self.data_dir), bam_file=b),
                          memory=1000,
                          remote_host='sra-login', remote_user='fg_cur')
                job.submit()

                jobs.append(job)
            else:
                execute_command('scp sra-login:{data_dir}/{file_name}.md5 {local_tmp}'.format(
                    data_dir=ena_data_dir,
                    file_name=b,
                    local_tmp=self.local_tmp
                ), user='fg_cur')
                f = open(os.path.join(self.local_tmp, b + '.md5'), 'r')
                l = f.readline().strip().split(' ')

                if l == '':
                    job = Job(name=b, command=command.format(data_dir=os.path.join(ENA_DIR, self.data_dir), bam_file=b),
                              memory=1000,
                              remote_host='sra-login', remote_user='fg_cur')
                    job.submit()

                    jobs.append(job)
                else:
                    self.bams_md5[l[-1].split('/')[-1]] = l[0]
                f.close()
                # jobs.remove(job)

        while len(jobs) > 0:
            time.sleep(60)
            for job in jobs[:]:
                try:
                    if not job.is_alive():
                        execute_command('scp sra-login:{data_dir}/{md5}.md5 {local_tmp}'.format(
                            md5=job.name,
                            local_tmp=self.local_tmp,
                            data_dir=ena_data_dir
                        ), user='fg_cur')
                        f = open(os.path.join(self.local_tmp, job.name + '.md5'), 'r')
                        l = f.readline().strip().split(' ')

                        # self.bams_md5[l[1]] = l[-1]
                        self.bams_md5[l[-1].split('/')[-1]] = l[0]
                        f.close()
                        jobs.remove(job)
                except Exception as e:
                    error = True
                    ERROR.append("""There was error generating {name}
                    {e}
                    Execution output for Job {id} is:\n{out}\n{err}""".format(name=job.name, e=str(e),
                                                                              id=job.job_id, out=job.out, err=job.error))

                    # print colored.red(e, bold=True)
                    # print colored.red('There was error generating {}'.format(job.name))
                    # print colored.red('Execution output for Job {} is:\n{}\n{}'.format(job.job_id, job.out,
                    #                                                                    job.error))
                    jobs.remove(job)
        if error:
            err_path = os.path.join(TEMP_FOLDER, acc + '_10x.err.txt')
            f = open(err_path, 'w')
            f.write("===================================\n".join(ERROR))
            f.close()
            print colored.red('There was errors generating the md5sum.\n Please check: %s'%err_path)
            exit(1)

    def after_broker(self, sub_dir):
        # print(self.added_files)
        self.added_files = [i for i in list(set(self.added_files)) if i is not None]
        ena_dir = os.path.join(ENA_DIR, self.data_dir)
        # subs_data_dir = os.path.join(sub_dir, self.acc)
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)

        for file_name in self.added_files:
            if not os.path.exists(os.path.join(sub_dir, file_name)):
                cmd = 'scp sra-login:{data_dir}/{file_name} {sub_dir}/'.format(
                    data_dir=ena_dir,
                    file_name=file_name,
                    sub_dir=sub_dir
                )
                print colored.green("copying {} from ENA staging to load dir".format(file_name))
                print(execute_command(cmd, user='fg_cur'))
            else:
                print colored.magenta("%s already exists in load dir. Not copying")


if __name__ == '__main__':
    from sys import argv

    # run_bam_converter('E-MTAB-6505', '91109')
    # exit()
    # parser = parse_arguments()
    # acc = 'E-MTAB-6831'
    # acc = 'E-MTAB-8119'
    # acc = 'E-MTAB-6831'
    # # acc = 'E-MTAB-6854'
    # # _sdrf_path = '/ebi/microarray/ma-exp/AutoSubmissions/annotare/MAGE-TAB_91109/unpacked/submission5969_annotare_v4.sdrf.txt'
    # # _sdrf_path = '/home/gemmy/PycharmProjects/ae_automation/tmp/submission7367_annotare_v1.sdrf.txt'
    # _sdrf_path = '/home/gemmy/PycharmProjects/ae_automation/tmp/E-MTAB-8119.sdrf.txt'
    # _sdrf_path = '/home/gemmy/PycharmProjects/ae_automation/tmp/E-MTAB-6831.sdrf.txt'
    from sys import argv

    acc = argv[1]
    _sdrf_path = argv[2]
    conv = BAM10X(acc, _sdrf_path)

    # main(acc, _sdrf_path)

    # get_def('read-I1_si-ACTTCACT_lane-001-chunk-001.fastq.gz',
    #         'read-RA_si-ACTTCACT_lane-001-chunk-001.fastq.gz')

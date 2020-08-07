import json
import os
import shutil
import sys
import time

from clint.textui import colored

from models.lsf_data_file import FileObject
from models.magetab.sdrf import SdrfCollection
from models.pair import Pair
from settings import TEMP_FOLDER, ENA_DIR, LOCAL_EXECUTION
from utils.common import execute_command
from utils.email.sender import send_email

# Django Setup and Imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ae_web')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ae_web.settings")

import django

django.setup()

from maintenance.models import Validate

__author__ = 'Ahmed G. Ali'


def copy_files(ena_dir, local_dir):
    """Copying the data directory for the the study from ENA machine to EBI local cluster.

    :param ena_dir: The directory containing data files to be validated and also the SDRF file.
        This directory should be in `/fire/staging/aexpress/`
    :type ena_dir: str
    :param local_dir: The temp directory created on the local shared storage. This is removed after the validation ended.
    :type local_dir: str
    :return: std_out and std_err of the copy command.
    :rtype: :obj:`tuple` of :obj:`str`
    """
    if not os.path.exists(local_dir):
        print 'creating %s' % local_dir
        os.mkdir(local_dir)
    cmd = 'scp -oStrictHostKeyChecking=no  sra-login:%s/*.txt %s' % (ena_dir, local_dir)
    print cmd
    if LOCAL_EXECUTION:
        out, err = execute_command('cp  %s/*.txt %s' % (ena_dir, local_dir))
    else:
        out, err = execute_command(cmd)
    print 'executed'
    return out, err


def validate(req_id, ena_dir):
    """
    Validates fastq files for a seq submission. This method is called by the Django API.
    It create a new DB record for the validation job that can be retrieved by the calling the check endpoint.
    
    Jobs statuses are:
        - P => Pending (used when the job is still running, or execution errors appeared)
        - F ==> Failed
        - V ==> Valid
     
    :param req_id: The request ID used by the client as a unique identifier for their job.
    :type req_id: str
    :param ena_dir: The directory on ENA machine that containing the datafiles and the SDRF.
    :type ena_dir: str

    """
    report = {'file_errors': {}, 'pairs_errors': [], 'valid_files': [], 'execution_errors': [], 'integrity_errors': []}
    v = Validate.objects.filter(job_id=req_id)
    if not v:
        v = Validate(job_id=str(req_id), data_dir=ena_dir)
        v.save()
    else:
        v = v[0]
    dir_name = ena_dir.split('/')[-1]
    if ena_dir.endswith('/'):
        dir_name = ena_dir.split('/')[-2]
    print ena_dir
    print dir_name
    try:
        local_dir = os.path.join(TEMP_FOLDER, str(req_id) + dir_name)
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)
        if not ena_dir.startswith(ENA_DIR):
            ena_dir = os.path.join(ENA_DIR, ena_dir)
        out, err = copy_files(ena_dir, local_dir)
        print out
        print err
        if err:
            report['execution_errors'].append(err)
        sdrf_file = ''
        data_files = []
        pairs = []

        for f in os.listdir(local_dir):
            if f.endswith('.sdrf.txt'):
                sdrf_file = os.path.join(local_dir, f)
                break
        try:
            sdrf = SdrfCollection(sdrf_file)
        except Exception, e:
            report['integrity_errors'].append(str(e))
            v.status = 'F'
            v.validation_report = json.dumps(report)
            v.save()
            return

        for i in range(len(sdrf.rows)):
            r = sdrf.rows[i]
            if r.is_paired:
                continue
            print colored.yellow(str(dict(out_file=os.path.join(local_dir, str(i + 1)),
                                          name=str(i + 1),
                                          file_name=r.data_file,
                                          base_dir=local_dir,
                                          ena_dir=ena_dir)))
            data_file = FileObject(out_file=os.path.join(local_dir, str(i + 1)),
                                   name=str(i + 1),
                                   file_name=r.data_file,
                                   base_dir=local_dir,
                                   ena_dir=ena_dir)
            data_file.start()
            data_files.append(data_file)

        for p1, p2 in sdrf.pairs:
            p = Pair(p1.data_file, p2.data_file, local_dir, ena_dir)
            p.run()

            pairs.append(p)

        live = True
        while live:
            time.sleep(10)
            p_live = False
            f_live = False
            for p in pairs:
                if p.is_alive():
                    p_live = True
                    break
            for f in data_files:
                if f.is_alive():
                    f_live = True
                    break
            live = f_live or p_live
        for p in pairs:
            if not p.errors:
                if p.file_1.errors:
                    report['file_errors'][p.file_1.file_name] = p.file_1.errors
                else:
                    report['valid_files'].append(p.file_1.file_name)
                if p.file_2.errors:
                    report['file_errors'][p.file_2.file_name] = p.file_2.errors

                else:
                    report['valid_files'].append(p.file_2.file_name)

                if p.file_1.execution_error:
                    report['execution_errors'].append(p.file_1.execution_error)
                if p.file_2.execution_error:
                    report['execution_errors'].append(p.file_2.execution_error)

            report['pairs_errors'] += p.errors

        for data_file in data_files:
            if data_file.errors:
                report['file_errors'][data_file.file_name] = data_file.errors
            else:
                report['valid_files'].append(data_file.file_name)
            if data_file.execution_error:
                report['execution_errors'].append(data_file.execution_error)
                shutil.rmtree(local_dir)
    except Exception, e:

        report['execution_errors'].append(str(e))

    v.validation_report = json.dumps(report)

    v.status = 'V'

    if report['execution_errors']:
        v.status = 'P'
        send_email(from_email='AE Automation<ae-automation@ebi.ac.uk>',
                   to_emails=['ahmed@ebi.ac.uk', 'awais@ebi.ac.uk'],
                   subject='Validation Execution Error',
                   body="""ID: %s\nError: %s""" % (req_id, str(report['execution_errors'])))
    elif report['file_errors'] or report['integrity_errors'] or report['pairs_errors']:
        v.status = 'F'
    v.save()
    print report


if __name__ == '__main__':
    from random import randint
    from sys import argv
    #validate(randint(1, 99999999), 'pairs')
    validate(argv[1], argv[2])

import StringIO
import os
import threading
import time

from dateutil.parser import parse

import settings
from dal.oracle.ae2.study import extract_geo_studies_without_ena_accessions
from dal.oracle.conan.conan_tasks import retrieve_job_status
from dal.oracle.era.study import extract_geo_studies
from models.conan import CONAN_PIPELINES
from resources.ssh import retrieve_banana_connection, get_ssh_out
from utils.conan.conan import submit_conan_task

__author__ = 'Ahmed G. Ali'

DIR = '/nfs/ma/home/fgpt/sw/lib/perl/supporting_files/geo_import_supporting_files/'


def unload_experiment(accession):
    # conan = ConanPage(url=settings.CONAN_URL)
    # conan.login(login_email=settings.CONAN_LOGIN_EMAIL)

    print 'unloading : ', accession
    # conan.unload_experiment(accession)
    submit_conan_task(accession=accession, pipeline_name=CONAN_PIPELINES.unload)
    job_status = retrieve_job_status(accession)
    while job_status != 'COMPLETED':
        print 'waiting for %s, Job status: %s' % (accession, job_status)
        if job_status == 'FAILED':
            raise Exception('%s Unload Failed' % accession)
        time.sleep(30)
        job_status = retrieve_job_status(accession)


def manage_threads(accessions):
    threads = []
    for acc in accessions:
        t = threading.Thread(target=unload_experiment, args=(acc,))
        threads.append(t)
        t.daemon = False
    running = []
    while True:
        while len(running) <= 10 and threads:
            t = threads.pop()
            t.start()
            time.sleep(3)
            running.append(t)
        if not running:
            break
        for t in running:
            if not t.is_alive():
                print 'removing thread'
                running.remove(t)
                break
        print 'Running Threads: ', len(running)
        print 'pending Threads: ', len(threads)
        time.sleep(30)


def add_ena_accession():
    banana, banana_ssh = retrieve_banana_connection()
    local_file, latest_file = retrieve_lates_file(banana, banana_ssh)
    accessions = extract_geo_accessions(local_file)
    manage_threads(accessions)
    banana.send('cd %s\n' % DIR)
    banana.send('/ebi/microarray/home/fgpt/sw/lib/perl/FGPT_CentOS_prod/import_geo_subs.pl -f %s &\n' %
                os.path.join(DIR, latest_file))
    print get_ssh_out(banana)
    banana_ssh.close()
    print 'job submitted'


def extract_geo_accessions(local_file):
    f = open(local_file, 'r')
    lines = f.readlines()
    f.close()
    accessions = []
    for l in lines:
        accessions.append('E-GEOD-' + l.strip().split('\t')[0].replace('GSE', '').replace('GDS', ''))
    return accessions


def retrieve_lates_file(banana, banana_ssh):
    banana.send('ls %s\n' % DIR)
    res = StringIO.StringIO(get_ssh_out(banana))
    dates = []
    for line in res.readlines():
        print line
        if 'reimport_accessions' not in line:
            continue
        dates += [parse(i.strip(), fuzzy=True) for i in line.split('\t') if 'reimport_accessions' in i]
    latest_file = 'reimport_accessions_' + max(dates).date().isoformat()
    sftp = banana_ssh.open_sftp()
    local_file = os.path.join(settings.TEMP_FOLDER, latest_file)
    sftp.get(os.path.join(DIR, latest_file), local_file)
    sftp.close()
    return local_file, latest_file


def main():
    geo_acc=[]

    ena_geo_studies = [i.study_alias for i in extract_geo_studies()]
    ae_geo_without_ena_acc = extract_geo_studies_without_ena_accessions()

    geo_acc += [a for a in ae_geo_without_ena_acc if a not in ena_geo_studies]




if __name__ == '__main__':
    add_ena_accession()

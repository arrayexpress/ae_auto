import argparse
import threading
import time

import settings
from dal.oracle.conan.conan_tasks import retrieve_job_status
from models.conan import CONAN_PIPELINES
from utils.conan.conan import submit_conan_task

__author__ = 'Ahmed G. Ali'


def clean_experiment(accession, email=None):
    # conan = ConanPage(url=settings.CONAN_URL)
    if not email:
        email = settings.CONAN_LOGIN_EMAIL
    # conan.login(login_email=email)
    # conan.clean_experiment(accession)
    submit_conan_task(accession=accession, pipeline_name=CONAN_PIPELINES.unload, starting_index=1)
    job_status = retrieve_job_status(accession)
    while job_status != 'COMPLETED':
        if job_status == 'FAILED':
            raise Exception('Clean Failed for ' + accession)
        time.sleep(30)
        job_status = retrieve_job_status(accession)


def extract_args():
    parser = argparse.ArgumentParser(
        description='Cleans experiments FTP using Conan Unload pipeline with clean experiments')
    parser.add_argument('accessions', nargs='+', metavar='E-ERAD-xxxx E-ERAD-yyy E-GEOD-zzzz',
                        help='List of accession numbers')
    parser.add_argument('-e', '--email', metavar='name@domain.com', help='Conan login email')
    return parser.parse_args()


def main(accessions, email):
    threads = []
    for acc in accessions:
        acc = acc.replace(',', '').strip()
        print acc
        # continue
        t = threading.Thread(target=clean_experiment, args=(acc, email))
        threads.append(t)
        t.daemon = False
        # t.start()

        # reload_experiment(accession=acc)
    running = []
    while True:
        while len(running) <= 10 and threads:
            t = threads.pop()
            t.start()
            running.append(t)
            time.sleep(5)
        if not running:
            break
        for t in running:
            if not t.is_alive():
                print 'removing thread'
                running.remove(t)
                break
        print 'Running Threads: ', len(running)
        print 'pending Threads: ', len(threads)
        time.sleep(60)


def extract_accessions():
    pass


if __name__ == '__main__':
    args = extract_args()
    if args.email:
        settings.CONAN_LOGIN_EMAIL = args.email
    accessions = extract_accessions()
    main(accessions, email=args.email)

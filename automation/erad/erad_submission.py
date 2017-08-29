import argparse
import os
import threading
import time
from clint.textui import colored
import settings
from dal.mysql.ae_autosubs.experiments import retrieve_experiment_status
from dal.oracle.conan.conan_tasks import retrieve_task, update_task_status_by_id
from models.conan import CONAN_PIPELINES
from utils.conan.conan import submit_conan_task
from utils.email.sender import send_email
from pwd import getpwuid

CONAN_LOGIN_EMAIL = settings.CONAN_LOGIN_EMAIL

__author__ = 'Ahmed G. Ali'

RED_FLAG = []
LOCK = threading.Lock()
REPORT = {}


def reload_experiment(accession):
    exp_path = os.path.join(settings.EXPERIMENTS_PATH, 'ERAD', accession, 'atlas')
    if os.path.exists(exp_path):
        return
    global RED_FLAG, REPORT
    skip_unload = False
    unload_failed = False

    task = retrieve_task(accession)
    unload_id = None
    if task and task.state == 'FAILED':
        unload_id = task.id
        print colored.green('%s found failed in unloading from a previous trial. Trying to load!' % accession)
        abort_task(task)
        skip_unload = True
        unload_failed = True

    # conan = ConanPage(url=settings.CONAN_URL)
    # conan.login(login_email=settings.CONAN_LOGIN_EMAIL)
    if not skip_unload:
        # conan.unload_experiment(accession)
        submit_conan_task(accession=accession, pipeline_name=CONAN_PIPELINES.unload)
        task = retrieve_task(accession)
        unload_id = task.id
        while task.state != 'COMPLETED':
            if task.state == 'FAILED':
                print colored.blue('%s Unload Failed\nTrying to load' % accession, bold=True)
                abort_task(task)
                unload_failed = True
                break
                # raise Exception('%s Unload Failed' % accession)
            time.sleep(30)
            task = retrieve_task(accession)
    load = wait_for_ae_export(accession)
    if load:
        # conan.load_experiment(accession)
        submit_conan_task(accession=accession, pipeline_name=CONAN_PIPELINES.load)

        task = retrieve_task(accession)
        load_id = task.id
        while task.state != 'COMPLETED':
            if task.state == 'FAILED':
                print colored.blue('%s Loading Failed. ' % accession, bold=True)
                if unload_failed:
                    print colored.red('%s Failed in both unloading and loading' % accession, bold=True)
                    abort_task(task)
                    with LOCK:
                        RED_FLAG.append(colored.red(('''%s Failed in both unloading and loading. Check below URLs:
                        Unload: %s/summary/%s
                        Load: %s/summary/%s''' % (accession, settings.CONAN_URL,
                                                  unload_id, settings.CONAN_URL,
                                                  load_id)).replace('//', '/'), bold=True))
                        REPORT[accession] += ('''Failed in both unloading and loading. Check below URLs:
                        Unload: %s/summary/%s
                        Load: %s/summary/%s''' % (settings.CONAN_URL,
                                                  unload_id, settings.CONAN_URL,
                                                  load_id)).replace('//', '/')
                return

            time.sleep(30)
            task = retrieve_task(accession)
    with LOCK:
        REPORT[accession] += 'Reloaded successfully'


def abort_task(task):
    before_after = 'before'
    if task.current_executed_index > 0:
        before_after = 'after'
    update_task_status_by_id(id=task.id, status='ABORTED',
                             status_message=task.status_message.replace('Failed at', 'Aborted ' + before_after))


def extract_args():
    parser = argparse.ArgumentParser(description='Reloads ERAD experiments into ArrayExpress using Conan')
    parser.add_argument('accessions', nargs='+', metavar='E-ERAD-xxxx E-ERAD-yyy E-ERAD-zzzz',
                        help='List of accession numbers')
    parser.add_argument('-e', '--email', metavar='name@domain.com', help='Conan login email')
    return parser.parse_args()


def wait_for_ae_export(accession):
    status = retrieve_experiment_status(accession)

    while status != 'AE2 Export Complete':
        print status
        time.sleep(30)
        status = retrieve_experiment_status(accession)
        if status in ['Export failed', 'Checking failed', 'Abandoned', '** CHECKER CRASH **',
                      'MAGE-TAB export failed', 'Validation failed']:
            with LOCK:
                REPORT[accession] += 'Failure: Experiment Reset Failed'
                print colored.red('Failure: Experiment Reset Failed')
            return False
    return True


def generate_atlas_curated_report(accessions):
    report = ''
    for acc in accessions:
        exp_path = os.path.join(settings.EXPERIMENTS_PATH, 'ERAD', acc, 'atlas')
        if os.path.exists(exp_path):
            owner = getpwuid(os.stat(exp_path).st_uid).pw_name
            report += """%s  |  %s\n""" % (acc, owner)
    if report != '':
        header = 'Accession     Curator'
        report = """The following experiment were previously curated for Atlas and now should be updated:\n\n%s\n%s\n""" %\
                 (header, '=' * (len(header)+3)) + report
    return report


def manage_threads(accessions):
    global REPORT
    threads = []
    for acc in accessions:
        # REPORT[acc] = ''
        # reload_experiment(acc)
        # break
        # print acc
        REPORT[acc] = ''
        t = threading.Thread(target=reload_experiment, args=(acc,))
        threads.append(t)
        t.daemon = False
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
        print 'Running Experiments: ', len(running)
        print 'pending Experiments: ', len(threads)
        time.sleep(30)
    if RED_FLAG:
        print colored.green('-' * 50 + '\nFAILURE REPORT\n' + '=' * 50)
    for flag in RED_FLAG:
        print flag
    msg = """This report is about ERAD experiments Loaded/updated in ArrayExpress.\n\n"""
    for k, v in REPORT.items():
        msg += """%s\t%s\n""" % (k, v)
    msg += '\n\n' + generate_atlas_curated_report(accessions)
    msg += """
This email was sent automatically from the AE Automation Tool.
Thank You!
AE Automation Tool."""
    send_email(from_email=settings.AUTOMATION_EMAIL, to_emails=[settings.CURATION_EMAIL], subject='ERAD Update Report',
               body=msg)
    print REPORT


if __name__ == '__main__':
    args = extract_args()
    if args.email:
        CONAN_LOGIN_EMAIL = args.email

    manage_threads(list(set(args.accessions)))

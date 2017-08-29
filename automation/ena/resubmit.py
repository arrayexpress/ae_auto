import threading
import time

from automation.ena.ena_brokering import ENASubmission

__author__ = 'Ahmed G. Ali'
experiments = '''ahmed_a7a E-MTAB-3851'''
# MAGE_8337 E-MTAB-94848373'''

def reload_experiment(dir_name, accession):
    # conan = ConanPage(url=settings.CONAN_URL)
    # conan.login(login_email=settings.CONAN_LOGIN_EMAIL)
    # conan.unload_experiment(accession)
    # job_status = retrieve_job_status(accession)
    # while job_status != 'COMPLETED':
    #     if job_status == 'FAILED':
    #         break
    #         raise Exception('%s Unload Failed' % accession)
    #     time.sleep(30)
    #     job_status = retrieve_job_status(accession)
    ena = ENASubmission(exp_dir=dir_name, accession=accession, skip_validation=True, new_alias='_resub', replace_idf=True)
    ena.submit_experiment()
    # conan.load_experiment(accession)
    # job_status = retrieve_job_status(accession)
    # while job_status != 'COMPLETED':
    #     if job_status == 'FAILED':
    #         raise Exception('Loading Failed')
    #     time.sleep(30)
    #     job_status = retrieve_job_status(accession)



def main():
    threads = []
    for line in experiments.split('\n'):
        folder, acc = line.strip().split(' ')
        t = threading.Thread(target=reload_experiment, args=(folder, acc))
        threads.append(t)
        t.daemon = False
    running = []
    while True:
        while len(running) <= 3 and threads:
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
        time.sleep(30)

if __name__ == '__main__':
    main()
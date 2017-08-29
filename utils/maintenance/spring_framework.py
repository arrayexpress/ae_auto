import time

from utils.common import execute_command

__author__ = 'Ahmed G. Ali'


def get_jobs_ids():
    out, err = execute_command('ssh banana "source /etc/profile.d/lsf.sh;bjobs -w | grep server"')
    ids = []
    for l in out.split('\n'):
        try:
            ids.append(int(l.split(' ')[0]))
        except:
            print l
    return ids


def kill_jobs(job_ids):
    print 'start kill'

    for i in job_ids:
        out, err = execute_command('ssh banana "source /etc/profile.d/lsf.sh;bkill -r %d"' % i)
        # print out, err
    # print 'end kill'
    while True:
        ids = get_jobs_ids()
        if not ids:
            break
        time.sleep(10)


def start_servers():
    out, err = execute_command(
        'ssh banana "source /etc/profile.d/lsf.sh;'
        ' /ebi/microarray/home/arrayexpress/ae2_production/software/framework/restart.sh"')
    out1, err1 = execute_command(
        'ssh banana "source /etc/profile.d/lsf.sh;'
        ' /ebi/microarray/home/arrayexpress/ae2_perftest/software/framework/restart.sh"')
    out2, err2 = execute_command(
        'ssh banana "source /etc/profile.d/lsf.sh;'
        ' /ebi/microarray/home/arrayexpress/ae2_curator/software/framework/restart.sh"')
    return '\n'.join([out,err,  out1,err1, out2, err2])


def main():
    print 'starting'
    ids = get_jobs_ids()
    print ids
    kill_jobs(ids)
    return start_servers()


if __name__ == '__main__':
    main()

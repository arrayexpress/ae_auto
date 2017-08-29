import collections
import os
import shutil

import time

from clint.textui import colored

from automation.erad.erad_submission import reload_experiment
from dal.mysql.ae_autosubs.experiments import retrieve_experiment_id_by_accession, retrieve_experiment_status, \
    retrieve_checker_score
from models.magetab.sdrf import SdrfCollection
from settings import TEMP_FOLDER, EXPERIMENTS_PATH, ANNOTARE_DIR, BASH_PATH
from utils.common import execute_command

__author__ = 'Ahmed G. Ali'


def wait_for_ae_export(accession, exp_dir):
    status = retrieve_experiment_status(accession)
    while status != 'AE2 Export Complete':
        # print status
        time.sleep(30)
        status = retrieve_experiment_status(accession)
        if status in ['Export failed', 'Checking failed', 'Abandoned', '** CHECKER CRASH **',
                      'MAGE-TAB export failed', 'Validation failed']:
            checker_score = retrieve_checker_score(accession)
            if checker_score == 34:
                print 'Checker score 34. Exporting'
                os.subprocess.call('source %s; reset_experiment.pl -e %s\n' % (BASH_PATH, exp_dir),
                                   shell=True, env=dict(ENV=BASH_PATH))
                time.sleep(120)
                wait_for_ae_export(accession, exp_dir)
            else:
                print colored.red('Failure: Experiment Reset Failed')
                # exit(1)
    print colored.green('Export Complete')


def extract_idf_file_name(exp_path, accession):
    lines = os.listdir(exp_path)
    f_name = ''
    idf = [l.strip() for l in lines if
           l.strip().endswith('.idf.txt') and l.strip().startswith(accession) and 'backup' not in l]
    if not idf or idf == []:
        idf = [l.strip() for l in lines if l.strip().endswith('.idf.txt') and 'backup' not in l]
    if idf:
        versions = [int(i.split('.')[0].split('_')[-1].replace('v', '')) for i in idf]
        max_index = versions.index(max(versions))
        f_name = idf[max_index]
    f_name = os.path.join(exp_path, f_name)
    if os.path.exists(f_name + '.backup'):
        shutil.copyfile(f_name + '.backup', f_name)
    else:
        shutil.copyfile(f_name, f_name + '.backup')
    return f_name


def main():
    dirs = [
        d for d in os.listdir(TEMP_FOLDER)
        if d.startswith('E-MTAB-') \
           and os.path.isdir(os.path.join(TEMP_FOLDER, d))
    ]
    # print dirs
    corrupted = ['E-MTAB-3800', 'E-MTAB-3964', 'E-MTAB-4002', 'E-MTAB-4069', 'E-MTAB-4082', 'E-MTAB-4096',
                 'E-MTAB-4159', 'E-MTAB-4549', 'E-MTAB-4694', 'E-MTAB-4686', 'E-MTAB-4723', 'E-MTAB-4846',
                 'E-MTAB-4264', 'E-MTAB-5044', 'E-MTAB-5169', 'E-MTAB-5362']
    errors = []
    # for d in dirs:
    #     print 'working on: ', d
    #     combined_path = os.path.join(TEMP_FOLDER, d, 'combined.txt')
    #     if not os.path.exists(combined_path):
    #         continue
    #     try:
    #         sdrf = SdrfCollection(file_path=combined_path, combined=True)
    #         paired = [r for r in sdrf.rows if r.is_paired]
    #         if paired:
    #             r = paired[0]
    #             if not(r.ena_run+'_1' in r.fastq_url or r.ena_run+'_1' in r.fastq_url):
    #                 corrupted.append(d)
    #     except Exception, e:
    #         errors.append([d,e])

    print corrupted
    print errors
    for exp in corrupted:
        exp_sub_tracking_id = retrieve_experiment_id_by_accession(exp)
        print 'MAGE-TAB_' + str(exp_sub_tracking_id)

        if not exp_sub_tracking_id:
            print "%s doesn't exist in subs tracking"
            continue
        mage_tab = os.path.join(ANNOTARE_DIR, 'MAGE-TAB_' + str(exp_sub_tracking_id))
        try:
            idf_file = extract_idf_file_name(mage_tab, exp)
        except Exception, e:
            print e
            continue
        print idf_file
        f = open(idf_file, 'r')
        lines = f.readlines()
        f.close()
        is_sdrf = False
        replace = '_1.fastq.gz'
        write_lines = []
        d = collections.OrderedDict()
        run_index = -1
        changed = False
        for line in lines:

            if line.strip() == '[SDRF]':
                is_sdrf = True
                write_lines.append(line.strip())
            if not is_sdrf:
                write_lines.append(line.strip())
            else:
                if line.startswith('Source Name'):
                    write_lines.append(line.strip())
                    parts = line.strip().split('\t')
                    run_index = parts.index('Comment[ENA_RUN]')
                    continue
                run = line.split('\t')[run_index]
                if run in d.keys():
                    d[run].append(line.strip())
                else:
                    d[run] = [line.strip()]

        for k, v in d.items():
            if len(v) > 1:
                if '_1.fastq.gz' in ' '.join(v) or '_2.fastq.gz' in ' '.join(v):
                    print colored.red('DAMAGED: '+'MAGE-TAB_' + str(exp_sub_tracking_id))
                    break
                changed = True
                v[0] = v[0].replace('.fastq.gz', '_1.fastq.gz')
                v[1] = v[1].replace('.fastq.gz', '_2.fastq.gz')
            write_lines += v
        if changed:
            f = open(idf_file, 'w')
            f.write('\n'.join(write_lines))
            f.close()
            out, err = execute_command('reset_experiment.pl -c ' + 'MAGE-TAB_' + str(exp_sub_tracking_id))
            print 'out: ', out
            print colored.red('error: ' + str(err))
            if not err:
                wait_for_ae_export(exp, 'MAGE-TAB_' + str(exp_sub_tracking_id))
                reload_experiment(exp)


if __name__ == '__main__':
    main()

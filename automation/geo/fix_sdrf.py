import argparse
import os
from copy import copy

import settings
from dal.oracle.era.data_file_meta import get_file_by_run

__author__ = 'Ahmed G. Ali'


def fix_geo(accession):

    load_dir = os.path.join(settings.EXPERIMENTS_PATH, 'GEOD', accession, '%s.idf.txt' % accession)
    f = open(load_dir, 'r')
    lines = [l.strip() for l in f.readlines()]
    f.close()

    if 'seq' not in [l for l in lines if 'Comment[AEExperimentType]' in l][0].split('\t')[1]:
        print '%s is not sequencing experiment!'% accession
        return

    load_dir = os.path.join(settings.EXPERIMENTS_PATH, 'GEOD', accession, '%s.sdrf.txt'%accession)
    f = open(load_dir, 'r')
    lines = [l.strip() for l in f.readlines()]
    f.close()

    header = lines[0].split('\t')
    file_index = -1
    run_index = -1
    if 'Comment [ENA_RUN]' in header:
        run_index = header.index('Comment [ENA_RUN]')
    else:
        raise Exception('No Runs')
    if 'Comment[FASTQ_URI]' in header:
        file_index = header.index('Comment [FASTQ_URI]')
    elif 'Comment [FASTQ_URI]' in header:
        file_index = header.index('Comment [FASTQ_URI]')
    else:
        header.insert(run_index+1, 'Comment[FASTQ_URI]')
    write_lines = ['\t'.join(header)]
    rewrite = False
    processed_runs = []
    added_files = []
    for i in range(1, len(lines)):
        line = lines[i].split('\t')
        if file_index != -1:
            if (line[run_index], line[file_index]) in processed_runs:
                continue

        if file_index == -1 or line[file_index] == '':
            files = get_file_by_run(line[run_index])
            if len(files) > 1:
                line[header.index('Comment [LIBRARY_LAYOUT]')] = 'PAIRED'
            for f in files:
                if f.data_file_path in added_files:
                    continue

                l = copy(line)
                l.insert(run_index + 1, 'ftp://ftp.sra.ebi.ac.uk/vol1/'+f.data_file_path)
                rewrite = True
                write_lines.append('\t'.join(l))
                added_files.append(f.data_file_path)
        processed_runs.append((line[run_index], line[file_index]))
    if rewrite:
        f = open(load_dir, 'w')
        f.write('\n'.join(write_lines))
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fixes Geo experiment SDRF in case of missing data files.')
    parser.add_argument('accession', metavar='E-GEOD-xxxx', type=str,
                        help='''The accession number for the experiment''')
    args = parser.parse_args()

    fix_geo(args.accession)

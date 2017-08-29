import argparse
import codecs
import os

import time

import datetime

from dal.oracle.biostudies.biostudies_transaction import retrieve_studies_by_accession

__author__ = 'Ahmed G. Ali'


def main(accs, out_dir):
    studies = {}
    write_val = ''
    header = []
    chars = []
    comms = []
    other = []

    for acc in accs:
        data = retrieve_studies_by_accession(acc)
        for row in data:
            s_acc = row.acc
            category = row.cat
            txt = row.txt


            if s_acc not in studies.keys():
                studies[s_acc] = {'chars':{}, 'comments':{}, 'other':{}}

            if 'characteristic' in category:
                studies[s_acc]['chars'][txt] = row.term_text
                chars.append(txt)
            elif 'comment' in category:
                studies[s_acc]['comments'][txt] = row.term_text
                comms.append(txt)
            else:
                studies[s_acc]['other'][txt] = row.term_text
                other.append(txt)
    print studies
    chars = list(set(chars))
    comms = list(set(comms))
    other = list(set(other))
    header = ['BioSD acc'] + ['Characteristics[%s]' % i for i in chars]+ ['Comment[%s]' % i for i in comms] + [i for i in other]
    write_val += '\t'.join(header) + os.linesep
    for acc in studies.keys():
        vals = [acc]
        tmp = []
        for char in chars:
            tmp.append(studies[acc]['chars'].get(char, ''))
        vals += tmp
        tmp = []
        for comm in comms:
            tmp.append(studies[acc]['comments'].get(comm, ''))
        vals += tmp
        tmp = []
        for oth in other:
            tmp.append(studies[acc]['other'].get(oth, ''))
        vals += tmp
        if len(header) != len(vals):
            print header
            print vals
            exit()
        write_val += '\t'.join(vals) + os.linesep

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    f = codecs.open(os.path.join(out_dir, datetime.datetime.now().isoformat().split('.')[0]), 'w')
    f.write(write_val)
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Format Biostudies output to excel like format')
    parser.add_argument('accessions', nargs='+', metavar='SAMEAxxx SAMEAyyy SAMEAzzz',
                        help='List of biostudy accession numbers')
    parser.add_argument('out_dir', type=str, help='''Output path where the file will be saved.
    File name will be the timestamp for execution.''')
    args = parser.parse_args()
    main(args.accessions, args.out_dir)

import os
import datetime
import subprocess
import shutil

import argparse
from dateutil.parser import parse

from dal.oracle.ae2.ae2_transaction import retrieve_today_updated_experiments
from settings import EXPERIMENTS_PATH, TEMP_FOLDER

__author__ = 'Ahmed G. Ali'


def main(update_date=None):
    res = retrieve_today_updated_experiments(update_date)
    experiments = {}
    if res and len(res) > 0:
        for r in res:
            if r.acc in experiments.keys():
                continue
            experiments[r.acc] = r
    print len(experiments), ' experiment found'
    updated_experiments = {}
    for k, v in experiments.items():
        file_path = os.path.join(EXPERIMENTS_PATH, k.split('-')[1], k, '%s.idf.txt' % k)
        # file_path = '/home/gemmy/E-MEXP-2594.idf.txt'
        subprocess.call("dos2unix " + file_path, shell=True)
        subprocess.call("mac2unix " + file_path, shell=True)
        # subprocess.call("perl -pi -e's/\r/\n/g' " + file_path, shell=True)
        f = open(file_path, 'r')
        lines = f.readlines()
        f.close()
        if v.doi and 'UNKNOWN_DOI_for_publication' in v.doi:
            v.doi = None
        add_comment = bool(v.text)
        add_pubmed = bool(v.pubmed)
        add_authors = bool(v.authorlist)
        add_doi = bool(v.doi)
        add_pub_title = bool(v.publication_title)
        updated = False
        tmp = []
        headers = []
        for old_line in lines:
            if old_line.split('\t')[0] not in headers:
                tmp.append(old_line)
                headers.append(old_line.split('\t')[0])
        if len(tmp) != len(lines):
            print 'duplicate found for %s.' % k
            lines = tmp
            updated = True
        lines_to_write = []
        fields = []
        for i in range(len(lines)):
            line = lines[i].strip()
            if line == '':
                continue
            if line.startswith('Public Release Date') and v.releasedate.date().isoformat() not in line:
                line = 'Public Release Date\t' + v.releasedate.date().isoformat()
                fields.append('release date')
                updated = True
            if line.startswith('Investigation Title') and v.title not in line:
                line = 'Investigation Title\t' + v.title
                updated = True
                fields.append('title')

            if line.startswith('Comment[AEExperimentDisplayName]'):
                add_comment = False
                if v.text and v.text not in line:
                    line = 'Comment[AEExperimentDisplayName]\t' + v.title
                    updated = True
                    fields.append('comment display Name')
            if line.lower().startswith('pubmed'):
                add_pubmed = False
                if v.pubmed and str(v.pubmed) not in line:
                    line = 'PubMed ID\t' + str(v.pubmed)
                    updated = True
                    fields.append('pubmed')
            if line.lower().startswith('publication author list'):
                add_authors = False
                if v.authorlist:
                    authors = [a.strip() for a in v.authorlist.replace('and ', '').split(',')]
                    if len(authors) == 1:
                        authors = [a.strip() for a in v.authorlist.replace('and ', '').split(';')]
                    for i in authors:
                        if i == ' ' or i == '':
                            continue
                        if i not in line.replace('and', ''):
                            line = 'Publication Author List\t' + v.authorlist
                            fields.append('author list')
                            updated = True
                            break

            if line.lower().startswith('publication title'):
                add_pub_title = False
                if v.publication_title and v.publication_title not in line:
                    line = 'Publication Title\t' + v.publication_title
                    updated = True
                    fields.append('pub title')
            if line.lower().startswith('publication doi'):
                add_doi = False
                if 'UNKNOWN_DOI_for_publication' in line:
                    line = 'Publication DOI\t'
                if v.doi and str(v.doi) not in line:
                    line = 'Publication DOI\t' + str(v.doi)
                    updated = True
                    fields.append('doi')
            lines_to_write.append(line)
        if add_comment:
            lines_to_write.append('Comment[AEExperimentDisplayName]\t' + v.title)
            fields.append('comment display Name')
            updated = True
        if add_pubmed:
            lines_to_write.append('PubMed ID\t' + str(v.pubmed))
            fields.append('pubmed')
            updated = True
        if add_authors:
            lines_to_write.append('Publication Author List\t' + v.authorlist)
            fields.append('authors')
            updated = True
        if add_pub_title:
            lines_to_write.append('Publication Title\t' + v.publication_title)
            updated = True
            fields.append('pub title')
        if add_doi:
            lines_to_write.append('Publication DOI\t' + str(v.doi))
            updated = True
            fields.append('doi')

        if updated:
            updated_experiments[k] = fields
            os.rename(os.path.join(EXPERIMENTS_PATH, k.split('-')[1], k, '%s.idf.txt' % k),
                      os.path.join(EXPERIMENTS_PATH, k.split('-')[1], k, '%s.idf.txt.backup_%s' % (
                          k, datetime.datetime.today().isoformat().replace('T', '-').replace(':', '-').split('.')[0])))
            f = open(os.path.join(EXPERIMENTS_PATH, k.split('-')[1], k, '%s.idf.txt' % k), 'w')
            f.write(os.linesep.join(lines_to_write))
            f.close()
            print os.path.join(EXPERIMENTS_PATH, k.split('-')[1], k, '%s.idf.txt' % k), ' written'

    f = open(os.path.join(TEMP_FOLDER, 'modify_idf_%s.txt' %
                          datetime.datetime.today().isoformat().replace('T', '-').replace(':', '-').split('.')[0]), 'w')
    f.write(os.linesep.join(['%s: %s' % (k, ', '.join(v)) for k, v in updated_experiments.items()]))
    f.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Modifies the IDF of the updated experiments')
    parser.add_argument('-d', '--update-date', metavar='date', type=str,
                        help="""The start date for checking. If not givin it will check for today only""")
    args = parser.parse_args()
    update_date = None
    if args.update_date:
        update_date = parse(args.update_date).date().isoformat()

    main(update_date)

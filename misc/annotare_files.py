from dal.mysql.annotare.data_files import retrieve_data_files_by_owned_by
from dal.mysql.annotare.submission import retrieve_submission_by_accession

__author__ = 'Ahmed G. Ali'


def main(acc):
    submission = retrieve_submission_by_accession(acc)[0]

    files = retrieve_data_files_by_owned_by(submission['id'])
    print files

if __name__ == '__main__':
    main('E-MTAB-4663')
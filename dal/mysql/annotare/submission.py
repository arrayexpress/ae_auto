from dal.mysql.annotare import db
from dal.mysql.common import execute_select

__author__ = 'Ahmed G. Ali'


def retrieve_submission_by_accession(acc):
    sql = """select * from submissions where accession = '%s' """ % acc
    return execute_select(sql, db)
# if __name__ == '__main__':
#     r = retrieve_submission_by_accession('E-MTAB-5308')
#     print r
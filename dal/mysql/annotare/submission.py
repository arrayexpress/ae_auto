from dal.mysql.annotare import db
from dal.mysql.comon import execute_select

__author__ = 'Ahmed G. Ali'


def retrieve_submission_by_accession(acc):
    sql = """select * from submissions where accession = '%s' """ % acc
    return execute_select(sql, db)

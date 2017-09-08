from dal.mysql.annotare import db
from dal.mysql.common import execute_select

__author__ = 'Ahmed G. Ali'


def retrieve_data_files_by_owned_by(submission_id):
    sql = '''SELECT  fileName, digest from data_files where ownedBy = %s''' % str(submission_id)
    print sql
    return execute_select(sql, db)

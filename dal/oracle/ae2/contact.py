from dal.oracle.ae2 import db
from dal.oracle.comon import execute_select

__author__ = 'Ahmed G. Ali'


def retrieve_contact_by_study_id(ae_id):
    sql = """SELECT * FROM CONTACT WHERE STUDY_ID=%s""" % str(ae_id)
    # print sql
    return execute_select(sql, db)

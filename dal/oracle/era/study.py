from dal.oracle.common import execute_select
from dal.oracle.era import db

__author__ = 'Ahmed G. Ali'


def extract_geo_studies():
    sql = """SELECT STUDY_ID, STUDY_ALIAS FROM STUDY WHERE CENTER_NAME='GEO'"""
    return execute_select(sql, db)


def get_study_xml_by_acc(study_acc):
    sql = """SELECT  xmltype.GetClobVal(STUDY_XML) as s_xml FROM STUDY WHERE STUDY_ID ='%s'""" % study_acc
    return execute_select(sql, db, True)


def get_ae_acc_by_ena_acc(ena_acc):
    sql = """SELECT ARRAYEXPRESS_ID FROM STUDY where STUDY_ID = '%s'""" % ena_acc
    # print sql
    return execute_select(sql, db)


def get_ena_acc_and_submission_acc_by_ae_acc(ae_acc):
    sql = """SELECT STUDY_ID, SUBMISSION_ID FROM STUDY where ARRAYEXPRESS_ID = '%s' or STUDY_ALIAS ='%s'""" % (ae_acc,ae_acc)
    print sql
    return execute_select(sql, db)

def get_study_by_acc(acc):
    sql = """SELECT * FROM STUDY WHERE STUDY_ID = '%s'""" % acc
    return execute_select(sql, db)

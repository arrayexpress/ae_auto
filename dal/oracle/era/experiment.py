from dal.oracle.comon import execute_select
from dal.oracle.era import db

__author__ = 'Ahmed G. Ali'


def retrieve_experiment_by_acc(acc):
    sql = """SELECT * FROM EXPERIMENT WHERE EXPERIMENT_ID = '%s'""" % acc
    return execute_select(sql, db)


def retrieve_experiments_by_submission_acc(submission_acc):
    return execute_select("""SELECT * FROM EXPERIMENT WHERE SUBMISSION_ID = '%s'""" % submission_acc, db)


def retrieve_experiments_by_study_acc(study_acc):
    return execute_select("""SELECT * FROM EXPERIMENT WHERE STUDY_ID = '%s'""" % study_acc, db)


def get_experiment_xml_by_acc(acc):
    sql = """SELECT  xmltype.GetClobVal(EXPERIMENT_XML) as e_xml FROM EXPERIMENT WHERE EXPERIMENT_ID ='%s'""" % acc
    return execute_select(sql, db, True)
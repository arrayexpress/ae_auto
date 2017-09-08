from dal.oracle.common import execute_select
from dal.oracle.era import db

__author__ = 'Ahmed G. Ali'


def retrieve_study_id_by_run_id(run_id):
    sql = """SELECT STUDY_ID FROM EXPERIMENT
 WHERE EXPERIMENT_ID = (SELECT EXPERIMENT_ID FROM RUN WHERE RUN_ID = '%s')""" % run_id
    return execute_select(sql, db)

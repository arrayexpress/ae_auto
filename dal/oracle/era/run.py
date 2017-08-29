from dal.oracle.comon import execute_select
from dal.oracle.era import db

__author__ = 'Ahmed G. Ali'


def retrieve_run_by_acc(acc):
    sql = """SELECT * FROM RUN WHERE RUN_ID = '%s'""" % acc
    return execute_select(sql, db)

def retrieve_runs_by_submission_acc(submission_acc):
    sql = """SELECT * FROM RUN WHERE SUBMISSION_ID = '%s'""" % submission_acc
    # print sql
    # exit()
    return execute_select(sql, db)

def retrieve_runs_by_experiment_acc(exp_acc):
    sql = """SELECT * FROM RUN WHERE EXPERIMENT_ID = '%s'""" % exp_acc
    # print sql
    # exit()
    return execute_select(sql, db)

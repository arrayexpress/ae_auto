from dal.oracle.common import execute_select
from dal.oracle.era import db

__author__ = 'Ahmed G. Ali'


def retrieve_ena_nodes_relations(ena_acc):
    sql = """SELECT * from ERA.WH_RUN where STUDY_ID = '%s' """ % ena_acc
    return execute_select(sql, db)

def retrieve_runs_by_experiment(exp_acc):
    sql = """SELECT * from ERA.WH_RUN where EXPERIMENT_ID = '%s' """ % exp_acc
    return execute_select(sql, db)

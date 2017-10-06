from dal.oracle.common import execute_select
from dal.oracle.era import db

__author__ = 'Ahmed G. Ali'


def retrieve_study_id_by_run_id(run_id):
    sql = """SELECT STUDY_ID FROM EXPERIMENT
 WHERE EXPERIMENT_ID = (SELECT EXPERIMENT_ID FROM RUN WHERE RUN_ID = '%s')""" % run_id
    return execute_select(sql, db)


def retrieve_runs_by_study_id(study_id):
    sql = """select * from RUN where EXPERIMENT_ID in 
(SELECT EXPERIMENT_ID FROM EXPERIMENT WHERE STUDY_ID = '%s')""" % study_id
    return execute_select(sql, db)


def retrieve_samples_by_study_id(study_id):
    sql = """select es.experiment_id, s.* from SAMPLE s,EXPERIMENT_SAMPLE es  where es.EXPERIMENT_ID in 
(SELECT EXPERIMENT_ID FROM EXPERIMENT  WHERE STUDY_ID = '%s') AND s.SAMPLE_ID = es.SAMPLE_ID""" % study_id
    return execute_select(sql, db)


def retrieve_files_by_study_id(study_id):
    sql = """select * from WEBIN_FILE  WHERE DATA_FILE_OWNER_ID in 
(select RUN_ID from RUN where EXPERIMENT_ID in 
(SELECT EXPERIMENT_ID FROM EXPERIMENT WHERE STUDY_ID = '%s') ) AND DATA_FILE_OWNER = 'RUN'""" % study_id
    return execute_select(sql, db)

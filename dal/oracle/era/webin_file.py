from dal.oracle.comon import execute_select
from dal.oracle.era import db

__author__ = 'Ahmed G. Ali'

def retrieve_files_by_run_owner(run_acc):
    return execute_select("""SELECT * FROM WEBIN_FILE WHERE DATA_FILE_OWNER_ID = '%s' AND DATA_FILE_OWNER = 'RUN'""" % run_acc, db)
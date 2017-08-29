from dal.oracle.comon import execute_select
from dal.oracle.era import db

__author__ = 'Ahmed G. Ali'


def get_file_by_run(run_acc):
    sql = """
            SELECT DATA_FILE_PATH FROM DATA_FILE_META
            WHERE DATA_FILE_OWNER = 'RUN'
              AND DATA_FILE_OWNER_ID='%s'
              AND DATA_FILE_FORMAT = 'FASTQ'
              """ % run_acc

    return execute_select(sql, db)

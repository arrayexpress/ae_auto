from dal.oracle.comon import execute_select, execute_insert
from dal.oracle.conan import db

__author__ = 'Ahmed G. Ali'


def retrieve_job_status(accession):
    sql_stmt = """SELECT STATE FROM CONAN_TASKS where NAME = '%s' and STATE != 'ABORTED' order by ID desc """ % accession
    result = execute_select(sql_stmt, db)

    if result and result[0]:
        return result[0].state

    return None


def retrieve_task(accession):
    sql_stmt = """SELECT * FROM CONAN_TASKS where NAME = '%s' and STATE != 'ABORTED' order by ID desc """ % accession
    result = execute_select(sql_stmt, db)

    if result and result[0]:
        return result[0]

    return None


def update_task_status_by_id(id, status, status_message):
    sql = """UPDATE CONAN_TASKS SET STATE = '%s', STATUS_MESSAGE='%s' WHERE ID = %s""" % (
        status, status_message, str(id))
    execute_insert(sql, db)

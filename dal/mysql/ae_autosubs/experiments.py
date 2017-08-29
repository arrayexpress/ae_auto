from dal.mysql.ae_autosubs import db
from dal.mysql.comon import execute_select, execute_insert

__author__ = 'Ahmed G. Ali'


def retrieve_experiment_status(ae_id):
    sql_stmt = """SELECT status FROM experiments where accession = '%s' """ % ae_id
    result = execute_select(sql_stmt, db)

    if result and result[0]:
        return result[0]['status']

    return None


def update_experiment_status(ae_id):
    execute_insert("""UPDATE experiments SET status = 'Checking failed',
                      comment='Automatically, back to private by GEO request' where accession = '%s'""" % ae_id, db)


def retrieve_checker_score(accession):
    sql_stmt = """SELECT checker_score FROM experiments where accession = '%s' """ % accession
    result = execute_select(sql_stmt, db)

    if result and result[0]:
        return result[0]['checker_score']

    return None


def retrieve_experiment_id_by_accession(accession):
    sql = """SELECT id FROM experiments WHERE accession = '%s'""" % accession
    res = execute_select(sql, db)
    if res and res[0]:
        return res[0]['id']
    return None

from dal.oracle.ae2 import db
from dal.oracle.common import execute_select

__author__ = 'Ahmed G. Ali'


def retrieve_study_id_by_acc(acc):
    sql = """select ID from STUDY where ACC = '{acc}'""".format(acc=acc)
    # print sql
    #
    return execute_select(sql, db)


def retrieve_study_by_acc(acc):
    sql = """select title, description from STUDY where ACC = '{acc}'""".format(acc=acc)
    # print sql
    res, con = execute_select(sql, db, keep_connection=True)
    a = 'No Description Available!'
    # print 'RESSSS: ', res
    if res and res[0]:
        a = res[0].description.read()
    con.close()
    res[0].description = a
    return res

def is_study_exists(accession):
    sql = """SELECT * from STUDY WHERE ACC = '%s'""" % accession
    res = execute_select(sql, db)
    if res and len(res) > 0:
        return True
    return False

def extract_geo_studies_without_ena_accessions():
    pass

from dal.oracle.ae2 import db
from dal.oracle.common import execute_select

__author__ = 'Ahmed G. Ali'


def is_array_design_exists(accession):
    sql = """SELECT * from PLAT_DESIGN WHERE ACC = '%s'""" % accession
    res = execute_select(sql, db)
    if res and len(res) > 0:
        return True
    return False

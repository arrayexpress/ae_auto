from dal.oracle.biostudies import db
from dal.oracle.common import execute_select

__author__ = 'Ahmed G. Ali'


def retrieve_studies_by_accession(acc):
    sql = """select bp.acc, epv.category,  TO_CHAR(epv.term_text) as term_text, ept.category as cat, ept.term_text as txt
            from BIO_PRODUCT bp, PRODUCT_PV ppv, EXP_PROP_TYPE ept, EXP_PROP_VAL epv where
            bp.acc = '%s' and bp.ID = ppv.OWNER_ID and
            ppv.PV_ID = epv.ID and epv.TYPE_ID = ept.ID""" % acc
    return execute_select(sql, db)

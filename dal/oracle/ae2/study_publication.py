from dal.oracle.ae2 import db
from dal.oracle.common import execute_insert, execute_select

__author__ = 'Ahmed G. Ali'


def insert_study_publication(study_id, pub_id):
    sql = """insert into STUDY_PUBLICATION (study_id, publication_id)
             values ({study_id}, {pub_id})""".format(study_id=study_id, pub_id=pub_id)
    # print sql
    execute_insert(sql, db)


def delete_study_publication(study_id, pub_id):
    sql = '''DELETE FROM STUDY_PUBLICATION WHERE STUDY_ID =%s AND PUBLICATION_ID = %s''' % (str(study_id), str(pub_id))
    # print sql
    execute_insert(sql, db)

def retrieve_associations_by_publication_id(pub_id):
    sql = '''SELECT * FROM STUDY_PUBLICATION WHERE PUBLICATION_ID = %s''' % str(pub_id)
    return execute_select(sql, db)
from dal.oracle.ae2 import db
from dal.oracle.common import execute_insert, execute_select

__author__ = 'Ahmed G. Ali'


def insert_publication(article):

    id = execute_select('select SEQ_PUBLICATION.nextval*50 as id from dual', db)[0].id
    sql = """INSERT INTO PUBLICATION
                        (
                        ID,
                        ACC,
                        DOI,
                        AUTHORLIST,
                        TITLE,
                        EDITOR,
                        ISSUE,
                        PAGES,
                        PUBLICATION,
                        PUBLISHER,
                        URI,
                        VOLUME,
                        PUBMEDID,
                        YEAR
                        )
                  VALUES(
                      '{id}',
                      '{PUBMED}',
                        '{DOI}',
                        '{AUTHORLIST}',
                        '{TITLE}',
                        '{EDITOR}',
                        '{ISSUE}',
                        '{PAGES}',
                        '{PUBLICATION}',
                        '{PUBLISHER}',
                        '{URI}',
                        '{VOLUME}',
                        '{PUBMED}',
                        '{YEAR}'
                      )""".format(
        id=str(id),
        PUBMED=article.get('id', ''),
        DOI=article.get('doi', None),
        AUTHORLIST=article.get('authorString', '').replace("'", '').encode('utf8'),
        TITLE=article.get('title', '').replace("'", '').encode('utf8'),
        EDITOR=article.get('editor', '').replace("'", '').encode('utf8'),
        ISSUE=article.get('issue', None),
        PAGES=article.get('pageInfo', None),
        PUBLICATION=article.get('journalTitle', '').encode('utf8'),
        PUBLISHER=article.get('publisher', '').encode('utf8'),
        URI=article.get('uri', '').encode('utf8'),
        VOLUME=article.get('journalVolume', ''),
        YEAR=article.get('pubYear', ''))
    execute_insert(sql, db)
    return str(id)


def retrieve_pub(acc, pubmed):
    sql = """SELECT  * FROM PUBLICATION WHERE PUBMEDID ='{pubmed}' OR ACC='{acc}'""".format(acc=str(acc), pubmed=str(pubmed))
    # sql = "SELECT  * FROM PUBLICATION WHERE PUBMEDID ='{pubmed}'".format(acc=str(acc), pubmed=str(pubmed))

    # print db
    # sql = "SELECT  * FROM PUBLICATION WHERE PUBMEDID ='6696735'"
    return execute_select(sql, db)

def retrieve_publication_by_acc(acc):
    sql = """SELECT * from PUBLICATION WHERE ACC = '%s'""" % str(acc)

    return execute_select(sql, db)

def delete_publication_by_id(pub_id):
    sql = """DELETE FROM PUBLICATION WHERE ID = %s""" % str(pub_id)
    execute_insert(sql, db)

if __name__ == '__main__':
    print retrieve_pub(acc=26273587, pubmed=20976176)

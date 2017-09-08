from dal.oracle.ae2 import db
from dal.oracle.common import execute_select, execute_insert

__author__ = 'Ahmed G. Ali'


def retrieve_existing_publications_by_accession(acc):
    sql = """select distinct pubid,
                             pubmed,
                             doi,
                             title,
                             authorlist,
                             publication,
                             publisher,
                             editor,
                             year,
                             volume,
                             issue,
                             pages,
                             uri,
                             studyid
            from view_publications
            where studyacc='{acc}'""".format(acc=acc)
    return execute_select(sql, db)


def retrieve_pub_id_by_doi(doi):
    sql = """select PUBID from view_publications
             where doi = '{doi}'""".format(doi=doi)
    # print sql
    return execute_select(sql, db)


def insert_publication_view(acc, article):
    sql = """INSERT INTO VIEW_PUBLICATIONS
                    (STUDYACC,
                    PUBMED,
                    DOI,
                    AUTHORLIST,
                    TITLE,
                    ISSUE,
                    PAGES,
                    PUBLICATION,
                    VOLUME,
                    YEAR
                    )
              VALUES(
                  '{STUDYACC}',
                  '{PUBMED}',
                  '{DOI}',
                  '{AUTHORLIST}',
                  '{TITLE}',
                  '{ISSUE}',
                  '{PAGES}',
                  '{PUBLICATION}',
                  '{VOLUME}',
                  '{YEAR}'
                  )""".format(STUDYACC=acc,
                              PUBMED=article.get('pmid', ''),
                              DOI=article.get('doi', None),
                              AUTHORLIST=article.get('authorString', '').replace("'", '').encode('utf8'),
                              TITLE=article.get('title', '').replace("'", '').encode('utf8'),
                              ISSUE=article.get('issue', None),
                              PAGES=article.get('pageInfo', None),
                              PUBLICATION=article.get('journalTitle', '').encode('utf8'),
                              VOLUME=article.get('journalVolume', ''),
                              YEAR=article.get('pubYear', ''))
    # print sql
    execute_insert(sql, db)


def update_publication_view_by_pubid(pub_id, article):
    sql = u"""UPDATE VIEW_PUBLICATIONS SET
                    PUBMED ='{PUBMED}' ,
                    DOI='{DOI}',
                    AUTHORLIST='{AUTHORLIST}',
                    TITLE='{TITLE}',
                    ISSUE='{ISSUE}',
                    PAGES='{PAGES}',
                    PUBLICATION='{PUBLICATION}',
                    VOLUME='{VOLUME}',
                    YEAR='{YEAR}'

              WHERE PUBID = {PUBID}""".format(PUBMED=article.get('pmid', ''),
                                              DOI=article.get('doi', None),
                                              AUTHORLIST=article.get('authorString', '').replace("'", ''),
                                              TITLE=article.get('title', '').replace("'", ''),
                                              ISSUE=article.get('issue', None),
                                              PAGES=article.get('pageInfo', None),
                                              PUBLICATION=article.get('journalTitle', ''),
                                              VOLUME=article.get('journalVolume', ''),
                                              YEAR=article.get('pubYear', ''),
                                              PUBID=str(pub_id))
    execute_insert(sql, db)


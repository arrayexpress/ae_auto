import datetime
from dal.oracle.ae2 import db
from dal.oracle.comon import execute_select

__author__ = 'Ahmed G. Ali'


def retrieve_permission_for_accession(acc):
    sql = """ select s.releasedate,o.sc_user_id
                from study s, sc_label l
                left join sc_owner o on l.id=o.sc_label_id
                where s.acc='{acc}'
                and l.name='{acc}'
                order by sc_user_id""".format(acc=acc)
    # print sql
    return execute_select(sql, db)


def retrieve_ena_accession(acc):
    sql = """select TEXT from study, study_annotations, controlled_vocabulary  where
                study.id = study_annotations.study_id and
                study_annotations.type_id = controlled_vocabulary.id and
                study.acc = '{acc}' and NAME = 'Comment[SecondaryAccession]'""".format(acc=acc)
    # print sql
    return execute_select(sql, db)


if __name__ == '__main__':
    print retrieve_permission_for_accession('a7a')


def retrieve_today_updated_experiments(update_date=None):
    if not update_date:
        update_date = datetime.datetime.today().date().isoformat()
    sql = """select sa.TEXT ,  s.ACC, s.TITLE, s.RELEASEDATE, p.DOI, p.PUBMED, p.AUTHORLIST, p.TITLE as publication_title
             from AE2.STUDY s join AE2.VIEW_PUBLICATIONS p on s.ACC = p.STUDYACC
             left join (select * from AE2.STUDY_ANNOTATIONS where TYPE_ID='151752' ) sa on s.ID = sa.STUDY_ID
             where  s.LASTUPDATEDATE >= DATE'%s' and s.ACC not like 'E-GEOD-%%'
             order by sa.TEXT asc""" % update_date

    return execute_select(sql, db)


def retrieve_release_date_by_ena_accession(ena_acc):
    sql = """SELECT s.ACC, s.RELEASEDATE
             FROM STUDY s join STUDY_ANNOTATIONS sa
             on s.ID=sa.STUDY_ID
             WHERE sa.TEXT = '%s' """ % ena_acc
    # print sql
    return execute_select(sql, db)

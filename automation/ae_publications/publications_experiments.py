import json
from django.db.models import Q
from dal.oracle.ae2.ae2_transaction import retrieve_permission_for_accession
from dal.oracle.ae2.publication import insert_publication, retrieve_publication_by_acc
from dal.oracle.ae2.study import retrieve_study_id_by_acc, retrieve_study_by_acc
from dal.oracle.ae2.study_publication import insert_study_publication
from dal.oracle.ae2.view_publications import retrieve_existing_publications_by_accession
from resources.europe_pmc import search, search_textmined
# from ae_web.ae_web import settings
# from django.core.management import setup_environ
# setup_environ(settings)
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ae_web')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ae_web.settings")
# from django.core.wsgi import get_wsgi_application

# os.environ['DJANGO_SETTINGS_MODULE'] = 'ae_web.ae_web.settings'
# application = get_wsgi_application()
import django

django.setup()
# from django.conf import settings

from publications.models import Experiment, Publication, Association

__author__ = 'Ahmed G. Ali'
NEW_PUBS = {}
CONNECTING_PUBS = {}
PRIVATE = {}


def get_permission(acc):
    """
    Checks whether the experiment is public or not.

    :param acc: ArrayExpress experiment accession. e.g. ``E-MTAB-xxxx``
    :type acc: str
    """
    permission = retrieve_permission_for_accession(acc)
    release_date = None
    is_public = None
    if permission and len(permission) > 0:
        release_date = permission[0]['releasedate']
        user_id = permission[0]['sc_user_id']
        is_public = False
        if user_id == 1:
            is_public = True
    return release_date, is_public


def main(query='arrayexpress'):
    """
    Main method of execution. it is baisically and infinit loop with termination condition that does the following:
        - Call Europe BMC utils for all articles matching the search word 'ArrayExpress' execluding GEO experiments.
        - Filter the collected list with those matching already existing ArrayExpress experiment.
        - Update the publication in AE database if already exists.
        - Calls the proper method to handle association based on the number of association with publication and experiments.

    :param query: The search value for Europe BMC API. Default: *arrayexpress*
    :type query: str

    """
    page = 1
    while True:
        art = search(query=query, page=page)
        if not art:
            break

        page += 1
        articles = search_textmined(art)
        for article in articles:
            for acc in article.get('accessions', []):
                if acc.startswith('E-GEOD-'):
                    continue
                release_date, is_public = get_permission(acc)
                # TODO: handle the case of private publications.
                pubs = retrieve_existing_publications_by_accession(acc)
                if is_public:
                    if pubs is None or len(pubs) == 0:
                        manage_no_existing_publications(acc, article)
                    elif len(pubs) == 1:
                        manage_single_existing_publication(article, pubs[0], acc)

                    else:  # Case more than one publication for the single accession
                        manage_more_than_one_publications(acc, article, pubs)
                else:
                    if acc not in PRIVATE.keys():
                        PRIVATE[acc] = [article]
                    else:
                        PRIVATE[acc].append(article)
    print 'new: ', len(NEW_PUBS)
    print '=' * 40
    print 'connected: ', len(CONNECTING_PUBS)
    print '=' * 40
    print 'private: ', len(PRIVATE)
    print '=' * 40


def manage_more_than_one_publications(acc, article, pubs):
    """
    This method is for the case of having more than one associated publications with the study in ArrayExpress database.

    :param acc: ArrayExpress accession. e.g. ``E-MTAB-xxxx``
    :type acc: str
    :param article: Json object as collected from Europe BMC.
    :type article: dict
    :param pubs: List of Json objects for publications found in ArrayExpress database.
    :type pubs: :obj:`list` of :obj:`dict`
    :return:
    """
    existing_pubs = [
        pub for pub in pubs if
        unicode(pub.get('title', None)) == unicode(article.get('title', '')) or
        pub.get('pubmed', None) == article.get('pmid', '')
    ]
    if len(existing_pubs) == 0:
        if acc not in NEW_PUBS.keys():
            NEW_PUBS[acc] = [article]
        else:
            NEW_PUBS[acc].append(article)
        add_association(acc, article)
        pub = retrieve_publication_by_acc(article['id'])
        if len(pub) == 0:
            insert_publication(article=article)
    else:
        add_association(acc, article, True)
        # pass
        # update_publication_view_by_pubid(existing_pubs[0].get('pubid'), article)


def manage_single_existing_publication(article, existing_pub, acc):
    """
    This method is for the case of having single associated publications with the study in ArrayExpress database.

    :param acc: ArrayExpress accession. e.g. ``E-MTAB-xxxx``
    :type acc: str
    :param article: Json object as collected from Europe BMC.
    :type article: dict
    :param existing_pub: Json object for the single publication found in the database.
    :type existing_pub: dict

    """
    if article.get('title', None) and existing_pub.get('title', None):
        if article.get('title', '').encode('utf8') == existing_pub.get('title', ''):
            # update_publication_view_by_pubid(existing_pub.get('pubid'), article)
            add_association(acc, article, True)
        elif article.get('title', '').encode('utf8') != existing_pub.get('title', ''):
            manage_no_existing_publications(acc, article)


def manage_no_existing_publications(acc, article):
    """
    This method is for the case where there is no any associated publications with the study in ArrayExpress database.

    :param acc: ArrayExpress accession. e.g. ``E-MTAB-xxxx``
    :type acc: str
    :param article: Json object as collected from Europe BMC.
    :type article: dict

    """
    is_associated = False

    pub_id = retrieve_publication_by_acc(article['id'])
    if pub_id and len(pub_id) > 0:
        pub_id = pub_id[0].id
        study_id = retrieve_study_id_by_acc(acc)
        if study_id:
            study_id = study_id[0]['id']
            is_associated = True
            if acc not in CONNECTING_PUBS.keys():
                CONNECTING_PUBS[acc] = [article]
            else:
                CONNECTING_PUBS[acc].append(article)
                insert_study_publication(study_id, pub_id)
    else:
        if acc not in NEW_PUBS.keys():
            NEW_PUBS[acc] = [article]
        else:
            NEW_PUBS[acc].append(article)
            pub_id = insert_publication(article)
            study_id = retrieve_study_id_by_acc(acc)[0]['id']

            insert_study_publication(study_id, pub_id)
    add_association(acc, article, is_associated)


def add_association(acc, article, is_associated=False):
    """
    Adding association between `Publication` and `Experiment` objects in the Django models which is used by
    curators to approve or reject linkage between an article and a study.

    :param acc: ArrayExpress accession. e.g. ``E-MTAB-xxxx``
    :type acc: str
    :param article: Json object as collected from Europe BMC.
    :type article: dict
    :param is_associated: Flag indicating whether the publication is already associated with the study in the
        AE database or not
    :type is_associated: bool

    """
    experiment = retrieve_study_by_acc(acc)[0]
    exp = Experiment.objects.filter(
        Q(accession=acc) | Q(title=experiment.title) | Q(description=experiment.description)).first()
    # print exp, exp_created
    if not exp:
        exp = Experiment(accession=acc,
                         title=experiment.title,
                         description=experiment.description)
        exp.save()
    pub = Publication.objects.filter(
        Q(pubmed=article.get('pmid', -1)) | Q(pmc_id=article.get('pmcid')) | Q(
            doi=article.get('doi', 'ANY THING ELSE')) | Q(title=article['title'])).first()
    if not pub:
        pub = Publication(pubmed=article.get('pmid', None), pmc_id=article.get('pmcid'),
                          doi=article.get('doi', None),
                          title=article['title'], whole_article=json.dumps(article))
        pub.save()
    else:
        pub.whole_article = json.dumps(article)
        pub.save()

    ass, ass_created = Association.objects.get_or_create(experiment=exp, publication=pub)
    if ass_created:
        ass.is_associated = is_associated
        ass.save()


if __name__ == '__main__':
    main()

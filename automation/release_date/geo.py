#! /usr/bin/env python
import argparse
import requests
from clint.textui import colored
import settings
from dal.mysql.ae_autosubs.experiments import retrieve_experiment_status, update_experiment_status
from dal.oracle.ae2.study import retrieve_study_id_by_acc
from models.conan import CONAN_PIPELINES
from resources.ssh import retrieve_plantain_connection, wait_execution
from utils.conan.conan import submit_conan_task
from utils.email.parser import geo_email_parse
from utils.email.sender import send_email

__author__ = 'Ahmed G. Ali'

ATLAS_EXPERIMENTS = []


def remove_geo_accession(geo_id):
    f = open(settings.GEO_ACCESSIONS_PATH, 'r')
    lines = f.readlines()
    f.close()
    for l in lines:
        if geo_id == l.strip().replace("- ", ''):
            lines.remove(l)
            break
    f = open(settings.GEO_ACCESSIONS_PATH, 'w')
    f.writelines(lines)
    f.close()


def change_to_private(email_body, email_address):
    ids = geo_email_parse(email_body)
    for geo_id, ae_id in ids.items():
        check_url = 'http://ves-hx-69.ebi.ac.uk:8983/solr/analytics/select?q=experimentAccession%3A' + ae_id + '&rows=0&wt=json&indent=true'
        # print check_url
        r = requests.get(check_url)
        # print colored.blue(r.content)
        if r.json()['response']['numFound'] > 0:
            ATLAS_EXPERIMENTS.append(ae_id)
        print 'geo id: ', geo_id, ' AE id: ', ae_id
        status = retrieve_experiment_status(ae_id)
        remove_geo_accession(geo_id)
        if status is None:
            print 'Not Imported'
            continue
        update_experiment_status(ae_id)

        if status not in (['Checking failed', 'GEO import failed', 'Validation failed', None]):
            exp = retrieve_study_id_by_acc(ae_id)
            if exp and len(exp) > 0:

                print colored.green('%s found and unloading starting' % ae_id)
                plantain, plantain_ssh = retrieve_plantain_connection()
                plantain.send(
                    'dos2unix /ebi/microarray/home/arrayexpress/ae2_production/data/EXPERIMENT/GEOD/%s*.txt\n' % ae_id)
                wait_execution(plantain)

                # conan = ConanPage(url=settings.CONAN_URL)
                # conan.login(login_email=email_address)
                # conan.unload_experiment(ae_id)
                submit_conan_task(accession=ae_id, pipeline_name=CONAN_PIPELINES.unload)
                print '%s unload submitted to Conan' % ae_id
            else:
                print colored.blue('%s not in AE database. It might has been unloaded before.' % ae_id)
        else:
            print colored.yellow('%s status is: %s. No need to unload' % (ae_id, status))
    if ATLAS_EXPERIMENTS:
        print 'sending email for ', ATLAS_EXPERIMENTS
        body = """Dear %s,
The following GEO experiments are turned into private as requested by GEO, and they are found in Atlas.
=======================================================================================================

%s

This email was sent automatically from the AE Automation Tool.
Thank You!
AE Automation Tool.""" % (settings.ATLAS_CONTACT['name'], '\n'.join(ATLAS_EXPERIMENTS))
        send_email(from_email=settings.AUTOMATION_EMAIL, to_emails=[settings.ATLAS_CONTACT['email']],
                   subject='GEO to Private Notification',
                   body=body)

        print colored.green('EMAIL SENT')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Returns GEO experiments into private.')
    parser.add_argument('accessions', nargs='+', metavar='GSExxx GDSyyy GSEzzz', help='List of accession numbers')
    parser.add_argument('-e', '--email', metavar='name@domain.com', help='Conan login email')
    args = parser.parse_args()
    email_body = '''
Dear ArrayExpress Team,

The Series %s was returned to private status.

Regards,
The GEO Team
*************


---- END OF MESSAGE BODY.  PLEASE DO NOT CHANGE THE DATA BELOW ----
SK#:15:60:5:235:2915403

Please leave the subject line unchanged, and do not change the message
at end from the line with "END OF MESSAGE BODY" to the end.

''' % ', '.join([i.replace(',', '') for i in args.accessions])
    email = settings.CONAN_LOGIN_EMAIL
    if args.email:
        email = args.email
    change_to_private(email_body, email)

import os
from dateutil.parser import parse
import requests
from dal.oracle.ae2.ae2_transaction import retrieve_ena_accession
from models.sra_xml import submission_api
import settings

__author__ = 'Ahmed G. Ali'


def update_release_date(accession, release_date):
    release_datetime = parse(release_date)
    ena_acc = retrieve_ena_accession(accession)
    if ena_acc:
        ena_acc = ena_acc[0].text
    print ena_acc
    save_dir = os.path.join(settings.TEMP_FOLDER, accession)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_file = os.path.join(save_dir, '%s_%s_change_date_submission.xml' % (accession, release_date))
    action_lst = [submission_api.ACTIONType(HOLD=submission_api.HOLDType(HoldUntilDate=release_date, target=ena_acc))]
    submission = submission_api.SubmissionType(broker_name='ArrayExpress',
                                               ACTIONS=submission_api.ACTIONSType(ACTION=action_lst),
                                               )
    print save_file
    submission.export(open(save_file, 'w'), 0, name_='SUBMISSION')
    files = {'SUBMISSION': open(save_file, 'rb')}
    r = requests.post(settings.ENA_SRA_URL, files=files, verify=False)
    content = r.content
    f = open(os.path.join(save_dir, '%s_%s_date_change_receipt.xml' % (accession, release_date)), 'w')
    f.write(content)
    f.close()
    print content



if __name__ == '__main__':
    accession = 'E-MTAB-3594'
    release_date = '2015-12-21'
    update_release_date(accession=accession, release_date=release_date)

import datetime
import os

import requests
import rt
from dateutil.parser import parse
import time
import settings
from dal.oracle.ae2.ae2_transaction import retrieve_release_date_by_ena_accession
from models.sra_xml import submission_api
from utils.email.sender import send_email

__author__ = 'Ahmed G. Ali'


def change_ena_release_date(ena_acc, ae_release_date):
    print (ena_acc, ae_release_date)
    action_lst = [submission_api.ACTIONType(
        HOLD=submission_api.HOLDType(HoldUntilDate=ae_release_date, target=ena_acc))]
    submission = submission_api.SubmissionType(submission_date=None,
                                               broker_name='ArrayExpress',
                                               alias=ena_acc + '_' + ae_release_date,
                                               center_name=None,
                                               accession=None,
                                               lab_name=None,
                                               submission_comment=None,
                                               IDENTIFIERS=None,
                                               TITLE=None,
                                               CONTACTS=None,
                                               ACTIONS=submission_api.ACTIONSType(ACTION=action_lst),
                                               SUBMISSION_LINKS=None,
                                               SUBMISSION_ATTRIBUTES=None)
    submission.export(
        open(os.path.join(settings.TEMP_FOLDER, '%s_submission.xml' % ena_acc), 'w'), 0,
        name_='SUBMISSION')
    url = settings.ENA_SRA_URL
    files = {'SUBMISSION': open(os.path.join(settings.TEMP_FOLDER, '%s_submission.xml' % (ena_acc)), 'rb')}
    r = requests.post(url, files=files, verify=False)
    content = r.content
    if '<html>' in content:
        time.sleep(20)
        change_ena_release_date(ena_acc, ae_release_date)
        return
    f = open(os.path.join(settings.TEMP_FOLDER, '%s_receipt.xml' % ena_acc), 'w')
    f.write(content)
    f.close()
    if 'success' in content:
        return True, content.split('<INFO>')[1].split('</INFO>')[0]
    return False, content.split('<ERROR>')[1].split('</ERROR>')[0]


def retrieve_ena_rt_tickets(queue='arrayexpress', **kwargs):
    tracker = rt.Rt('https://helpdesk.ebi.ac.uk/REST/1.0/', 'arrayexpress', '04kySSpu')
    tracker.login()
    tickets = tracker.search(Queue=queue, **kwargs)
    return_tickets = []
    for ticket in tickets:
        t = {}

        ticket_id = ticket.get('id').split('/')[1]
        t['id'] = ticket_id
        t['subject'] = ticket.get('Subject', '')
        t['owner'] = ticket.get('Owner', '')

        # attachments = [a for a in tracker.get_attachments(ticket_id) if a['Creator'] != u'1']
        attachments = tracker.get_attachments(ticket_id)
        for att in attachments:
            cont = tracker.get_attachment(ticket_id, att[0])
            if cont.get('Creator', None) == '1':
                continue
            t['content'] = cont.get('Content', '')
            break
        return_tickets.append(t.copy())
    return return_tickets


def check_ena_release(ticket):
    studies = ticket['content'].split('RELEASE_DATE | STUDY_ID | STUDY_TITLE')[
        1].split('\n')
    REPORT = {'CORRECT': [], 'FIXED': [], 'ERROR': [], 'COMMENT': []}
    for study in studies:
        if study == '' or '|' not in study:
            continue
        items = study.split(' | ')
        release_date = parse(items[0])
        ena_acc = items[1].split('(')[1].split(')')[0]
        res = retrieve_release_date_by_ena_accession(ena_acc)
        if not res:
            continue
        res = res[0]
        ae_acc = res.acc
        ae_release_date = res.releasedate
        if release_date.date() != ae_release_date.date():
            if release_date.date() > datetime.datetime.now().date():
                changed, msg = change_ena_release_date(ena_acc, ae_release_date.date().isoformat())
                # changed = True
                # msg = 'Went well'
                if changed:
                    REPORT['FIXED'].append(ae_acc + ':' + ena_acc +' ' +release_date.date().isoformat()+' '+msg)
                    # self.move_ticket_to_release_date()
                else:
                    REPORT['ERROR'].append((ae_acc + ':' + ena_acc, release_date.date().isoformat(), msg))
            else:
                if ae_release_date.date() > datetime.datetime.now().date():
                    REPORT['ERROR'].append(ae_acc + ':' + ena_acc+' '+ release_date.date().isoformat()+
                                           """ Release dates are not identical and already released on ENA.""")
                    REPORT['COMMENT'].append([ena_acc, ae_acc, ae_release_date.date().isoformat()])
        else:
            REPORT['CORRECT'].append((ae_acc + ':' + ena_acc, release_date.date().isoformat()))
            # self.move_ticket_to_release_date()
    tracker = rt.Rt('https://helpdesk.ebi.ac.uk/REST/1.0/', 'arrayexpress', '04kySSpu')
    tracker.login()
    if not REPORT['ERROR']:
        if not REPORT['FIXED']:
            comm = tracker.comment(ticket_id=ticket['id'], text='All are correct')
            try:
                ed = tracker.edit_ticket(ticket_id=ticket['id'], Status='resolved')
            except Exception, e:
                print e
                pass
            print 'done'
        else:
            comm = tracker.comment(ticket_id=ticket['id'], text='Following were fixed:\n' + '\n'.join(REPORT['FIXED']))
            ed = tracker.edit_ticket(ticket_id=ticket['id'], Status='resolved')
            print 'done'
    else:
        if ticket['owner'] !='ahmed':
            ed = tracker.edit_ticket(ticket_id=ticket['id'], Owner='ahmed', Status='open')
        comm = tracker.comment(ticket_id=ticket['id'],
                               text='There are the following errors:\n' +
                                    '\n'.join(REPORT['ERROR']) + "\nRequest sent to ENA using Ahmed's email")
        if REPORT['COMMENT']:
            ena_message = "Dear ENA Colleague,\n" + \
                          "Kindly suppress the following Project(s) to the dates specified below:\n\n"

            for c in REPORT['COMMENT']:
                ena_message += '%s to %s. This is ArrayExpress %s\n' % (c[0], c[2], c[1])
            ena_message += '\nThanks,\nArrayExpress Data Management.'
            comm2 = tracker.reply(ticket_id=ticket['id'], text=ena_message, cc='datasubs@ebi.ac.uk', bcc='')
            print comm2
            send_email(body=ena_message,
                       from_email='ahmed@ebi.ac.uk',
                       to_emails=['datasubs@ebi.ac.uk'],
                       subject='Project Suppress Request')

    print 'done'


def main():
    tickets = retrieve_ena_rt_tickets(queue='arrayexpress',  **{'Subject__like': 'ENA (Webin-24)', 'Owner__exact':'Nobody', 'Status': 'new'})
    for ticket in tickets:
        check_ena_release(ticket)


if __name__ == '__main__':
    main()
    # tickets = retrieve_ena_rt_tickets('arrayexpress', **{'Subject__like': 'ENA (Webin-24)'})
    # for k, v in tickets[0].items():
    #     print '%s: %s' % (k, v)
    #     print '=' * 50
    # for t in tickets:
    #     print '%s: %s' % (t['id'], t['subject'])

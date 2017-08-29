import os

import datetime
import requests
import time
from dateutil.parser import parse
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import settings
from automation.release_date.geo import change_to_private
from dal.oracle.ae2.ae2_transaction import retrieve_release_date_by_ena_accession
from models.sra_xml import submission_api
from utils.email.sender import send_email
from utils.ui_interfaces.otrs.otrs_locators import OtrsLocators
from utils.ui_interfaces.page import BasePage

__author__ = 'Ahmed G. Ali'
MESSAGE_HEADERS = {'ENA': 'ENA (Webin-24):',
                   'GEO': '[geo] GEO'}
REPORT = {'CORRECT': [], 'FIXED': [], 'ERROR': []}


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


def send_ena_report():
    global REPORT
    if len(REPORT['ERROR']) == len(REPORT['FIXED']) == len(REPORT['CORRECT']) == 0:
        print 'No Report to be sent'
        return
    msg = """This report is about ENA Release Date Check.\n\n"""
    if len(REPORT['ERROR']) > 0:
        msg += 'The following experiments failed in updating via ENA Webin:\n'
        msg += '===========================================================\n\n'
        msg += 'ACC | RELEASE DATE | ENA MESSAGE\n'
        for i in REPORT['ERROR']:
            msg += '%s | %s | %s\n' % (i[0], i[1], i[2])
        msg += '\n'

    if len(REPORT['FIXED']) > 0:
        msg += 'The following experiments were updated on ENA:\n'
        msg += '===============================================\n\n'
        msg += 'ACC | RELEASE DATE | ENA MESSAGE\n'
        for i in REPORT['FIXED']:
            msg += '%s | %s | %s\n' % (i[0], i[1], i[2])
        msg += '\n'
    if len(REPORT['CORRECT']) > 0:
        msg += 'The following experiments were correct:\n'
        msg += '========================================\n\n'
        msg += 'ACC | RELEASE DATE\n'
        for i in REPORT['CORRECT']:
            msg += '%s | %s\n' % (i[0], i[1])
        msg += '\n'
    msg += """
This email was sent automatically from the AE Automation Tool.
Thank You!
AE Automation Tool."""
    send_email(from_email=settings.AUTOMATION_EMAIL, to_emails=['catsnow@ebi.ac.uk'],
               subject='ENA Release dates report',
               body=msg)


class OtrsPage(BasePage):
    """
    Extends BasePage class.
    It is a holder for all the functionality for the homepage http://visual.ly/
    """

    def login(self, user_name, password):
        self.driver.find_element(*OtrsLocators.USER_NAME).send_keys(user_name)
        self.driver.find_element(*OtrsLocators.PASSWORD).send_keys(password)
        btn = self.driver.find_element(*OtrsLocators.SIGN_IN_BTN)
        while not btn.is_enabled():
            continue
        btn.click()

        try:

            WebDriverWait(self.driver, 10).until(
                expected_conditions.text_to_be_present_in_element(
                    locator=OtrsLocators.GREETINGS, text_='ahmed@ebi.ac.uk'
                )
            )
            return True
        except:

            return False

    def get_tickets_ids(self, header):
        tables = self.driver.find_elements_by_tag_name('table')
        links = []
        for i in range(len(tables)):
            table_body = tables[i].find_element_by_tag_name('tbody')
            tr = table_body.find_element_by_tag_name('tr')
            tds = None
            try:
                # self.driver.find_elements_by_link_text()
                td = tr.find_elements_by_class_name('mainhead')
                if len(td) > 1:
                    td = td[1]
                else:
                    continue
                if header in td.text and 'file processing errors' not in td.text:
                    links.append(tables[i + 1].find_element_by_tag_name('tbody').find_element_by_tag_name(
                        'tr').find_element_by_link_text('Zoom').get_attribute('href'))

            except NoSuchElementException:
                pass

        return links

    def handle_ena_release(self, links):
        global REPORT
        for link in links:
            try:
                self.driver.get(link)
                studies = \
                    self.driver.find_element_by_class_name('message').text.split('RELEASE_DATE | STUDY_ID | STUDY_TITLE')[
                        1].split('\n')

                for study in studies:
                                if study == '' or '|' not in study:
                        continue

                    items = study.split(' | ')
                    release_date = parse(items[0])
                    ena_acc = items[1].split('(')[1].split(')')[0]
                    res = retrieve_release_date_by_ena_accession(ena_acc)[0]
                    ae_acc = res.acc
                    ae_release_date = res.releasedate
                    if release_date.date() != ae_release_date.date():
                        if release_date.date() > datetime.datetime.now().date():
                            changed, msg = change_ena_release_date(ena_acc, ae_release_date.date().isoformat())
                            if changed:
                                REPORT['FIXED'].append((ae_acc + ':' + ena_acc, release_date.date().isoformat(), msg))
                                self.move_ticket_to_release_date()
                            else:
                                REPORT['ERROR'].append((ae_acc + ':' + ena_acc, release_date.date().isoformat(), msg))
                        else:
                            REPORT['ERROR'].append((ae_acc + ':' + ena_acc, release_date.date().isoformat(),
                                                    """Release dates are not identical and already released on ENA."""))
                    else:
                        REPORT['CORRECT'].append((ae_acc + ':' + ena_acc, release_date.date().isoformat()))
                        self.move_ticket_to_release_date()
            except Exception, e:
                print 'ERROR'
                print ena_acc
                print e
                print '='*30


    def move_ticket_to_release_date(self):
        select = Select(self.driver.find_element_by_name('DestQueueID'))
        select.select_by_value('19')
        # self.driver.find_element_by_css_selector('body > table:nth-child(9) > tbody > tr:nth-child(2) > td > form > input.button').click()
        self.driver.find_element_by_xpath('/html/body/table[5]/tbody/tr[2]/td/form/input[5]').click()

    def handle_geo_to_private(self, links):
        msg = ''
        for link in links:
            print link
            self.driver.get(link)
            msg += self.driver.find_element_by_class_name('message').text
            self.move_ticket_to_release_date()
        change_to_private(msg, settings.CONAN_LOGIN_EMAIL)


if __name__ == '__main__':
    otrs = OtrsPage(url='http://www.ebi.ac.uk/microarray-srv/otrs/index.pl')

    otrs.login('ahmed', 'enggemmy')
    links = otrs.get_tickets_ids(MESSAGE_HEADERS['ENA'])
    otrs.handle_ena_release(links)
    send_ena_report()
    otrs.driver.get(url='http://www.ebi.ac.uk/microarray-srv/otrs/index.pl')
    links = otrs.get_tickets_ids(MESSAGE_HEADERS['GEO'])
    otrs.handle_geo_to_private(links)

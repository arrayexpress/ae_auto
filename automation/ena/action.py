import argparse
import uuid

import os

import datetime
import requests
import time
from clint.textui import colored
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from dal.oracle.era.era_transaction import retrieve_samples_by_study_id
from models.sra_xml import submission_api
import settings

__author__ = 'Ahmed G. Ali'


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description=
                                     """
Submits an action for existing ENA object. 

Action lists are:
    - Cancel
    - Suppress
    - Kill
    - Release
    - Rollback

"""
                                     )
    parser.add_argument('accession', type=str, help="""ENA Accession.""")
    parser.add_argument('-t', '--test', action='store_true', help='Submits action to ENA test server')
    group = parser.add_mutually_exclusive_group()
    _group = parser.add_argument_group("Extra Arguments")
    _group.add_argument('-d', '--date', type=valid_date_type, help="Suppress date")
    _group.add_argument('-sa', '--samples', action='store_true', help="Apply the same actions on sample.")
    group.add_argument('-s', '--suppress', action='store_true', help='SUPPRESS ENA object')
    group.add_argument('-c', '--cancel', action='store_true', help='CANCEL ENA object')
    group.add_argument('-k', '--kill', action='store_true', help='KILL ENA object')
    group.add_argument('-re', '--release', action='store_true', help='RELEASE ENA object')
    group.add_argument('-ro', '--rollback', action='store_true', help='ROLLBACK ENA object')

    return parser


def create_xml(ena_acc, action, date=None, samples=False):
    file_name = str(uuid.uuid4()) + '.xml'
    date_str = ""
    if date:
        if action != 'SUPPRESS':
            raise argparse.ArgumentTypeError("Date arguments can go only with suppress!")
        else:
            date_str = 'HoldUntilDate="%s"' % date
    actions = ["""<ACTION><%s target="%s" %s/></ACTION>""" % (action.upper(), ena_acc, date_str)]
    if samples:
        samples = retrieve_samples_by_study_id(ena_acc)
        for s in samples:
            actions.append("""    <ACTION><%s target="%s" %s/></ACTION>""" % (action.upper(), s.sample_id, date_str))

    submission = """<?xml version="1.0" encoding="UTF-8"?>
<SUBMISSION alias="%s" xmlns:com="SRA.common" broker_name="ArrayExpress">
    <ACTIONS>
        %s
    </ACTIONS>
</SUBMISSION>

    """ % (ena_acc + '_' + action, '\n'.join(actions))
    print submission
    # exit()
    tmp_file = os.path.join('/tmp', file_name)
    f = open(tmp_file, 'w')
    f.write(submission)
    f.close()
    return tmp_file


def send_ena_action(ena_acc, action, test=False, date=None, samples=False):
    file_path = create_xml(ena_acc, action, date, samples)
    url = settings.ENA_SRA_URL
    if test:
        url = settings.ENA_SRA_DEV_URL
        print colored.magenta('This submission is going to ENA Dev Server')
    content = '<html>'
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    while '<html>' in content:
        files = {'SUBMISSION': open(file_path, 'rb')}
        r = requests.post(url, files=files, verify=False, timeout=1000)
        content = r.content
        if '<html>' not in content:
            break
        else:
            time.sleep(20)
    print content
    server = 'production'
    if test:
        server = 'test'
    if 'success="true' not in content:
        print colored.cyan('FAILURE: Failed submission to ENA. with the following errors ')
        errors = content.split('<ERROR>')
        for e in errors[1:]:
            print colored.red(e.split('</ERROR>')[0])
        return False, [i.split('</ERROR>')[0] for i in errors]


    else:
        print colored.green("%s was applied successfully on %s in the %s server" % (action, ena_acc, server))
        return True, []


def valid_date_type(arg_date_str):
    """custom argparse *date* type for user dates values given from the command line"""
    try:
        d = datetime.datetime.strptime(arg_date_str, "%Y-%m-%d")
        return arg_date_str
    except ValueError:
        msg = "Given Date ({0}) not valid! Expected format, YYYY-MM-DD!".format(arg_date_str)
        raise argparse.ArgumentTypeError(msg)

if __name__ == '__main__':
    parser = parse_arguments()
    args = parser.parse_args()
    ena_acc = args.accession
    action = ''
    if args.cancel:
        action = 'CANCEL'
    elif args.suppress:
        action = 'SUPPRESS'
    elif args.kill:
        action = 'KILL'
    elif args.release:
        action = 'RELEASE'
    elif args.rollback:
        action = 'ROLLBACK'
    test = args.test
    date = args.date
    samples = args.samples
    print ena_acc, action
    send_ena_action(ena_acc, action, test, date, samples)

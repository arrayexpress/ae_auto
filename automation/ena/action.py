import argparse
import uuid

import os
import requests
import time
from clint.textui import colored
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
    group.add_argument('-c', '--cancel', action='store_true', help='CANCEL ENA object')
    group.add_argument('-s', '--suppress', action='store_true', help='SUPPRESS ENA object')
    group.add_argument('-k', '--kill', action='store_true', help='KILL ENA object')
    group.add_argument('-re', '--release', action='store_true', help='RELEASE ENA object')
    group.add_argument('-ro', '--rollback', action='store_true', help='ROLLBACK ENA object')

    return parser


def create_xml(ena_acc, action):
    file_name = str(uuid.uuid4())+'.xml'
    submission = """<?xml version="1.0" encoding="UTF-8"?>
<SUBMISSION alias="%s" xmlns:com="SRA.common" broker_name="ArrayExpress">
    <ACTIONS>
        <ACTION>
            <%s target="%s"/>
        </ACTION>
    </ACTIONS>
</SUBMISSION>

    """ % (ena_acc+'_'+action, action.upper(), ena_acc)
    print submission
    tmp_file = os.path.join('/tmp', file_name)
    f = open(tmp_file, 'w')
    f.write(submission)
    f.close()
    return tmp_file



def send_ena_action(ena_acc, action, test=False):
    file_path = create_xml(ena_acc, action)
    url = settings.ENA_SRA_URL
    if test:
        url = settings.ENA_SRA_DEV_URL
        print colored.magenta('This submission is going to ENA Dev Server')
    content = '<html>'
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


    else:
        print colored.green("%s was applied successfully on %s in the %s server" % (action, ena_acc, server))


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
    print ena_acc, action
    send_ena_action(ena_acc, action, test)

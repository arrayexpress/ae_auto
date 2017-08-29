from dal.oracle.ae2.study import retrieve_study_id_by_acc
from settings import CURATION_EMAIL
from utils.common import execute_command
from utils.email.sender import send_email

__author__ = 'Ahmed G. Ali'

def main():
    out, err = execute_command("""sudo -u fg_cur -H sh -c "ssh oy-ena-login-1 ls -d /fire/staging/aexpress/*/" """)
    # print out
    # print '-' * 30
    # print err
    # print '-' * 30
    dirs = out.split('\n')
    removed = []
    not_removed = []
    for d in dirs:
        directory = d.replace('/fire/staging/aexpress/', '').replace('/','')
        if directory.startswith('E-MTAB'):

            acc = '-'.join(directory.split('-')[:3])
            print acc
            id = retrieve_study_id_by_acc(acc)
            if id:
                out1, err1 = execute_command("""sudo -u fg_cur -H sh -c "ssh oy-ena-login-1 rm -rf %s" """%d)
                if err1:
                    not_removed.append('%s:%s' % (directory, err1))
                    print err1
                else:
                    removed.append(directory)
    if removed:
        send_email(from_email='AE Automation<ae-automation@ebi.ac.uk>',
                   to_emails=[CURATION_EMAIL],
                   # to_emails=['ahmed@ebi.ac.uk'],
                   subject='/fire/staging Cleaning Report',
                   body="""Dear Curator,
The directories below have been deleted from /fire/staging. These were found loaded in AE database.

Thanks,
AE Automation Tool.

REMOVED DIRECTORY LIST:
=======================
%s""" % '\n'.join(removed))
    if not_removed:
        send_email(from_email='AE Automation<ae-automation@ebi.ac.uk>',
                   # to_emails=['ahmed@ebi.ac.uk', CURATION_EMAIL],
                   to_emails=['ahmed@ebi.ac.uk'],
                   subject='/fire/staging Error Report',

                   body="""
        ERROR DIRECTORY LIST:
        =======================
        %s""" % '\n'.join(not_removed))


if __name__ == '__main__':
    main()
import threading

import time

from automation.geo.import_adf import import_geo_platform
from automation.geo.import_series import import_geo_series
from dal.oracle.ae2.plat_design import is_array_design_exists
from dal.oracle.ae2.study import is_study_exists
from resources.eutils import esearch, esummary
from utils.email.sender import send_email

__author__ = 'Ahmed G. Ali'


def get_query_params(term):
    a = esearch(db='gds', term=term, history=True)
    return int(a['esearchresult']['count']), a['esearchresult']['querykey'], a['esearchresult']['webenv']


def send_report(total, imported, skipped, error):
    msg = """Dear Curators,
Geo Platform import report.
Collected: %d
Imported: %d
Skipped: %d
Errors: %d
""" % (total, imported, skipped, len(error.keys()))
    if len(error) > 0:
        msg += 'Error are as follows:\n'
        for k, v in error.items():
            msg += '%s: %s\n' % k, v
    send_email(from_email='AE Automation<ae-automation@ebi.ac.uk>', to_emails=['ahmed@ebi.ac.uk'],
               subject='Geo Platform Import Report',
               body=msg)


def main(is_array=True):
    if is_array:
        count, query_key, web_env = get_query_params('GPL[ETYP]')
    else:
        count, query_key, web_env = get_query_params('GSE[ETYP]')
    imported = 0
    skipped = 0
    error = {}

    for i in range(0, count, 500):
        result = esummary(db='gds', query_id=query_key, web_env=web_env, ret_start=i)
        threads = []
        for uid, val in result['result'].items():
            try:
                geo_acc = val['accession']
                if is_array:
                    ae_acc = geo_acc.replace('GPL', 'A-GEOD-')
                    if not is_array_design_exists(ae_acc):
                        t = threading.Thread(target=import_geo_platform, args=(geo_acc,))
                        threads.append(t)
                        t.daemon = False
                        # import_geo_platform(geo_acc)
                        # imported += 1
                    else:
                        skipped += 1
                else:
                    ae_acc = geo_acc.replace('GSE', 'E-GEOD-')
                    if not is_study_exists(ae_acc):
                        import_geo_series(geo_acc)
                        imported += 1
                    else:
                        skipped += 1
            except Exception, e:
                error[uid] = str(e)
        # send_email(from_email='AE Automation<ae-automation@ebi.ac.uk>', to_emails=['ahmed@ebi.ac.uk'],
        #            subject='Geo Platform pre import',
        #            body='Going to import %d platforms' % len(threads))
        running = []
        while True:
            while len(running) <= 10 and threads:
                t = threads.pop()
                t.start()
                running.append(t)
                time.sleep(5)
            if not running:
                break
            for t in running:
                if not t.is_alive():
                    running.remove(t)
                    imported += 1
                    break
            time.sleep(30)

    send_report(total=count, imported=imported, skipped=skipped, error=error)


if __name__ == '__main__':
    # main(False)
    main(False)

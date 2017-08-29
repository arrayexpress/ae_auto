import csv

from dal.oracle.ae2.contact import retrieve_contact_by_study_id
from dal.oracle.ae2.study import retrieve_study_id_by_acc
from dal.oracle.era.era_transaction import retrieve_study_id_by_run_id
from dal.oracle.era.study import get_ae_acc_by_ena_acc

__author__ = 'Ahmed G. Ali'


def main(in_file, out_file):
    files = []
    f = open(in_file, 'r')
    lines = f.readlines()
    f.close()
    for l in lines:
        if l == '' or l.startswith('FILE_NAME') or '|' not in l or '|-' in l:
            continue
        parts = l.split('|')
        run_acc = parts[-1].strip()
        ena_acc = retrieve_study_id_by_run_id(run_acc)[0].study_id
        ae_acc = get_ae_acc_by_ena_acc(ena_acc)[0].arrayexpress_id
        if not ae_acc:
            files[ena_acc] = {
                'files': [(parts[0].strip(), parts[1].strip())],
                'ae_acc': None,
                'user_email': None

            }
            continue
        ae_id = retrieve_study_id_by_acc(ae_acc)
        comments = ''
        user_email = 'UNKOWN'

        if ae_id:
            ae_id = ae_id[0].id
            user = retrieve_contact_by_study_id(ae_id)
            user_email = user[0].email
        else:
            comments = 'Not Loaded in AE database'
        # if ena_acc in files.keys():
        #     files[ena_acc]['files'].append((parts[0].strip(), parts[1].strip()))
        # else:
        files.append({
            'ena_acc': ena_acc,
            'file': parts[0].strip(),
            'error': parts[1].strip(),
            'ae_acc': ae_acc,
            'user_email': user_email,
            'comments': comments
        })

    with open(out_file, 'w') as csv_file:
        fieldnames = ['ena_acc', 'file', 'error', 'ae_acc', 'user_email', 'comments']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for f in files:
            writer.writerow(f)


if __name__ == '__main__':
    from sys import argv

    in_file = argv[1]
    out_file = argv[2]
    main(in_file, out_file)

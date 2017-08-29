import gzip
import os
import shutil
import urllib2
from contextlib import closing
import settings
from models.soft_mapper import SoftHeaderMapper, SoftTableMapper
from utils.common import execute_command
from utils.email.sender import send_email

__author__ = 'Ahmed G. Ali'


def download_soft_file(geo_acc, by='platform'):
    # adf_tmp_dir =os.path.join(settings.TEMP_FOLDER, geo_accession.replace('GPL', 'A-GEOD-'))
    adf_tmp_dir = os.path.join(settings.ADF_LOAD_DIR, geo_acc.replace('GPL', 'A-GEOD-'))
    if not os.path.exists(adf_tmp_dir):
        os.mkdir(adf_tmp_dir)
    file_name = geo_acc + '_family.soft.gz'
    with closing(urllib2.urlopen(settings.GEO_SOFT_URL % by + geo_acc + '/' + file_name)) as r:
        with open(os.path.join(adf_tmp_dir, file_name), 'wb') as f:
            shutil.copyfileobj(r, f)

    return os.path.join(adf_tmp_dir, file_name)


def parse_soft_file(soft_file):
    table = []
    start_header = False
    start_table = False
    header = []
    with gzip.open(soft_file, 'rb') as infile:
        for line in infile:
            if '^PLATFORM =' in line:
                start_header = True
            if line.startswith('!platform_table_begin'):
                start_header = False
                start_table = True
                continue
            if '!platform_table_end' in line:
                break
            if start_header:
                header.append(line)
                # print line
            if start_table:
                table.append(line)

    return header, table


def generate_adf(geo_accession, header, table):
    header_obj = SoftHeaderMapper(header)
    header_obj.generate_header()
    # print 'header generated'
    table_obj = SoftTableMapper(table)

    # 'HEADER'
    # print table_obj.ae_header

    # for r in table_obj.rows:
    #     print r.print_soft()
    adf_file = os.path.join(settings.ADF_LOAD_DIR, geo_accession.replace('GPL', 'A-GEOD-'),
                            geo_accession+ '.adf.txt')
    f = open(adf_file, 'w')
    f.write(header_obj.header_txt + '\n[main]\n' + table_obj.table)
    f.close()
    comments_file = os.path.join(settings.ADF_LOAD_DIR, geo_accession.replace('GPL', 'A-GEOD-'),
                                 geo_accession.replace('GPL', 'A-GEOD-') + '_comments.txt')
    f = open(comments_file, 'w')
    f.write(table_obj.comments)
    f.close()

    # print table_obj.ae_header


def import_geo_platform(geo_acc):
    try:
        soft_file = download_soft_file(geo_acc)
        header, table = parse_soft_file(soft_file)

        generate_adf(geo_acc, header, table)
        adf_file = os.path.join(settings.ADF_LOAD_DIR, geo_acc.replace('GPL', 'A-GEOD-'),
                                geo_acc+ '.adf.txt')
        print execute_command('magetab_insert_array.pl -f %s -a %s -c' % (adf_file, geo_acc.replace('GPL', 'A-GEOD-')))

        # shutil.copyfile(os.path.join(settings.ADF_LOAD_DIR, geo_acc.replace('GPL', 'A-GEOD-')), )
        out, err = execute_command('reset_array.pl -a A-GEOD-%s -c' % geo_acc.replace('GPL', ''))
        if 'error' in out.lower() or 'error' in err.lower():
            msg = """Dear Curators,
While trying to execute rest_array.pl for %s the we had the following output:
%s
%s""" % (geo_acc, out, err)
            send_email(from_email='AE Automation<ae-automation@ebi.ac.uk>',
                       to_emails=['miamexpress@ebi.ac.uk', 'ahmed@ebi.ac.uk'],
                       subject='GEO Array Error ' + geo_acc.replace('GPL', 'A-GEOD-'),
                       body=msg)

    except Exception, e:
        msg = """The following error occurred while importing: %s
%s""" % (geo_acc, str(e))
        send_email(from_email='AE Automation<ae-automation@ebi.ac.uk>',
                   to_emails=['ahmed@ebi.ac.uk'],
                   subject='Platform imported',
                   body=msg)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Downloads and converts a GEO Platform into MAGE-TAB')
    parser.add_argument('accession', metavar='GPLxxxx', type=str,
                        help='''The accession number for the GEO Platform''')
    args = parser.parse_args()
    geo_accession = args.accession
    import_geo_platform(geo_accession)
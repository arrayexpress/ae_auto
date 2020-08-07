import gzip
import os
import shutil
import socket
import urllib2
from contextlib import closing

import requests
from ftplib import FTP
import settings
from models.conan import CONAN_PIPELINES
from models.soft_mapper import SoftHeaderMapper, SoftTableMapper
from utils.common import execute_command
from utils.conan.conan import submit_conan_task
from utils.email.sender import send_email

__author__ = 'Ahmed G. Ali'


def get_platform_url(geo_acc):
    platform_number = geo_acc.replace('GPL', '')
    ftp_dir = ''
    if int(platform_number) < 1000:
        ftp_dir = 'GPLnnn'
    else:
        char_dif = len(platform_number) - len('nnn')
        ftp_dir = 'GPL' + platform_number[:char_dif] + 'nnn'
    url = settings.GEO_PLATFORM_URL.format(dir_name=ftp_dir, accession=geo_acc, arch=geo_acc+'_family.soft.gz')
    return url


def download_soft_file(geo_acc, by='platform'):
    # adf_tmp_dir =os.path.join(settings.TEMP_FOLDER, geo_accession.replace('GPL', 'A-GEOD-'))
    adf_tmp_dir = os.path.join(settings.ADF_LOAD_DIR, geo_acc.replace('GPL', 'A-GEOD-'))

    if not os.path.exists(adf_tmp_dir):
        os.mkdir(adf_tmp_dir)
    file_name = geo_acc + '_family.soft.gz'
    host = settings.GEO_SOFT_URL % by + geo_acc
    url = get_platform_url(geo_acc)
    print url
    # link = FTP(host=settings.GEO_SOFT_URL % by + geo_acc + , timeout=5)

    # r = requests.get(url, stream=True)
    # with open(os.path.join(adf_tmp_dir, file_name), 'wb') as f:
    # for chunk in r.iter_content(chunk_size=1024):
    #     if chunk:  # filter out keep-alive new chunks
    #         f.write(r.content)

    # with closing(urllib2.urlopen(settings.GEO_SOFT_URL % by + geo_acc + '/' + file_name)) as r:
    #     with open(os.path.join(adf_tmp_dir, file_name), 'wb') as f:
    #         shutil.copyfileobj(r, f)
    # local_filename = os.path.join(adf_tmp_dir, file_name)
    # print host
    # with closing(FTP()) as ftp:
    #     try:
    #         ftp.connect('ftp.ncbi.nih.gov',port=21, timeout= 30 * 60)  # 30 mins timeout
    #         # print ftp.getwelcome()
    #         ftp.login('anonymous', '')
    #         ftp.set_pasv(True)
    #         ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    #         ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 75)
    #         ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
    #         with open(local_filename, 'w+b') as f:
    #             res = ftp.retrbinary('RETR %s' % url.split('ftp.ncbi.nih.gov/')[1], f.write)
    #
    #             if not res.startswith('226 Transfer complete'):
    #                 # logging.error('Downloaded of file {0} is not compile.'.format(orig_filename))
    #                 os.remove(local_filename)
    #                 return None
    #
    #         # os.rename(local_filename, self.storage + filename + file_ext)
    #         # ftp.rename(orig_filename, orig_filename + '.copied')
    #
    #         # return filename + file_ext
    #
    #     except:
    #         raise
    #         # logging.exception('Error during download from FTP')
    command = """wget -m %s -O %s """ % (url, os.path.join(adf_tmp_dir, file_name))
    print command
    print execute_command(command)
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
                            geo_accession + '.adf.txt')
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
                                geo_acc + '.adf.txt')
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
            return
        submit_conan_task(accession=geo_acc.replace('GPL', 'A-GEOD-'), pipeline_name=CONAN_PIPELINES.load_adf)

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

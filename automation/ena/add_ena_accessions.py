import codecs
from itertools import groupby, count
from operator import itemgetter

import os
import shutil
import copy
from dal.mysql.ae_autosubs.experiments import retrieve_experiment_id_by_accession
from dal.oracle.era.study import get_ena_acc_and_submission_acc_by_ae_acc
from dal.oracle.era.wh_run import retrieve_ena_nodes_relations
from models.ena_models import ENAStudy
from models.magetab.idf import IDF
from models.magetab.sdrf import SdrfCollection
from settings import ANNOTARE_DIR, ENA_FTP_URI

__author__ = 'Ahmed G. Ali'


def extract_idf_file_name(exp_path, accession):
    """
    Extracts the the IDF file name with latest version. IDF files first generated with the format ``submission_xxx.id.txt``
    For other versions the file name will follow the convention of  ``E-MTAB-xxxx_v1.idf.txt``, ``E-MTAB-xxxx_v2.idf.txt`` and so on...

    :param exp_path: Full path containing the experiment's MAGETAB files.
    :type exp_path: str
    :param accession: ArrayExpress Accession Number, e.g. E-MTAB-xxxx
    :type accession: str

    :return: The full path for IDF file with the highest version
    :rtype: str
    """
    lines = os.listdir(exp_path)
    f_name = ''
    idf = [l.strip() for l in lines if
           l.strip().endswith('.idf.txt') and l.strip().startswith(accession) and 'backup' not in l]
    if not idf or idf == []:
        idf = [l.strip() for l in lines if l.strip().endswith('.idf.txt') and 'backup' not in l]
    if idf:
        versions = [int(i.split('.')[0].split('_')[-1].replace('v', '')) for i in idf]
        max_index = versions.index(max(versions))
        f_name = idf[max_index]
    f_name = os.path.join(exp_path, f_name)
    return f_name


def extract_sdrf_file_name(exp_path, accession):
    """
        Extracts the the SDRF file name with latest version. IDF files first generated with the format ``submission_xxx.id.txt``
        For other versions the file name will follow the convention of  ``E-MTAB-xxxx_v1.sdrf.txt``, ``E-MTAB-xxxx_v2.sdrf.txt`` and so on...

        :param exp_path: Full path containing the experiment's MAGE-TAB files.
        :type exp_path: str
        :param accession: ArrayExpress Accession Number, e.g. E-MTAB-xxxx
        :type accession: str

        :return: The full path for SDRF file with the highest version
        :rtype: str
        """
    lines = os.listdir(os.path.join(exp_path, 'unpacked'))
    sdrf_file_name = [l.strip() for l in lines if accession in l and '_v' in l]
    if not sdrf_file_name or sdrf_file_name == []:
        sdrf_file_name = [l.strip() for l in lines if
                          'submission' in l and 'annotare' in l and l.strip().endswith('.sdrf.txt')]
    if sdrf_file_name:
        versions = []
        for i in sdrf_file_name:
            v = i.split('.')[0].split('_')[-1]
            if v.startswith('v'):
                versions.append(int(v.replace('v', '')))
            else:
                versions.append(-1)
        max_index = versions.index(max(versions))
        return os.path.join(exp_path, 'unpacked', sdrf_file_name[max_index])
    return None


def get_full_path(dir_name):
    auto_subs = '/'.join(ANNOTARE_DIR.split('/')[:-1])
    for d in os.listdir(auto_subs):
        if os.path.exists(os.path.join(auto_subs, d, dir_name)):
            return os.path.join(auto_subs, d, dir_name)


def get_idf_path(ae_acc, dir_name):
    idf_file = extract_idf_file_name(exp_path=dir_name, accession=ae_acc)
    backup_dir = os.path.join(dir_name, 'backups')
    backup = False
    if not os.path.exists(backup_dir):
        backup = True
        os.mkdir(backup_dir)
        shutil.copy2(idf_file, os.path.join(backup_dir, backup_dir))
    if os.path.exists(idf_file + '_original'):
        idf_file = idf_file + '_original'
        if backup:
            shutil.copy2(idf_file, os.path.join(backup_dir, idf_file))
    elif os.path.exists(idf_file + 'before_ena'):
        idf_file = idf_file + 'before_ena'
        if backup:
            shutil.copy2(idf_file, os.path.join(backup_dir, idf_file))
    return idf_file


def get_magetab_path(ae_acc):
    """
    Retrieve full path containing MAGE-TAB files for an experiment given its accession by searching Subs-tracking database
    and then search recursively in the submission directory.

    :param ae_acc: ArrayExpress accession, e.g. E-MTAB-xxxx
    :type ae_acc: str

    :return: Full path for the directory containing MAGE-TAB files
    """
    exp_id = retrieve_experiment_id_by_accession(ae_acc)
    dir_name = 'MAGE-TAB_' + str(exp_id)
    dirs = os.listdir(ANNOTARE_DIR)
    if dir_name in dirs:
        dir_name = os.path.join(ANNOTARE_DIR, dir_name)
    else:
        dir_name = get_full_path(dir_name)
    return dir_name


def get_fq_uri(acc, pair_order=''):
    vol = None
    sub_dir = acc[:6]
    if len(acc) > 9:
        vol = acc[9:]
        vol = '0' * (3 - len(vol)) + vol
    fq_uri = ENA_FTP_URI + sub_dir
    if vol:
        fq_uri += '/' + vol
    fq_uri += '/' + acc + '/' + acc
    fq_uri += '%s.fastq.gz' % pair_order
    return fq_uri


def get_mage_tab(ae_acc):
    """
    Parse the MAGE-TAB files into mapping objects.

    :param ae_acc: ArrayExpress accession, e.g. E-MTAB-xxxx
    :type ae_acc: str

    :return: (idf_object, sdrf_object)
    :rtype: (IDF, SdrfCollection)
    """
    dir_name = get_magetab_path(ae_acc)
    print dir_name
    # print dir_name
    idf_file = get_idf_path(ae_acc, dir_name)
    sdrf_file = extract_sdrf_file_name(exp_path=dir_name, accession=ae_acc)
    idf_obj = IDF(idf_path=idf_file, skip_release_date=True)
    sdrf_obj = SdrfCollection(file_path=sdrf_file, mixed_pairs=True)

    return idf_obj, sdrf_obj


def as_range(g):
    l = list(g)
    return l[0], l[-1]


def get_idf_ena_comment(runs):
    """
    Constructs the comments added to the IDF file.
    These comments containing ENA runs associated with the brokered experiment.

    :param runs: List of ENA run accessions

    :return: The constructed comment containing ENA runs URLs
    :rtype: str
    """
    runs_int = sorted(list(set(list([int(r.replace('ERR', '')) for r in runs if r != '']))))
    urls = []
    print urls
    l = [as_range(g) for _, g in groupby(runs_int, key=lambda n, c=count(): n - next(c))]
    for i in l:
        url = 'http://www.ebi.ac.uk/ena/data/view/ERR%s-ERR%s' % (i[0], i[1])
        urls.append(url)

    return "Comment[SequenceDataURI]\t" + '\t'.join(sorted(list(set(urls))))


def add_ena_accessions(ae_acc, idf, sdrf, out_file):
    """
    Adds ENA accessions to an ArrayExpress experiment.

    :param ae_acc: Experiment's accession numbner. e.g. E-MTAB-xxxx
    :param idf: Idf object
    :type idf: IDF
    :param sdrf: SDRF object
    :type sdrf: SdrfCollection
    :param out_file: Full path for the output file that contains IDF and SDRF together after adding ENA accessions.
    """
    study = get_ena_acc_and_submission_acc_by_ae_acc(ae_acc)
    ena_accession = study[0].study_id
    # submission_accession = study[0].submission_id

    ena_study = ENAStudy(ena_accession)
    for row in sdrf.rows:
        exp = ena_study.get_exp_by_file_name(row.data_file)

        if exp:
            # print exp
            run = exp.get_run_by_file_name(row.data_file)
            row.ena_run = run.run_acc
            row.bio_sample = run.sample.bio_sample
            row.ena_sample = run.sample.sample_acc
            row.ena_experiment = exp.exp_acc
            if not row.fq_uri:
                row.fq_uri = get_fq_uri(run.run_acc, row.pair_order)
        else:
            print 'No Experiment: ', row.__dict__
            exit()
    empty = [r.__dict__ for r in sdrf.rows if r.ena_run is None]
    if empty:
        for i in empty:
            print i
            print '-' * 30
            exit()
    idf_ena_comment = get_idf_ena_comment([r.ena_run for r in sdrf.rows])
    # print idf_ena_comment

    combined = ['[IDF]'] + idf.lines + \
               ['Comment[SecondaryAccession]\t' +
                ena_accession] + \
               [idf_ena_comment] + \
               ['[SDRF]'] + sdrf.get_lines_with_ena()
    # for i in combined:
    #     print i.encode('utf8')
    # idf_file = os.path.join(idf.id_path.replace('_original', '').replace('before_ena', ''))
    f = codecs.open(out_file, 'w', 'UTF8')
    try:
        write_string = (u'%s' % os.linesep).join([i for i in combined])
    except Exception, e:
        write_string = (u'%s' % os.linesep).join([i.decode('utf8') for i in combined])
    f.write(write_string)
    f.close()
    print 'combined magetab written to ' + out_file

    # for l in sdrf.get_lines_with_ena():
    #     print l


if __name__ == '__main__':
    # import urllib2
    # try:
    #     request = urllib2.Request('ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR974/ERR974984/ERR974984.fastq.gz')
    #     response = urllib2.urlopen(request)
    #     print 'Web site exists'
    # except urllib2.URLError, e:
    #     print e
    # _idf, _sdrf = get_mage_tab(ae_acc='E-MTAB-4617')
    # add_ena_accessions(ae_acc='E-MTAB-4617', idf=_idf, sdrf=_sdrf, out_file=_idf.id_path)
    runs = """ERR2093974
ERR2093974
ERR2093975
ERR2093975
ERR2093976
ERR2093976
ERR2093977
ERR2093977
ERR2093978
ERR2093978
ERR2093979
ERR2093979
ERR2093980
ERR2093980
ERR2093981

""" .split('\n')
    print get_idf_ena_comment(runs)
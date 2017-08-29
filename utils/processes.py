__author__ = 'Ahmed G. Ali'

from bsub import bsub

UNLOADER_PATH = '/ebi/microarray/home/arrayexpress/ae2_production/software/framework/MAGETABUnLoader.sh'
UNLOAD_CLEAN_PATH = '/ebi/microarray/home/arrayexpress/ae2_production/software/bin/unloadCleanup.sh'
FULL_FTP_LOCATION = '/ebi/ftp/pub/databases/arrayexpress/data/'


def unload_experiment(ae_id):
    unload_command = """%s -a %s""" % (UNLOADER_PATH, ae_id)
    clean_command = """%s -a %s -f %s""" % (UNLOAD_CLEAN_PATH, ae_id, FULL_FTP_LOCATION)
    print unload_command
    print clean_command
    j = bsub(unload_command)
    j2 = j.then(clean_command)
    print j
    print j2
    print dir(j)
    print dir(j2)
    print j.__dict__
    print j2.__dict__

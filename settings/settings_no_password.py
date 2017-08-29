__author__ = 'Ahmed G. Ali'
ANNOTARE_DB = {
    'name': 'annotare2',
    'host': 'mysql-annotare-prod.ebi.ac.uk',
    'port': 4444,
    'username': '',
    'password': ''

}
AE_AUTO_SUB_DB = {
    'name': 'ae_autosubs',
    'host': 'mysql-ae-autosubs-prod.ebi.ac.uk',
    'port': 4091,
    'username': '',
    'password': ''

}
AE2 = {
    'name': 'AE2PRO',
    'host': 'ora-vm5-022.ebi.ac.uk',
    'port': '1531',
    'username': '',
    'password': ''

}

BIOSTUDIES_DB = {
    'name': 'BIOSDRO',
    'host': 'ora-dlvm-010.ebi.ac.uk',
    'port': '1521',
    'username': '',
    'password': '',
    'is_service': True

}
ERA = {
    'name': 'ERAPRO',
    'host': 'ora-vm-009.ebi.ac.uk',
    'port': '1541',
    'username': '',
    'password': ''

}
CONAN_DB = {
    'name': 'AE2PRO',
    'host': 'ora-vm5-022.ebi.ac.uk',
    'port': '1531',
    'username': '',
    'password': ''

}

ANNOTARE_DIR = '/ebi/microarray/ma-exp/AutoSubmissions/annotare/'

GEO_ACCESSIONS_PATH = '/ebi/microarray/home/fgpt/sw/lib/perl/supporting_files/geo_import_supporting_files/geo_accessions.yml'
TEMP_FOLDER = '/nfs/ma/home/arrayexpress/ae_automation/ae_automation/tmp/'
ADF_LOAD_DIR = '/nfs/ma/home/arrayexpress/ae2_production/data/ARRAY/GEOD'
BASH_PATH = '/nfs/ma/home/arrayexpress/ae_automation/ae_automation/env_bashrc'
EXPERIMENTS_PATH = '/ebi/microarray/home/arrayexpress/ae2_production/data/EXPERIMENT/'
ADF_DB_FILE = '/nfs/production3/ma/home/atlas3-production/sw/configs/adf_db_patterns.txt'

ENA_SRA_URL = 'https://www.ebi.ac.uk/ena/submit/drop-box/submit/' \
              '?auth='
ENA_SRA_DEV_URL = 'https://www-test.ebi.ac.uk/ena/submit/drop-box/submit/' \
              '?auth='
ENA_FTP_URI = 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/'
ENA_DIR = '/fire/staging/aexpress/'

CONAN_URL = 'http://banana.ebi.ac.uk:14054/conan2/'

CONAN_LOGIN_EMAIL = ''

AUTOMATION_EMAIL = 'AE Automation<ae-automation@ebi.ac.uk>'
SMTP = 'smtp.ebi.ac.uk'
CURATION_EMAIL = ''

GEO_SOFT_URL = 'ftp://ftp.ncbi.nih.gov/pub/geo/DATA/SOFT/by_%s/'

ATLAS_CONTACT = {'name': 'Curators', 'email': ''}
PMC_BASE_URL = 'http://www.ebi.ac.uk/europepmc/webservices/rest/'
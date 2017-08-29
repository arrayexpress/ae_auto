import re
import string

import settings
from dateutil.parser import parse

__author__ = 'Ahmed G. Ali'
MAPPING = {
    "ID": "Reporter Name",
    "SEQUENCE": "Reporter Sequence",
    "GB_ACC": "Reporter Database Entry [genbank]",
    "GB_LIST": "Reporter Database Entry [genbank]",
    "GB_RANGE": "Comment[GB_RANGE]",
    "RANGE_GB": "Comment[RANGE_GB]",
    "RANGE_START": "Comment[RANGE_START]",
    "RANGE_END": "Comment[RANGE_END]",
    "RANGE_STRAND": "Comment[RANGE_STRAND]",
    "GI": "Reporter Database Entry [gi]",
    "GI_LIST": "Reporter Database Entry [gi]",
    "GI_RANGE": "Comment[GI_RANGE]",
    "CLONE_ID": "Reporter Database Entry [clone_id]",
    "CLONE_ID_LIST": "Reporter Database Entry [clone_id]",
    "ORF": "Comment[ORF]",
    "ORF_LIST": "Comment[ORF]",
    "GENOME_ACC": "Comment[GENOME_ACC]",
    "SNP_ID": "Reporter Database Entry [dbsnp]",
    "SNP_ID_LIST": "Reporter Database Entry [dbsnp]",
    "miRNA_ID": "Reporter Database Entry [mirbase]",
    "miRNA_ID_LIST": "Reporter Database Entry [mirbase]",
    "SPOT_ID": "Comment[SPOT_ID]",
    "ORGANISM": "Reporter Group [organism]",
    "PT_ACC": "Reporter Database Entry [genbank]",
    "PT_LIST": "Reporter Database Entry [genbank]",
    "PT_GI": "Reporter Database Entry [genbank]",
    "PT_GI_LIST": "Reporter Database Entry [genbank]",
    "SP_ACC": "Reporter Database Entry [swissprot]",
    "SP_LIST": "Reporter Database Entry [swissprot]",
    "Description": "Reporter Comment",
    "LOCUSLINK_ID": "Reporter Database Entry [locus]",
    "UNIGENE_ID": "Reporter Database Entry [unigene]",
    "CHROMOSOMAL_LOCATION": "Reporter Database Entry [chromosome_coordinate]",
    "DESCRIPTION": "Reporter Comment"
}


class SoftHeaderMapper:
    def __init__(self, header):
        self.is_seq = False
        self.header_txt = None
        elms = {}
        self.refs = []
        self.heading = []
        for line in header:
            parts = line.replace('!', '').replace('^', '').strip().split('=')
            tag = parts[0].strip()
            value = '='.join(parts[1:]).strip()
            tag = tag.lower().replace('platform_', '')
            # print tag, ': ', value

            if tag.lower() == 'technology' and value.lower() == 'high-throughput sequencing':
                self.is_seq = True
            if tag.startswith('#'):
                v = MAPPING.get(tag.replace('#', '').upper(), '')
                if v != '':
                    self.heading.append((v, value.replace('"', ' ').replace("'", ' ')))
                if v.startswith('Reporter Database Entry'):
                    self.refs.append(v.split('[')[1].split(']')[0])

            if tag in elms.keys():

                elms[tag] += ' ' + value
            else:
                elms[tag] = value
        self.__dict__.update(elms)

    def generate_header(self):
        geo_date = parse(' '.join(self.__dict__.get('status').split(' ')[2:])).date().isoformat()

        relations = re.findall('\s[A-FH-Z]', self.__dict__.get('relation', ''))
        alternatives = []
        for r in relations:
            if r.startswith('ternative to:'):
                alternatives.append(r)
        email = [i.strip() for i in self.__dict__.get('contact_email', 'geo@ncbi.nlm.nih.gov').split(',')]
        if len(email) > 1 and 'geo@ncbi.nlm.nih.gov' in email:
            email.remove('geo@ncbi.nlm.nih.gov')
        email = email[0]
        header_txt = [
            ('Array Design Name', self.__dict__.get('title')),
            ('Provider', '%s (%s)' % (
                self.__dict__.get('contact_name', ''), email)),
            ('Printing Protocol', self.__dict__.get('manufacture_protocol', '')),
            ('Surface Type', self.__dict__.get('coating', '')),
            # ('Surface Type Term Source Ref', self.__dict__.get('coating','')),
            ('Substrate Type', self.__dict__.get('platform_support', '')),
            # ('Comment[ArrayExpressAccession]', self.__dict__.get('platform').replace('GPL', 'A-GEOD-')),
            ('Comment[SecondaryAccession]', self.__dict__.get('platform')),
            ('Comment[Description]', self.generate_description()),
            ('Comment[SubmittedName]', self.__dict__.get('title')),
            ('Comment[Organism]', self.__dict__.get('organism')),
            ('Comment[ArrayExpressReleaseDate]', geo_date),
            ('Comment[AdditionalFile:TXT]', self.__dict__.get('platform').replace('GPL', 'A-GEOD-') + '_comments.txt'),
            ('Term Source Name', '\t'.join(self.refs))

        ]
        self.header_txt = ''
        for k, v in header_txt:
            self.header_txt += '%s\t%s\n' % (k, v)

    def generate_description(self):
        des = []
        if self.__dict__.get('manufacturer', None):
            des.append('Array Manufacturer: ' + self.__dict__.get('manufacturer'))
        if self.__dict__.get('catalog_number', None):
            des.append('Catalogue number: ' + self.__dict__.get('catalog_number'))
        if self.__dict__.get('distribution', None):
            des.append('Distribution: ' + self.__dict__.get('distribution'))
        if self.__dict__.get('technology', None):
            des.append('Technology: ' + self.__dict__.get('technology'))
        return '%s %s' % (', '.join(des), '<br/>'.join(['%s = %s' % (i[0], i[1]) for i in self.heading]))


class SoftTableMapper:
    def __init__(self, table):
        self.table = ''
        self._allowed_dbs = {}
        self.header_descriptions = []
        header_parsed = False
        self.rows = []
        self.soft_header = []
        self.ae_header = []
        self.load_allowed_dbs()
        self.indexes = []
        self.comments = ''

        while True:

            if len(table) == 0:
                break
            line = table[0]

            parts = line.strip().split('\t')
            for i in range(len(parts)):
                if parts[i] == '':
                    parts[i] = ' '
            self.comments += '\t'.join([p for i, p in enumerate(parts) if i not in self.indexes]) + '\n'
            if not header_parsed:
                self.soft_header = parts
                header_parsed = True
                self.get_ae_header()

                for i in range(len(self.ae_header)):
                    if self.ae_header[i].lower().startswith('reporter') and 'comment' not in self.ae_header[i].lower():
                        self.indexes.append(i)
                self.comments = ''
                del table[0]
                continue
            line = '\t'.join([p for i, p in enumerate(parts) if i in self.indexes]) + '\n'

            self.table += filter(lambda x: x in string.printable, line)
            del table[0]

        self.table = '\t'.join(
            [h for h in self.ae_header if self.ae_header.index(h) in self.indexes]) + '\n' + self.table
        self.comments = '\t'.join(
            [h for h in self.ae_header if self.ae_header.index(h) not in self.indexes]) + '\n' + self.comments

    def get_ae_header(self):
        for item in self.soft_header:
            if item in MAPPING.keys():
                self.ae_header.append(MAPPING[item])
            elif 'LINK_PRE:' in item:
                lookup_url = '?'.join(
                    [i for i in self.header_descriptions if i[0] == item][0].split('"')[1].split('?')[:-1])
                db_name = self.get_db_name(lookup_url)
                if db_name:
                    self.ae_header.append('Reporter Database Entry [%s]' % db_name)
            else:
                self.ae_header.append('Comment[%s]' % item)

    def get_db_name(self, url):
        if url in self._allowed_dbs.keys():
            return self._allowed_dbs[url]
        return None

    def load_allowed_dbs(self):
        f = open(settings.ADF_DB_FILE, 'r')
        lines = f.readlines()
        f.close()
        for line in lines:

            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue
            self._allowed_dbs[parts[2].replace('http://', '').replace('https://', '')] = parts[0]

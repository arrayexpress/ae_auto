import os
import re
import string
from collections import OrderedDict

import chardet
import datetime
import csv
from clint.textui import colored
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import unicodedata

__author__ = 'Ahmed G. Ali'


class IDFElementSingle:
    def __init__(self, exps, reg):
        elms = {}
        for title, val in exps.items():
            if not val:
                val = ['']
            elms[title.replace(reg + '_', '')] = val[0]
        self.__dict__.update(elms)


class IDFElementMultiple(list):
    def __init__(self, exps, reg):
        super(IDFElementMultiple, self).__init__()
        lst = [len(vals) for t, vals in exps.items()]
        if not lst:
            max_val = 0
        else:
            max_val = max([len(vals) for t, vals in exps.items()])
        elements = []
        for i in range(max_val):
            element = {}
            for k in exps.keys():
                if len(exps[k]) > i:
                    element[k] = [exps[k][i]]
                else:
                    element[k] = [None]
            elements.append(element)
        for element in elements:
            self.append(IDFElementSingle(element, reg))


class IDF:
    def __init__(self, idf_path=None, combined=False, skip_release_date=False):

        self.lines = []
        self.rewrite = False
        self.skip_release_date = skip_release_date
        if self.skip_release_date:
            print colored.magenta('Take care! Release date are not going to be edited.', bold=True)
        self.id_path = idf_path
        self.combined = combined
        self.original_mapping = {}
        if idf_path:
            self.__load_idf()
        self.experiment = IDFElementSingle(dict([i for i in self.__dict__.items() if i[0].startswith('experiment')]),
                                           'experiment')
        self.persons = IDFElementMultiple(dict([i for i in self.__dict__.items() if i[0].startswith('person')]),
                                          'person')
        self.protocols = IDFElementMultiple(dict([i for i in self.__dict__.items() if i[0].startswith('protocol')]),
                                            'protocol')

        self.terms = IDFElementMultiple(dict([i for i in self.__dict__.items() if i[0].startswith('term')]),
                                        'term')
        self.publications = IDFElementMultiple(
            dict([i for i in self.__dict__.items() if i[0].startswith('publication') or i[0].startswith('pubmed')]),
            'publication')
        self.__dict__['mage-tab_version'] = ['1.1']

    def __load_idf(self):
        elms = {}
        lines = []
        with open(self.id_path, 'rb') as csvfile:
            idf_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            for row in idf_reader:
                # row = [u"".join([re.sub(r'[\x00-\x1f]', '',c) for c in unicodedata.normalize('NFKD', i.decode('utf8')) if not unicodedata.combining(c)]) for i in row]
                row = [re.sub(r'[\x00-\x1f]', '', i).decode('utf8') for i in row]
                if self.combined:
                    if '[idf]' in row[0].lower() or row == ['']:
                        continue
                    if '[sdrf]' in row[0].lower():
                        break
                line = '\t'.join(row)
                self.rewrite = True
                line = filter(lambda x: x in string.printable, line)
                lines.append(line)
                if row[0] == 'Public Release Date':
                    if parse(row[1]) < datetime.datetime.now() + datetime.timedelta(
                            days=10) and not self.skip_release_date:
                        self.rewrite = True
                        line = line.replace(row[1], (datetime.date.today() + datetime.timedelta(days=10)).isoformat())
                        row[1] = (datetime.date.today() + datetime.timedelta(days=10)).isoformat()
                        # lines[i] = line.encode('utf8', 'ignore')

                    elif parse(row[1]) > (datetime.datetime.now() + relativedelta(years=2)):
                        self.rewrite = True
                        line = line.replace(row[1], (datetime.date.today() + relativedelta(years=2)).isoformat())
                        row[1] = (datetime.date.today() + relativedelta(years=2)).isoformat()
                        # lines[i] = line.encode('utf8', 'ignore')
                self.original_mapping[row[0].lower().replace(' ', '_')] = row[0]
                elms[row[0].lower().replace(' ', '_')] = row[1:]
                if not line.startswith('SDRF File'):
                    self.lines.append(line)

        self.__dict__.update(elms)

    def generate_idf(self):
        # print self.original_mapping
        # exit()
        fields = OrderedDict([
            ('MAGE-TAB Version', '1.1'),
            ('Investigation Title', ''),
            ('Experiment Description', None),
            ('Experimental Design', None),
            ('Experimental Design Term Source REF', None),
            ('Experimental Design Term Accession Number', None),
            ('Experimental Factor Name', None),
            ('Experimental Factor Type', None),
            ('Experimental Factor Term Source REF', None),
            ('Experimental Factor Term Accession Number', None),
            ('Person Last Name', None),
            ('Person First Name', None),
            ('Person Mid Initials', None),
            ('Person Email', None),
            ('Person Phone', None),
            ('Person Fax', None),
            ('Person Address', None),
            ('Person Affiliation', None),
            ('Person Roles', None),
            ('Date of Experiment', None),
            ('Public Release Date', None),
            ('Protocol Name', None),
            ('Protocol Type', None),
            ('Protocol Term Source REF', None),
            ('Protocol Term Accession Number', None),
            ('Protocol Description', None),
            ('Protocol Hardware', None),
            ('Protocol Software', None),
            ('Term Source Name', None),
            ('Term Source File', None),
            ('Term Source Version', None)
        ])
        if hasattr(self, 'comments'):
            for c, v in self.comments.items():
                fields['Comment[%s]' % c] = v

        for k, v in fields.items():
            fields[k] = '\t'.join(getattr(self, k.lower().replace(' ', '_'), []))

        for h, v in fields.items():
            print '%s\t%s' % (h, v)


if __name__ == '__main__':
    idf = IDF(idf_path='/home/gemmy/submission3559_annotare_v1.idf.txt')
    for p in idf.protocols:
        print p.description
    exit()
    for k, v in idf.__dict__.items():

        if isinstance(v, str):
            print k, ': ', v
        elif isinstance(v, IDFElementMultiple):
            for a in v:
                if isinstance(a, str):
                    print k, ': ', a
                else:
                    print k, ': ', a, a.__dict__
        elif isinstance(v, IDFElementSingle):
            print k, ': ', v, v.__dict__
        else:
            print k, ': ', v
    for p in idf.persons:
        print p.__dict__
        # print idf.experiment.__dict__

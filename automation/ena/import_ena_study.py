import os
from collections import OrderedDict

from dal.oracle.era.experiment import get_experiment_xml_by_acc, retrieve_experiments_by_study_acc
from dal.oracle.era.study import get_study_xml_by_acc, get_study_by_acc
from models.magetab.idf import IDF
# from models.sra_xml.study_api import parse
from models.sra_xml import study_api, experiment_api
from settings import TEMP_FOLDER

import xml.etree.ElementTree as ET
__author__ = 'Ahmed G. Ali'


def extract_factors(exp):
    factors = {}
    for att in exp.EXPERIMENT[0].EXPERIMENT_ATTRIBUTES.EXPERIMENT_ATTRIBUTE:
        if 'factor' in att.TAG.lower():
            factors[att.TAG.split(':')[1].strip()] = att.VALUE

    return factors

def main(study_acc):
    study = get_study_by_acc(study_acc)
    study = study[0]
    print study
    ae_acc = ''
    if study.arrayexpress_id:
        ae_acc = study.arrayexpress_id
    elif study.center_name == 'GEO':
        ae_acc = study.study_alias.split(':')[1].strip().replace('GSE', 'E-GEOD-')
    else:
        ae_acc = 'E-MTAB-new'

    # exit()
    study_xml = get_study_xml_by_acc(study_acc)
    # print study[0].s_xml
    tmp_path = os.path.join(TEMP_FOLDER, study_acc)
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    study_xml[0][0].s_xml = study_xml[0][0].s_xml.read()
    study_xml[1].close()
    study_xml = study_xml[0][0]
    f_name = os.path.join(tmp_path, 'study.xml')
    f = open(f_name, 'w')
    f.write(study_xml.s_xml)
    f.close()

    a = study_api.parse(f_name, silence=True)

    idf = IDF()
    # print a.STUDY[0].__dict__
    study_xml = a.STUDY[0]
    idf.investigation_title = [study_xml.DESCRIPTOR.STUDY_TITLE.strip().replace('_', ' ')]
    idf.comments = OrderedDict()
    if study_xml.DESCRIPTOR.STUDY_TYPE.existing_study_type == 'Other':
        idf.comments['aeexperimenttype'] = [study_xml.DESCRIPTOR.STUDY_TYPE.new_study_type]
    else:
        idf.comments['aeexperimenttype'] = [study_xml.DESCRIPTOR.STUDY_TYPE.existing_study_type]

    idf.experiment_description = [study_xml.DESCRIPTOR.STUDY_DESCRIPTION.replace('\n', ' ')]
    idf.generate_idf()

    experiments = retrieve_experiments_by_study_acc(study_acc)
    # print experiments
    exp_xmls = []
    for e in experiments:
        exp = get_experiment_xml_by_acc(e.experiment_id)
        exp[0][0].e_xml = exp[0][0].e_xml.read()
        exp[1].close()
        exp = exp[0][0]
        # exp_xmls.append(exp)
        f_name = os.path.join(tmp_path, 'exp_%s.xml' % e.experiment_id)
        f = open(f_name, 'w')
        f.write(exp.e_xml)
        f.close()
        exp_xmls.append(experiment_api.parse(f_name, silence=True))

        break

    print exp_xmls[0]
    factors = extract_factors(exp_xmls[0])
    print factors



    # print idf.__dict__
    # print idf.experiment.__dict__
    # print idf


if __name__ == '__main__':
    main('ERP014059')

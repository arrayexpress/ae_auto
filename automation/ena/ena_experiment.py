import random
import string

import os
import time
import unicodedata

from clint.textui import colored

from models.sra_xml import run_api, study_api, submission_api, experiment_api, sample_api
from resources.eutils import esearch

__author__ = 'Ahmed G. Ali'


def load_centers():
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'centrelist'), 'r')
    lines = f.readlines()
    f.close()
    centers = {}
    for i in range(1, len(lines)):
        a = lines[i].strip().split('\t')
        if len(a) == 1:
            continue
        # a[0] = unicodedata.normalize('NFKD', a[0])
        # a[0] = u"".join([c for c in a[0] if not unicodedata.combining(c)]).strip()
        # a[1] = unicodedata.normalize('NFKD', a[1])
        # a[1] = u"".join([c for c in a[1] if not unicodedata.combining(c)]).strip()
        centers[a[1].replace('"', '')] = a[0].replace('"', '')
    return centers


class ENAExperiment:
    def __init__(self, accession, sdrf, idf, time_stamp, added_samples=[], study_accession=None, new_alias=None,
                 center_name=None):
        self.accession = accession
        self.idf = idf
        self.sdrf = sdrf
        self.time_stamp = time_stamp
        self.added_samples = added_samples
        self.study_accession = study_accession
        if not new_alias:
            new_alias = ''
        if self.added_samples and new_alias == '':
            self.new_alias = str(int(time.time()))
        else:
            self.new_alias = new_alias
        self.submitter = [p for p in self.idf.persons if p.roles == 'submitter']
        if not self.submitter:
            self.submitter = self.idf.persons[0]
        else:
            self.submitter = self.submitter[0]
        if not hasattr(self.submitter, 'mid_initials'):
            self.submitter.mid_initials = ''
        if center_name:
            self.submitter.affiliation = center_name
        else:
            mapped_centers = load_centers()
            replace = True
            for k, v in mapped_centers.items():
                if self.submitter.affiliation == k:
                    self.submitter.affiliation = v
                    print colored.green('''Center name found.
                    Using this name for submission:%s instead of the name in the IDF: %s''' % (v, k))
                    replace = False
                    break
            if replace:
                self.submitter.affiliation = unicodedata.normalize('NFKD', self.submitter.affiliation)
                self.submitter.affiliation = u"".join(
                    [c for c in self.submitter.affiliation if not unicodedata.combining(c)]).strip()

        self.searched_organisms = {}
        self.save_dir = None

    def generate_xmls(self, save_dir):
        self.save_dir = save_dir
        self.__generate_experiment_xml()
        self.__generate_run_xml()
        self.__generate_sample_xml()
        self.__generate_study_xml()
        self.__generate_submission_xml()

    def __generate_sample_xml(self):
        added_samples = []
        samples = []
        for row in self.sdrf.rows:
            dct = row.__dict__
            if row.__dict__.get('ena_alias', None):
                continue
            sample = row.source
            if sample in added_samples or sample in self.added_samples:
                continue
            added_samples.append(sample)
            protocols = []
            for protocol_name in row.exp_protocols:
                protocol = [pr for pr in self.idf.protocols if pr.name.strip().lower().replace(' ', '') ==
                            protocol_name.strip().lower().replace(' ', '')]
                if not protocol:
                    continue
                protocol = protocol[0]
                protocols.append(protocol.description)
            attribute_list = [sample_api.AttributeType(TAG='isolate',
                                                       VALUE='not applicable')]
            organism = ''
            for char in row.chars:
                if char.keys()[0].lower() == 'organism':
                    organism = char.values()[0]['value']
                attribute_list.append(sample_api.AttributeType(TAG=char.keys()[0],
                                                               VALUE=char.values()[0]['value'],
                                                               UNITS=char.values()[0]['unit']))
            taxonomy_id = None
            if organism not in self.searched_organisms.keys():
                eutils_result = esearch(db='taxonomy', term=organism)
                if eutils_result['esearchresult']['idlist']:
                    taxonomy_id = int(eutils_result['esearchresult']['idlist'][0])
                else:
                    raise Exception('Taxonomy ID for %s was not found on eutils. '
                                    'Please try to check the organism in the SDRF' % organism)
                self.searched_organisms[organism] = taxonomy_id
            sample_name = sample_api.SAMPLE_NAMEType(TAXON_ID=self.searched_organisms[organism],
                                                     SCIENTIFIC_NAME=organism,
                                                     COMMON_NAME=None,
                                                     ANONYMIZED_NAME=None,
                                                     INDIVIDUAL_NAME=None)
            samples.append(
                sample_api.SampleType(self.submitter.affiliation,
                                      alias='%s:%s' % (self.accession + self.new_alias, sample),
                                      broker_name='ArrayExpress',
                                      accession=None,
                                      IDENTIFIERS=None,
                                      TITLE=sample,
                                      SAMPLE_NAME=sample_name,
                                      DESCRIPTION='Protocols: %s' % ' '.join(protocols),
                                      SAMPLE_LINKS=None,
                                      SAMPLE_ATTRIBUTES=sample_api.SAMPLE_ATTRIBUTESType(
                                          SAMPLE_ATTRIBUTE=attribute_list)))

        sample_set = sample_api.SampleSetType(SAMPLE=samples)
        sample_set.export(
            open(os.path.join(self.save_dir, '%s_%s_sample.xml' % (self.accession, self.time_stamp)), 'w'), 0,
            name_='SAMPLE_SET')

    def __generate_experiment_xml(self):
        experiments = []
        added_extracts = []
        for row in self.sdrf.rows:
            extract = row.extract_detailed
            if extract in added_extracts or row.source in self.added_samples:
                continue
            added_extracts.append(extract)
            single = None
            paired = None

            if not row.is_paired:
                single = experiment_api.SINGLEType()

            else:
                paired = experiment_api.PAIREDType(NOMINAL_LENGTH=round(float(row.nominal_length)),
                                                   NOMINAL_SDEV=row.nominal_sdev)

            protocols = []
            for protocol_name in row.exp_protocols:
                protocol = [pr for pr in self.idf.protocols if pr.name.strip().lower().replace(' ', '') ==
                            protocol_name.strip().lower().replace(' ', '')]
                if not protocol:
                    continue
                protocol = protocol[0]
                protocols.append(protocol.description)
            library_descriptor = experiment_api.LibraryDescriptorType(LIBRARY_NAME=extract,
                                                                      LIBRARY_STRATEGY=row.library_strategy,
                                                                      LIBRARY_SOURCE=row.library_source,
                                                                      LIBRARY_SELECTION=row.library_selection,
                                                                      LIBRARY_LAYOUT=experiment_api.LIBRARY_LAYOUTType(
                                                                          SINGLE=single, PAIRED=paired),
                                                                      TARGETED_LOCI=None,
                                                                      POOLING_STRATEGY=None,
                                                                      LIBRARY_CONSTRUCTION_PROTOCOL=' '.join(
                                                                          protocols))
            # library_descriptor.export(sys.stdout, 0)
            spot_spectator = None
            if row.is_paired:
                print row.new_data_file, row.source, row.read_index
                read_specs = [
                    experiment_api.READ_SPECType(READ_INDEX=0,
                                                 READ_LABEL='F',
                                                 READ_CLASS='Application Read',
                                                 READ_TYPE='Forward',
                                                 RELATIVE_ORDER=None,
                                                 BASE_COORD=1,
                                                 EXPECTED_BASECALL_TABLE=None),

                    experiment_api.READ_SPECType(READ_INDEX=1,
                                                 READ_LABEL='R',
                                                 READ_CLASS='Application Read',
                                                 READ_TYPE='Reverse',
                                                 RELATIVE_ORDER=None,
                                                 BASE_COORD=int(row.read_index),
                                                 EXPECTED_BASECALL_TABLE=None)
                ]
                spot_decode = experiment_api.SPOT_DECODE_SPECType(SPOT_LENGTH=int(row.spot_length),
                                                                  READ_SPEC=read_specs)
                spot_spectator = experiment_api.SpotDescriptorType(SPOT_DECODE_SPEC=spot_decode)
            if '.csfasta' in row.new_data_file or '.qual' in row.new_data_file:
                read_specs = [
                    experiment_api.READ_SPECType(READ_INDEX=0,
                                                 READ_LABEL='F',
                                                 READ_CLASS='Application Read',
                                                 READ_TYPE='Forward',
                                                 RELATIVE_ORDER=None,
                                                 BASE_COORD=1,
                                                 EXPECTED_BASECALL_TABLE=None)
                ]
                spot_decode = experiment_api.SPOT_DECODE_SPECType(READ_SPEC=read_specs)
                spot_spectator = experiment_api.SpotDescriptorType(SPOT_DECODE_SPEC=spot_decode)
            sample_alias = row.__dict__.get('ena_alias', None)
            if not sample_alias:
                sample_alias = '%s:%s' % (self.accession + self.new_alias, row.source)
            design = experiment_api.LibraryType(DESIGN_DESCRIPTION=self.idf.investigation_title[0],
                                                SAMPLE_DESCRIPTOR=experiment_api.SampleDescriptorType(
                                                    refname=sample_alias),
                                                LIBRARY_DESCRIPTOR=library_descriptor,
                                                SPOT_DESCRIPTOR=spot_spectator)
            # design.export(sys.stdout, 0)

            ls454 = None
            illumina = None
            helicos = None
            abi_solid = None
            complete_genomics = None
            pacbio_smrt = None
            ion_torrent = None
            capillary = None
            oxford_nanopore = None
            bgiseq = None

            extract_protocol = [p for p in self.idf.protocols if p.name == row.extract_protocol]
            if not extract_protocol:
                print colored.red('Protocol Error!', bold=True)
                print colored.red('Extract Protocol is missing for some samples in the SDRF. \n'
                                  'Please make sure there is no empty protocol '
                                  'reference just before the Assay Name column.')
                exit(1)
            recognized=False
            extract_protocol = extract_protocol[0]
            if not extract_protocol.hardware or extract_protocol.hardware == '':
                print colored.red('Hardware is missing for extract protocol.\nPlease check IDF', bold=True)
                exit(1)

            # Case Illumina
            if extract_protocol.hardware.startswith('Illumina') or \
                    extract_protocol.hardware.startswith('Solexa') or \
                    extract_protocol.hardware.startswith('HiSeq') or \
                    extract_protocol.hardware.startswith('NextSeq'):
                recognized = True
                if 'HiSeq' in extract_protocol.hardware:
                    tmp = [i.strip() for i in extract_protocol.hardware.split('HiSeq') if i != '']
                    tmp.insert(-1, 'HiSeq')
                    extract_protocol.hardware = ' '.join(tmp)
                illumina = experiment_api.ILLUMINAType(INSTRUMENT_MODEL=extract_protocol.hardware)

            # Case LS454
            if '454' in extract_protocol.hardware or 'GS' in extract_protocol.hardware:
                recognized = True
                ls454 = experiment_api.LS454Type(INSTRUMENT_MODEL=extract_protocol.hardware)
            # Case HELICOS
            if 'Helicos' in extract_protocol.hardware:
                recognized = True
                helicos = experiment_api.HELICOSType(INSTRUMENT_MODEL=extract_protocol.hardware)
            # Case SOLiD
            if 'SOLiD' in extract_protocol.hardware or \
                            'AB 5500 Genetic Analyzer'.lower() in extract_protocol.hardware.lower() or \
                            'AB 5500xl Genetic Analyzer'.lower() in extract_protocol.hardware.lower():
                recognized = True
                abi_solid = experiment_api.ABI_SOLIDType(INSTRUMENT_MODEL=extract_protocol.hardware)

            # Case Ion Torrent
            if extract_protocol.hardware.startswith('Ion'):
                recognized = True
                ion_torrent = experiment_api.ION_TORRENTType(INSTRUMENT_MODEL=extract_protocol.hardware)
            # Case Complete Genome
            if "Complete Genomics" in extract_protocol.hardware:
                recognized = True
                complete_genomics = experiment_api.COMPLETE_GENOMICSType(INSTRUMENT_MODEL=extract_protocol.hardware)

            # Case OXFORD_NANOPORE
            if 'MinION' in extract_protocol.hardware or 'GridION' in extract_protocol.hardware:
                recognized = True
                complete_genomics = experiment_api.OXFORD_NANOPOREType(INSTRUMENT_MODEL=extract_protocol.hardware)
            if 'BGISEQ' in extract_protocol.hardware.upper():
                recognized = True
                bgiseq = experiment_api.BGISEQType(INSTRUMENT_MODEL=extract_protocol.hardware)
            if extract_protocol.hardware.lower() in [
                'ab 3730xl genetic analyzer',
                'ab 3730 genetic analyzer',
                'ab 3500xl genetic analyzer',
                'ab 3500 genetic analyzer',
                'ab 3130xl genetic analyzer',
                'ab 3130 genetic analyzer',
                'ab 310 genetic analyzer'
            ]:
                recognized = True
                capillary = experiment_api.CAPILLARYType(INSTRUMENT_MODEL=extract_protocol.hardware)
            if 'pacbio' in extract_protocol.hardware.lower():
                recognized = True
                pacbio_smrt = experiment_api.PACBIO_SMRTType(INSTRUMENT_MODEL=extract_protocol.hardware)

            if not recognized:
                print colored.red(
                    "Hardware: '%s' has not been recognized as one of the platforms accepted by ENA." %
                    extract_protocol.hardware, bold=True)
                exit(1)
            platform = experiment_api.PlatformType(
                LS454=ls454,
                ILLUMINA=illumina,
                HELICOS=helicos,
                ABI_SOLID=abi_solid,
                COMPLETE_GENOMICS=complete_genomics,
                PACBIO_SMRT=pacbio_smrt,
                ION_TORRENT=ion_torrent,
                CAPILLARY=capillary,
                OXFORD_NANOPORE=oxford_nanopore,
                BGISEQ=bgiseq
            )
            # platform.export(sys.stdout, 0)
            attributes_lst = []
            for factor in row.factors:
                factor_val = factor.keys()[0]
                # encoding = chardet.detect(factor_val)
                # char_set = encoding['encoding']
                # factor_val = factor_val.decode(char_set)
                # factor_val = unicodedata.normalize('NFKD', factor_val)
                # factor_val = u"".join([c for c in factor_val if not unicodedata.combining(c)]).strip()
                attr = experiment_api.AttributeType(TAG='Experimental Factor: ' +factor.values()[0],
                                                    VALUE= factor_val, UNITS=None)
                # attr.export(sys.stdout, 0)
                attributes_lst.append(attr)
            expt_attributes = None
            if attributes_lst:
                expt_attributes = experiment_api.EXPERIMENT_ATTRIBUTESType(EXPERIMENT_ATTRIBUTE=attributes_lst)
            if self.study_accession:
                study_acc = None
            else:
                study_acc = self.accession + self.new_alias
            experiment = experiment_api.ExperimentType(center_name=self.submitter.affiliation,
                                                       alias='%s:%s' % (self.accession + self.new_alias, extract),
                                                       broker_name='ArrayExpress',
                                                       accession=None,
                                                       IDENTIFIERS=None,
                                                       TITLE=self.idf.investigation_title[0],
                                                       STUDY_REF=experiment_api.STUDY_REFType(
                                                           refcenter=self.submitter.affiliation,
                                                           accession=self.study_accession,
                                                           refname=study_acc, IDENTIFIERS=None),
                                                       DESIGN=design,
                                                       PLATFORM=platform,
                                                       PROCESSING=experiment_api.ProcessingType(),
                                                       EXPERIMENT_LINKS=None,
                                                       EXPERIMENT_ATTRIBUTES=expt_attributes)
            # experiment.export(sys.stdout, 0)
            experiments.append(experiment)
        exp_set = experiment_api.ExperimentSetType(EXPERIMENT=experiments)
        exp_set.export(
            open(os.path.join(self.save_dir, '%s_%s_experiment.xml' % (self.accession, self.time_stamp)), 'w'), 0,
            name_='EXPERIMENT_SET')

    def __generate_submission_xml(self):

        contact = submission_api.CONTACTType(name='%s %s %s' % (self.submitter.first_name,
                                                                self.submitter.mid_initials,
                                                                self.submitter.last_name))
        contacts = submission_api.CONTACTSType(CONTACT=[contact])
        xmls = ['sample', 'experiment', 'run']
        if not self.added_samples:
            xmls.append('study')
        else:
            submission = submission_api.SubmissionType(submission_date=None,
                                                       broker_name='ArrayExpress',
                                                       alias=self.accession + ''.join(
                                                           random.choice(string.ascii_uppercase + string.digits)
                                                           for _ in range(2)
                                                       ),
                                                       center_name=self.submitter.affiliation,
                                                       accession=None,
                                                       lab_name=None,
                                                       submission_comment=None,
                                                       IDENTIFIERS=None,
                                                       TITLE=self.idf.investigation_title[0],
                                                       CONTACTS=contacts,
                                                       ACTIONS=submission_api.ACTIONSType(ACTION=[
                                                           submission_api.ACTIONType(MODIFY=submission_api.MODIFYType(
                                                               source='%s_%s_study.xml' % (
                                                                   self.accession, self.time_stamp), schema='study'))]),
                                                       SUBMISSION_LINKS=None,
                                                       SUBMISSION_ATTRIBUTES=None)
            submission.export(
                open(os.path.join(self.save_dir, '%s_%s_submission_modify.xml' % (self.accession, self.time_stamp)),
                     'w'), 0, name_='SUBMISSION')
        action_lst = []
        for xml in xmls:
            action_lst.append(submission_api.ACTIONType(
                ADD=submission_api.ADDType(source='%s_%s_%s.xml' % (self.accession, self.time_stamp, xml), schema=xml)))
        action_lst.append(
            submission_api.ACTIONType(HOLD=submission_api.HOLDType(HoldUntilDate=self.idf.public_release_date[0])))
        submission = submission_api.SubmissionType(submission_date=None,
                                                   broker_name='ArrayExpress',
                                                   alias=self.accession + ''.join(
                                                       random.choice(string.ascii_uppercase + string.digits)
                                                       for _ in range(2)
                                                   ),
                                                   center_name=self.submitter.affiliation,
                                                   accession=None,
                                                   lab_name=None,
                                                   submission_comment=None,
                                                   IDENTIFIERS=None,
                                                   TITLE=self.idf.investigation_title[0],
                                                   CONTACTS=contacts,
                                                   ACTIONS=submission_api.ACTIONSType(ACTION=action_lst),
                                                   SUBMISSION_LINKS=None,
                                                   SUBMISSION_ATTRIBUTES=None)

        submission.export(
            open(os.path.join(self.save_dir, '%s_%s_submission.xml' % (self.accession, self.time_stamp)), 'w'), 0,
            name_='SUBMISSION')

    def __generate_study_xml(self):
        ae_types = {"RNA-seq of coding RNA": "RNASeq",
                    "RNA-seq of non coding RNA": "RNASeq",
                    "ChIP-seq": "Gene Regulation Study",
                    "CLIP-seq": "Gene Regulation Study"
                    }
        ae_type = [v for k, v in ae_types.items() if
                   self.idf.__dict__['comment[aeexperimenttype]'][0].lower() in k.lower() or
                   k.lower() in self.idf.__dict__['comment[aeexperimenttype]'][0].lower()]
        if ae_type:
            des_type = study_api.STUDY_TYPEType(
                existing_study_type=ae_type[0])
        else:
            des_type = study_api.STUDY_TYPEType(existing_study_type='Other',
                                                new_study_type=self.idf.__dict__['comment[aeexperimenttype]'][0])
        project_id = 0
        if self.added_samples:
            project_id = None
        descriptor = study_api.DESCRIPTORType(STUDY_TITLE=self.idf.investigation_title[0],
                                              STUDY_TYPE=des_type,
                                              STUDY_ABSTRACT=self.idf.experiment.description,
                                              CENTER_NAME=self.submitter.affiliation,
                                              CENTER_PROJECT_NAME=self.idf.investigation_title[0],
                                              PROJECT_ID=project_id,
                                              RELATED_STUDIES=None,
                                              STUDY_DESCRIPTION=self.idf.experiment.description)
        url_link = study_api.URL_LINKType1(LABEL='%s in ArrayExpress' % self.accession,
                                           URL='http://www.ebi.ac.uk/arrayexpress/experiments/%s' % self.accession)
        link = study_api.LinkType(URL_LINK=url_link)
        study_link = study_api.STUDY_LINKSType(STUDY_LINK=[link])
        study = study_api.StudyType(self.submitter.affiliation,
                                    alias=self.accession + self.new_alias,
                                    broker_name='ArrayExpress',
                                    accession=self.study_accession,
                                    IDENTIFIERS=None,
                                    DESCRIPTOR=descriptor,
                                    STUDY_LINKS=study_link,
                                    STUDY_ATTRIBUTES=None)
        study_set = study_api.StudySetType([study])
        study_set.export(open(os.path.join(self.save_dir, '%s_%s_study.xml' % (self.accession, self.time_stamp)), 'w'),
                         0, name_='STUDY_SET')

    def __generate_run_xml(self):
        runs = []
        added_aliases = []
        added_files = []
        for row in self.sdrf.rows:
            if (row.is_paired and not row.combined) or \
                    (row.source in self.added_samples or '.qual.' in row.new_data_file):
                continue
            row2 = None
            file_type = 'fastq'
            if row.new_data_file.endswith('.bam'):
                file_type = 'bam'
            if row.new_data_file.endswith('.sff'):
                file_type = 'sff'
            if row.new_data_file.endswith('.cram'):
                file_type = 'cram'
            if '.csfasta.' in row.new_data_file:
                file_type = "SOLiD_native_csfasta"
                row2 = [r for r in self.sdrf.rows if
                        r.source == row.source and '.qual.' in r.new_data_file and row.new_data_file.split('.')[
                            0] in r.new_data_file][0]
            if '.qual.' in row.new_data_file:
                file_type = 'SOLiD_native_qual'

            file1 = run_api.FILEType(checksum_method='MD5',
                                     ascii_offset=None,
                                     quality_encoding=None,
                                     filetype=file_type,
                                     unencrypted_checksum=None,
                                     filename=row.new_data_file,
                                     quality_scoring_system=None,
                                     checksum=row.md5,
                                     READ_LABEL=None)
            files = [file1]
            added_files.append(row.new_data_file)
            if row2 and row2.new_data_file not in added_files:
                file2 = run_api.FILEType(checksum_method='MD5',
                                         ascii_offset=None,
                                         quality_encoding=None,
                                         filetype='SOLiD_native_qual',
                                         unencrypted_checksum=None,
                                         filename=row2.new_data_file,
                                         quality_scoring_system=None,
                                         checksum=row2.md5,
                                         READ_LABEL=None)
                files.append(file2)
            files = run_api.FILESType(files)
            data = run_api.DATA_BLOCKType(FILES=files)
            exp_ref = run_api.EXPERIMENT_REFType(refcenter=self.submitter.affiliation,
                                                 accession=None,
                                                 refname='%s:%s' % (self.accession +
                                                                    self.new_alias, row.extract_detailed),
                                                 IDENTIFIERS=None)
            alias = '%s:%s' % (self.accession + self.new_alias, row.assay_name)
            if alias in added_aliases:
                added_aliases.append(alias)
                alias += '_' + str(added_aliases.count(alias) - 1)
            else:
                added_aliases.append(alias)
            run = run_api.RunType(
                broker_name='ArrayExpress',
                run_date=None,
                center_name=self.submitter.affiliation,
                run_center=row.performer,
                accession=None,
                alias=alias,
                IDENTIFIERS=None,
                TITLE=None,
                EXPERIMENT_REF=exp_ref,
                SPOT_DESCRIPTOR=None,
                PLATFORM=None,
                PROCESSING=None,
                RUN_TYPE=None,
                DATA_BLOCK=data,
                RUN_LINKS=None,
                RUN_ATTRIBUTES=None)
            runs.append(run)
        for pair in self.sdrf.pairs:
            if pair[0].source in self.added_samples or pair[1].source in self.added_samples \
                    or '.qual.' in pair[0].new_data_file or '.qual.' in pair[1].new_data_file:
                continue
            qual1 = None
            file_type = 'fastq'
            if pair[0].new_data_file.endswith('.bam'):
                file_type = 'bam'
            if pair[0].new_data_file.endswith('.cram'):
                file_type = 'cram'
            if '.csfasta.' in pair[0].new_data_file:
                file_type = "SOLiD_native_csfasta"
                qual1 = [r for r in self.sdrf.rows if r.source == pair[0].source and '.qual.' in r.new_data_file][0]
            read_lable = None
            if pair[0].new_data_file != pair[1].new_data_file:
                read_lable = 'F'
            file1 = run_api.FILEType(checksum_method='MD5',
                                     ascii_offset=None,
                                     quality_encoding=None,
                                     filetype=file_type,
                                     unencrypted_checksum=None,
                                     filename=pair[0].new_data_file,
                                     quality_scoring_system=None,
                                     checksum=pair[0].md5,
                                     READ_LABEL='F')
            files = [file1]
            if qual1:
                files.append(run_api.FILEType(checksum_method='MD5',
                                              ascii_offset=None,
                                              quality_encoding=None,
                                              filetype='SOLiD_native_qual',
                                              unencrypted_checksum=None,
                                              filename=qual1.new_data_file,
                                              quality_scoring_system=None,
                                              checksum=qual1.md5,
                                              READ_LABEL='F'))

            if pair[0].new_data_file != pair[1].new_data_file:
                qual2 = None
                file_type = 'fastq'
                if pair[1].new_data_file.endswith('.bam'):
                    file_type = 'bam'
                if pair[1].new_data_file.endswith('.cram'):
                    file_type = 'cram'
                if '.csfasta.' in pair[1].new_data_file:
                    file_type = "SOLiD_native_csfasta"
                    qual2 = [r for r in self.sdrf.rows if r.source == pair[1].source and '.qual.' in r.new_data_file][0]
                file2 = run_api.FILEType(checksum_method='MD5',
                                         ascii_offset=None,
                                         quality_encoding=None,
                                         filetype=file_type,
                                         unencrypted_checksum=None,
                                         filename=pair[1].new_data_file,
                                         quality_scoring_system=None,
                                         checksum=pair[1].md5,
                                         READ_LABEL='R')
                files.append(file2)
                if qual2:
                    files.append(run_api.FILEType(checksum_method='MD5',
                                                  ascii_offset=None,
                                                  quality_encoding=None,
                                                  filetype='SOLiD_native_qual',
                                                  unencrypted_checksum=None,
                                                  filename=qual2.new_data_file,
                                                  quality_scoring_system=None,
                                                  checksum=qual2.md5,
                                                  READ_LABEL='R'))
            files = run_api.FILESType(files)
            data = run_api.DATA_BLOCKType(FILES=files)
            exp_ref = run_api.EXPERIMENT_REFType(refcenter=self.submitter.affiliation,
                                                 accession=None,
                                                 refname='%s:%s' % (self.accession + self.new_alias,
                                                                    pair[0].extract_detailed),
                                                 IDENTIFIERS=None)
            alias = '%s:%s' % (self.accession + self.new_alias, pair[0].assay_name)
            if alias in added_aliases:
                added_aliases.append(alias)
                alias += '_' + str(added_aliases.count(alias) - 1)
            else:
                added_aliases.append(alias)
            run = run_api.RunType(
                broker_name='ArrayExpress',
                run_date=None,
                center_name=self.submitter.affiliation,
                run_center=pair[0].performer,
                accession=None,
                alias=alias,
                IDENTIFIERS=None,
                TITLE=None,
                EXPERIMENT_REF=exp_ref,
                SPOT_DESCRIPTOR=None,
                PLATFORM=None,
                PROCESSING=None,
                RUN_TYPE=None,
                DATA_BLOCK=data,
                RUN_LINKS=None,
                RUN_ATTRIBUTES=None)
            runs.append(run)
        run_set = run_api.RunSetType(RUN=runs)
        run_set.export(open(os.path.join(self.save_dir, '%s_%s_run.xml' % (self.accession, self.time_stamp)), 'w'), 0,
                       name_='RUN_SET')
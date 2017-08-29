__author__ = 'Ahmed G. Ali'


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='submits and loads sequencing experiment to ENA and ArrayExpress')
    parser.add_argument('dir_name', metavar='MAGE-TAB_xxxx', type=str,
                        help='''The directory name where the submission meta-date files exists.
                                If used without the base_dir argument then the default base directory is:
                                 /ebi/microarray/ma-exp/AutoSubmissions/annotare/''')
    parser.add_argument('accession', metavar='E-MTAB-xxxx', type=str,
                        help='''The accession number for the experiment''')
    parser.add_argument('-bd', '--base_dir', metavar='path/to/experiment/directory/__without__/MAGE-TAB_xxx', type=str,
                        help="""The base directory for the experiment's data.
                       If not given the default value is /ebi/microarray/ma-exp/AutoSubmissions/annotare/""")
    parser.add_argument('-ed', '--ena_dir', metavar='path/to/fastq/files/directory/', type=str,
                        help="""The location of fastq files on ENA machine.
                       If not given the default value is /fire/staging/aexpress/""")
    parser.add_argument('-ic', '--is_combined', action='store_true',
                        help='A flag indicating that the IDF and SDRF are in the same file.')
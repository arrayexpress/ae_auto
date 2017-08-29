import os
from shutil import copyfile

__author__ = 'Ahmed G. Ali'

EXP_DIR = '/ebi/ftp/pub/databases/arrayexpress/data/experiment'
FTP_GATE = '/ebi/microarray/db/AE/ArrayExpress-files/ftp-gate/'
LOAD_DIR = '/ebi/microarray/home/arrayexpress/ae2_production/data/EXPERIMENT/'


def main():
    dirs = os.listdir(EXP_DIR)
    print dirs
    for dr in dirs:
        if os.path.isdir(os.path.join(EXP_DIR, dr)):
            for exp in os.listdir(os.path.join(EXP_DIR, dr)):
                original = os.path.join(EXP_DIR, dr, exp, exp + '.idf.txt_original')
                if os.path.exists(original):
                    print 'copying ' + exp
                    # print (original, os.path.join(FTP_GATE, exp + '.idf.txt'))
                    copyfile(original, os.path.join(FTP_GATE, exp + '.idf.txt'))
                    if os.path.exists(os.path.join(LOAD_DIR,exp.split('-')[1], exp, exp + '.idf.txt')):
                        # print (original, os.path.join(LOAD_DIR,exp.split('-')[1], exp, exp + '.idf.txt'))
                        try:
                            copyfile(original, os.path.join(LOAD_DIR,exp.split('-')[1], exp, exp + '.idf.txt'))
                        except:
                            pass
                    # exit()


if __name__ == '__main__':
    main()

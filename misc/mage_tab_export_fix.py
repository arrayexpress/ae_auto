import argparse

__author__ = 'Ahmed G. Ali'


def fix_idf(file_path):
    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()
    write_lines = []
    for i in range(len(lines)):
        line = lines[i].strip().split('\t')
        write_line = []
        if line[0] == 'Term Source Name' or line[0] == '"Term Source Name"':
            line.append('ArrayExpress')
        if line[0] == 'Term Source File' or line[0] == '"Term Source File"':
            line.append('http://www.ebi.ac.uk/arrayexpress/')

        for part in line:
            if part.endswith('"'):
                part = part.replace('"', '')
            write_line.append(part)

        write_lines.append('\t'.join(write_line))
    f = open(file_path, 'w')
    f.write('\n'.join(write_lines))
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fixes Export IDF.')
    parser.add_argument('file_path', metavar='PATH_TO_FILE.idf', type=str,
                        help='''The path to the IDF file''')
    args = parser.parse_args()
    try:
        fix_idf(args.file_path)
    except:
        pass
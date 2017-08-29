__author__ = 'Ahmed G. Ali'
import os
path = '/home/gemmy/blueprint_sample_annotations_12Aug2015.txt'

f = open(path, 'r')
lines = [l.strip() for l in f.readlines()]
f.close()
header = lines[0].split('\t')
f1 = header.index('FASTQ1')
md1 = header.index('MD5_1')
f2 = header.index('FASTQ2')
md2 = header.index('MD5_2')

header.remove('FASTQ2')
header.remove('MD5_2')
write_lines = ['\t'.join(header)]

for i in range(1, len(lines)):
    l = lines[i].split('\t')
    pair2 = l[f2]
    md5_2 = l[md2]
    l.remove(pair2)
    l.remove(md5_2)
    write_lines.append('\t'.join(l))
    l[f1] = pair2
    l[md1] = md5_2
    write_lines.append('\t'.join(l))
f = open('/home/gemmy/res.txt', 'w')
f.write(os.linesep.join(write_lines))
f.close()




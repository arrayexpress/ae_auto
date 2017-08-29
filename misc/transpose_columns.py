__author__ = 'Ahmed G. Ali'

f = open('/home/gemmy/robert_scrape_of_BioSamples.txt', 'r')
lines = f.readlines()
f.close()
extra_header = ['', '', '', '', '', '', '', 'BIOMATERIAL TYPE', 'COLLECTION METHOD', 'DONOR AGE', 'DONOR ID',
                'MOLECULE', 'Sample Name', 'TISSUE DEPOT', 'biomaterial provider', 'organism part', 'sample term id']

write_lines = ['\t'.join(extra_header)]
for i in range(0, len(lines), 10):
    line = lines[i]
    # print line
    line = line.strip().split('\t')
    base_line = line[:7]
    print base_line
    # exit()
    for j in range(i, i+10):
        field = lines[j].split('\t')[8].strip()
        print field

        base_line.append(field)
        # print base_line
        # exit()
    write_lines.append('\t'.join(base_line))


f = open('/home/gemmy/robert_scrape_of_BioSamples.txt_modified', 'w')
f.write('\n'.join(write_lines))
f.close()

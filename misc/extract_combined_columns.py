__author__ = 'Ahmed G. Ali'

f = open('/home/gemmy/E-GEOD-16256_NIH_epigenome_cells_RNA-seq.sdrf.txt', 'r')
lines = f.readlines()
f.close()
extra_header = ['sample_term_id', 'assay_term_id', 'nucleic_acid_term_id', 'Design_description', 'Library_name',
                    'EDACC_Genboree_Experiment_Page', 'EDACC_Genboree_Sample_Page']

write_lines = ['\t'.join(lines[0].strip().split('\t') + sorted(extra_header))]
for line in lines[1:]:
    line = line.strip().split('\t')
    txt = line[2]
    txt = txt.replace('Design description', 'Design_description').replace('Library name', 'Library_name').replace(
        'EDACC Genboree Experiment Page', 'EDACC_Genboree_Experiment_Page').replace('EDACC Genboree Sample Page',
                                                                                    'EDACC_Genboree_Sample_Page')

    words = txt.split(' ')
    extra_index = 0
    d = {}
    for i in range(len(words)):
        if words[i].strip().replace(':', '') == extra_header[extra_index]:
            extra_index += 1
            if extra_index == len(extra_header):
                d[extra_header[extra_index - 1]] = words[i + 1]
                break
            else:
                next_index = words.index(extra_header[extra_index] + ':')
                d[extra_header[extra_index - 1]] = ' '.join(words[i + 1:next_index])

    for k in sorted(d.keys()):
        line.append(d[k])
    write_lines.append('\t'.join(line))
f = open('/home/gemmy/E-GEOD-16256_NIH_epigenome_cells_RNA-seq.sdrf.txt_modified', 'w')
f.write('\n'.join(write_lines))
f.close()

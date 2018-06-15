from models.magetab.sdrf import SdrfCollection

__author__ = 'Ahmed G. Ali'

def get_def(file_name1, file_name2):
    diff=[]
    for i in range(min(len(file_name1), len(file_name2))):
        if file_name1[i] != file_name2[i]:
            diff .append([i, file_name1[i], file_name2[i]])
    return diff

def main(sdrf_path):
    sdrf = SdrfCollection(file_path=sdrf_path, has_extra_rows=True)
    # print sdrf.extra_rows
    groups = {}
    print len(sdrf.extra_rows)
    for row in sdrf.extra_rows:
        for p in sdrf.pairs:
            if row.original_assay == p[0].original_assay:
                if row.original_assay in groups.keys():
                    groups[row.original_assay].append(row)
                else:
                    groups[row.original_assay] = [p[0], p[1], row]
                continue
    print groups
    # for row in sdrf.extra_rows:
    #     file_name = row.data_file
    #     min_def = -1
    #     pair = None
    #     for p in sdrf.pairs:
    #         ref_name = p[0].data_file
    #         diff = get_def(file_name, ref_name)
    #         if min_def == -1:
    #             min_def = diff
    #             pair = p
    #             continue
    #         if len(diff) > min_def:
    #             min_def = diff
    #             pair = p
    #     groups.append([pair[0], pair[1], row])
    for g in groups.values():
        print ' | '.join(a.data_file for a in g)



    exit()
    groups=[]
    grouped_indeces = []
    diffs = {}
    for i in range(len(sdrf.rows)):
        row = sdrf.rows[i]
        # group=[i]
        for j in range(i+1, len(sdrf.rows)):
            if j in grouped_indeces:
                continue
            grouped_indeces.append(j)
            diffs[(sdrf.rows[i], sdrf.rows[j])] = get_def(sdrf.rows[i].new_data_file, sdrf.rows[j].new_data_file)
        # groups.append(group)
    for v in diffs.values():
        rows = [k for k in diffs.keys() if diffs[k] == v]
        print rows

    # print diffs

        # print(row.data_file)


if __name__ == '__main__':
    from sys import argv

    _sdrf_path = argv[1]
    main(_sdrf_path)

    # get_def('read-I1_si-ACTTCACT_lane-001-chunk-001.fastq.gz',
    #         'read-RA_si-ACTTCACT_lane-001-chunk-001.fastq.gz')
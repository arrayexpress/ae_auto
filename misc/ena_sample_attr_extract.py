import xml.etree.ElementTree as ET

from dal.oracle.era.sample import retrieve_xml_by_biosample_id_list

__author__ = 'Ahmed G. Ali'


def main():
    f = open('/home/gemmy/amy_washu_bioSD_accessions.txt', 'r')
    lines = f.readlines()
    f.close()
    bio_samples_ids = [i.strip() for i in lines]
    recurrence = {}
    for s_id in bio_samples_ids:
        if s_id not in recurrence.keys():
            recurrence[s_id] = 1
        else:
            recurrence[s_id] +=1

    xmls = retrieve_xml_by_biosample_id_list(bio_samples_ids)
    write_lines = ['\t'.join(['BIOSAMPLE_ID', 'DONER_SEX', 'DONER_ETHENTICITY'])]
    for xml in xmls:
        doner_sex, doner_ethenticity = extract_params(xml.sample_xml)
        for i in range(recurrence[xml.biosample_id]):
            write_lines.append('\t'.join([xml.biosample_id, doner_sex, doner_ethenticity]))
    f = open('/home/gemmy/sample_out.txt', 'w')
    f.write('\n'.join(write_lines))
    f.close()


def extract_params(xml):
    root = ET.fromstring(xml)
    attrs = root.find('SAMPLE').find('SAMPLE_ATTRIBUTES').findall('SAMPLE_ATTRIBUTE')
    doner_sex = None
    doner_ethnicity = None
    for attr in attrs:
        if attr.find('TAG').text == 'DONOR_SEX':
            doner_sex = attr.find('VALUE').text
        if attr.find('TAG').text == 'DONOR_ETHNICITY':
            doner_ethnicity = attr.find('VALUE').text
        if doner_sex and doner_ethnicity:
            break
    return doner_sex, doner_ethnicity


if __name__ == '__main__':
    main()

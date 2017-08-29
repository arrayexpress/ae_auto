ENA_FTP_URI = 'ftp://ftp.sra.ebi.ac.uk/vol1/fastq/'
runs = {1: 'ERA00132201'}
URLs = {}
for run, acc in runs.items():
    vol = None
    sub_dir = acc[:6]
    if len(acc) > 9:
        vol = acc[9:]
        vol = '0' * (3 - len(vol)) + vol
        
    ena_run = acc
    fq_uri = ENA_FTP_URI + sub_dir
    if vol:
        fq_uri += '/' + vol
    fq_uri += '/' + acc + '/' + acc
    fq_uri += '%s.fastq.gz'
    URLs[run] = [fq_uri % '_1',fq_uri % '_2' ]
print URLs
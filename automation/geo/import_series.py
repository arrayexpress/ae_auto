from automation.geo.import_adf import download_soft_file, parse_soft_file

__author__ = 'Ahmed G. Ali'

def import_geo_series(geo_acc):
    soft_file = download_soft_file(geo_acc, 'series')
    # header, table = parse_soft_file(soft_file)

if __name__ == '__main__':
    import_geo_series('GSE81117')


class ADF:
    def __init__(self, header, table):
        self.header = header.__dict__
        self.name = self.header.get('title', '')
        self.provider = '%s (%s)' % (self.header.get('contact_name',''), self.header.get('contact_email','geo@ncbi.nlm.nih.gov'))
        self. printing_protocol = self.header.get('manufacture_protocol', '')
        self. surface_type = self.header.get('coating','')
        self. substrate_type = self.header.get('platform_support', '')
        self. ae_accession = self.header.get('platform').replace('GPL', 'A-GEOD-')
        self.geo_acc = self.header.get('platform')
        self.description = self.header.get('description')


        # print self.__dict__

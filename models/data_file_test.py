from models.lsf_data_file import FileObject

__author__ = 'Ahmed G. Ali'
f = FileObject('out_file', 'name', 'file_name', 'base_dir', user='ahmed', queue='production-rh7', args=None)
f.run()
# import gzip
# import os
# import threading
#
# from utils.common import execute_command
#
# __author__ = 'Ahmed G. Ali'
#
#
# def get_file_type(fq_file):
#     if fq_file.endswith('.gz'):
#         return 'gz'
#     if fq_file.endswith('.bz2'):
#         return 'bz2'
#     if fq_file.endswith('.bam'):
#         return 'bam'
#     if fq_file.endswith('cram'):
#         return 'cram'
#     if fq_file.endswith('sff'):
#         return 'sff'
#     else:
#         raise Exception(
#             'File type is not supported. Please check more details on http://www.ebi.ac.uk/ena/submit/read-file-formats'
#         )
#
#
# class FileObject(threading.Thread):
#     def __init__(self, thread_id, name, file_name, base_dir):
#         threading.Thread.__init__(self)
#         self.threadID = thread_id
#         self.name = name
#         self.file_name = file_name
#         self.base_dir = base_dir
#         self.file_type = ''
#         self.reads = {}
#         self.errors = []
#         self.working_file = file_name
#         self.execution_error = None
#
#     def run(self):
#         try:
#             try:
#                 self.file_type = get_file_type(self.file_name)
#             except Exception, e:
#                 self.errors.append(str(e))
#                 return
#             print "Starting " + self.name
#             if self.file_type == 'bam':
#                 self.working_file = self.file_name.replace('.bam', '.fastq.gz')
#                 cmd = 'samtools bam2fq %s | gzip > %s' % (os.path.join(self.base_dir, self.file_name),
#                                                           os.path.join(self.base_dir,
#                                                                        self.working_file))
#
#                 out, err = execute_command(cmd)
#                 if err:
#                     self.execution_error = err
#                     return
#             if self.file_type == 'cram':
#                 self.working_file = self.file_name.replace('.cram', '.fastq.gz')
#                 cmd = 'cramtools  fastq -I %s | gzip > %s' % (os.path.join(self.base_dir, self.file_name),
#                                                               os.path.join(self.base_dir,
#                                                                            self.working_file))
#
#                 out, err = execute_command(cmd)
#                 if err:
#                     self.execution_error = err
#                     return
#
#             elif self.file_type == 'bz2':
#                 self.working_file = self.file_name.replace('.bz2', '.gz')
#                 cmd = 'bunzip2 -c < %s | gzip -c > %s' % (os.path.join(self.base_dir, self.file_name),
#                                                           os.path.join(self.base_dir,
#                                                                        self.working_file))
#
#                 out, err = execute_command(cmd)
#                 if err:
#                     self.execution_error = err
#                     return
#
#             elif self.file_type == 'sff':
#                 self.working_file = self.file_name.replace('.sff', '.fastq.gz')
#                 cmd = 'sff2fastq  %s | gzip -c > %s' % (os.path.join(self.base_dir, self.file_name),
#                                                         os.path.join(self.base_dir,
#                                                                      self.working_file))
#
#                 out, err = execute_command(cmd)
#                 if err:
#                     self.execution_error = err
#                     return
#
#             self.validate()
#         except Exception, e:
#             self.execution_error = str(e)
#
#     def validate(self):
#         print os.path.join(self.base_dir, self.working_file)
#         counter = 0
#         with gzip.open(os.path.join(self.base_dir, self.working_file), 'r') as fin:
#             next_id = True
#             next_seq = False
#             next_plus = False
#             next_qual = False
#             current_id = None
#             for line_ in fin:
#                 line = line_.strip()
#                 # print line
#                 counter += 1
#                 if line.strip() == '':
#                     continue
#                 if next_id:
#                     if line.strip()[-2] == '/':
#                         key = line.strip()[:-2]
#                     else:
#                         key = line.strip().split(' ')[0]
#                     current_id = key
#                     if key in self.reads.keys():
#                         self.reads[key]['errors'].append('Repeated read in lines %s and %s' % (
#                             self.reads[key]['line'], counter))
#                         self.errors.append('Repeated read %s in lines %s and %s' % (
#                             line, self.reads[key]['line'], counter))
#                     else:
#                         self.reads[key] = {
#                             'seq': 0,
#                             'qual': 0,
#                             'errors': [],
#                             'line': counter,
#                             'seq_id': line
#                         }
#
#                     next_id = False
#                     next_seq = True
#                     continue
#                 # if len(self.reads[current_id]['errors']) > 0:
#                 #     continue
#                 if next_seq:
#                     next_seq = False
#                     next_plus = True
#                     self.reads[current_id]['seq'] = len(line.strip())
#                     if len(line.strip()) < 36:
#                         self.reads[current_id]['errors'].append(
#                             'Sequence length less than 36, line ' + str(counter))
#                         self.errors.append(
#                             'Sequence length in read %s less than 36, line %s' % (current_id, str(counter)))
#                     continue
#                 if next_plus:
#                     next_plus = False
#                     if not line.startswith('+'):
#                         self.reads[current_id]['errors'].append(
#                             'Plus is missing in read %s, line: %s' % (current_id, str(counter)))
#                         self.errors.append('Plus is missing in read %s, line: %s' % (current_id, str(counter)))
#
#                         next_qual = True
#                     else:
#                         next_qual = True
#                         continue
#                 if next_qual:
#                     self.reads[current_id]['qual'] = len(line.strip())
#                     if self.reads[current_id]['qual'] != self.reads[current_id]['seq']:
#                         self.reads[current_id]['errors'].append(
#                             "Sequence and quality don't have the same length for read id: %s line %s" % (
#                                 current_id, counter))
#                         self.errors.append(
#                             "Sequence and quality don't have the same length for read id: %s line %s."
#                             " Seq len: %s, Qual len: %s" % (
#                                 current_id, counter, self.reads[current_id]['seq'], self.reads[current_id]['qual']))
#                     next_id = True
#                     next_qual = False
#                     continue
#
#

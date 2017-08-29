import collections
import gzip
import json
import os
from datetime import datetime
from sys import argv

import settings
from utils.common import execute_command
from utils.lsf.job import LSFJob

__author__ = 'Ahmed G. Ali'


def get_file_type(fq_file):
    if fq_file.endswith('.gz'):
        return 'gz'
    if fq_file.endswith('.bz2'):
        return 'bz2'
    if fq_file.endswith('.bam'):
        return 'bam'
    if fq_file.endswith('cram'):
        return 'cram'
    if fq_file.endswith('sff'):
        return 'sff'
    else:
        raise Exception(
            'File type is not supported. Please check more details on http://www.ebi.ac.uk/ena/submit/read-file-formats'
        )


class FileObject(LSFJob):
    def __init__(self, out_file, name, file_name, base_dir, ena_dir, user='ahmed', queue='production-rh7', args=None):
        if not args:
            args = []
        super(self.__class__, self).__init__(out_file=out_file, description='Validating ' + name)
        self.ena_dir = ena_dir
        self.args_dict = {
            'out_file': out_file,
            'name': name,
            'file_name': file_name,
            'base_dir': base_dir,
            'ena_dir': ena_dir,
            'user': user,
            'queue': queue,
            'args': args
        }
        self.command = "python {file} '{args}' ".format(user=user,
                                                        queue=queue,
                                                        file=os.path.realpath(__file__),
                                                        args=json.dumps(self.args_dict),
                                                        out_file=out_file)
        input_args = os.path.join(base_dir, file_name + '_inputargs.json')
        f = open(input_args, 'w')
        f.write(json.dumps(self.args_dict))
        f.close()
        if settings.LOCAL_EXECUTION:
            self.command = "source /home/gemmy/PycharmProjects/ae_automation/settings/bashrc; " \
                       "python {file} {args_file} ".format(user=user,
                                                              queue=queue,
                                                              file=os.path.realpath(__file__),
                                                              args=json.dumps(self.args_dict),
                                                              out_file=out_file,
                                                              args_file=input_args)
        else:
            self.command = "ssh ebi-login-001 \"source /etc/profile.d/lsf.sh; " \
                       "bsub -u {user} -q {queue} -M 8000 " \
                       "'source /nfs/production3/ma/home/arrayexpress/ae_automation/resources-rh7/bashrc; " \
                       "python {file} {args_file}'\" ".format(user=user,
                                                              queue=queue,
                                                              file=os.path.realpath(__file__),
                                                              args=json.dumps(self.args_dict),
                                                              out_file=out_file,
                                                              args_file=input_args)
        self.name = name
        self.file_name = file_name
        self.base_dir = base_dir
        self.file_type = ''
        self.reads = {}
        self.errors = []
        self.keys = []
        self.working_file = file_name
        self.execution_error = None
        self.serialize_file = os.path.join(self.base_dir, self.name + '_serialize.json')
        if os.path.exists(self.serialize_file):
            os.remove(self.serialize_file)

    def start(self):
        self.run()

    def run(self):
        print self.command
        out, err = execute_command(self.command)
        print self.command
        print 'Out:\n', out
        print  '-' * 30
        print 'Error:\n', err
        print '----------------------'

        # while self.is_alive():
        #     # print 'sleeping'
        #     sleep(10)

    def load_results(self):
        f = open(self.serialize_file, 'r')
        self.__dict__.update(json.loads(f.read()))
        f.close()

    def copy_file(self):
        if settings.LOCAL_EXECUTION:
            cmd = 'cp %s/%s %s' % (self.ena_dir, self.file_name, self.base_dir)
        else:
            cmd = 'scp -oStrictHostKeyChecking=no  oy-ena-login-1:%s/%s %s' % (self.ena_dir, self.file_name, self.base_dir)

        print cmd
        out, err = execute_command(cmd)
        print out, err
        # out, err = execute_command('cp  -r %s %s' % (ena_dir, local_dir))
        # print out, err
        # exit()
        return out, err

    def main(self):
        self.copy_file()
        try:
            try:
                self.file_type = get_file_type(self.file_name)
            except Exception, e:
                self.errors.append(str(e))
                return
            print "Starting " + self.name
            if self.file_type == 'bam':
                self.working_file = self.file_name.replace('.bam', '.fastq.gz')
                cmd = 'samtools bam2fq %s | gzip > %s' % (os.path.join(self.base_dir, self.file_name),
                                                          os.path.join(self.base_dir,
                                                                       self.working_file))

                out, err = execute_command(cmd)
                if err:
                    self.execution_error = err
                    return
            if self.file_type == 'cram':
                self.working_file = self.file_name.replace('.cram', '.fastq.gz')
                cmd = 'cramtools  fastq -I %s | gzip > %s' % (os.path.join(self.base_dir, self.file_name),
                                                              os.path.join(self.base_dir,
                                                                           self.working_file))

                out, err = execute_command(cmd)
                if err:
                    self.execution_error = err
                    return

            elif self.file_type == 'bz2':
                self.working_file = self.file_name.replace('.bz2', '.gz')
                cmd = 'bunzip2 -c < %s | gzip -c > %s' % (os.path.join(self.base_dir, self.file_name),
                                                          os.path.join(self.base_dir,
                                                                       self.working_file))

                out, err = execute_command(cmd)
                if err:
                    self.execution_error = err
                    return

            elif self.file_type == 'sff':
                self.working_file = self.file_name.replace('.sff', '.fastq.gz')
                cmd = 'sff2fastq  %s | gzip -c > %s' % (os.path.join(self.base_dir, self.file_name),
                                                        os.path.join(self.base_dir,
                                                                     self.working_file))

                out, err = execute_command(cmd)
                if err:
                    self.execution_error = err
                    return

            self.validate()
        except Exception, e:

            self.execution_error = str(e)
        finally:
            print 'writing serializer'
            # self.keys = None

            f = open(self.serialize_file, 'w')
            f.write(json.dumps(self.__dict__))
            f.close()

            print 'serializer written to: ', self.serialize_file

    def is_alive(self):
        if os.path.exists(self.serialize_file):
            self.load_results()
            return False
        return True

    def validate(self):
        # print os.path.join(self.base_dir, self.working_file)
        counter = 0
        with gzip.open(os.path.join(self.base_dir, self.working_file), 'r') as fin:
            next_id = True
            next_seq = False
            next_plus = False
            next_qual = False
            current_id = None
            self.keys = []
            for line_ in fin:
                line = line_.strip()
                # print line
                counter += 1
                key = ''
                # if counter > 66719270:
                #     break
                # # if counter % 1000000 == 0:
                #     print counter
                    # keys = [i['key'] for i in self.reads.values()]
                    # duplicate = [item for item, count in collections.Counter(keys).items() if count > 1]
                    # print 'Duplicated ', duplicate
                if line.strip() == '':
                    continue
                if next_id:
                    if line.strip()[-2] == '/':
                        key = line.strip()[:-2]
                    else:
                        key = line.strip().split(' ')[0]
                    current_id = counter
                    # if key in self.reads.keys():
                    #     self.reads[key]['errors'].append('Repeated read in lines %s and %s' % (
                    #         self.reads[key]['line'], counter))
                    #     self.errors.append('Repeated read %s in lines %s and %s' % (
                    #         line, self.reads[key]['line'], counter))
                    # else:
                    read = {
                        'seq': 0,
                        'qual': 0,
                        # 'errors': [],
                        # 'line': counter,
                        'seq_id': line,
                        'key': key
                    }
                    self.keys.append((current_id, key))
                    read_id = line
                    next_id = False
                    next_seq = True
                    continue
                # if len(self.reads[current_id]['errors']) > 0:
                #     continue
                if next_seq:
                    next_seq = False
                    next_plus = True
                    read['seq'] = len(line.strip())
                    if len(line.strip()) < 36:
                        # self.reads[current_id]['errors'].append(
                        #     'Sequence length less than 36, line ' + str(counter))
                        self.errors.append(
                            'Sequence length in read %s less than 36, line %s' % (key, str(counter)))
                    continue
                if next_plus:
                    next_plus = False
                    if not line.startswith('+'):
                        # self.reads[current_id]['errors'].append(
                        #     'Plus is missing in read %s, line: %s' % (current_id, str(counter)))
                        self.errors.append('Plus is missing in read %s, line: %s' % (key, str(counter)))

                        next_qual = True
                    else:
                        next_qual = True
                        continue
                if next_qual:
                    read['qual'] = len(line.strip())
                    if line.startswith('@') and (' ' in line.strip() or line.strip()[-1:-2] == '/1' or line.strip()[-1:-2] == '/2'):
                        self.errors.append('Quality for read %s is missing at line: %d' %(read_id, counter))
                        next_seq = True
                        next_qual = False
                        if line.strip()[-2] == '/':
                            key = line.strip()[:-2]
                        else:
                            key = line.strip().split(' ')[0]
                        read = {
                            'seq': 0,
                            'qual': 0,
                            # 'errors': [],
                            # 'line': counter,
                            'seq_id': line,
                            'key': key
                        }
                        self.keys.append((current_id, key))
                        read_id = line
                        continue

                    if read['qual'] != read['seq']:
                        # self.reads[current_id]['errors'].append(
                        #     "Sequence and quality don't have the same length for read id: %s line %s" % (
                        #         current_id, counter))
                        self.errors.append(
                            "Sequence and quality don't have the same length for read id: %s line %s."
                            " Seq len: %s, Qual len: %s" % (
                                read_id, counter, read['seq'], read['qual']))
                    next_id = True
                    next_qual = False
                    continue

        # self.validate_singularity()

    def validate_singularity(self):
        print 'Starting Validating Singularity', datetime.utcnow()
        keys = [i[1] for i in self.keys]
        keys_set = set(keys)
        if len(keys_set) != len(keys):
            duplicate = [item for item, count in collections.Counter(keys).items() if count > 1]
            for k in duplicate:
                self.errors.append('%s read is repeated in the file' % k)
        print 'Finish Validating Singularity', datetime.utcnow()


if __name__ == '__main__':
    f = open(argv[1], 'r')
    print argv[1]
    j = f.read()
    print j
    args = json.loads(j)
    print 'ARGS', args
    f.close()

    f = FileObject(
        args['out_file'],
        args['name'],
        args['file_name'],
        args['base_dir'],
        args['ena_dir'],
        args['user'],
        args['queue'],
        args['args'])
    f.main()
    # f.main()

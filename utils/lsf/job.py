import os
from abc import ABCMeta
from abc import abstractmethod

from utils.common import execute_command

__author__ = 'Ahmed G. Ali'


class LSFJob(object):
    __metaclass__ = ABCMeta

    def __init__(self, out_file, description):
        self.out_file = out_file
        self.job_id = None
        self.description = description
        self.args_dict = {}

    @abstractmethod
    def run(self):
        pass

    def status(self):
        cmd = "ssh ebi-login-001  \"source /etc/profile.d/lsf.sh; bjobs %s\"" % self.job_id
        out, err = execute_command(cmd)
        lines = out.split('\n')
        if len(lines) == 1:
            return 'completed'
        job_line = lines[1]
        print lines[0]
        print [i for i in job_line.split(' ') if i != '']

    def output(self):
        pass


if __name__ == '__main__':
    print os.path.realpath(__file__)

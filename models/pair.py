import os
import threading

import time

from models.lsf_data_file import FileObject

__author__ = 'Ahmed G. Ali'


class Pair():
    def __init__(self, file_1, file_2, base_dir, ena_dir):
        self.base_dir = base_dir
        # self.file_1 = FileObject(file_1, file_1, file_1, self.base_dir)
        self.file_1 = FileObject(out_file=os.path.join(base_dir, file_1 + '_out'),
                                 name=file_1,
                                 file_name=file_1,
                                 base_dir=base_dir,
                                 ena_dir=ena_dir)
        self.file_2 = FileObject(out_file=os.path.join(base_dir, file_2 + '_out'),
                                 name=file_2,
                                 file_name=file_2,
                                 base_dir=base_dir,
                                 ena_dir=ena_dir)
        self.errors = []

    def run(self):
        self.validate()

    def is_alive(self):
        if self.file_1.is_alive() or self.file_2.is_alive():
            return True
        print self.file_1.keys
        diff = list(set([i[1] for i in self.file_1.keys]) - set([i[1] for i in self.file_2.keys]))
        diff2 = list(set([i[1] for i in self.file_2.reads.keys()]) - set([i[1] for i in self.file_1.reads.keys()]))
        for d in diff:
            print diff
            self.errors.append("""Read %s in file: %s doesn't have a pair in file: %s""" % (
                d, self.file_1.file_name, self.file_2.file_name))
        for d in diff2:
            self.errors.append("""Read %s in file: %s doesn't have a pair in file: %s""" % (
                d, self.file_2.file_name, self.file_1.file_name))
        return False

    def validate(self):
        self.file_1.start()
        self.file_2.start()

        # self.file_1.join()
        # self.file_2.join()
        # while self.file_1.is_alive() or self.file_2.is_alive():
        #     # time.sleep(10)
        #     continue
        #
        # diff = list(set(self.file_1.reads.keys()) - set(self.file_2.reads.keys()))
        # diff2 = list(set(self.file_2.reads.keys()) - set(self.file_1.reads.keys()))
        # for d in diff:
        #     print diff
        #     self.errors.append("""Read %s in file: %s doesn't have a pair in file: %s""" % (
        #         self.file_1.reads[d]['seq_id'], self.file_1.file_name, self.file_2.file_name))
        # for d in diff2:
        #     self.errors.append("""Read %s in file: %s doesn't have a pair in file: %s""" % (
        #         self.file_2.reads[d]['seq_id'], self.file_2.file_name, self.file_1.file_name))

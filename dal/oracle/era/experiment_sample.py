from dal.oracle.comon import execute_select
from dal.oracle.era import db

__author__ = 'Ahmed G. Ali'


def retrieve_sample_acc_by_exp_acc(exp_acc):
    return execute_select("""SELECT SAMPLE_ID FROM EXPERIMENT_SAMPLE WHERE EXPERIMENT_ID ='%s'""" % exp_acc, db)

import datetime
from dal.oracle.common import execute_select
from dal.oracle.conan import db

__author__ = 'Ahmed G. Ali'


def retrieve_daemon_failed_tasks():
    sql = """SELECT ct.* FROM CONAN_TASKS ct join CONAN_USERS cu on ct.USER_ID = cu.ID
            where ct.STATE='FAILED' and cu.LAST_NAME='Daemon'"""
    return execute_select(sql, db)


def retrieve_daemon_more_than_week_running_tasks():
    sql = """SELECT ct.* FROM CONAN_TASKS ct join CONAN_USERS cu on ct.USER_ID = cu.ID
              where ct.STATE='RUNNING' and cu.LAST_NAME='Daemon'
              AND START_DATE < TO_DATE('%s', 'YYYY-MM-DD"T"HH24:MI:SS')""" % \
          (datetime.datetime.today() - datetime.timedelta(days=7)).isoformat().split('.')[0]
    # print sql
    # exit()
    return execute_select(sql, db)
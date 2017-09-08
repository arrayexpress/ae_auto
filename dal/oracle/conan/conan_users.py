from dal.oracle.common import execute_select
from dal.oracle.conan import db

__author__ = 'Ahmed G. Ali'


def retrieve_user_by_email(email):
    sql = """SELECT ID FROM CONAN_USERS WHERE EMAIL='%s' AND USER_NAME != 'conan-daemon'"""% email
    return execute_select(sql, db)
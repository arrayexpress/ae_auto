__author__ = 'Ahmed G. Ali'
import MySQLdb as mdb

def retrieve_connection(db):
    con = mdb.connect(host=db['host'], user=db['username'], passwd=db['password'], port=db['port'], db=db['name'])
    return con


def execute_select(sql_stmt, db):
    res = []
    con = None
    try:
        con = retrieve_connection(db)
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(sql_stmt)
        res = cur.fetchall()
    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        if con:
            con.close()
    return res

def execute_insert(sql_stmt, db):
    con = None
    try:
        con = retrieve_connection(db)
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute(sql_stmt)
        con.commit()
    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:
        if con:
            con.close()
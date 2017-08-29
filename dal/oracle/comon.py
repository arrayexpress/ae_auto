__author__ = 'Ahmed G. Ali'
import dbms


def retrieve_connection(db):
    # print db
    con = dbms.connect.oracle(user=db['username'], password=db['password'], database=db['name'], host=db['host'],
                              port=db['port'], is_service=db.get('is_service', False))
    return con


def execute_select(sql_stmt, db, keep_connection=False):
    res = []
    con = None
    try:
        con = retrieve_connection(db)
        cur = con.cursor()
        # print sql_stmt
        cur.execute(sql_stmt)
        res = cur.fetchall()
    except Exception, e:
        raise
        print e
    finally:
        if keep_connection:
            return res, con
        if con:
            con.close()
    return res


def execute_insert(sql_stmt, db):
    con = None
    try:
        con = retrieve_connection(db)
        cur = con.cursor()
        cur.execute(sql_stmt)
        con.commit()
    except Exception, e:
        raise Exception(str(e) + '\n' + sql_stmt)
        print e
        print "Error %d: %s" % (e.args[0], e.args[1])
    finally:
        if con:
            con.close()

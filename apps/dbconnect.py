import psycopg2
import pandas as pd 

def getdblocation():
    db = psycopg2.connect(
        host='localhost',
        database='CIEM',
        user='postgres',
        port=5433,
        password='1234'
    )

    return db

def modifydatabase(sql, values):
    db=getdblocation()
    cursor=db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()

def querydatafromdatabase(sql, values, dfcolumns=None):
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    if dfcolumns is None:
        rows = pd.DataFrame(cur.fetchall())
    else:
        rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows

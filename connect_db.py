import mysql.connector as mydb

def conn_db():
    
    conn = mydb.connect(
        host='localhost',
        port='3306',
        user='root',
        password='Nero8910',
        database='mydb'
    )
    return conn
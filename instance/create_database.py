import bcrypt
import sqlite3


# Create table
database = 'database.db'
sql_query = '''
            CREATE TABLE IF NOT EXISTS diet(
                id INTEGER PRIMARY KEY NOT NULL,
                nome VARCHAR(80) UNIQUE NOT NULL,
                descricao VARCHAR(80) NOT NULL,
                data DATETIME NOT NULL,
                status VARCHAR(80) NOT NULL)
            '''


# Function
def execute_query(database, sql_query):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(sql_query)
    con.commit()
    cur.close()
    con.close()


# Create table
execute_query(database, sql_query)

#!/usr/bin/python
import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters and connect to postgreSQL server. Also
        # create a server and query the database for its current version.
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print('Connected')
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        #sql commands:

       # close the communication with the PostgreSQL
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
if __name__ == '__main__':
    connect()

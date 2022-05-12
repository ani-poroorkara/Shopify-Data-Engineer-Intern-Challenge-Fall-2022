import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Connect to Database.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Success!")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_schema(db_file, schema_file):
    """
    Create Schema for DB.
    """
    try:
        conn = sqlite3.connect(db_file)
        with open(schema_file) as f:
            conn.executescript(f.read())
        print("Success!")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    
"""
Run script!
"""
if __name__ == '__main__':
    create_connection(r"database\shopifyimgrepo.db")
    create_schema(r"database\shopifyimgrepo.db", 'schema.sql')

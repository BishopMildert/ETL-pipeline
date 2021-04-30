import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error

load_dotenv()

HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))
USER = os.environ.get("POSTGRES_USER")
PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")
DATABASE = os.environ.get("DB")

def connection():
    return psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        port=PORT,
        database=DATABASE
    )

def query(conn, sql):#Get data from database
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        input(f"ERROR: {e}")

def update(conn, sql, values, should_commit=True, should_return=False):#Push data to database
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, tuple(values))
            if should_commit:
                conn.commit()
            if should_return:
                result = cursor.fetchall()
                return result
    except Exception as e:
        input(f"ERROR: {e}")

def init_db():
    try:
        conn = connection()
        # print("PostgreSQL server information")
        # print(conn.get_dsn_parameters(), "\n")
        # record = query(conn,"SELECT version();")
        # print("You are connected to - ", record, "\n")

        fd = open("src/db/db-init.sql", 'r')
        sql = fd.read()
        fd.close()
        query(conn, sql)
        print(query(conn, "SELECT * FROM product"))
        conn.commit()

        if (connection):
            conn.close()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

if __name__ == "__main__":
    init_db()
    
    
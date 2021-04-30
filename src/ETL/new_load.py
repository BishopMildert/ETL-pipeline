import os
import psycopg2
import uuid
from dotenv import load_dotenv
from datetime import datetime
from psycopg2 import Error
from src.db.core import query, update, connection, init_db

def load(data):
    conn = connection()

    for index,row in enumerate(data): # enumerate is an option
        copy = dict(row)
        copy = load_franchise_data(conn, copy) # load franchise data (replace location with ID)
        copy = load_payment_data(conn, copy) # load payment data ( replace payment_method with ID)
        copy = load_transaction_data(conn, copy) # load transaction data (replace location with ID? ask for suggestions)
        copy = load_product_data(conn, copy) # load products data ( replace basket with list of IDs)
        copy = load_basket_data(conn, copy) #load basket IDs
    
    conn.commit()
    conn.close()

def load_franchise_data(conn, row):
    cafe_location = row["location"]
    SQL = ("SELECT * FROM franchises WHERE cafe_location = %s")
    values = (cafe_location,)
    result = update(conn, SQL, values, should_commit=False, should_return=True)
    if len(result) == 0:
        SQL = ("INSERT INTO franchises (id, cafe_location)"
            "VALUES (%s,%s)")
        new_id = str(uuid.uuid4())
        val = (new_id,cafe_location)
        update(conn, SQL, val, should_commit=False, should_return=False)
        row["location"] = new_id
        return row
    row["location"] = result[0][0]
    return row

def load_product_data(conn, row):
    product_list = row["basket"] 
    product_id_list = []
    for product in product_list:
        SQL = ("SELECT * FROM products WHERE price = %s and product_name = %s")
        values = (product["price"], product["product"])
        result = update(conn, SQL, values, should_commit=False, should_return=True)
        if len(result) == 0:
            SQL = ("INSERT INTO products (id, product_name, price, size)"
                "VALUES (%s,%s,%s,%s)")
            new_id = str(uuid.uuid4())
            val = (new_id,product["product"],product["price"],product["size"])
            update(conn, SQL, val, should_commit=False, should_return=False)
            product_id_list.append(new_id)
        else:
            product_id_list.append(result[0][0])
    row["basket"] = product_id_list
    return row

def load_basket_data(conn, row):
    #this will always need to be uploaded
    for item in row["basket"]:
        SQL = ("INSERT INTO baskets (id, transaction_id, product_id)"
        "VALUES (%s,%s,%s)")
        new_id = str(uuid.uuid4())
        val = (new_id,row["location"],item)
        update(conn, SQL, val, should_commit=False, should_return=False)
    return row
        
def load_transaction_data(conn, row):
    #this will always need to be uploaded

    SQL = ("INSERT INTO transactions (id, payment, franchise, date_time, cost_total)"
        "VALUES (%s,%s,%s,%s,%s)")
    new_id = str(uuid.uuid4())
    val = (new_id,row["payment_method"],row["location"],row["datetime"],row["total_price"])
    update(conn, SQL, val, should_commit=False, should_return=False)
    row["location"] = new_id
    #row["location"] = new_id #currently we are changing location to be the transaction ID ( this can be changed! Ask for others input pls adam)
    return row
 

def load_payment_data(conn, row):
    #this is a very simple reference table which will contain CASH, CARD or OTHER
    #This should only ever happen ONCE
    payment_method = row["payment_method"]
    SQL = ("SELECT * FROM payments WHERE payment_type = %s")
    values = (payment_method,)
    result = update(conn, SQL, values, should_commit=False, should_return=True)
    if len(result) == 0:
        SQL = ("INSERT INTO payments (id, payment_type)"
            "VALUES (%s,%s)")
        new_id = str(uuid.uuid4())
        val = (new_id,payment_method)
        update(conn, SQL, val, should_commit=False, should_return=False)
        row["payment_method"] = new_id
        return row
    row["payment_method"] = result[0][0]
    return row

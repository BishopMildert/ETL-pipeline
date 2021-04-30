# importing libraries
import os
import psycopg2
import uuid
from dotenv import load_dotenv
from datetime import datetime
from psycopg2 import Error
from src.db.core import query, update, connection

# loading env data
'''
!!!CURRENTLY ON HOLD - PRIORITISING TRANSFORM SCRIPT!!!

'''

load_dotenv()

class Product:
    def __init__(self, name, size, price):
        self.id = uuid.uuid4()
        self.name = name
        self.size = size
        self.price = price
    
    def load_2db(self, query:str):
        sql = 'INSERT INTO product(id, name, size, price) VALUES(%s, %s, %s, %s)'
        return query(sql, (self.id, self.name, self.size, self.price))

class Transaction: #last to be made
    def __init__(self, customer, payment, franchise, date_time):
        self.id = uuid.uuid4()
        self.customer = Customer() # needs to add correct functionality
        self.obj_payment = Payment()
        self.obj_franchise = Franchise()
        self.date_time = datetime(date_time)

class Basket:
    def __init__(self, transaction, product):
        self.obj_transaction = Transaction()

def Load_Product_Data(data):
    conn = connection()
    for product in data:
        try:
            update(conn, "INSERT INTO product(size, name, price, id) VALUES (%s, %s, %s, %s)", product.values(), False)
        except:
            print("Invalid input, skipping insertion")
    conn.commit()
    conn.close()

def Load_Basket_Data(data):
    conn = connection()
    for basket in data:
        try:
            update(conn, "INSERT INTO basket(transaction, product, id) VALUES (%s, %s, %s)", basket.values(), False)
        except:
            print("Invalid input, skipping insertion")
    conn.commit()
    conn.close()
        
def Load_Transaction_Data(data):
    conn = connection()
    for transaction in data:
        try:
            update(conn, "INSERT INTO transaction(date_time, franchise, payment, id) VALUES (%s, %s, %s, %s)", transaction.values(), False)
        except:
            print("Invalid input, skipping insertion")
    conn.commit()
    conn.close()

def load_franchise_table(data): # see transform.convert_locations_to_keys for the locations_dict
    conn = connection()
    for i in (data): 
        SQL = ("INSERT INTO franchise (id, cafe_location)"
            "VALUES (%s,%s)")
        val = (data[i],i)
        update(conn, SQL, val, False)
    conn.commit()
    conn.close()   

def load_payment_table():
    #this is a very simple reference table which will contain CASH, CARD or OTHER
    #This should only ever happen ONCE
    conn = connection()
    options = ["CASH","CARD","OTHER"]
    for num,i in enumerate(options): 
        SQL = ("INSERT INTO payment (id, type)"
            "VALUES (%s,%s)")
        val = (num+1,i)
        update(conn, SQL, val, False)
    conn.commit()
    conn.close()

import csv
import pandas as pd
import uuid
from src.db.core import connection, query
select_all_orders = "SELECT * from product"
conn = connection()

basket_items = []

"""READ THE ORIGINAL FILE DATA"""
#read the input data into a table
file = pd.read_csv("./data/2021-02-23-isle-of-wight.csv")
df = pd.DataFrame(file)

#read the csv file into a table     
df.columns = ["datetime", "location", "customer_info", "basket", "payment_method", "total_price", "card_details"]
#read all the data from the basket column
products = df.basket
# make a new column as string values
df['new_col'] = df['basket'].str.split(',')


def create_basket(num, i):
    #create a basket  
    # num is the transaction basket string i.e "Large,Hot chocolate,2.9,Large,Chai latte,2.6,Large,Hot chocolate,2.9"
    basket = i
    #seperate items in the basket into seperate items 
    dp = list(zip(*[iter(basket)]*3))
    #create basket dictionary
    for item in dp:
        basket = {"size": "", "name": "", "price": ""}
        basket["size"] = item[0]
        basket["name"] = item[1]
        basket["price"] = item[2]
    print(basket)
    #     #check through products table in database
    # #add product id to basket table 
    # for item in basket_items:
    #     basket = {"id": "", "transaction_id": "", "product": "" }
    #     basket['product'] = item
    #load_basket(basket)
                

    
#list out each transaction 
def print_transactions():
    for num, i in enumerate(df['new_col'], 1): 
        #create new dictionary which shows transaction id 
        d = {"transaction_id": " ", "payment": " ", "franchise": " ", "date_time": " "}
        d['transaction_id'] = num
        create_basket(num, i)
        #print the individual transactions 
        #print(d)
print_transactions()
import pandas as pd
import numpy as np
import datetime
#from src.ETL.extract import file_loader
from src.db.core import update, connection, query
import uuid
#1. Extract all the code into a pandas dataframe (done)
#2. Transform the data into a usable table that we can split into order by order: (e.g A list of dictionaries contained size:, price, name like you did initially)
#2- an example row would look like this = pandas dataframe of ["2021-02-23 09:00:48","Isle of Wight",[{"size" : "Large", "name" : "Hot chocolate", "price" : 2.9},{"size" : "Large", "name" : "Chai latte", "price" : 2.6},{"size" : "Large", "name" : "Hot chocolate", "price" : 2.9}], CASH"]
#3 load the data into the database: Ideally we should have a group of functions that will look at an order and load it one at a time where the row is the input
#3 i.e:
#3 1. look at location in SQL, if it is present set the ID to that, if not upload it to the franchise table and return the ID
#3 2. look at the payment method in SQL. If it is in datbase set ID to that, if not upload it to the franchise table and return the ID
#3 3. load the transaction table and return the transaction ID
#3 4. look at the products in SQL - if the product is in the SQL table set ID to that, if not upload it to product table and return ID
#4 5. upload all basket using the list of product IDs and transaction IDs


def transform(data):
    #function that will take in a pandas dataframe, and return the cleaned data
    data = drop_sensitive_data(data)
    list_of_dictionaries = data.to_dict('records') #Pandas doesn't let us have lists inside cells so convert to dicitonaries
    for index,row in enumerate(list_of_dictionaries):
        list_of_dictionaries[index]["basket"] = format_orders(row["basket"])
    return list_of_dictionaries

def drop_sensitive_data(data):
    #function that will drop names and card details
    to_drop = ['customer_info','card_details']
    data.drop(columns=to_drop, inplace=True)
    return data


def format_orders(row):
    try:
        basket_list = row.split(',')
        transactions = []
        # for i in basket_list:
        #     temp_order_list = []
        for j in range(int(len(basket_list)/3)):
            new_dictionary = dict(size=basket_list[(j*3)], product=basket_list[(j*3)+1], price=float(basket_list[(j*3)+2]))
            transactions.append(new_dictionary)
        
        return transactions
    except:
        pass

#################################################################
#    No Code below this is used currently (but will be useful)  #
#################################################################
# class Transform:
#     def __init__(self, csv_file):
#         '''
#         file_path needs to be in .CSV format
#         '''
#         try:
#             # this 
#             header = ["datetime", "location", "customer_info", "basket", "payment_method", "total_price", "card_details"]
#             #self.file_path = file_path
#             self.dataframe = pd.read_csv(csv_file, names=header)              
#         except Exception as e:
#             print(f'ERROR {e}')
    

#     def product_list(self):
#         '''
#         returns a list of dict from Products dataframe
#         needs to check for updates and 
#         '''
#         try:
#             # loading basket information into a single DF
#             products = self.dataframe['basket'].str.split(',', expand=True)
#             products_array = products.to_numpy()
            
#             num = products.shape
#             num = int((num[0]*num[1])/3)
#             # return np array back into pandas df
#             products = pd.DataFrame(products_array.reshape(num,3)).dropna()
#             products = products.drop_duplicates()
#             # adding correct columns
#             products = products.rename(columns={0:'size', 1:'product', 2:'price'})
#             products['price'] = pd.to_numeric(products['price'])
            
#             # transform df into dict obj
#             products_dict = products.to_dict('records')
#             # checking for duplicates in the products list
#             product_check = []
#             for i in products_dict:
#                 for j in products_dict:
#                     if i['price'] == j['price'] and i['product'] == j['product'] and j['size']!= '':
#                         i['size'] = j['size']
#                         product_check.append(i)
#                     else:
#                         if i['size'] == '':
#                             i['size'] = 'Regular'
#             products_dict = product_check
            
#             for product in products_dict:
#                 product['id'] = str(uuid.uuid4())
            
#             return products_dict

#         except Exception as e:
#             print(f'ERROR {e}')
    
#     # def format_datetime(self):
#     #     try:
#     #         dt_df = self.dataframe['datetime']
#     #         dt_df = pd.to_datetime(dt_df, errors='coerce')
#     #         return dt_df
#     #     except Exception as e:
#     #         print(f'ERROR {e}')
    
#     # another method?
#     def transaction(self, products: list, order: list):
#         try:
#             orders = self.dataframe['basket'].str.split(',')
#             basket = []
#             next((item for item in products if item["product"]=='Flavoured latte - Vanilla'), None)
#             pass
#         except Exception as e:
#             print(f'ERROR {e}')


#     def convert_payment_type(self):
#         #function that will go through and change all payment types to 1,2,3
#         # 1 will reference CASH, 2 will reference CARD, 3 will be OTHER
#         for i in range(len(self.dataframe['payment_method'])):
#             example = self.dataframe['payment_method'][i]
#             if example == "CASH":
#                 self.dataframe.loc[i, 'payment_method']= 1
#             elif example == "CARD":
#                 self.dataframe.loc[i, 'payment_method']= 2
#             else:
#                 self.dataframe.loc[i, 'payment_method']= 3

#     def return_unique_locations(self, df):
#         #used by transform_transactions_and_franchises
#         #this will go through a data frame and return every unique location as part of a set
#         unique_locations = set()
#         for i in range(len(df['location'])):     
#             unique_locations.add(df['location'][i])
#         return unique_locations

#     #This version is not future proof - it assumes that the current database locations is empty
#     def convert_set_locations_to_dict_with_keys(self, df):
#         # used by transform_transactions_and_franchises
#         unique_locations = self.return_unique_locations(df) # gets a set of unique locations
#         location_dict = dict.fromkeys(unique_locations, 0)
#         for key in location_dict:
#             location_dict[key] = str(uuid.uuid4())
#         return location_dict
        
#     def convert_locations_to_keys(self, df):
#         # used by transform_transactions_and_franchises
#         location_dict = self.convert_set_locations_to_dict_with_keys(df)
#         for i in range(len(df['location'])):
#             df.loc[i, 'location'] = location_dict[df.loc[i, 'location']]
#         return location_dict

#     def transform_transactions_and_franchises(self):
#         #id payment, cafe, datetime
#         self.drop_sensitive_data() 
#         self.convert_payment_type()
#         self.format_datetime()
#         transactions_table= self.dataframe.copy()
#         location_dict = self.convert_locations_to_keys(transactions_table)
#         to_drop = ['total_price', 'basket']
#         transactions_table.drop(columns=to_drop, inplace=True)
#         transactions_table = transactions_table.to_dict('records')
#         for num,i in enumerate(transactions_table):
#             i["transaction_id"] = num
#         return transactions_table, location_dict

    
#     def format_datetime(self):
#         '''
#         Date Format: YYYY-MM-DD HH:MM:SS
#         '''
#         for i in range(len(self.dataframe['datetime'])):
#             example = self.dataframe['datetime'][i]
#             #split up date[0] and time[1]
#             example = example.split(" ")
#             #seperate date into year, month, day
#             example[0] = example[0].split("-")
#             #seperate time into hour, minute, second
#             example[1] = example[1].split(":")

#             if len(example[0]) != 3:
#                 print("Wrong format for date you dingus")
#             if len(example[1]) != 3:
#                 print("Wrong format for time you dingus")
#             if len(example) != 2:
#                 print("Two many spaces in your date time you dingus")

#             #turn str to int
#             for j in range(len(example[0])):
#                 try:
#                     example[0][j] = int(example[0][j])
#                 except:
#                     print("You didn't give me a number for date you dingus")
#             for j in range(len(example[1])):
#                 try:
#                     example[1][j] = int(example[1][j])
#                 except:
#                     print("You didn't give me a number for date you dingus")

#             try:
#                 date_and_time = datetime.datetime(example[0][0], example[0][1], example[0][2], example[1][0], example[1][1], example[1][2])
#             except:
#                 date_and_time = None

#             if type(date_and_time) == type(datetime.datetime.now()):
#                 self.dataframe.loc[i, 'datetime'] = str(date_and_time)
#             else:
#                 self.dataframe.loc[i, 'datetime'] = None

# def transaction_and_whole_basket(orders, products):
#     temp_order = []
#     for index, order in enumerate(orders):
#         y = []
#         for item in order:
#             if item in products:
#                 y.append(item)
#         empty.append(dict(transaction_id=index, basket=y))
#     return temp_order


# # format orders into nice and tidy dict

# def change_list_of_products_to_ids(transform_object):
#     #transform object must be the Transform class
#     #pulls the entire product database, and replaces any products with their ids only
#     #the input will be an object of the Transform
#     #    [[{"size" : "large", "price" : 1.9, "name": "coffee"}], [,,,]]
#     #the output will look like [["uuid123"],["uuid124","uuid125",uuid126]]
    
#     conn = connection()
#     orders = format_orders(transform_object.dataframe)
#     #my_transaction_and_whole_basket(orders, products):
#     sql = ("SELECT * FROM product")# and price = %s")
#     unique_products = query(conn, sql)
#     #print(unique_products)
#     #3 nested for loops is very very bad - look at reducing this
#     for index,i in enumerate(orders):
#         for index1,j in enumerate(i):
#             for k in unique_products:
#                 if (k[1] == j["product"] and k[3] == float(j["price"])):
#                     orders[index][index1] = k[0]
#                     break
#     return orders

# def convert_ids_to_transaction_ids(orders):
#     #the final format required for the load function
#     #we inputs the list of order ids e.g [["uuid123"],["uuid124","uuid125",uuid126]]
#     #we output a list of dictionaries: e.g [{"transaction": 0, "product": "uuid123" , id: random_uuid1},
#     #                                       {"transaction": 1, "product": "uuid124" , id: random_uuid2},
#     #                                       {"transaction": 1, "product": "uuid125" , id: random_uuid3},
#     #                                       {"transaction": 1, "product": "uuid125" , id: random_uuid4}]  the random uuids do not matter at all
    
#     final_basket_list = []
#     for index, i in enumerate(orders):
#         for index2, j in enumerate(i):
#             final_basket_list.append({"transaction": index,
#                                       "product" : j,  
#                                       "id" : str(uuid.uuid4())  # this can 
#                                         })
#     return final_basket_list

# def prepare_basket(file_path):
#     #function that runs everything together and returns the final basket list
#     #[{"transaction": 0, "product": "uuid123" , id: random_uuid1},
#     #{"transaction": 1, "product": "uuid124" , id: random_uuid2},
#     #{"transaction": 1, "product": "uuid125" , id: random_uuid3},
#     #{"transaction": 1, "product": "uuid125" , id: random_uuid4}]
#     transform_object = Transform(file_path)
#     orders_list = change_list_of_products_to_ids(transform_object)
#     final_basket_list = convert_ids_to_transaction_ids(orders_list)
#     return final_basket_list
    
# if __name__=="__main__":
#     transform_object = Transform()
#     orders_list = change_list_of_products_to_ids(transform_object)
#     final_basket_list = prepare_basket('./data/2021-02-23-isle-of-wight.csv')
#     print(final_basket_list)


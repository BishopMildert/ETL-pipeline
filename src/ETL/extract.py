import csv
import pandas as pd 
from io import BytesIO

'''
function to read file
'''
def extract(s3_object):
    #function that will read a file and return everything as a list of dictionaries
    data = []
    try:  
        with BytesIO(s3_object.get()["Body"].read()) as bio:
            data = pd.read_csv(bio, header=None, sep=',')
            data.columns =["datetime", "location", "customer_info", "basket", "payment_method", "total_price", "card_details"]
    except FileNotFoundError:
        print(f"'{s3_object}' file was not found.\n")
        input("Check to see Error has been resolved.")
    return data


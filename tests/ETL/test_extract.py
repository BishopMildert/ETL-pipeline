from src.ETL.extract import *
from pandas._testing import assert_frame_equal
import pandas as pd
#test file for the csv file readers for the Isle of Wight

def test_file_loader():
    expected = pd.DataFrame(data=[["2021-02-23 09:00:48","Isle of Wight","Morgan Berka","Large,Hot chocolate,2.9,Large,Chai latte,2.6,Large,Hot chocolate,2.9",
                                  "CASH",8.40,"None"]],
                                  
                                columns=["datetime", "location", "customer_info", "basket", "payment_method", "total_price", "card_details"], dtype=None, copy=False)

    actual = extract("tests/data/file_read.csv")
    assert_frame_equal(expected, actual)

mock_data =  pd.DataFrame(data=[["Large,Hot chocolate,2.9,Large,Chai latte,2.6,Large,Hot chocolate,2.9"]],
                                  
                                columns=["basket"], dtype=None, copy=False)
expected = pd.DataFrame(data=[[{"size" : "Large", "name" : "Hot chocolate" "price",2.9},
                               {"size" : "Large", "name" : "Hot Chai latte" "price",2.6},
                               {"size" : "Large", "name" : "Hot chocolate" "price",2.9}]],
                                  
                                columns=["basket"], dtype=None, copy=False)
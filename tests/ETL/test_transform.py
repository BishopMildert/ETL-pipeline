import pandas as pd
from src.ETL.transform import *
from pandas._testing import assert_frame_equal


def test_format_datetime():
    def mock_data():
        return pd.DataFrame(data=[["2021-02-23 09:00:48"],["2021-02-2a 09:00:48"],["2021-02-23- 09:00:48"],["2021-02-23 09::0:48"],["2021-13-23 09:00:48"]],
                                columns=["datetime"], dtype=None, copy=False)
    expected = pd.DataFrame(data=[["2021-02-23 09:00:48"],[None],["2021-02-23 09:00:48"],[None],[None]],
                            columns=["datetime"], dtype=None, copy=False)
    actual = format_datetime(mock_data())
    assert_frame_equal(expected, actual)

def test_drop_sensitive_data():
    def mock_data():
        return pd.DataFrame(data=[["Adam Flatley", "999999999999","yes"],["Christian Royle", "111111111","Also yes"]],
                                columns=["customer_info", "card_details", "return this"], dtype=None, copy=False)
    expected = pd.DataFrame(data=[["yes"],["Also yes"]],
                            columns=["return this"], dtype=None, copy=False)
    actual = drop_sensitive_data(mock_data())
    assert_frame_equal(expected, actual)
    
def test_check_correct_basket():
    #jess should be writing this
    def mock_data():
        pass
    pass


def test_transform():
    def mock_data():
        return pd.DataFrame(data=[["2021-02-23 09:00:48","Isle of Wight","Morgan Berka","Large,Hot chocolate,2.9,Large,Chai latte,2.6,Large,Hot chocolate,2.9",
                                  "CASH",8.40,"None"]],
                                columns=["datetime", "location", "customer_info", "basket", "payment_method", "total_price", "card_details"], dtype=None, copy=False)
        
    {"datetime" : "2021-02-23 09:00:48", "location" : "Isle of Wight", "basket" : [{"size" : "Large", "name" : "Hot chocolate" "price",2.9},
                               {"size" : "Large", "name" : "Hot Chai latte" "price",2.6},
                               {"size" : "Large", "name" : "Hot chocolate" "price",2.9}],
                                "payment_method" : "CASH",  "total_price" : 8.40}
    actual = transform()
    assert_frame_equal(expected,actual)
    
    
def test_clean_basket():
    def mock_data():
        return "Large,Hot chocolate,2.9,Large,Chai latte,2.6,Large,Hot chocolate,2.9"
    
    expected = [{"size" : "Large", "name" : "Hot chocolate" "price",2.9},
                               {"size" : "Large", "name" : "Hot Chai latte" "price",2.6},
                               {"size" : "Large", "name" : "Hot chocolate" "price",2.9}]
    actual = clean_basket(mock_data())
    assert_frame_equal(expected,actual)

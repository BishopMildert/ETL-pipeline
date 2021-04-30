from src.ETL.extract import extract
from src.ETL.transform import transform
from src.ETL.new_load import load


def run_etl(s3_object):

    data = extract(s3_object) # extracts all the data from the CSV
    data = transform(data) # transforms the data into a more readable state (i.e parses the basket, removes Personal info)
    load(data) # connects all the transformed data to the database
    
if __name__ == "__main__":
    the_file = './data/2021-02-23-isle-of-wight.csv'
    run_etl(the_file)
    
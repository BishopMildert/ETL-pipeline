import csv
import boto3 # library used to access AWS API
from src.app import run_etl

def execute(event, context):   
    bucket = event["Records"][0]["s3"]["bucket"]["name"] 
    key = event["Records"][0]["s3"]["object"]["key"]

    s3_resource = boto3.resource("s3")
    s3_object = s3_resource.Object(bucket, key)
       
    run_etl(s3_object)
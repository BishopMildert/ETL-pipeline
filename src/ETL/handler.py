def run(event, context):
   
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    s3_resourse = boto3.resource("s3")
    s3_object = s3_resourse.Object(bucket, key)
    raw = s3_object.get()["Body"].read().decode("utf-8").splitlines()
    
    x_data = csv.reader(raw)
    
    data = []
    for line in x_data:
        data.append(line)
        
    print(data[0])    
    print(data[1])
    print(data[3])
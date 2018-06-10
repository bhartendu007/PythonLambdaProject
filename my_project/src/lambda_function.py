# Importing packages

import urllib
import pandas as pd
import json

# aws boto3 python module required to connect to S3 bucket instance
import boto3

def parse_excel(file_path):

     df = pd.read_excel(file_path, sheet_name = "MICs List by CC")
     df = df.fillna("NULL")
     my_json_object = []
     for i in range(df.shape[0]):
         series_dict = df.iloc[i]
         my_json_object.append(dict(series_dict))        #rows data to dict format
     return my_json_object                               #return list of dictionary
     
 
def my_lambda_handler(event, context):

     try :

       outfilename = "/tmp/" + "test.xls"
       url_of_file = "https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.xls"
       urllib.request.urlretrieve(url_of_file, outfilename)        #storing excel data in locally
       json_object = parse_excel( outfilename )                      # call parse_excelfile and collect data in json format
       
       AWS_BUCKET_NAME = 'myjsondata_to_s3bucket'           
       s3 = boto3.resource( 's3' )
       bucket = s3.Bucket( AWS_BUCKET_NAME )                       #connect to S3 bucket instance and store json data
       path = 'myjsondata.txt'
       data = json_object
       
       bucket.put_object(
        ACL='public-read',
        ContentType='application/json',
        Key=path,
        Body=data,
       )

       body = {
        "uploaded": "true",
        "bucket": AWS_BUCKET_NAME,
        "path": path,
           }
       
       return {
        "statusCode": 200,
        "body": json.dumps(body)
           }
       
       
     except Exception as error:
           print(error)
                  
     

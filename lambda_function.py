import json
from botocore.vendored import requests
import re
import os
import boto3
import botocore
import copy
from time import localtime, strftime
from decimal import Decimal
import uuid
from uuid import UUID

import lighting_label_verification

def lambda_handler(event, context):
    beginning_time = context.get_remaining_time_in_millis()
    
    bodystr = event.get("body", None)
    
    if bodystr is None:
        body = {}
    elif isinstance(bodystr,dict):
        body = bodystr
    else:
        body = json.loads(bodystr)
    
    callback_url = body.get("callback_url", -1)
    
    bucket_name = body.get("s3_bucket")
    path = body.get("s3_file")
    path='https://s3.us-east-2.amazonaws.com/lighting-input-files/projecttest.xlsm'
	
    results = {}
    
    s3 = boto3.resource('s3')
        

		
    # Return results from lighting_label_verification python file
    results=lighting_label_verification.lighting_verification(path)
	
    #Generate job ID
    job_id = "{}".format(uuid.uuid4())
    #job_id=1
    

    #Save results for the job ID in dynamo
    dynamodb = boto3.resource('dynamodb')
    
    #dynamo_3 is the dynamodb table
    table = dynamodb.Table("lighting_label")

    item = {
        "job_id": job_id,
        "results": copy.deepcopy(results),
        "input_request": body,
        "execution_time_ms": beginning_time - context.get_remaining_time_in_millis(),
        "execution_date_time": strftime("%Y-%m-%d %H:%M:%S", localtime()) 
        }

    #item = properConversion(item)
	
	#change results to item
    table.put_item(Item=item)
	 
    #Put the job ID in the results & return/hit callback URL
    results["job_id"] = job_id

    return finishUp(callback_url, results, 200)
	
	
def finishUp(callback_url, results, statusCode):
    payload = {
        #"isBase64Encoded": False,
        "statusCode": statusCode,
        "headers": {},
        "body": results
    }

	
    #Hit callback URL with a response
    if (callback_url != -1):
        requests.post(callback_url, json=payload)
        
    return payload

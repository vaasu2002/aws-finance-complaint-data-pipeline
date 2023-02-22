import json
import pymongo
import os
import boto3
import datetime
import requests
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
BUCKET_NAME = os.getenv("BUCKET_NAME")
MONGODB_URL = os.getenv("MONGODB_URL")

DATA_SOURCE_URL = f"https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/" \
                      f"?date_received_max=<todate>&date_received_min=<fromdate>" \
                      f"&field=all&format=json"

client = pymongo.MongoClient(MONGODB_URL)

def get_from_data_to_data():
    from_date = "2023-01-01"
    from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")

    if COLLECTION_NAME in client[DATABASE_NAME].list_collection_names():

        res = client[DATABASE_NAME][COLLECTION_NAME].find_one(sort=[("to_date",pymongo.DESCENDING)])

        if res is not None:
            from_date = res["to_date"]
        
    to_date = datetime.datetime.now() #current date

    return {
        "form_date": from_date.strftime("%Y-%m-%d"),
        "to_date": to_date.strftime("%Y-%m-%d"),
        "from_date_obj": from_date,
        "to_date_obj": to_date
    }

def save_from_date_to_date(data, status=True):
    data.update({"status": status})
    client[DATABASE_NAME][COLLECTION_NAME].insert_one(data)

def lambda_handler(event, context):
    from_date, to_date, from_date_obj, to_date_obj = get_from_data_to_data().values()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if current_date==from_date:
        return {
            'statusCode': 200,
            'body': json.dumps('Pipeline has already downloaded all data upto yesterday')
        }

    url = DATA_SOURCE_URL.replace("<fromdate>", from_date).replace("<todate>", to_date)
    data = requests.get(url, params={'User-agent': 'your bot '})

    finance_complaint_data = list(map(lambda x:x["_source"],
                                    filter(lambda x:"_source" in x.keys(),
                                        json.loads(data.content)))
                                )

    s3 = boto3.resource('s3')
    s3object = s3.Object(BUCKET_NAME,f"inbox/{from_date.replace('-','_')}_{to_date.replace('-','_')}_finance_cpmplaint.json")
    s3object.put(
        Body=(bytes(json.dumps(finance_complaint_data).encode('UTF-8')))
    )


    save_from_date_to_date({"from_date": from_date_obj, "to_date": to_date_obj})

    return {
        'statusCode': 200,
        'body': json.dumps('Pipeline has been executed successfully')
    }
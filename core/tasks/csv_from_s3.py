import pandas as pd
from loguru import logger
import boto3

from core.celery import app
from back_edesoft.models import User

def lambda_handler(event, context):
    """Lambda handler"""
    logger.info("Start lambda 'csv_to_db'")
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]
    csv_to_db.delay(bucket_name, object_key)
    logger.info("Done")
    return {"statusCode": 200, "body": "Success"}

@app.task(bind=True, name="csv_to_db")
def csv_to_db(self, bucket_name, object_key):
    """Reads a csv file and saves the data to the database"""
    logger.info("Start task 'csv_to_db'")
    s3 = boto3.client("s3")
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    except Exception as e:
        logger.error(e)
        return
    data = obj.get()["Body"].read().decode("utf-8").splitlines()
    df = pd.read_csv(data)
    for row in df.iterrows():
        User.objects.get_or_create(
            name=row[1][0],
            email=row[1][1],
            password=row[1][2],
            cpf=row[1][3],
            phone=row[1][4],
            cnpj=row[1][5],
        )
    logger.info("Done")
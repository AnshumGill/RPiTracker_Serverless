import logging
import httpx
import asyncio
from bs4 import BeautifulSoup
import boto3
from boto3.dynamodb.conditions import Attr
from time import time
from constants import *
from config import *
from telegram import Bot

dynamodb=boto3.resource('dynamodb')
table=dynamodb.Table(dynamodb_table)
bot=Bot(token=telegram_token)

# Resolving logging issues for AWS Lambda
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level = logging.INFO, force=True)

async def get_info(client:object,vendor:Vendor,url:str)->None:
    '''
        Async function to scrape URL and populate objects using information from page using BeautifulSoup
    '''
    resp = await client.get(url,headers=headers,follow_redirects=True)
    if(resp.status_code==200):
        soup=BeautifulSoup(resp.content,'html5lib')
        vendor.model_elem.scrape_content(soup)
        vendor.price_elem.scrape_content(soup)
        vendor.stock_elem.scrape_content(soup)
        temp_raspi=RaspPi(vendor.model_elem,vendor.price_elem,vendor.stock_elem,vendor.urls.index(url),vendor.gst_inc)
        previously_notified=table.scan(
            Select="SPECIFIC_ATTRIBUTES",
            FilterExpression=Attr("model").eq(temp_raspi.model),
            ProjectionExpression="notified")['Items']
        if(len(previously_notified) > 0 and len(previously_notified[0])>0):
            previously_notified=previously_notified[0]['notified']
        if(temp_raspi.available and not previously_notified):
            send_telegram_notification(vendor,temp_raspi)
            temp_raspi.mark_notified(True)
        if(not temp_raspi.available and previously_notified):
            temp_raspi.mark_notified(False)
        vendor.add_raspi(temp_raspi)
        logging.info(f"Name - {temp_raspi.model}, Price - {temp_raspi.price}, Avail - {temp_raspi.available}")
    else:
        logging.warning(f"Status Code - {resp.status_code} From {vendor.name}")

async def scrape_url(vendors:list)->None:
    '''
        Async function to iterate over all vendors and urls for those vendors to gather 
        subtasks of get_info function
    '''
    async with httpx.AsyncClient() as client:
        tasks=[]
        for vendor in vendors:
            for url in vendor.urls:
                tasks.append(asyncio.create_task(get_info(client,vendor,url)))
        await asyncio.gather(*tasks,return_exceptions=True)

def send_telegram_notification(vendor:Vendor,raspi:RaspPi)->None:
    '''
        Function to send telegram notifications for the configured bot
    '''
    logging.info(f"Sending notification for {vendor.name}, {raspi.model}")
    bot.send_message(text=f"{raspi.model} is available for {raspi.price} at {vendor.urls[raspi.url_ref]}",chat_id=chat_id)

def add_entries(vendors:list)->None:
    '''
        Function to iterate over all vendor objects and all raspberry pi objects to add 
        records inside DynamoDB
    '''
    for vendor in vendors:
        for raspi in vendor.raspi:
            item={
                'model':raspi.model,
                'price':int(raspi.price),
                'available':raspi.available,
                'url':vendor.urls[raspi.url_ref],
                'vendor':vendor.name,
                'notified':raspi.notified,
                'last_updated':int(time())
            }
            resp=table.put_item(Item=item)
            logging.debug(resp)

def lambda_handler(event, context)->dict:
    '''
        Function invoked by lambda function on AWS
    '''
    asyncio.run(scrape_url(vendors))
    json_data=[v.toJSON() for v in vendors]
    logging.debug(json_data)
    add_entries(vendors)
    return {
        'statusCode': 204,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': ""
    }

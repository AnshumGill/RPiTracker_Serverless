import logging
import httpx
import asyncio
from bs4 import BeautifulSoup
import re
import os
import json
from constants import *

root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level = logging.INFO, force=True)

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))

def get_contents(soup,element):
    elem=soup.find(element.tag,{element.attr:element.val})
    if(elem is not None):
        if(element.extra_elem!=None):
            elem=elem.find(element.extra_elem)
        elem=elem.text.strip()
    else:
        return None
    return elem

async def get_info(client,vendor,url):
    resp = await client.get(url,headers=headers,follow_redirects=True)
    if(resp.status_code==200):
        soup=BeautifulSoup(resp.content,'html5lib')
        name=get_contents(soup,vendor.model_elem)
        price=get_contents(soup,vendor.price_elem)
        avail=get_contents(soup,vendor.stock_elem)
        if(avail is not None):
            if('-' in avail):
                avail=avail.split('-')[0].strip()
        avail=not(avail.lower() in oos_strings)
        if(price is not None):
            price=re.sub("[^0-9.]","",price)
            price=float(price[1:] if price[0]=="." else price)
            price=price if vendor.gst_inc else price*1.18
        vendor.add_raspi(RaspPi(name,price,avail,vendor.urls.index(url)))
        print(f"Name - {name}, Price - {price}, Avail - {avail}")
    else:
        print(f"Status Code - {resp.status_code} From {vendor.name}")

async def scrape_url(vendors):
    async with httpx.AsyncClient() as client:
        tasks=[]
        for vendor in vendors:
            for url in vendor.urls:
                tasks.append(asyncio.create_task(get_info(client,vendor,url)))
        await asyncio.gather(*tasks,return_exceptions=True)

def lambda_handler(event, context):
    asyncio.run(scrape_url(vendors))
    json_data=[v.toJSON() for v in vendors]
    print(json_data)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'body': json.dumps(json_data)
    }

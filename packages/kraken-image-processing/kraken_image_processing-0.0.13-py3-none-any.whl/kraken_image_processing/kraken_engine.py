from kraken_image_processing import kraken_image_processing as k   

from kraken_class_entity.entity import Entity
from kraken_class_entity.entities import Entities
import asyncio
import uuid
import requests
import json
import datetime

def run():

    entities = Entities()
    entities.api_url = 'https://krakenengine.tactik8.repl.co/api'

    params = {'record_type': 'schema:Imageobject'}


    entities.search_api(params, 200, 0)
    loop = asyncio.get_event_loop()
    records = []
    for i in entities.entities:
        records.append(i.record)
    records = loop.run_until_complete(run_async(records))


    print(len(records))
    count = 0
    for i in records:
        img = i.get('temp:pil_img', None)
        if img:
            exist = True
            count += 1
        else:
            exist = False
        #print(i.get('@id', None), exist)
    print('Success:', count)


    # Process
    output_records = []
    actions = []
    count = 0
    for i in records:
        count += 1
        print('Processing record:', count)
        if i.get('temp:pil_img', None):
            

            start_time=datetime.datetime.now()

            result = k.get(i)
            output_records.append(result)
            end_time=datetime.datetime.now()
            action = {
                '@type': 'schema:action',
                '@id': str(uuid.uuid4()),
                'schema:object': i,
                'schema:result': result, 
                'schema:startTime': start_time,
                'schema:endTime': end_time,
                'schema:instrument': {'@type': 'schema:WebAPI', 'schema:url': 'https://replit.com/@tactik8/imageproc2#kraken_image_processing'},
                'datasource': 'image_proc.kraken_engine'
            }
            actions.append(action)
            post_action(action)
            #e = Entity()
            #e.load(action)
            #e.post_api()


    print('Output n: ', len(output_records))

    # Save records
    output_entities = Entities()
    #output_entities.load(actions)
    #output_entities.post_api()
    print('Saved')


def post_action(action):
    url = 'https://krakenengine.tactik8.repl.co/api'

    headers = {'Content-Type': 'application/json'}
    data = json.dumps(action, default = str)
    r = requests.post(url, headers = headers, data = data)



async def run_async(records):
    tasks = []
    for i in records:
        tasks.append(asyncio.ensure_future(k.load_async(i)))
    print('starting')
    records = await asyncio.gather(*tasks, return_exceptions=True)
    return records
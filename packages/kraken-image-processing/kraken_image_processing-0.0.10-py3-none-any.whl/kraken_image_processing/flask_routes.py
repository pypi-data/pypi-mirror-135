import os
from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import jsonify
import requests
import json
import datetime
import time
import uuid
import random
from kraken_image_processing import kraken_image_processing as k   


# Initalize app
test_mode = False


# Initialize flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = b'_5#mn"F4Q8z\n\xec]/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



@app.route('/', methods=['GET'])
def main_get():

    url = 'https://imageproc2.tactik8.repl.co/api'
    files = {'file': open('img.png', 'rb')}

    params = {'@type':'schema:imageObject', '@id': 'some_id'}
    #data = json.dumps(record, default = str)

    #r = requests.post(url, params=params, files=files)
    #print(r.json())

    return Response('ok')


@app.route('/api', methods=['GET'])
def api_get():
    """Process get data
    """

    return Response('ok')


@app.route('/api', methods=['POST'])
def api_post():
    """Process get data
    """
    
    file = request.files['file'].read()
    record = {
        '@id': request.values.get('@id'),
        '@id': request.values.get('@type')
        }

    records = k.process(record, file)
    print(records)
    return Response('ok')

    # save the single "profile" file
    uploads_dir = os.path.join(app.instance_path, 'uploads')
    uploads_dir = 'uploads'


    image = request.files['file']
    image.save(os.path.join(uploads_dir, image.filename))

    return jsonify('ok')





def run_api():
    app.run(host='0.0.0.0', debug=False)


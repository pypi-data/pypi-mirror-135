import requests
import cv2
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from urllib.request import Request, urlopen  # Python 3
import pyimgbox
import aiohttp

def get(record):

    return get_pil_img(record)


def get_pil_img(record):
    
    filepath = record.get('temp:filepath', None)
    pil_img = record.get('temp:pil_img', None)
    cv2_img = record.get('temp:cv2_img', None)
    url = record.get('schema:contentUrl', None)

    if pil_img:
        return pil_img
    elif filepath:
        return get_image_from_path(filepath)
    elif url:
        return get_image_from_url(url)
    
    

def get_cv2_img(pil_img):
    return get_cv2_from_pil(pil_img)



def get_image_from_path(image_object, filepath):
    pil_img = Image.open(filepath) 

    return pil_img


def get_image_from_url(url):
    
    # Load image
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'referer': 'https://youramateurporn.com/'
    }

    try:
        r = requests.get(url, headers = headers, timeout = 20)
        pil_img = Image.open(BytesIO(r.content))

        return pil_img

    except:
        return None

async def get_image_from_url_async(url):
    
    # Load image
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'referer': 'https://youramateurporn.com/'
    }

    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            async with session.get(url) as response:
                content = await response.read()

        pil_img = Image.open(BytesIO(content))

        return pil_img

    except Exception as e:
        print(e)
        return None

def get_cv2_from_pil(pil_img):

    if type(pil_img) is bool: 
        pil_img = pil_img.astype(np.uint8) * 255

    cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    return cv2_img




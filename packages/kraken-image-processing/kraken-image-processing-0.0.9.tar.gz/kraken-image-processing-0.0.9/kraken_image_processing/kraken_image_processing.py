

from kraken_image_processing import kraken_image_io
from kraken_image_processing.extractors import kraken_image_generic
from kraken_image_processing.extractors import kraken_image_person
from kraken_image_processing.extractors import kraken_image_face
from kraken_image_processing.extractors import kraken_image_text

from kraken_image_processing import download_models
import os


from io import BytesIO
#from kraken_image_processing.extractors import kraken_image_objects


from kraken_image_processing import post_to_image_share
from PIL import Image

download_models.download_models()


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def get(image_file):
    return process(image_file)



async def load_async(record):
    """Load image from url
    """
    url = record.get('schema:contentUrl', None)
    record['temp:pil_img'] = await kraken_image_io.get_image_from_url_async(url)

    return record


def process(record, image_byte = None):
    """Process record. If file_path provided, load image from disk instead of url.
    """

    records = []
    
    if image_byte:
        file_jpgdata = BytesIO(image_byte)
        pil_img = Image.open(file_jpgdata)

        record['temp:pil_img'] = pil_img


    # Load image
    pil_img = record.get('temp:pil_img', None)
    if not pil_img:
        pil_img = kraken_image_io.get_pil_img(record)
    record['temp:cv2_img'] = kraken_image_io.get_cv2_img(pil_img)

    # Process image generic
    print('Get generic')
    records += kraken_image_generic.get(record)

    # retrieve and process persons from image
    print('Get persons')
    records += kraken_image_person.get(record)

    # process faces from image
    print('Get faces')
    records += kraken_image_face.get(record)

    # process text from image
    print('Get text')
    records += kraken_image_text.get(record)

    # process objects from image
    print('Get text')
    #records += kraken_image_objects.get(record)

    # Save original image to share
    records += post_to_image_share.post(record)


    return records


async def process_async(record):
    """Process record. If file_path provided, load image from disk instead of url.
    """

    records = []
    
    # Load image
    pil_img = record.get('temp:pil_img', None)
    if not pil_img:
        pil_img = kraken_image_io.get_pil_img(record)
    record['temp:cv2_img'] = kraken_image_io.get_cv2_img(pil_img)

    # Process image generic
    print('Get generic')
    records += kraken_image_generic.get(record)

    # retrieve and process persons from image
    print('Get persons')
    records += kraken_image_person.get(record)

    # process faces from image
    print('Get faces')
    records += kraken_image_face.get(record)

    # process text from image
    print('Get text')
    records += kraken_image_text.get(record)



    # Save original image to share
    records += await post_to_image_share.post_async(record)


    return records



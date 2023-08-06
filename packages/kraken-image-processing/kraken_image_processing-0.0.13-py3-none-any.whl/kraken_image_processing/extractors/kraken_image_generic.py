
from kraken_image_processing.extractors import kraken_image_hash 
from kraken_image_processing.extractors import kraken_image_nude 




def get(record):
    return process_image(record)


def process_image(record):

    records = []

    cv2_img = record.get('temp:cv2_img', None)
    pil_img = record.get('temp:pil_img', None)


    record_type = record.get('@type', None)
    record_id = record.get('@id', None)


    # Get size
    i = {'@type': record_type, '@id': record_id}
    i['schema:height'], i['schema:width'], colors = cv2_img.shape
    i['datasource'] = 'kraken_image_generic'
    records.append(i)

    # get image hash
    i = {'@type': record_type, '@id': record_id}
    i['schema:hash'] = kraken_image_hash.get(cv2_img)
    i['datasource'] = 'kraken_image_generic'

    records.append(i)

    # get image hash256
    i = {'@type': record_type, '@id': record_id}
    i['schema:sha256'] = kraken_image_hash.get_sha256(pil_img)
    i['datasource'] = 'kraken_image_generic'

    records.append(i)


    # get image rating
    i = {'@type': record_type, '@id': record_id}
    i['schema:isFamilyFriendly'] = not kraken_image_nude.get(pil_img)
    i['datasource'] = 'kraken_image_nude'

    records.append(i)


    return records

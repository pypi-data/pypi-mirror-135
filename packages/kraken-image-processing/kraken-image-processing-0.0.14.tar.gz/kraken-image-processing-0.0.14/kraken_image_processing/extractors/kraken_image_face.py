import cv2
import uuid

from kraken_image_processing.extractors import kraken_image_face_gender 
from kraken_image_processing.extractors import kraken_image_face_age
from kraken_image_processing.extractors import kraken_image_face_emotions 
from kraken_image_processing.extractors import kraken_image_face_embeddings 
import pkg_resources


#model = pkg_resources.resource_stream(__name__, 'models/nn4.small2.v1.t7')

model = 'models/nn4.small2.v1.t7'

embedder = cv2.dnn.readNetFromTorch(model)



def get(image_object):
    return process_faces(image_object)


def process_faces(record):

    faces = get_faces(record)

    records = []

    new_image_object = {
        '@type': record.get('@type', None),
        '@id': record.get('@id', None)
    }

    for f in faces:

        record_type = f.get('@type', None)
        record_id = f.get('@id', None)
        img = f.get('temp:cv2_img', None)

        width, height, colors = img.shape
        if not width or width < 20 or not height or height < 30:
            continue

        record_type = 'schema:person'
        record_id = str(uuid.uuid4())


        # get emotion
        try:
            i = {'@type': record_type, '@id': record_id}
            i['emotion'] = kraken_image_face_emotions.get(img)
            i['datasource'] = 'kraken_image_face_emotion'
            records.append(i)
        except:
            print('error emotions')

        # get gender
        try:
            i = {'@type': record_type, '@id': record_id}
            i['schema:gender'] = kraken_image_face_gender.get(img)
            i['datasource'] = 'kraken_image_face_gender'
            records.append(i)
        except:
            print('error gender')

        # get age
        try:
            i = {'@type': record_type, '@id': record_id}
            i['schema:age'] = kraken_image_face_age.get(img)
            i['datasource'] = 'kraken_image_face_age'
            records.append(i)
        except:
            print('error age')


        # get embeddings
        try:
            i = {'@type': record_type, '@id': record_id}
            i['embeddings'] = kraken_image_face_embeddings.get(img)
            i['datasource'] = 'kraken_image_face_embeddings'
            records.append(i)
        except:
            print('error embeddings')


        new_image_object['schema:about'] = records

    return [new_image_object]



def get_faces(record):
    # returns cv2 faces


    img = record.get('temp:cv2_img', None)


    # Load the cascade
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the faces

    persons = []
    for (x, y, w, h) in faces:

        record_type = 'schema:person'
        record_id = str(uuid.uuid4())
        person = {'@type': record_type, '@id': record_id}


        crop_img = img[y:y+h, x:x+w]

        filename = 'images/faces/' + record_id + '.png'
        cv2.imwrite(filename, crop_img)
        person['temp:cv2_img'] = crop_img
        persons.append(person)

    return persons



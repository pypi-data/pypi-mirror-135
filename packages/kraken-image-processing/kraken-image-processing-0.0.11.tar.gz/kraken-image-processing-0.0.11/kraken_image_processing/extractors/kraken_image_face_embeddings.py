import cv2
import uuid
from fer import FER
import pkg_resources


#model = pkg_resources.resource_stream(__name__, 'models/nn4.small2.v1.t7')
model =  'models/nn4.small2.v1.t7'

embedder = cv2.dnn.readNetFromTorch(model)


def get(image):
    return get_embeddings(image)





def get_embeddings(image):
    """
    https://github.com/Ravi-Singh88/Face-Recognition-OpenCV-Facenet/blob/master/extract_embeddings.py
    
    """
    faceBlob = cv2.dnn.blobFromImage(image, 1.0 / 255,
				(96, 96), (0, 0, 0), swapRB=True, crop=False)
    embedder.setInput(faceBlob)
    vec = embedder.forward()
    embeddings = vec.flatten()
    return embeddings

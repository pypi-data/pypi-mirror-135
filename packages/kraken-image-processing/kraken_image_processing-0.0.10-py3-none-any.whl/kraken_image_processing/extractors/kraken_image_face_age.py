
import cv2
import math
import pkg_resources

#ageProto = "kraken_image_processing/models/age_deploy.prototxt"
#ageModel = "kraken_image_processing/models/age_net.caffemodel"


ageProto = pkg_resources.resource_stream(__name__, 'models/age_deploy.prototxt')

ageModel = pkg_resources.resource_stream(__name__, 'models/age_net.caffemodel')



MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']


#load the network
ageNet = cv2.dnn.readNet(ageModel,ageProto)


def get(image_path):
    return get_age(image_path)

def get_age(image_path):

    # Load image
    if isinstance(image_path, str):
        image = cv2.imread(image_path)
    else:
        image = image_path



    blob = cv2.dnn.blobFromImage(image, 1.0, (227, 227), 
    MODEL_MEAN_VALUES, swapRB=False)
    
    ageNet.setInput(blob)
    agePreds = ageNet.forward()
    age = ageList[agePreds[0].argmax()]

    return age

import cv2
import math
import pkg_resources



#genderProto = "kraken_image_processing/models/gender_deploy.prototxt"
#genderModel = "kraken_image_processing/models/gender_net.caffemodel"


genderProto = pkg_resources.resource_stream(__name__, 'models/gender_deploy.prototxt')

genderModel = pkg_resources.resource_stream(__name__, 'models/gender_net.caffemodel')



MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

genderList = ['Male', 'Female']



#load the network
genderNet = cv2.dnn.readNet(genderModel, genderProto)




def get(image_path):
    return get_gender(image_path)

def get_gender(image_path):

    # Load image
    if isinstance(image_path, str):
        image = cv2.imread(image_path)
    else:
        image = image_path



    blob = cv2.dnn.blobFromImage(image, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
    genderNet.setInput(blob)
    genderPreds = genderNet.forward()
    gender = genderList[genderPreds[0].argmax()]



    return gender
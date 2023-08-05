

'''
from imageai.Detection import ObjectDetection
import os


def get(image_object):
    return get_objects(image_object)


def get_objects(image_object):
    """Retrieves objects from image file
    """
    img = image_object.get('temp:pil_img', None)

    execution_path = os.getcwd()
    print(execution_path)

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    #detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
    detector.setModelPath( "yolo.h5")

    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=img,  minimum_percentage_probability=30)

    for eachObject in detections:
        print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
        print("--------------------------------")
    return detections


'''
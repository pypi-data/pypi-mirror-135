import cv2
import uuid
import numpy as np



def get(image_path):
    #return get_persons(image_path)
    return []



def get_persons(image_path):
    """
    https://thedatafrog.com/en/articles/human-detection-video/
    """

    # Load image
    if isinstance(image_path, str):
        img = cv2.imread(image_path)
    else:
        img = image_path

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # resizing for faster detection
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    #boxes, weights = hog.detectMultiScale(image, winStride=(8,8) )
    boxes, weights = hog.detectMultiScale(img)

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    cv2_persons = []
    for (xA, yA, xB, yB) in boxes:
        crop_img = img[yA:yB, xA:xB]
        cv2_persons.append(crop_img)
        # display the detected boxes in the colour picture
        cv2.rectangle(img, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
    filename = 'images_persons/' + str(uuid.uuid4()) + '.png'
    cv2.imwrite(filename, img)
    return cv2_persons

        
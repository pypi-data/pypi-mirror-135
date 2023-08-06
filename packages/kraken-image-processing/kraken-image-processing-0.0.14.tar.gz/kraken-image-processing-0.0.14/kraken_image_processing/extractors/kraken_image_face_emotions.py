import cv2
import uuid
from fer import FER



def get(image):
    return get_emotions(image)

def get_emotions(image):

    emo_detector = FER()
    # Capture all the emotions on the image
    captured_emotions = emo_detector.detect_emotions(image)
    top_emotion = emo_detector.top_emotion(image)

    e, p = top_emotion

    return e
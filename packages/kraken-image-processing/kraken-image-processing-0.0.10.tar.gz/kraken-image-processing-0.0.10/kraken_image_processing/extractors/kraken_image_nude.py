import nude
from nude import Nude


def get(image_path):
    return get_nude(image_path)

def get_nude(image_path):

    """
    schema:isFamilyFriendly = False
    """

    return nude.is_nude(image_path)


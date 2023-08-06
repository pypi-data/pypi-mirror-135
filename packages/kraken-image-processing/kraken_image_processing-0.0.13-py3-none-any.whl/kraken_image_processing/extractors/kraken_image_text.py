import pytesseract
import os


#os.system("install-pkg tesseract-ocr")
#os.system("python -m pytest tests -vv")

try:
    test = pytesseract.pytesseract.get_tesseract_version()
except:
    os.system("install-pkg tesseract-ocr")



"""
Requires installing tesseract-ocr:
install-pkg tesseract-ocr

"""
pytesseract.pytesseract.tesseract_cmd = "tesseract"

os.environ["TESSDATA_PREFIX"] = "/home/runner/.apt/usr/share/tesseract-ocr/4.00/tessdata/"



def get(image_object):

    return _get_text(image_object)


def _get_text(image_object):
    """Does OCR for image file
    """

    img = image_object.get('temp:pil_img', None)

    text = pytesseract.image_to_string(img)

    output_record = {}
    output_record['@id'] = image_object.get('@id', None)
    output_record['@type'] = image_object.get('@type', None)

    output_record['schema:embeddedTextCaption'] = text



    return [output_record]

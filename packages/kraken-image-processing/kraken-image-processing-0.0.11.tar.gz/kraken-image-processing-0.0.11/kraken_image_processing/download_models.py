import requests
import os

def download_models():

    print('Models download started.')


    directory = 'models'

    create_directory(directory)
    models = []
    models.append(('nn4.small2.v1.t7', 'https://storage.cmusatyalab.org/openface-models/nn4.small2.v1.t7')) 
    models.append(('age_net.caffemodel', 'https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/age_net.caffemodel'))

    models.append(('age_net.caffemodel', 'https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/age_net.caffemodel'))

    models.append(('gender_net.caffemodel', 'https://github.com/eveningglow/age-and-gender-classification/raw/master/model/gender_net.caffemodel'))

    models.append(('haarcascade_frontalface_default.xml', 'https://github.com/kipr/opencv/raw/master/data/haarcascades/haarcascade_frontalface_default.xml'))

    models.append(('age_deploy.prototxt', 'https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/age_deploy.prototxt'))

    models.append(('gender_deploy.prototxt', 'https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/gender_deploy.prototxt'))



    for file, url in models:
        filepath = directory + '/' + file
        if not check_if_exist(filepath):
            download_file(url, filepath)

    print('Models download completed.')

def create_directory(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        a=1



def check_if_exist(filepath):

    return os.path.isfile(filepath)


def download_file(url, filepath):
    print('Downloading ', filepath)
    r = requests.get(url)
    open(filepath, 'wb').write(r.content)


download_models()
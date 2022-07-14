from django.conf import settings
from .utilities import CROPS_DATA_F, Min_THRESH
from fastai.vision import open_image
from fastai.basic_train import load_learner
import os


def irrigation(sector, moisture):
    enracinement = CROPS_DATA_F[sector.crop]["enracinement"] 
    type_soil = sector.farm.soil_type
            
    thresh = Min_THRESH[enracinement][type_soil]["min"]
    print(thresh)

    if (moisture >= 0.95):
        action = "stop"
    elif (moisture <= thresh):
        action = "start"
    else:
        action = "nothing"
    return action


def disease_image_detection():
    img = open_image(os.path.join(os.getcwd(), 'alternaria-tomato.jpg'))
    learn = load_learner(os.getcwd(), file='leaf_diseases_model.pkl')
    print(str(learn.predict(img)[0]))



def temperature_ext():
    pass


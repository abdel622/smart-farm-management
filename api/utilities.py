from pyexpat import model
import random
import string

from urllib3 import Retry
from . import models
import math


import requests
import json

# def algo(x):
#     return (math.atan2(x[0] - mlat, x[1] - mlng) + 2 * math.pi) % (2*math.pi)



def get_agromonitoring_data(obj, polygon_name):
    res = obj.split(" ")
    res = [x.split(",") for x in res]
    res = [[float(x[1]), float(x[0])] for x in res]

    res = order_coordinates(res)

    res = get_polygon_data(res, polygon_name)

    return res



def get_polygon_data(coor, name):
    url = "http://api.agromonitoring.com/agro/1.0/polygons?appid=4f2159a79886fb4a974fcb8b98542309"

    payload = json.dumps({
        "name": name,
        "geo_json": {
            "type": "Feature",
            "properties": {},
            "geometry": {
            "type": "Polygon",
            "coordinates": [
            coor
            ]
            }
        }
        })
    headers = {
        'Content-Type': 'application/json'
        }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.text

def order_coordinates(coor):
    mlat = sum(x[0] for x in coor) / len(coor)
    mlng = sum(x[1] for x in coor) / len(coor)

    # points.sort(key=lambda x: math.atan2(x[1] - 0, x[0] - 0))

    coor.sort(key=lambda x:(math.atan2(x[0] - mlat, x[1] - mlng) + 2 * math.pi) % (2*math.pi))
    coor.append(coor[0])
    coor.reverse()

    return coor


def key_generator():
    key = ''.join(random.choice(string.digits+string.ascii_lowercase) for x in range(6))
    # if models.Gateway.objects.filter(key_identifier=key).exists() or models.Node.objects.filter(key_identifier=key).exists():
    if models.Device.objects.filter(key_identifier=key).exists():
        key = key_generator()
    return key







def get_crop(value):
    values = {
        'TM':'Tomate',
        'PT':'Pomme de terre',
        'OI':'Oignon',
        'PM':'Pommier'
    }

    return values[value]

CROPS_DATA_F = {
    "Menthe":{
        "enracinement":"peu-profond"
    },
    "Oignon":{
        "enracinement":"peu-profond"
    },
    "Ail":{
        "enracinement":"peu-profond"
    },
    "Chou":{
        "enracinement":"peu-profond"
    },
    "Fraisier":{
        "enracinement":"peu-profond"
    },
    "Pomme de terre":{
        "enracinement":"peu-profond"
    },
    "Haricot":{
        "enracinement":"peu-profond"
    },
    "Melon":{
        "enracinement":"moyen-profond"
    },
    "Navet":{
        "enracinement":"moyen-profond"
    },
    "Poivron":{
        "enracinement":"moyen-profond"
    },
    "Pois":{
        "enracinement":"moyen-profond"
    },
    "Betterave":{
        "enracinement":"moyen-profond"
    },
    "Carotte":{
        "enracinement":"moyen-profond"
    },
    "Pastèque":{
        "enracinement":"moyen-profond"
    },
    "Patate Douce":{
        "enracinement":"moyen-profond"
    },
    "Tomate":{
        "enracinement":"moyen-profond"
    },
    "Citrouille":{
        "enracinement":"moyen-profond"
    },
    "Mais":{
        "enracinement":"moyen-profond"
    },
    "Colza":{
        "enracinement":"moyen-profond"
    },
    "Céréales":{
        "enracinement":"moyen-profond"
    },
    "Abricotier":{
        "enracinement":"profond"
    },
    "Pêcher":{
        "enracinement":"profond"
    },
    "Avocatier":{
        "enracinement":"profond"
    },
    "Olivier":{
        "enracinement":"profond"
    },
    "Pommier":{
        "enracinement":"profond"
    },
    "Amandier":{
        "enracinement":"profond"
    },
}



SOIL_TYPES = {
    "AR":"Argileux",
    "LA":"Limono-Argileux",
    "AL":"Argilo-Limoneux",
    "LM":"Limoneux",
    "SL":"Sablono-Limoneux",
    "SB":"Sabloneux",
}


Min_THRESH = {
    "peu-profond":{
        "AR":{
            "min":0.79,
        },
        "LA":{
            "min":0.78,
        },
        "AL":{
            "min":0.77,
         },
        "LM":{
            "min":0.73,
        },
        "SL":{
            "min":0.68,
        },
        "SB":{
            "min":0.71,
        }
    },
    "moyen-profond":{
        "AR":{
            "min":0.69,
        },
        "LA":{
            "min":0.67,
        },
        "AL":{
            "min":0.65,
         },
        "LM":{
            "min":0.59,
        },
        "SL":{
            "min":0.52,
        },
        "SB":{
            "min":0.56,
        }
    },
    "profond":{
        "AR":{
            "min":0.58,
        },
        "LA":{
            "min":0.56,
        },
        "AL":{
            "min":0.53,
         },
        "LM":{
            "min":0.45,
        },
        "SL":{
            "min":0.36,
        },
        "SB":{
            "min":0.42,
        }
    },

}









SOIL_DATA = {
    "AR":{
        "sensor_value_calibration":328.00,
    },
    "LA":{
        "sensor_value_calibration":350.31,
    },
    "AL":{
        "sensor_value_calibration":371.04,
    },
    "LM":{
        "sensor_value_calibration":395.16,
    },
    "SL":{
        "sensor_value_calibration":425.17,
    },
    "SB":{
        "sensor_value_calibration":438.29,
    }
}

from xmlrpc.client import DateTime
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .utilities import key_generator

user_model = get_user_model()



DEVICE_TYPES =  (
    ("central", "CENTRAL"),
    # ("VANNE", "ARDUINO VANNE"),
    ("field", "FIELD")
)

FERTILISATION_MODE = (
    ("FT", "Fertilization"),
    ("FG", "Fertigation"),
)

PRODUCTION_UNITS = (
    ("KG", "Kilogrammes"),
    ("TN", "Tonnes"),
    ("QN", "Quintals")
)

# Data For Choice Fields
MOROCCO_REGIONS = (
    ("TT", "Tanger-Tétouan-Al Hoceima"),
    ("OR", "L'Oriental"),
    ("FM", "Fès-Meknès"), 
    ("BM", "Beni Mellal-Khénifra"),
    ("RS", "Rabat-Salé-Kénitra"),
    ("CS", "Casablanca-Settat"), 
    ("MS", "Marrakech-Safi"), 
    ("DF", "Drâa-Tafilalet"),
    ("SM", "Souss-Massa"), 
    ("GO", "Guelmim-Oued Noun"), 
    ("LS", "Laâyoune-Sakia El Hamra"), 
    ("DO", "Dakhla-Oued Ed Dahab")
)

SOIL_TYPES = (
    ("AR", "Argileux"),
    ("LA", "Limono-Argileux"),
    ("AL", "Argilo-Limoneux"),
    ("LM", "Limoneux"),
    ("SL", "Sablono-Limoneux"),
    ("SB", "Sabloneux"),
)

FOR_PRELEVEMENTS = (
    ('SS', 'Semences'),
    ('PL', 'Plants'),
    ('EC', 'Engrais Chimique'),
    ('EO', 'Engrais Organique'),
    ('PS', 'Pesticide-Acaricide'),
    ('HB', 'Herbicide'),
    ('FG', 'Fongicide')
)

MV_TYPES = (
    ('SS', 'Semences'),
    ('PL', 'Plants'),
)

FERTILIZER_TYPES = (
    ('EC', 'Engrais Chimique'),
    ('EO', 'Engrais Organique'),
)

PHYTO_TYPES = (
    ('PS', 'Pesticide-Acaricide'),
    ('HB', 'Herbicide'),
    ('FG', 'Fongicide')
)

CROPS = (
    ('TM', 'Tomate'),
    ('PT', 'Pomme de terre'),
    ('OI', 'Oignon'),
    ('PM', 'Pommier')
)

NODE_TYPES = (
    ("S", "Sender"),
    ("R", "Receiver")
)

SENSOR_TYPES = (
    ("AT", "Temperature/Air"),
    ("AH", "Humidite/Air"),
    ("SM", "Humidite/Sol"),
    # ("SP", "Ph/Sol"),
    # ("SN", "NPK/Sol"),
    ("HF", "Humidite Foliaire")



)

# App Models
class Profile(models.Model):
    user = models.OneToOneField(user_model, on_delete=models.CASCADE, related_name='profile')
    city = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=2, choices=MOROCCO_REGIONS, null=True)
    postal_code = models.CharField(max_length=10, null=True)
    profile_photo = models.ImageField(upload_to ='uploads/', null=True)
    telephone = models.CharField(max_length=20, null=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username


class Stock(models.Model):
    # name = models.CharField(max_length=100)
    farm = models.OneToOneField('Farm', related_name='stock', on_delete=models.CASCADE)
    


    def __str__(self):
        return f'Stock - {self.farm.name}'

# class Input(models.Model):
#     # name = models.CharField(max_length=100)
#     # type = models.CharField(max_length=2, choices=INPUT_TYPES)
#     stock = models.ForeignKey('Stock', related_name='inputs', on_delete=models.CASCADE)
#     product = models.ForeignKey('Fertilizer', related_name='input', on_delete=models.CASCADE)
#     quantity = models.FloatField() 

#     def __str__(self):
#         return f'Input {self.id} / Stock {self.stock.id}'


class Fertilizer(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=FERTILIZER_TYPES)
    formula = models.CharField(max_length=200, null=True, blank=True)
    unit = models.CharField(max_length=10)
    price_unit = models.FloatField()
    stock = models.ForeignKey('Stock', related_name='fertilizers', on_delete=models.CASCADE)
    quantity = models.FloatField()
    
    # quantity = models.FloatField() 

    def __str__(self):
        return f'Fertilizer {self.id} - {self.name}'
    

class ProductPhyto(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=PHYTO_TYPES)
    unit = models.CharField(max_length=10)
    price_unit = models.FloatField()
    stock = models.ForeignKey('Stock', related_name='phyto_products', on_delete=models.CASCADE)
    quantity = models.FloatField()
    # quantity = models.FloatField() 

    def __str__(self):
        return f'Product Phyto {self.id} - {self.name}'

class MaterielVegetal(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=MV_TYPES)
    unit = models.CharField(max_length=10)
    price_unit = models.FloatField()
    stock = models.ForeignKey('Stock', related_name='mv_products', on_delete=models.CASCADE)
    quantity = models.FloatField()
    # quantity = models.FloatField() 

    def __str__(self):
        return f'Materiel Vegetal {self.id} - {self.name}'

class Phytosanitary_Treatement(models.Model):
    location = models.ForeignKey("Sector", on_delete=models.CASCADE, related_name='phytosanitary_treatements')
    date = models.DateTimeField() 
    product = models.ForeignKey("ProductPhyto", related_name="phytosanitary_treatements",on_delete=models.CASCADE)
    quantity = models.FloatField()
    cost = models.FloatField(null=True)

    def __str__(self):
        return f'Phytosanitary_Treatement {self.id} - Sector {self.location.id} / Farm {self.location.farm.id }'

class Fertilizing(models.Model):
    location = models.ForeignKey("Sector", on_delete=models.CASCADE, related_name='fertilizing_operations')
    date = models.DateTimeField() 
    product = models.ForeignKey("Fertilizer", related_name="fertilizing_operations",on_delete=models.CASCADE)
    quantity = models.FloatField()
    mode_apport = models.CharField(max_length=2, null=True, choices=FERTILISATION_MODE)
    cost = models.FloatField(null=True)


    def __str__(self):
        return f'Fertilizing Operations {self.id} - Sector {self.location.id} / Farm {self.location.farm.id }'



class SoilLabor(models.Model):
    date = models.DateTimeField()
    location = models.ForeignKey("Sector", on_delete=models.CASCADE, related_name='soil_labors')
    cost = models.FloatField(null=True)

    def __str__(self):
        return f'Soil Labor {self.id} - Sector {self.location.id} / Farm {self.location.farm.id}'

class Sowing(models.Model):
    date = models.DateTimeField()
    location = models.ForeignKey("Sector", on_delete=models.CASCADE, related_name='sowings')
    crop = models.CharField(max_length=2, choices=CROPS)
    product = models.ForeignKey("MaterielVegetal", related_name="sowing_operations",on_delete=models.CASCADE)
    quantity = models.FloatField()
    cost = models.FloatField(null=True)

    def __str__(self):
        return f'Sowing Operations {self.id} / Crop {self.crop} - Sector {self.location.id} / Farm {self.location.farm.id}' 


class Desherbage(models.Model):
    location = models.ForeignKey("Sector", on_delete=models.CASCADE, related_name='desherbage_operations')
    date = models.DateTimeField() 
    product = models.ForeignKey("ProductPhyto", related_name="desherbage_operations",on_delete=models.CASCADE, null=True)
    quantity = models.FloatField()
    type = models.CharField(max_length=10)
    cost = models.FloatField(null=True)


    def __str__(self):
        return f'Desherbage Operations {self.id} - Sector {self.location.id} / Farm {self.location.farm.id }'

class Irrigation(models.Model):
    location = models.ForeignKey("Sector", on_delete=models.CASCADE, related_name='irrigations')
    date = models.DateTimeField() 
    # product = models.ForeignKey("Input", related_name="desherbage_operations",on_delete=models.CASCADE, null=True)
    quantity = models.FloatField()
    # type = models.CharField(max_length=10)
    cost_unit = models.FloatField(null=True)
    pluvio_fic = models.FloatField(null=True)
    duree = models.FloatField(null=True)


    def __str__(self):
        return f'Irrigation {self.id} - Sector {self.location.id} / Farm {self.location.farm.id }'


class Harvesting(models.Model):
    date = models.DateTimeField()
    location = models.ForeignKey("Sector", on_delete=models.CASCADE, related_name='harvestings')
    cost = models.FloatField(null=True)
    production = models.FloatField()
    production_unit = models.CharField(max_length=2, null=True, choices=PRODUCTION_UNITS)


    def __str__(self):
        return f'Haversting {self.id} - Sector {self.location.id} / Farm {self.location.farm.id}'


class Gateway(models.Model):
    farm = models.ForeignKey("farm", related_name="gateways", on_delete=models.CASCADE)    
    key_identifier = models.CharField(max_length=6)

    def __str__(self):
        return f'Gateway {self.id} - Farm {self.farm.id}'


class Node(models.Model):
    status = models.BooleanField(default=False)
    location = models.ForeignKey('Sector', on_delete=models.CASCADE, related_name='nodes')
    gateway = models.ForeignKey("Gateway", related_name='connected_nodes', on_delete=models.CASCADE)
    # type = models.CharField(max_length=2, choices=NODE_TYPES)
    key_identifier = models.CharField(max_length=6)

    
    def __str__(self):
        return f'Node {self.id} - Sector {self.location.id}'


class Sensor(models.Model):
    type = models.CharField(max_length=2, choices=SENSOR_TYPES)
    node = models.ForeignKey("Node", related_name='sensors', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.type} - Sector {self.node.location.id}'


class AirTemperatureSensorReadings(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='air_temperatures')
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f'{self.id} - Air Temperature - Sector {self.sensor.node.location.id} - {self.created_at}'


class AirHumiditySensorReadings(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='air_humidities')
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f'{self.id} - Air Humidity - Sector {self.sensor.node.location.id} - {self.created_at}'

class SoilMoistureSensorReadings(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='soil_moistures')
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f'{self.id} - Soil Moisture - Sector {self.sensor.node.location.id} - {self.created_at}'

class LeafWetnessSensorReadings(models.Model):
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='leaf_wetnesses')
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f'{self.id} - Leaf Wetness - Sector {self.sensor.node.location.id} - {self.created_at}'

# class SoilPhSensorReadings(models.Model):
#     sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='soil_phs')
#     created_at = models.DateTimeField(auto_now_add=True)
#     value = models.FloatField()

#     def __str__(self):
#         return f'{self.id} - Soil Ph - Sector {self.sensor.location.id} - {self.created_at}'

# class SoilNPKSensorReadings(models.Model):
#     sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name='soil_npks')
#     created_at = models.DateTimeField(auto_now_add=True)
#     value = models.CharField(max_length=150)

#     def __str__(self):
#         return f'{self.id} - Soil NPK - Sector {self.sensor.location.id} - {self.created_at}'


class Notification(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    title = models.CharField(max_length=200)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='notifications')
    readed = models.BooleanField(default=False)

    def __str__(self):
        return f'Notificaton-{self.id}-{self.profile.user.username}'
    
class Farm(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='farms')
    area = models.FloatField()
    soil_texture = models.CharField(max_length=2, choices=SOIL_TYPES)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)



    @classmethod
    def sectors_area(self, model_obj, sector_id=None):
        if sector_id:
            value = Sector.objects.get(id=sector_id).area
        else:
            value = 0
        return sum([y.area for y in model_obj.sectors.all() ]) - value

        

    def __str__(self):
        return f'{self.id}-{self.name}'

class Sector(models.Model):
    name = models.CharField(max_length=100)
    farm = models.ForeignKey('Farm', on_delete=models.CASCADE, related_name='sectors')
    area = models.FloatField()
    crop = models.CharField(max_length=2, choices=CROPS, null=True)
    irrigation_cost_unit = models.FloatField(null=True)
    pluvio_fic = models.FloatField(null=True)
    is_connected = models.BooleanField(default=False)
    is_irrigation_automatic = models.BooleanField(default=False)
    coordinates = models.CharField(max_length=1000, null=True)
    last_irrigation = models.DateTimeField(null=True)
    is_irrigation_started = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}-{self.farm.name}-{self.name}'


class Staff(models.Model):
    name = models.CharField(max_length=100)
    cin = models.CharField(max_length=50)
    age = models.IntegerField()
    position = models.CharField(max_length=100)
    farm = models.ForeignKey('Farm', on_delete=models.SET_NULL, related_name='staff', null=True)


    def __str__(self):
        return f'{self.id}-{self.name}-{self.cin}'


class Prelevements(models.Model):
    for_operation = models.CharField(max_length=2, choices=FOR_PRELEVEMENTS, null=True)
    stock =models.ForeignKey('Stock', related_name='prelevements', on_delete=models.CASCADE)
    date = models.DateTimeField()
    input_name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.id}-{self.input_name}-{self.date}'


class Device(models.Model):
    key_identifier = models.CharField(max_length=6, default=key_generator, unique=True, editable=False)
    type = models.CharField(max_length=20, choices=DEVICE_TYPES, default="field")

    def __str__(self):
        return f'{self.id}-{self.key_identifier}'
    


class Cost(models.Model):
    sector = models.ForeignKey('Sector', related_name='costs', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    montant = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return f'Cost {self.id}-Sector {self.sector.id}'

def save_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        # profile.save()

post_save.connect(save_profile, sender=user_model)


def save_stock(sender, instance, created, **kwargs):
    if created:
        # Stock.objects.create(farm=instance, name=f'Stock Farm {instance.id}')
        Stock.objects.create(farm=instance)
        # profile.save()

post_save.connect(save_stock, sender=Farm)

def save_prelevement(sender, instance, created, **kwargs):
    if created:
        type_operation = ""
        if type(instance)==Sowing:
            type_operation = f'Semis-Plantation Secteur-{instance.location.id}'
        elif type(instance)==Fertilizing:
            type_operation = f'Fertilisation Secteur-{instance.location.id}'
        elif type(instance)==Phytosanitary_Treatement:
            type_operation = f'Traitement Phyto Secteur-{instance.location.id}'

        
        product = instance.product
        if (product.quantity - instance.quantity >= 0):
            Prelevements.objects.create(
            input_name = instance.product.name,
            for_operation = instance.product.type,
            date = instance.date,
            quantity = instance.quantity,
            stock = instance.location.farm.stock,
            unit=instance.product.unit
            )
            Cost.objects.create(
                sector=instance.location,
                montant=float(instance.quantity)*float(product.price_unit) + float(instance.cost),
                description=type_operation
            )
            product.quantity = product.quantity - instance.quantity
            product.save() 
        else:
            print("Error")
            
        # profile.save()

post_save.connect(save_prelevement, sender=Phytosanitary_Treatement)
post_save.connect(save_prelevement, sender=Fertilizing)
post_save.connect(save_prelevement, sender=Sowing)


def edit_crop(sender, instance, created, **kwargs):
    if created:
        sector = instance.location
        sector.crop = instance.crop
        sector.save()

post_save.connect(edit_crop, sender=Sowing)



def save_cost(sender, instance, created, **kwargs):
    if created:
        Cost.objects.create(
                sector=instance.location,
                montant=float(instance.cost),
                description=f''   
            )


post_save.connect(save_cost, sender=SoilLabor)
post_save.connect(save_cost, sender=Harvesting)


def save_cost_irrigation(sender, instance, created, **kwargs):
    if created:
        Cost.objects.create(
                sector=instance.location,
                montant=float(instance.cost_unit)*float(instance.quantity)*10*float(instance.location.area),
                description=f''   
            )


post_save.connect(save_cost_irrigation, sender=Irrigation)

def save_sensors(sender, instance, created, **kwargs):
    if created:
        for item in SENSOR_TYPES:
            Sensor.objects.create(
                node=instance,
                type=item[0]
            )
        # profile.save()

post_save.connect(save_sensors, sender=Node)


# def update_inut(sender, instance, created, **kwargs):
#     if created:
#         for item in SENSOR_TYPES:
#             Sensor.objects.create(
#                 node=instance,
#                 type=item[0]
#             )
#         # profile.save()

# post_save.connect(update_inut, sender=Prelevements)


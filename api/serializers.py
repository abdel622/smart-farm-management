from statistics import mode
from wsgiref import validate
from rest_framework import serializers 
from django.db.models import Q

from . import models
from . import utilities


# INPUT_SOWING_CHOICES = [(v.id, v.name) for v in models.Input.objects.filter(Q(type="PL") | Q(type="SS"))]
# print(INPUT_SOWING_CHOICES)





class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ('id', 'user', 'city', 'region', 'is_completed', 'postal_code', 'profile_photo', 'telephone')




class FarmSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.Farm
        fields = ('id', 'name', 'area','soil_texture', 'lat', 'lng')


    #Specify the owner of the farm created
    def create(self, validated_data):
        user_profile = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user_profile = models.Profile.objects.get(user=request.user) 
        
        return models.Farm.objects.create(
            name=validated_data['name'],
            area = validated_data['area'],
            soil_texture=validated_data['soil_texture'],
            lat = validated_data['lat'],
            lng = validated_data['lng'],
            owner=user_profile                                                 # The owner
        )



class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sector
        fields = ('id', 'name', 'farm', 'area', 'crop', 'coordinates', 'is_connected', 'is_irrigation_automatic', 'is_irrigation_started')
    
    
    def validate(self, data):
        farm_object = data['farm']
        
        request = self.context.get("request")

        if request.method == "POST":
            sum_areas = farm_object.sectors_area(farm_object) + data['area']

            if (sum_areas > farm_object.area ):
                raise serializers.ValidationError("Area Limit Exceeded !")

        if request.method == "PATCH":
            print(data)
            print(request.data)
            sum_areas = farm_object.sectors_area(farm_object, request.data['id']) + data['area']

            if (sum_areas > farm_object.area ):
                raise serializers.ValidationError("Area Limit Exceeded !")
            
            # try:
            # print(request.data['coordinates'])
            # print(getattr(request.data, 'coordinates', None))
            # print(getattr(request.data, 'coordinates', None)!=None)

            try:
                if request.data['is_irrigation_automatic']:
                    if models.Sector.objects.get(id=request.data['id']).pluvio_fic==None or models.Sector.objects.get(id=request.data['id']).irrigation_cost_unit==None: 
                        raise serializers.ValidationError("Vous devez spécifier la pluviométrie fictive et le coûts unitaire de l'irrigation")
            except:
                pass

            if  request.data['coordinates']:
                print(request.data['id'])
                if models.Sector.objects.get(id=request.data['id']).coordinates:
                    pass
                else:
                    res = utilities.get_agromonitoring_data(request.data['coordinates'], f'farm-{farm_object.id}-sector-{request.data["id"]}' )                
                    

                    if res==500:
                        raise serializers.ValidationError("Error !")
                    else:
                        center = ''
                        for coor in res['center']:
                            center += f'{coor} '
                        center = center.strip()
                        data['coordinates'] = f'{res["id"]} {center}'
                        # sector = models.Sector.objects.get(id=request.data['id'])
                        # sector.polygon = res['id']

                        # sector.center = center.strip()
                        # sector.save()
                    # print(type(res))
                    # print(res['id'])
                    # print(res['center'])
                    




                    # print("Result: ", request.data['coordinates']) 
            # except:
                # raise serializers.ValidationError("Error !")
        
        return data

    # def create(self, validated_data):
    #     request = self.context.get("request")
    #     if request and hasattr(request, "user"):
    #         user_profile = models.Profile.objects.get(user=request.user) 
        
    #     return models.Farm.objects.create(
    #         name=validated_data['name'],
    #         area = validated_data['area'],
    #         soil_texture=validated_data['soil_texture'],
    #         lat = validated_data['lat'],
    #         lng = validated_data['lng'],
    #         owner=user_profile                                                 # The owner
    #     )


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = ('id', 'name', 'farm', )

class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fertilizer
        fields = ('id', 'name', 'type', 'stock', 'quantity', 'formula', 'price_unit', 'unit',)

class ProductPhytoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductPhyto
        fields = ('id', 'name', 'type', 'stock', 'quantity', 'price_unit', 'unit',)


class MaterielVegetalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaterielVegetal
        fields = ('id', 'name', 'type', 'stock', 'quantity', 'price_unit', 'unit',)

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Staff
        fields = ('id', 'name', 'cin', 'age', 'position', 'farm')

class PhytosanitaryTreatementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phytosanitary_Treatement
        fields = ('id', 'location', 'date', 'product', 'quantity',)

class FertilizingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fertilizing
        fields = ('id', 'location', 'date', 'product', 'quantity',)

class SowingSerializer(serializers.ModelSerializer):
    
    # product = serializers.ChoiceField(choices=[])
    take_from_stock = serializers.BooleanField(default=False)
    
    class Meta:

        model = models.Sowing
        fields = ['id', 'location', 'crop', 'date', 'product', 'quantity', 'take_from_stock']
        # 'product', 'quantity', 'take_from_stock'
    

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     choice =[]
    #     qs = models.Input.objects.filter(Q(type="PL") | Q(type="SS"))
    #     for item in qs:
    #         choice.append((item.id, item.name))
    #     self.fields['product'].choices = choice

    # INPUT_SOWING_CHOICES = [(v.id, v.name) for v in models.Input.objects.filter(Q(type="PL") | Q(type="SS"))]

    
    def create(self, validated_data):
        print(validated_data)
        if validated_data['take_from_stock']:
            obj = validated_data['product']
            if ((obj.quantity - validated_data['quantity']) >= 0):
                print("Diff", (obj.quantity - validated_data['quantity']))
                obj.quantity = obj.quantity - validated_data['quantity']
                models.Sowing.objects.create(
                    location=validated_data['location'],
                    crop=validated_data['crop'],
                    date=validated_data['date'],
                    product=models.Input.objects.get(id=validated_data['product'].id),
                    quantity= validated_data['quantity']
                )
                obj.save()
        return validated_data


    # def create(self, validated_data):
    #     print("HI")
    #     print(self.fields['product'])
    #     print(validated_data)

        
    # #     # return validated_data
    #     models.Sowing.objects.create(
    #         location=validated_data['location'],
    #         crop=validated_data['crop'],
    #         date=validated_data['date'],
    #         product=models.Input.objects.get(id=self.validated_data['product']),
    #         quantity= validated_data['quantity']
    #     )

    #     return validated_data


        


class HarvestingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Harvesting
        fields = ('id', 'location', 'date', 'quantity',)


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gateway
        fields = ('id', 'farm', 'key_identifier')
        read_only_fields = ['key_identifier']
    

    def create(self, validated_data):
        return models.Gateway.objects.create(
            farm=validated_data['farm'],
            key_identifier = utilities.key_generator()
        )
        


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Node
        fields = ('id', 'type', 'location', 'gateway', 'status', 'key_identifier')
        read_only_fields = ['key_identifier']
    
    def create(self, validated_data):
        return models.Node.objects.create(
            type=validated_data['type'],
            location = validated_data['location'],
            gateway = validated_data['gateway'],
            status = validated_data['status'],
            key_identifier = utilities.key_generator()
        )


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sensor
        fields = ('id', 'node', 'type')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ('id', 'profile', 'date', 'readed', 'content', 'title')
    

class AirTemperatureSensorReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AirTemperatureSensorReadings
        fields = ('id', 'sensor', 'created_at', 'value')



    


class AirHumiditySensorReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AirHumiditySensorReadings
        fields = ('id', 'sensor', 'created_at', 'value')
    
class SoilMoistureSensorReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SoilMoistureSensorReadings
        fields = ('id', 'sensor', 'created_at', 'value')
    
    # def create(self, validated_data):
    #     print("hello")
    #     return models.SoilMoistureSensorReadings.objects.create(
    #         value=validated_data['value'],
    #         sensor = validated_data['sensor']
    #     )
    
 
    
# class SoilPhSensorReadingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.SoilPhSensorReadings
#         fields = ('id', 'sensor', 'created_at', 'value')

# class SoilNPKSensorReadingsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.SoilNPKSensorReadings
#         fields = ('id', 'sensor', 'created_at', 'value')


class LeafWetnessSensorReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LeafWetnessSensorReadings
        fields = ('id', 'sensor', 'created_at', 'value')

    

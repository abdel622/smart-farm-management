from django.db.models import Q
import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from . import serializers
from . import models
from . import services
from django.shortcuts import get_object_or_404
import datetime
import requests
import os
import json
from .utilities import CROPS_DATA_F, Min_THRESH,get_crop
from django.utils.timezone import localdate, localtime

def get_category_info(item):
    if item=='EC' or item=='EO':
        return 'engrais'
    
    if item=='PS' or item=='HB' or item=='FG':
        return 'phyto'
    
    if item=='PL':
        return 'plant'
    
    if item=='SS':
        return 'semence'
    

class isCompletedProfile(APIView):

    def get(self, request):
        profile = request.user.profil
        
        return Response({"profile":profile.id, "status":profile.is_completed}, status=status.HTTP_200_OK)



class DashboardView(APIView):
    """
    Custom
    """

    def get(self, request, format=None):
        """
        Custom
        """
        # usernames = [user.username for user in User.objects.all()]

        len_sectors = sum([len(item.sectors.all()) for item in models.Farm.objects.filter(owner=request.user.profile) ])
        len_farms = len(models.Farm.objects.filter(owner=request.user.profile))
        sectors_data = []

        user = request.user
        farms = user.profile.farms.all()

        for farm in farms:
            for sector in farm.sectors.all():
                try:
                    res = sector.nodes.all()[0].sensors.all()
                    latest_moisture = res.get(type="SM").soil_moistures.all().last().value
                    sm = round(latest_moisture*100, 2)
                except:
                    sm = None

                
                try:
                    res = sector.nodes.all()[0].sensors.all()
                    latest_humidity = res.get(type="AH").air_humidities.all().last().value
                    ah = round(latest_humidity*100, 2)
                except:
                    ah = None


                try:
                    res = sector.nodes.all()[0].sensors.all()
                    latest_temp = res.get(type="AT").air_temperatures.all().last().value
                    at = round(latest_temp,2)
                except:
                    at = None

                sectors_data.append(
                    {
                        "name":sector.name,
                        "farm_name":sector.farm.name,
                        "area":sector.area,
                        "crop":sector.crop,
                        "sm":sm,
                        "ah":ah,
                        "at":at
                    }
                )
        is_completed = request.user.profile.is_completed
        username = request.user.username
        # len_sectors = sum([])
        # print(models.Farm.objects.filter(owner=request.user.profile)[0].get_number_sectors())
        return Response([{'farms':len_farms, 'sectors':len_sectors, 'is_completed':is_completed, 'sectors_data':sectors_data, 'username':username}])


class WeatherView(APIView):

    def get(self, request, format=None):
        
        city = request.user.profile.city
        api_key = os.environ["OPENWEATHER_KEY"]

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}, 504&appid={api_key}&units=metric&lang=fr"

        print(api_key)
        print(url)


        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text)

        # print(type(response.text))
        
        return Response(json.loads(response.text), status=status.HTTP_200_OK)

class StockItems(APIView):
    def get(self, request, stock_id):
        stock = models.Stock.objects.get(id=stock_id)        
        print(stock_id)

        data = {}
        data['fertilizers'] = []
        data['phyto_products'] = []
        data['mv_products'] = []
        for fertilizer in stock.fertilizers.all():
            data['fertilizers'].append({
                "id":fertilizer.id,
                "name":fertilizer.name,
                "type":fertilizer.type,
                "formula":fertilizer.formula,
                "quantity":fertilizer.quantity,
                "price":fertilizer.price_unit,
                "unit":fertilizer.unit,
                "farm":fertilizer.stock.farm.id


            }) 
        for phyto_prodcut in stock.phyto_products.all():
            data['phyto_products'].append({
                "id":phyto_prodcut.id,
                "name":phyto_prodcut.name,
                "type":phyto_prodcut.type,
                "quantity":phyto_prodcut.quantity,
                "price":phyto_prodcut.price_unit,
                "unit":phyto_prodcut.unit,
                "farm":phyto_prodcut.stock.farm.id


            })

        for mv_product in stock.mv_products.all():
            data['mv_products'].append({
                "id":mv_product.id,
                "name":mv_product.name,
                "type":mv_product.type,
                "quantity":mv_product.quantity,
                "price":mv_product.price_unit,
                "unit":mv_product.unit,
                "farm":mv_product.stock.farm.id


            })
        print(data)

        return Response(data, status=status.HTTP_200_OK)


class stockDash(APIView):

    def get(self, request, farm_id):
        farms = request.user.profile.farms

        obj = get_object_or_404(farms, pk=farm_id)

        fertilizers = obj.stock.fertilizers.all()
        products_phyto = obj.stock.phyto_products.all()
        mv = obj.stock.mv_products.all()


        # inputs = obj.stock.inputs.all()

        # categories = list(set(map(lambda x:x.type, inputs)))
# 
        stock_categories = {
            "Fertilisants":0,
            "Phyto":0,
            "Semences":0,
            "Plants":0
        }

        for fertilizer in obj.stock.fertilizers.all():
            stock_categories["Fertilisants"] = stock_categories["Fertilisants"] + fertilizer.quantity

        for phyto_product in obj.stock.phyto_products.all():
            stock_categories["Phyto"] = stock_categories["Phyto"] + phyto_product.quantity
        
        for plant in obj.stock.mv_products.filter(type="PL"):
            stock_categories["Plants"] = stock_categories["Plants"] + plant.quantity

        for semence in obj.stock.mv_products.filter(type="SS"):
            stock_categories["Semences"] = stock_categories["Semences"] + semence.quantity




        # for category in categories:
        #     stock_categories[category] = 0
        
        # for input in inputs:
        #     stock_categories[input.type] = stock_categories[input.type] + input.quantity


        stock_categories = [list(stock_categories.keys()), list(stock_categories.values())]
        print(stock_categories)

        data = {}

        data["stock_len"] = len(fertilizers) + len(products_phyto) + len(mv)
        data["prelevements"] = len(obj.stock.prelevements.all())
        # data["prelevements"] = 0

        data["id"] = obj.stock.id
        data['stock_categories'] = stock_categories

        return Response(data, status=status.HTTP_200_OK)

class stock_history(APIView):

    def get(self, request, farm_id):

        farms = request.user.profile.farms

        obj = get_object_or_404(farms, pk=farm_id)

        data = []

        for item in obj.stock.prelevements.all():
            print(item)
            print(item.input_name)
            print(type(item.date))

            data.append({
                "input_name":item.input_name,
                "date":item.date.strftime("%d/%m/%Y, %H:%M:%S"),
                "quantity":item.quantity,
                "unit":item.unit
            })
        # data["stock_len"] = len(obj.stock.inputs.all())
        # data["prelevements"] = len(obj.stock.prelevements.all())
        # data["id"] = obj.stock.id

        return Response(data, status=status.HTTP_200_OK)

class takeout(APIView):
    """
    Custom
    """

    def post(self, request, farm_id, input_category, input_id):
        data = request.data
        print(data['quantity'])
        user = request.user
        # get_user_model().objects.all()[0].profile.farms.all().get(id=13).stock.inputs.all().get(id=5).quantity


        # obj = user.profile.farms.get(id=farm_id).stock.inputs.get(id=input_id) 



        if (input_category=="EC" or input_category=="EO"):
            obj = get_object_or_404(user.profile.farms.get(id=farm_id).stock.fertilizers.all(), pk=input_id)

        elif (input_category=="PS" or input_category=="HB" or input_category=="FG"):
            obj = get_object_or_404(user.profile.farms.get(id=farm_id).stock.phyto_products.all(), pk=input_id)

        elif (input_category=="SS" or input_category=="PL"):
            obj = get_object_or_404(user.profile.farms.get(id=farm_id).stock.mv_products.all(), pk=input_id)

        if not data['quantity']:
            return Response({"message":"out of range"}, status = status.HTTP_400_BAD_REQUEST)
        
        if (obj.quantity - float(data['quantity']) >= 0):
            value =  obj.quantity - data['quantity']
            obj.quantity = value
            obj.save()

            new_prelevement = models.Prelevements.objects.create(
                stock=user.profile.farms.get(id=farm_id).stock,
                quantity=data['quantity'],
                input_name = obj.name,
                for_operation = obj.type,
                date = datetime.datetime.now()
            )

            return Response({"message":"updated", "value":value}, status = status.HTTP_200_OK)
        else:
            return Response({"message":"out of range"}, status = status.HTTP_400_BAD_REQUEST)





        # serializer = serializers.StudentSerializer(data=request.data)
        # if serializer.is_valid():
            # serializer.save()
            # return Response(serializer.data, status = status.HTTP_201_CREATED)
        # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    # queryset = models.Profile.objects.all()

    def get_queryset(self):
        return models.Profile.objects.filter(user=self.request.user)



class FarmsViewSet(viewsets.ModelViewSet):
    
    """
    A viewset for viewing and editing farm instances.
    """

    serializer_class = serializers.FarmSerialzer

    def get_queryset(self):
        return models.Farm.objects.filter(owner=self.request.user.profile)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     # services.disease_image_detection()

    def retrieve(self, request, pk=None):
        queryset = models.Farm.objects.filter(owner=self.request.user.profile)
        farm = get_object_or_404(queryset, pk=pk)
        serializer = serializers.FarmSerialzer(farm)
        res = serializer.data

        res['sectors'] = len(farm.sectors.all())
        res['stock_items'] = len(farm.stock.fertilizers.all())+len(farm.stock.phyto_products.all())+len(farm.stock.mv_products.all())
        return Response(res)



class SectorViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing sector instances.
    """

    serializer_class = serializers.SectorSerializer

    def get_queryset(self):
        farm = models.Farm.objects.get(id=self.kwargs['farm_id'])
        print(farm)
        sectors = models.Sector.objects.filter(farm=farm)
        return sectors


    # def retrieve(self, request, farm_id, pk=None):
    #     queryset = models.Sector.objects.all()
    #     sector = get_object_or_404(queryset, pk=pk)
    #     serializer = serializers.SectorSerializer(sector)
    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     sector_object = self.get_object()
    #     sector_object.delete()
    #     return Response(status=status.HTTP_204_NO_                                                            NTENT)


class StockViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing stock instances.
    """

    serializer_class = serializers.StockSerializer
    # queryset = models.Stock.objects.all()

    def get_queryset(self):
        farm = models.Farm.objects.get(id=self.kwargs['farm_id'])
        print(farm)
        stocks = models.Stock.objects.filter(farm=farm)
        return stocks



class FertilizerViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing input instances.
    """

    serializer_class = serializers.FertilizerSerializer
    # queryset = models.Input.objects.all()

    def get_queryset(self):
        stock = models.Stock.objects.get(id=self.kwargs['stock_id'])
        fertilizers = models.Fertilizer.objects.filter(stock=stock)
        return fertilizers


class ProductPhytoViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing input instances.
    """

    serializer_class = serializers.ProductPhytoSerializer
    # queryset = models.Input.objects.all()

    def get_queryset(self):
        stock = models.Stock.objects.get(id=self.kwargs['stock_id'])
        objects = models.ProductPhyto.objects.filter(stock=stock)
        return objects

class MaterielVegetalViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing input instances.
    """

    serializer_class = serializers.MaterielVegetalSerializer
    # queryset = models.Input.objects.all()

    def get_queryset(self):
        stock = models.Stock.objects.get(id=self.kwargs['stock_id'])
        objects = models.MaterielVegetal.objects.filter(stock=stock)
        return objects


class StaffViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing staff instances.
    """

    serializer_class = serializers.StaffSerializer
    # queryset = models.Staff.objects.all()

    def get_queryset(self):
        farm = models.Farm.objects.get(id=self.kwargs['farm_id'])
        staff = models.Staff.objects.filter(farm=farm)
        return staff


class SowingViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing sowing instances.
    """

    serializer_class = serializers.SowingSerializer
    # queryset = models.Staff.objects.filter(Q(type="PL") | Q(type="SS"))
    # queryset = models.Sowing.objects.all()

    def get_queryset(self):
        sector = models.Sector.objects.get(id=self.kwargs['sector_id'])
        sowings = models.Sowing.objects.filter(location=sector)
        return sector


class HarvestingViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing harvesting instances.
    """

    serializer_class = serializers.HarvestingSerializer
    # queryset = models.Staff.objects.filter(Q(type="PL") | Q(type="SS"))
    # queryset = models.Harvesting.objects.all()

    def get_queryset(self):
        sector = models.Sector.objects.get(id=self.kwargs['sector_id'])
        harvestings = models.Harvesting.objects.filter(location=sector)
        return harvestings
        

    
class PhytosanitaryTreatementsViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing phytosanitary-treatements instances.
    """

    serializer_class = serializers.PhytosanitaryTreatementsSerializer
    # queryset = models.Staff.objects.filter(Q(type="PL") | Q(type="SS"))
    # queryset = models.Phytosanitary_Treatement.objects.all()

    def get_queryset(self):
        sector = models.Sector.objects.get(id=self.kwargs['sector_id'])
        phyto_treats = models.Phytosanitary_Treatement.objects.filter(location=sector)
        return phyto_treats


class FertilizingViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing fertilizing instances.
    """

    serializer_class = serializers.FertilizingSerializer
    # queryset = models.Staff.objects.filter(Q(type="PL") | Q(type="SS"))
    # queryset = models.Fertilizing.objects.all()


    def get_queryset(self):
        sector = models.Sector.objects.get(id=self.kwargs['sector_id'])
        fertilizing = models.Fertilizing.objects.filter(location=sector)
        return fertilizing



class GatewayViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing gateway instances.
    """

    serializer_class = serializers.GatewaySerializer
    # queryset = models.Staff.objects.filter(Q(type="PL") | Q(type="SS"))
    # queryset = models.Gateway.objects.all()

    def get_queryset(self):
        farm = models.Farm.objects.get(id=self.kwargs['farm_id'])
        gateways = models.Gateway.objects.filter(farm=farm)
        return gateways


class NodeViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing node instances.
    """

    serializer_class = serializers.NodeSerializer
    # queryset = models.Staff.objects.filter(Q(type="PL") | Q(type="SS"))
    # queryset = models.Node.objects.all()

    def get_queryset(self):
        gateway = models.Gateway.objects.get(id=self.kwargs['gateway_id'])
        nodes = models.Node.objects.filter(gateway=gateway)
        return nodes


class SensorViewSet(viewsets.ModelViewSet):

    """
    A viewset for viewing and editing sensor instances.
    """

    serializer_class = serializers.SensorSerializer
    # queryset = models.Staff.objects.filter(Q(type="PL") | Q(type="SS"))
    # queryset = models.Sensor.objects.all()
    def get_queryset(self):
        node = models.Node.objects.get(id=self.kwargs['node_id'])
        sensors = models.Sensor.objects.filter(node=node)
        return sensors

class NotificationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing notification instances.
    """

    serializer_class = serializers.NotificationSerializer
    # queryset = models.Staff.objects.filter(Q(type="PL") | Q(type="SS"))
    # queryset = models.Notification.objects.all()

    def get_queryset(self):
        profile = self.request.user.profile
        notifications = models.Notification.objects.filter(profile=profile)
        return notifications


class AirTemperatureSensorReadingsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Air Temperature instances.
    """

    serializer_class = serializers.AirTemperatureSensorReadingsSerializer
    # queryset = models.AirTemperatureSensorReadings.objects.all()

    def get_queryset(self):
        sensor = models.Sensor.objects.get(id=self.kwargs['sensor_id'])
        values = models.AirTemperatureSensorReadings.objects.filter(sensor=sensor)
        return values

    


class AirHumiditySensorReadingsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Air Humidity instances.
    """

    serializer_class = serializers.AirHumiditySensorReadingsSerializer
    # queryset = models.AirHumiditySensorReadings.objects.all()

    def get_queryset(self):
        sensor = models.Sensor.objects.get(id=self.kwargs['sensor_id'])
        values = models.AirHumiditySensorReadings.objects.filter(sensor=sensor)
        return values

class SoilMoistureSensorReadingsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Soil Moisture instances.
    """

    serializer_class = serializers.SoilMoistureSensorReadingsSerializer
    # queryset = models.SoilMoistureSensorReadings.objects.all()

    def get_queryset(self):
        sensor = models.Sensor.objects.get(id=self.kwargs['sensor_id'])
        values = models.SoilMoistureSensorReadings.objects.filter(sensor=sensor)
        return values
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.SoilMoistureSensorReadingsSerializer(data=request.data)
        if serializer.is_valid():
            soil_moisture = serializer.save()
            data = serializer.data

            moist = data.get('value')

            sector = models.Sensor.objects.get(id=serializer.data.get('sensor')).node.location
            farm = models.Sensor.objects.get(id=serializer.data.get('sensor')).node.location.farm

            enracinement = CROPS_DATA_F[get_crop(sector.crop)]["enracinement"] 
            type_soil = farm.soil_texture
            
            thresh = Min_THRESH[enracinement][type_soil]["min"]
            print(thresh)

            if (moist >= 0.95):
                res = data
                res['irrigation_status'] = "stop"
                sector.is_irrigation_started = False
                sector.save()
                print(sector.last_irrigation)
                date_difference = localtime() - sector.last_irrigation
                print(date_difference)
                models.Irrigation.objects.create(
                    location=sector,
                    date=sector.last_irrigation,
                    cost_unit=sector.irrigation_cost_unit,
                    duree=(date_difference.seconds/3600),
                    pluvio_fic=sector.pluvio_fic,
                    quantity=(date_difference.seconds/3600)*sector.pluvio_fic,
                )
                return Response(res, status=status.HTTP_201_CREATED)
            elif (moist <= thresh):
                res = data
                res['irrigation_status'] = "start"
                sector.is_irrigation_started = True
                sector.last_irrigation = datetime.datetime.now()
                sector.save()
                return Response(res, status=status.HTTP_201_CREATED)
            else:
                res = data
                res['irrigation_status'] = "irrigating"
                return Response(res, status=status.HTTP_201_CREATED)

            # return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


# class SoilPhSensorReadingsViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing Soil Ph instances.
#     """

#     serializer_class = serializers.SoilPhSensorReadingsSerializer
#     # queryset = models.SoilPhSensorReadings.objects.all()

#     def get_queryset(self):
#         sensor = models.Sensor.objects.get(id=self.kwargs['sensor_id'])
#         values = models.SoilPhSensorReadings.objects.filter(sensor=sensor)
#         return values


# class SoilNPKSensorReadingsViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing Soil NPK instances.
#     """

#     serializer_class = serializers.SoilNPKSensorReadingsSerializer
#     # queryset = models.SoilNPKSensorReadings.objects.all()

#     def get_queryset(self):
#         sensor = models.Sensor.objects.get(id=self.kwargs['sensor_id'])
#         values = models.SoilNPKSensorReadings.objects.filter(sensor=sensor)
#         return values


class LeafWetnessSensorReadingsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Leaf Wetness instances.
    """

    serializer_class = serializers.LeafWetnessSensorReadingsSerializer
    # queryset = models.LeafWetnessSensorReadings.objects.all()

    def get_queryset(self):
        sensor = models.Sensor.objects.get(id=self.kwargs['sensor_id'])
        values = models.LeafWetnessSensorReadings.objects.filter(sensor=sensor)
        return values




class LinkUnlinkDeviceView(APIView):

    def post(self, request):
        action = request.data["action"]
        sector_id = request.data["sector_id"]
        farm_id = request.data["farm_id"]

        sector = models.Sector.objects.get(pk=sector_id)
        farm = models.Farm.objects.get(pk=farm_id)

        if action=="link":
            node_id = request.data["node_id"]
            gateway_id = request.data["gateway_id"]

            get_object_or_404(models.Device, key_identifier=gateway_id, type="central")
            get_object_or_404(models.Device, key_identifier=node_id, type="field")

            if models.Node.objects.filter(key_identifier=node_id).exists():
                return Response({
                "detail":"failed",
                "message":"already exists"
            },
            status=status.HTTP_400_BAD_REQUEST
            )

            try:
                gateway = models.Gateway.objects.get(key_identifier=gateway_id)
            except models.Gateway.DoesNotExist:
                gateway = models.Gateway.objects.create(
                farm=farm,
                key_identifier = gateway_id
            )

            models.Node.objects.create(
                key_identifier=node_id,
                location = sector,
                gateway=gateway
            )

            sector.is_connected = True
            sector.save()

            return Response({
                "detail":"success",
                "data":{
                    "gateway_id":gateway_id,
                    "node_id":node_id
                }
            },
            status=status.HTTP_200_OK
            )
        
        if action=="unlink":
            node_id = request.data["node_id"]
            gateway_id = request.data["gateway_id"]

            # arduino_id = request.data["arduino_id"]
            # sector = models.Sector.objects.get(pk=sector_id)

            obj = get_object_or_404(models.Node, key_identifier=node_id)

            # arduino_obj = models.Arduino.objects.get(
            #     arduino_id=arduino_id,
            #     sector = sector
            # )
            obj.delete()

            sector.is_connected = False
            sector.save()

            return Response({
                "detail":"success"
            },
            status=status.HTTP_200_OK
            )
        else:
            return Response({
                "detail":"error"
            },
            status=status.HTTP_400_BAD_REQUEST)

class SectorDetailsData(APIView):
    def get(self, request, farm_id, sector_id):
        print(farm_id)
        print(sector_id)

        sector = models.Sector.objects.get(pk=sector_id)
        farm = models.Farm.objects.get(pk=farm_id)
        stock = models.Farm.objects.get(pk=farm_id).stock.id

        data = {}

        sensor_data = {}
            
            # print(values)
            

        if sector.nodes.all().exists():
            data['exists'] = sector.nodes.all().exists()
            data['node_id'] = sector.nodes.all()[0].key_identifier
            data['gateway_id'] = sector.nodes.all()[0].gateway.key_identifier

            for sensor in sector.nodes.all()[0].sensors.all():
                if sensor.type=="AT":
                    values = [(i.created_at.strftime("%H:%M"), i.value) for i in sensor.air_temperatures.all()]
                    sensor_data["AT"] = values
                elif sensor.type=="AH":
                    values = [(i.created_at.strftime("%H:%M"), i.value) for i in sensor.air_humidities.all()]
                    sensor_data["AH"] = values
                elif sensor.type=="SM":
                    values = [(i.created_at.strftime("%H:%M"), i.value) for i in sensor.soil_moistures.all()]
                    sensor_data["SM"] = values
                elif sensor.type=="HF":
                    values = [(i.created_at.strftime("%H:%M"), i.value) for i in sensor.leaf_wetnesses.all()]
                    sensor_data["HF"] = values

            data['sensors_values'] = sensor_data
            
        else:
            sensor_data["AT"] = []
            sensor_data["AH"] = []
            sensor_data["SM"] = []
            sensor_data["HF"] = []

            data['sensors_values'] = sensor_data


        data['stock'] = stock

        sum_costs = round(sum([x.montant for x in sector.costs.all()]), 2)
        sum_water = round(sum([x.quantity for x in sector.irrigations.all()]), 2)

        data['costs'] = sum_costs
        data['water'] = sum_water



        return Response({'detail':'Success', 'data':data}, status=status.HTTP_200_OK)


class CreateOperation(APIView):
    def post(self, request, farm_id, sector_id):
        print(farm_id, sector_id)
        print(request.data)

        sector = get_object_or_404(models.Sector.objects.all(), pk=request.data['location'])
        if request.data['type']=='soil-labor':
            models.SoilLabor.objects.create(
                date=request.data['date'],
                location=sector,
                cost=request.data['cost']
            )
        elif request.data['type']=='phyto-treatements':
            print("PHYTO")
            models.Phytosanitary_Treatement.objects.create(
                date=request.data['date'],
                location=sector,
                cost=request.data['cost'],
                product=models.ProductPhyto.objects.get(id=request.data['product']),
                quantity=request.data['quantity']
            )
        elif request.data['type']=='sowing':
            models.Sowing.objects.create(
                date=request.data['date'],
                location=sector,
                cost=request.data['cost'],
                product=models.MaterielVegetal.objects.get(id=request.data['product']),
                quantity=request.data['quantity'],
                crop=request.data['crop']
            )
        elif request.data['type']=='fertilization':
            models.Fertilizing.objects.create(
                date=request.data['date'],
                location=sector,
                cost=request.data['cost'],
                product=models.Fertilizer.objects.get(id=request.data['product']),
                quantity=request.data['quantity'],
                mode_apport=request.data['mode_apport']
            )
        elif request.data['type']=='irrigation':
            models.Irrigation.objects.create(
                date=request.data['date'],
                location=sector,
                cost_unit=request.data['cost_unit'],
                quantity=request.data['duree']*request.data['pluvio_fic'],
                duree=request.data['duree'],
                pluvio_fic=request.data['pluvio_fic'],
            )
        elif request.data['type']=='harvesting':
            models.Harvesting.objects.create(
                date=request.data['date'],
                location=sector,
                cost=request.data['cost'],
                production=request.data['production'],
                production_unit=request.data['production_unit'],
            )

        return Response("Success", status=status.HTTP_200_OK)


class IrrigationOptions(APIView):

    def get(self, request, farm_id, sector_id):
        farm = get_object_or_404(models.Farm.objects.all(), pk=farm_id)
        sector = get_object_or_404(farm.sectors.all(), pk=sector_id)

        data = {}

        data['pluvioFic'] = sector.pluvio_fic
        data['costUnit'] = sector.irrigation_cost_unit

        return Response({'data':data}, status=status.HTTP_200_OK)



    def post(self, request, farm_id, sector_id):
        farm = get_object_or_404(models.Farm.objects.all(), pk=farm_id)
        sector = get_object_or_404(farm.sectors.all(), pk=sector_id)

        sector.pluvio_fic = request.data['pluvioFic']
        sector.irrigation_cost_unit = request.data['costUnit']
        sector.save()

        return Response({'data':"success"}, status=status.HTTP_200_OK)


class cost_history(APIView):
    def get(self, request, sector_id):
        sector = get_object_or_404(models.Sector.objects.all(), pk=sector_id)

        data = []

        # data['costs'] = sector.costs

        for item in sector.costs.all():
            data.append(
                {
                "date":item.date.strftime("%d/%m/%Y, %H:%M:%S"),
                "montant":round(item.montant, 2),
                "description":item.description
                }
            )

        return Response({'data': data}, status=status.HTTP_200_OK)


class SatelliteData(APIView):


    def post(self, request, sector_id):
        sector = get_object_or_404(models.Sector.objects.all(), id=sector_id)


        if request.data['type'] == "mv":
            models.VegetationSatellite.objects.create(
                date=datetime.datetime.fromtimestamp(request.data['date_ndvi']),
                ndvi=request.data['ndvi'],
                sector=sector
            )

            models.MeteoSatellite.objects.create(
                date=datetime.datetime.fromtimestamp(request.data['date_meteo']),
                temp=request.data['temp'],
                sector=sector,
                humidity=request.data['humidity'],
                pression=request.data['pression'],
                wind_speed=request.data['wind_speed'],
                wind_direction=request.data['wind_direction'],
                uvi=request.data['uvi']
            )
        else:
            models.SolSatellite.objects.create(
                date=datetime.datetime.fromtimestamp(request.data['date_meteo']),
                surface_temp=request.data['surface_temp'],
                temp_10cm=request.data['temp_10cm'],
                humidity_sol=request.data['humidity_sol'],
                sector=sector
            )
        
        return Response({'data':"success"}, status=status.HTTP_200_OK)
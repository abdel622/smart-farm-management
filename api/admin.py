from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.Notification)

admin.site.register(models.Farm)
admin.site.register(models.Stock)
# admin.site.register(models.Input)
admin.site.register(models.Fertilizer)
admin.site.register(models.MaterielVegetal)
admin.site.register(models.ProductPhyto)
admin.site.register(models.Staff)



admin.site.register(models.Sector)
admin.site.register(models.SoilLabor)
admin.site.register(models.Sowing)
admin.site.register(models.Fertilizing)
admin.site.register(models.Phytosanitary_Treatement)
# admin.site.register(models.Desherbage)
admin.site.register(models.Irrigation)
admin.site.register(models.Harvesting)


admin.site.register(models.Gateway)
admin.site.register(models.Node)
admin.site.register(models.Sensor)
admin.site.register(models.SoilMoistureSensorReadings)
# admin.site.register(models.LeafWetnessSensorReadings)
admin.site.register(models.AirTemperatureSensorReadings)
admin.site.register(models.AirHumiditySensorReadings)
# admin.site.register(models.SoilPhSensorReadings)
# admin.site.register(models.SoilNPKSensorReadings)

admin.site.register(models.VegetationSatellite)
admin.site.register(models.SolSatellite)
admin.site.register(models.MeteoSatellite)


admin.site.register(models.Device)

admin.site.register(models.Prelevements)

admin.site.register(models.Cost)


















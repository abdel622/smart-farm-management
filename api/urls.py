from email.mime import base
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register(r'profiles', views.ProfileViewSet, basename='profiles'),
router.register(r'farms', views.FarmsViewSet, basename='farms')
router.register(r'sectors/(?P<farm_id>[0-9]+)', views.SectorViewSet, basename='sectors')
router.register(r'stocks/(?P<farm_id>[0-9]+)', views.StockViewSet, basename='stocks')
# router.register(r'inputs/(?P<stock_id>[0-9]+)', views.InputViewSet, basename='inputs')
router.register(r'fertilizers/(?P<stock_id>[0-9]+)', views.FertilizerViewSet, basename='fertilizers')
router.register(r'products-phyto/(?P<stock_id>[0-9]+)', views.ProductPhytoViewSet, basename='product-phyto')
router.register(r'materiel-vegetal/(?P<stock_id>[0-9]+)', views.MaterielVegetalViewSet, basename='material-vegetal')

router.register(r'staff/(?P<farm_id>[0-9]+)', views.StaffViewSet, basename='staff')
router.register(r'sowings/(?P<sector_id>[0-9]+)', views.SowingViewSet, basename='sowings')
router.register(r'harvestings/(?P<sector_id>[0-9]+)', views.HarvestingViewSet, basename='harvestings')
router.register(r'phytosanitary-treatements/(?P<sector_id>[0-9]+)', views.PhytosanitaryTreatementsViewSet, basename='phytosanitary-treatements')
router.register(r'fertilizing/(?P<sector_id>[0-9]+)', views.FertilizingViewSet, basename='fertilizing')
router.register(r'gateways/(?P<farm_id>[0-9]+)', views.GatewayViewSet, basename='gateways')
router.register(r'nodes/(?P<gateway_id>[0-9]+)', views.NodeViewSet, basename='nodes')
router.register(r'sensors/(?P<node_id>[0-9]+)', views.SensorViewSet, basename='sensors')
router.register(r'notifications', views.NotificationViewSet, basename='notifications')
# Sensor Readings
router.register(r'air_temperature/(?P<sensor>[0-9]+)', views.AirTemperatureSensorReadingsViewSet, basename='air_temperatures')
router.register(r'air_humidity/(?P<sensor>[0-9]+)', views.AirHumiditySensorReadingsViewSet, basename='air_humidities')
router.register(r'soil_moisture/(?P<sensor>[0-9]+)', views.SoilMoistureSensorReadingsViewSet, basename='soil_moistures')
# router.register(r'soil_ph/(?P<sensor>[0-9]+)', views.SoilPhSensorReadingsViewSet, basename='soil_phs')
# router.register(r'soil_npk/(?P<sensor>[0-9]+)', views.SoilNPKSensorReadingsViewSet, basename='soil_npks')
# router.register(r'leaf_wetness/(?P<sensor>[0-9]+)', views.LeafWetnessSensorReadingsViewSet, basename='leaf_wetnesses')










urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard-view'),
    path('takeout/<int:farm_id>/<slug:input_category>/<int:input_id>/', views.takeout.as_view(), name='takeout-view'),
    path('stock-items/<int:stock_id>/', views.StockItems.as_view(), name='stock-items'),
    path('stock-dash/<int:farm_id>/', views.stockDash.as_view(), name='stock-dash'),
    path('stock-history/<int:farm_id>/', views.stock_history.as_view(), name='stock-history'),
    path('weather/', views.WeatherView.as_view(), name='weather'),
    path('link-unlink/', views.LinkUnlinkDeviceView.as_view(), name='link-unlink'),
    path('farm/<int:farm_id>/<int:sector_id>/sector-data/', views.SectorDetailsData.as_view(), name='sector-data'),
    path('create-operation/<int:farm_id>/<int:sector_id>/', views.CreateOperation.as_view(), name='create-operation'),
    path('irrigation-options/<int:farm_id>/<int:sector_id>/', views.IrrigationOptions.as_view(), name='irrigation-options'),
    path('cost-history/<int:sector_id>/', views.cost_history.as_view(), name='cost-history'),
    path('satellite-data/<int:sector_id>/', views.SatelliteData.as_view(), name='satellite-data'),
    path('add_coordinates/<int:sector_id>/', views.add_coordinates.as_view(), name='add-coordinates'),







]

urlpatterns += router.urls

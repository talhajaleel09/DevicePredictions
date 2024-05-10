from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.retrieve_devices, name='retrieve_devices'),
    path('devices/<int:device_id>/', views.fetch_device, name='fetch_device'),
    path('devices/add/', views.add_device, name='add_device'),
    path('devices/bulk_add/', views.bulk_add_device, name='bulk_add_device'),
    path('devices/predict/<int:device_id>/', views.predict_by_id, name='predict_by_id'),
]
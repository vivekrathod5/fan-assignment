from django.urls import path
from .views import fan_simulator, consumption_interface, consumption_data

urlpatterns = [
    path('simulator/', fan_simulator, name='fan_simulator'),
    path('consumption/', consumption_interface, name='consumption_interface'),
    path('fan/consumption/', consumption_data, name='consumption_data'),
]

from django.urls import path
from .views import caddy_config_view # importamos la funcion creada en views

urlpatterns = [
    path('api/config', caddy_config_view), # le damos una ruta a la funcion
]
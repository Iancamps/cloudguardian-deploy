from django.urls import path
from .views import (
    caddy_config_view, Register, login, logout, UserDelete, AddIPs, DeleteIPs, AddRoutes, DeleteRoutes, listarUsers 
)
# importamos las funciones y clases creadas en views

from rest_framework.authtoken.views import obtain_auth_token  # importamos la vista que Django proporciona para obtener tokens

urlpatterns = [
    path('register/', Register.as_view(), name = 'register'), # endpoint para registros
    path('login/', login, name = 'login'), # endpoint para logins
    path('login/logout/', logout, name = 'logout'), # endpoint para cerrar sesion eliminando el token
    path('api/config/', caddy_config_view, name = 'configuration'), # le damos una ruta a la funcion == http://localhost:8000/api/config
    path('user-delete/', UserDelete.as_view(), name = 'user-delete'), # endpoint para eliminar usuarios
    path('ips-bloqueadas/add/', AddIPs.as_view(), name = 'ips-added'), # endpoint para añadir ips permitidas y bloqueadas
    path('ips-bloqueadas/delete/', DeleteIPs.as_view(), name = 'ips-deleted'), # endpoint para eliminar ips permitidas y bloqueadas
    path('rutas-protegidas/add/', AddRoutes.as_view(), name = 'routes-added'), # endpoint para añadir rutas protegidas
    path('rutas-protegidas/delete/', DeleteRoutes.as_view(), name = 'routes-deleted'), # endpoint para eliminar rutas protegidas
    path('lista/', listarUsers.as_view()) # endpoint para listar
    
]
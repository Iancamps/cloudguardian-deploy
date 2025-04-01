from django.urls import path
from .views import caddy_config_view, RegisterUserView, login_view, logout_view # importamos la funcion creada en views
from rest_framework.authtoken.views import obtain_auth_token  # importamos la vista que Django proporciona para obtener tokens

urlpatterns = [
    path('register/', RegisterUserView.as_view()), # endpoint para registros
    path('token/', obtain_auth_token, name='api_token_auth'), # creamos el endpoint para obtener el token
    path('login/', login_view, name='login'), # endpoint para logins
    path('login/logout/', logout_view, name='logout'), # cerrar sesion eliminando el token
    path('api/config', caddy_config_view), # le damos una ruta a la funcion == http://localhost:8000/api/config
]
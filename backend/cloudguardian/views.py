import requests
from rest_framework.decorators import api_view # convierte la función de vista en una vista basada en función de Django REST Framework
from rest_framework.decorators import permission_classes # se usa para definir las reglas de permisos para una vista
from rest_framework.permissions import IsAuthenticatedOrReadOnly # la vista solo permite escrituras (PUT) a los usuarios autenticados, pero permite lecturas (GET) a los usuarios no autenticados.
from rest_framework.authentication import TokenAuthentication # esto es para usar la autenticacion por token
from rest_framework.permissions import IsAuthenticated # esto es para darle solo los permisos a los autenticados
from django.contrib.auth import authenticate # verifica si el username y password son correctos
from rest_framework.authtoken.models import Token # almacena los tokens de autenticación de los usuarios
from rest_framework.response import Response # encapsula la respuesta que se enviará al cliente, siguiendo el formato adecuado (JSON).
from rest_framework import status # contiene códigos de estado HTTP estándar
import json # para poder manejar archivos .json
import os # para interactuar con el sistema operativo
from rest_framework import request
from .serializers import UserRegisterSerializer
from rest_framework.views import APIView #  clase base para crear vistas de drf

# Ruta absoluta al archivo caddy_config.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "..", "deploy", "caddy.json") # Eso construye la ruta relativa correcta al caddy.json aunque estés dentro del contenedor o en local

# ESTA ES LA CLASE PARA REGISTRAR USUARIOS

class RegisterUserView(APIView): # Creamos la vista que hereda de APIView, lo que significa que esta vista manejará peticiones HTTP como POST
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data) # creamos una instancia de UserRegisterSerializer y le pasamos los datos que vienen en la petición (request.data)
        if serializer.is_valid(): # Verificamos si los datos enviados son válidos, es decir, si cumplen con las reglas del serializador
            serializer.save() # Llamamos a serializer.save(), que a su vez ejecutará el método create que definimos en el serializador, creando un usuario en la base de datos.
            return Response({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED) # Si va bien, respondemos con un mensaje JSON y el código 201
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Si los datos no son válidos, devolvemos los errores y un código 400 Bad Request
    
# ESTA ES LA CLASE PARA PROTEGER A LOS USUARIOS

class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication] # Si un usuario intenta acceder sin un token válido, obtendrá un error 401 Unauthorized
    permission_classes = [IsAuthenticated] # Solo si esta autenticado puede acceder

    def get(self, request): # definimos el metodo get para cuando intenten acceder a esta vista
        return Response({"message": "Tienes acceso a esta vista protegida"}) # si el token es correcto accederan a dicha vista



# DEFINICION DE LA VISTA

@api_view(['POST']) # Define la función login_view, que solo acepta peticiones POST.
# Esta es la funcion para el POST
def login_view(request):
    username = request.data.get("username") # obtenemos el username del cuerpo de la request
    password = request.data.get("password") # obtenemos la password del cuerpo de la request

    user = authenticate(username=username, password=password) # verificamos que las credenciales son correctas

    if user: # si el usuario existe
        token, created = Token.objects.get_or_create(user=user) # si el usuario no tiene token en la bbdd crea uno para el 
        return Response({"token": token.key}, status=status.HTTP_200_OK) # devuelve el token y el codigo de estado 200
    
    return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_400_BAD_REQUEST) # si hay algun error devuelve un mensaje y un error 400

# Define la funcion para cerrar sesion de usuario eliminando el token

@api_view(['POST']) # Solo permite peticiones POST
def logout_view(request):
    try:
        # Obtener el token desde los headers de autorización.
        token = request.headers.get('Authorization')

        if not token:
            return Response({'error': 'No se proporcionó token en la solicitud'}, status=status.HTTP_400_BAD_REQUEST)

        # CORRECTO: quitar "Token " del principio
        token = token.replace("Token ", "").replace('"', '').strip()
        
        # Buscar el token en la base de datos.
        user_token = Token.objects.get(key=token)

        # Borrar el token del usuario, efectivamente haciendo logout.
        user_token.delete()

        return Response({'message': 'Logout exitoso, token eliminado.'}, status=status.HTTP_200_OK)

    except Token.DoesNotExist:
        return Response({'error': 'Token no válido o ya expirado.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT']) # configuramos la vista para manejar los métodos HTTP GET y PUT

@permission_classes([IsAuthenticatedOrReadOnly]) # solo los autenticados pueden modificar, los demas solo lectura

def caddy_config_view(request): # definimos la funcion que va a leer o modificar el .json
    JSON_PATH = '/etc/caddy/caddy.json'  # Ruta dentro del contenedo
    
    # Esta es la funcon para el GET
    if request.method == 'GET': # en caso de que la peticion sea GET intenta abrir el archivo en solo lectura
        try: 
            with open(JSON_PATH, 'r', encoding='utf-8') as f: # abrimos el archivo en modo lectura y le ponemos el alias f
                data = json.load(f)  # cargamos los datos del archivo en la variable data
            return Response(data) # devuelve los datos obtenidos con el load
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) # si no consigue leerlo devuelve un error 500

    # Esta es la funcion para el PUT
    elif request.method == 'PUT': # si la peticion es PUT intenta actualizar el archivo .json con la informacion enviada
        try:
            new_config = request.data # guardamos la configuracion recibida en la peticion en una variable

            if not isinstance(new_config, dict): # comprobamos que los datos que nos han mandado son en formato diccionario
                return Response({'error': 'El JSON enviado no es válido.'}, status=status.HTTP_400_BAD_REQUEST) # en caso de que no sea en formato diccionario devolvemos un error 400

            with open(JSON_PATH, 'w', encoding='utf-8') as f: # si todo ha ido bien abrimos el archivo en modo escritura y le pones un alias(f)
                json.dump(new_config, f, indent=4) # actualizamos el archivo con los datos del json recibido y lo indentamos para una mejor visual


            #  Intentamos recargar Caddy automáticamente 
            try:
                response = requests.post(os.environ.get("CADDY_ADMIN", "http://caddy:2019") + "/load", json=new_config)



                if response.status_code != 200:
                    return Response({'warning': 'Configuración guardada, pero Caddy no se recargó automáticamente.'}, status=status.HTTP_202_ACCEPTED)

            except Exception as reload_error:
                return Response({'warning': f'Guardado, pero error al recargar Caddy: {reload_error}'}, status=status.HTTP_202_ACCEPTED)

            return Response({'message': 'Configuración actualizada y Caddy recargado'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)# en caso de que algo falle en el proceso se devuelve un error 500
from rest_framework.decorators import api_view # convierte la función de vista en una vista basada en función de Django REST Framework
from rest_framework.decorators import permission_classes # se usa para definir las reglas de permisos para una vista
from rest_framework.permissions import IsAuthenticatedOrReadOnly # la vista solo permite escrituras (PUT) a los usuarios autenticados, pero permite lecturas (GET) a los usuarios no autenticados.
from rest_framework.response import Response # encapsula la respuesta que se enviará al cliente, siguiendo el formato adecuado (JSON).
from rest_framework import status # contiene códigos de estado HTTP estándar
import json # para poder manejar archivos .json
import os # para interactuar con el sistema operativo
import requests


# Ruta absoluta al archivo caddy_config.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "..", "deploy", "caddy.json") # Eso construye la ruta relativa correcta al caddy.json aunque estés dentro del contenedor o en local

# DEFINICION DE LA VISTA

@api_view(['GET', 'PUT']) # configuramos la vista para manejar los métodos HTTP GET y PUT

#@permission_classes([IsAuthenticatedOrReadOnly])  # le indicamos los tipos de permisos(anteriormente hemos importado el requerido)

def caddy_config_view(request): # definimos la funcion que va a leer o modificar el .json
    JSON_PATH = '/etc/caddy/caddy.json'  # Ruta dentro del contenedo
    
    if request.method == 'GET': # en caso de que la peticion sea GET intenta abrir el archivo en solo lectura
        try: 
            with open(JSON_PATH, 'r', encoding='utf-8') as f: # abrimos el archivo en modo lectura y le ponemos el alias f
                data = json.load(f)  # cargamos los datos del archivo en la variable data
            return Response(data) # devuelve los datos obtenidos con el load
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) # si no consigue leerlo devuelve un error 500

    elif request.method == 'PUT': # si la peticion es PUT intenta actualizar el archivo .json con la informacion enviada
        try:
            new_config = request.data # guardamos la configuracion recibida en la peticion en una variable

            if not isinstance(new_config, dict): # comprobamos que los datos que nos han mandado son en formato diccionario
                return Response({'error': 'El JSON enviado no es válido.'}, status=status.HTTP_400_BAD_REQUEST) # en caso de que no sea en formato diccionario devolvemos un error 400

            with open(JSON_PATH, 'w', encoding='utf-8') as f: # si todo ha ido bien abrimos el archivo en modo escritura y le pones un alias(f)
                json.dump(new_config, f, indent=4) # actualizamos el archivo con los datos del json recibido y lo indentamos para una mejor visual


            #  Intentamos recargar Caddy automáticamente 
            try:
                response = requests.post("http://caddy:2019/load", json={
                    "config": new_config,
                    "adapter": "json"
                })
                if response.status_code != 200:
                    return Response({'warning': 'Configuración guardada, pero Caddy no se recargó automáticamente.'}, status=status.HTTP_202_ACCEPTED)

            except Exception as reload_error:
                return Response({'warning': f'Guardado, pero error al recargar Caddy: {reload_error}'}, status=status.HTTP_202_ACCEPTED)

            return Response({'message': 'Configuración actualizada y Caddy recargado'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)# en caso de que algo falle en el proceso se devuelve un error 500
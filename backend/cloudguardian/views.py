import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from rest_framework.decorators import api_view # convierte la función de vista en una vista basada en función de Django REST Framework
from rest_framework.decorators import permission_classes # se usa para definir las reglas de permisos para una vista
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly # la vista permite escrituras (PUT) a los autenticados, pero permite solo lecturas (GET) a los usuarios no autenticados
from rest_framework.authentication import TokenAuthentication # esto es para usar la autenticacion por token
from rest_framework.permissions import IsAuthenticated # esto es para darle solo los permisos a los autenticados
from django.contrib.auth import authenticate # verifica si el username y password son correctos
from rest_framework.authtoken.models import Token # almacena los tokens de autenticación de los usuarios
from rest_framework.response import Response # encapsula la respuesta que se enviará al cliente, siguiendo el formato adecuado (JSON).
from rest_framework import status # contiene códigos de estado HTTP estándar
import json # para poder manejar archivos .json
from rest_framework import request
from .serializers import UserRegisterSerializer
from rest_framework.views import APIView #  clase base para crear vistas de drf
from .models import UserJSON # importamos el modelo para el json se cada usuario


# 🔵🔵🔵 RUTAS NECESARIAS 🔵🔵🔵

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "..", "deploy", "caddy.json") # Eso construye la ruta relativa correcta al caddy.json aunque estés dentro del contenedor o en local

# 🟢🟢🟢 ESTA ES LA CLASE Y FUNCION PARA REGISTRAR USUARIOS 🟢🟢🟢

class Register(APIView): # Creamos la vista que hereda de APIView, lo que significa que esta vista manejará peticiones HTTP como POST
    
    def post(self, request):
        
        username = request.data.get("username") # obtenemos el nombre de usuario
        password = request.data.get("password") # obtenemos la contraseña
        
        serializer = UserRegisterSerializer(data = request.data) # creamos una instancia de UserRegisterSerializer y le pasamos los datos que vienen en la petición (request.data)
        
        if serializer.is_valid(): # Verificamos si los datos enviados son válidos, es decir, si cumplen con las reglas del serializador
            user = serializer.save() # Llamamos a serializer.save(), que a su vez ejecutará el método create que definimos en el serializador, creando un usuario en la base de datos y le pasamos los datos a la variable user
            
            user_json_path = os.path.join(BASE_DIR, f"caddy_{user.username}.json") # creamos la ruta para el JSON de la base de datos

            try:
                
                with open(JSON_PATH, "r", encoding='utf-8') as f:
                    data_base = json.load(f) # cargamos los datos en una variable

                with open(user_json_path, "w", encoding="utf-8") as f: # creamos una copia con la ruta que definimos antes
                    json.dump(data_base, f, indent=4) # dumpeamos los datos del JSON base al JSON del usuario nuevo
                    
                with open(user_json_path, "r+", encoding='utf-8') as f:
                    data = json.load(f) # cargamos el archivo en la variable data
                    
                    users = data["apps"]["http"]["servers"]["Cloud_Guardian"]["routes"][0]["handle"][1]["basic"]["users"] # accedemos a la sección de usuarios del json
                    
                    users[username] = password # añadimos el usuario del json
        
                    # Sobreescribir el archivo JSON con los nuevos datos
                    f.seek(0)  # Ir al inicio del archivo
                    json.dump(data, f, indent = 4) # dumpeamos los datos
                    f.truncate()  # Ajustar el tamaño del archivo

                    UserJSON.objects.create(user = user, json_data = data_base) # guardamos el nuevo JSON en la base de datos

            except:
                return Response({"error": f"Error al crear el archivo JSON"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR) # si pasa algo en el proceso mandamos un msg y un codigo de estado

            return Response({"message": "Usuario registrado y JSON generado"}, status = status.HTTP_201_CREATED) # si todo va bien devolvemos esto
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔴🔴🔴 CLASE Y FUNCION PARA ELIMINAR USUARIOS DE LA BASE DE DATOS 🔴🔴🔴

from django.contrib.auth.models import User # importamos el modelo de usuario

class UserDelete(APIView): # definimos la clase para eliminar usuarios
    
    def post(self, request): # definimos la funcion que recibe la peticion mediante el metodo post
        
        # Elimina un usuario por su nombre de usuario si indican la masterkey necesaria
        username = request.data.get("username") # obtenemos el username de la peticion
        key = request.data.get("masterkey") # obtenemos la masterkey aunque la llamamos key para compararla despues
        masterkey = "delete" # aqui tenemos el valor de la masterkey
        
        if key == masterkey: # si la key es igual a la masterkey dale accesi
            
            try:
                
                user = User.objects.get(username = username) # obtenemos el usuario de la base de datos
                user.delete() # lo borramos de la base de datos
                    
                return Response({"message":f"Usuario: {username} eliminado correctamente"}, status = status.HTTP_202_ACCEPTED) # si todo sale bien
            
            except User.DoesNotExist: 
                return Response({"error":f"El usuario: {username} no existe"}, status = status.HTTP_404_NOT_FOUND) # si no existe devolvemos esto
            
        else:
            Response({"Contraseña maestra incorrecta, no puedes eliminar usuarios"}, status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION) # si fallas con la masterkey te aparecera esto
  
""" LISTA DE USUARIOS PARA TESTEAR COSAS """   
            
class listarUsers(APIView):
    def get(self, request):
        usersList = User.objects.values()
        jsonList = UserJSON.objects.values()
        return Response(f"Lista de usuarios: {usersList}, JSON de los usuarios: {jsonList}")
    
""" LISTA DE USUARIOS PARA TESTEAR COSAS """   
    

# 👋👋👋 FUNCIONES PARA INICIO DE SESION Y CIERRE DE SESION 👋👋👋

@api_view(['POST']) # solo acepta peticiones POST.

def login(request):  # ✅✅✅ Define la función login_view ✅✅✅
    
    username = request.data.get("username") # obtenemos el username del cuerpo de la request
    password = request.data.get("password") # obtenemos la password del cuerpo de la request

    user = authenticate(username = username, password = password) # verificamos que las credenciales son correctas

    if user: # si el usuario existe
        token, created = Token.objects.get_or_create(user = user) # si el usuario no tiene token en la bbdd crea uno para el
        
        try:
            
            user_config = UserJSON.objects.get(user = user) # obtenemos el JSON de la base de datos del user pasado por parametro
            json_data = user_config.json_data  # extraemos los datos JSON guardados
            
        except UserJSON.DoesNotExist:
            return Response({f"No existe un JSON para el usuario: {user}"}, status = status.HTTP_404_NOT_FOUND) # si no existe
            
        return Response({f"token: {token.key} \n caddy_config: {json_data}"}, status = status.HTTP_200_OK) # devuelve el token, el contenido del json y el codigo de estado 200
    
    return Response({"error": "Credenciales incorrectas"}, status = status.HTTP_400_BAD_REQUEST) # si hay algun error devuelve un mensaje y un error 400

@api_view(['POST']) # Solo permite peticiones POST

def logout(request): # ❌❌❌ Define la funcion para cerrar sesion de usuario eliminando el token ❌❌❌
    
    try:
        
        token = request.headers.get('Authorization') # obtener el token desde los headers de autorización.

        if not token:
            return Response({'error': 'No se proporcionó token en la solicitud'}, status = status.HTTP_400_BAD_REQUEST) # si no existe e token lo decimos y mandamos un error 400

        token = token.split(':')[1] # eliminar el prefijo 'Token:' del token que viene en el header.
        token = token.replace('"', '') # reemplazamos las comillas por nada
        token = token.replace(' ', '') # reemplazamos los espacios por nada

        user_token = Token.objects.get(key=token) # buscar el token en la base de datos.

        user_token.delete()  # borrar el token del usuario

        return Response({'message': 'Logout exitoso, token eliminado.'}, status=status.HTTP_200_OK) # si se ha eliminado mandamos un msg y un estado 200

    except Token.DoesNotExist:
        return Response({'error': 'Token no válido o ya expirado.'}, status=status.HTTP_400_BAD_REQUEST) # si se ha pasado un token pero no es valido o ya a expirado


# 🖥️🖥️🖥️ FUNCION PARA LEER O MODIFICAR EL JSON PARA VER O MODIFICAR SU CONFIGURACION 🖥️🖥️🖥️

@api_view(['GET', 'PUT']) # configuramos la vista para manejar los métodos HTTP GET y PUT
@authentication_classes([TokenAuthentication]) # es para autenticar el token automaticamente
@permission_classes([IsAuthenticated]) # solo los autenticados pueden modificar, los demas solo lectura
def caddy_config_view(request): # definimos la funcion que va a leer o modificar el .json
    
    # JSON_PATH = '/etc/caddy/caddy.json'  # Ruta dentro del contenedor
    
    user = request.user  # el usuario es automáticamente autenticado por DRF
        
    try:
        user_config = UserJSON.objects.get(user = user) # obtenemos los datos del JSON del user autenticado de la base de datos y los metemos en el objeto user_config
            
    except user_config.DoesNotExist:
        return Response({"error": "No se encontró configuración para este usuario."}, status=status.HTTP_404_NOT_FOUND) # si no existe devuelve esto

    # 📖 Esta es la funcon para el GET 📖
    if request.method == 'GET':
        return Response(user_config.json_data) # devuelve simplemente los datos de dentro del user_config

    # ✏️ Esta es la funcion para el PUT ✏️
    elif request.method == 'PUT':
        new_config = request.data # metemos la nueva configuracion en una variable, esta nueva configuracion la hemos obtenido de la peticion

        if not isinstance(new_config, dict): # comprobamos que los datos que nos han mandado son en formato diccionario
            return Response({'error': 'El JSON enviado no es válido.'}, status = status.HTTP_400_BAD_REQUEST) # en caso de que no sea en formato diccionario devolvemos un error 400

        user_config.json_data = new_config # le pasamos la nueva configuracion a nuestra configuracion
        user_config.save() # lo guardamos en la base de datos

        return Response({"message": "Configuración actualizada correctamente."}, status=status.HTTP_200_OK) # si todo va bien devolvemos esto

    # 🟡🟡🟡 Intentamos recargar Caddy automáticamente 🟡🟡🟡
    try:
        response = request.post(os.environ.get("CADDY_ADMIN", "http://caddy:2019") + "/load", json=new_config)

        if response.status_code != 200:
            return Response({'warning': 'Configuración guardada, pero Caddy no se recargó automáticamente.'}, status=status.HTTP_202_ACCEPTED)

    except Exception as reload_error:
        return Response({'warning': f'Guardado, pero error al recargar Caddy: {reload_error}'}, status=status.HTTP_202_ACCEPTED)

    return Response({'message': 'Configuración actualizada y Caddy recargado'}, status=status.HTTP_200_OK)
        
# 🪪🪪🪪 CLASES PARA AÑADIR Y ELIMINAR IPS PERMITIDAS Y BLOQUEADAS 🪪🪪🪪
        
class AddIPs(APIView): # ✅ Esta es la clase para añadir ips al json ✅
    
    def post(self, request): # funcion que recibe una peticion mediante el metodo post
        
        new_ips_allow = request.data.get("allow-ips") # obtenemos las ips a permitir de la peticion
        new_ips_deny = request.data.get("deny-ips") # obtenemos las ips a bloquear de la peticion
        
        try: 
            
            with open(JSON_PATH, 'r+', encoding="utf-8") as f: # abrimos nuestro caddy.json
                data = json.load(f) # cargamos todos los datos en una variable data
                
                ips_allow = data["apps"]["http"]["security"]["remote_ip"]["allow"] # lista de ips permitidas
                ips_deny = data["apps"]["http"]["security"]["remote_ip"]["deny"] # lista de ips denegadas
                
                if not new_ips_allow and not new_ips_deny: # si no se añade ninguna ip para permitir ni bloquear devolvemos un mensaje y un codigo de estado 400
                    return Response({"message":"No se ha añadido ninguna IP, vuelva a intentarlo."}, status = status.HTTP_400_BAD_REQUEST)
                
                if new_ips_allow in ips_allow and new_ips_deny in ips_deny: # si las ips ya estan en las listas de nuestro json devolvemos un msg y un codigo de estado 400
                    return Response({"message":"Alguna de las ips añadidas ya existe, porfavor vuelve a revisarlo y añade ips que no esten añadidas"}, status = status.HTTP_400_BAD_REQUEST)
                else:
                    if new_ips_allow:
                        ips_allow.append(new_ips_allow) # añadimos las permitidas si nos han pasado alguna
                    if new_ips_deny:
                        ips_deny.append(new_ips_deny) # añadimos las denegadas si nos han pasado alguna
                    
                    # Sobreescribir el archivo JSON con los nuevos datos
                    f.seek(0)  # Ir al inicio del archivo
                    json.dump(data, f, indent=4) # dumpeamos los datos
                    f.truncate()  # Ajustar el tamaño del archivo
                    
                    return Response({"message": f"IPs permitidas: '{new_ips_allow}' y IPs denegadas '{new_ips_deny}' añadidas correctamente"}, status=status.HTTP_201_CREATED) # si todo sale bien devolvemos esto
        except:
            
            Response({"message":"Ha ocurrido un error al intentar añadir las ips"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR) # si hay algun error en el proceso devolvemos esto

class DeleteIPs(APIView): # ❌ clase para eliminar ips ❌
    
    def post(self, request): # funcion que decibe la peticion del cliente mediante el metodo post
        
        delete_ips_allow = request.data.get("allow-ips") # obtenemos las ips permitidas a eliminar 
        delete_ips_deny = request.data.get("deny-ips") # obtenemos las ips bloqueadas a eliminar
        
        try: 
            
            with open(JSON_PATH, 'r+', encoding="utf-8") as f: # abrimos nuestro json
                data = json.load(f) # cargamos los datos
                
                ips_allow = data["apps"]["http"]["security"]["remote_ip"]["allow"] # lista de ips permitidas
                ips_deny = data["apps"]["http"]["security"]["remote_ip"]["deny"] # lista de ips denegadas
                
                if not delete_ips_allow and not delete_ips_deny: # comprobamos que se haya añadido alguna ip sino devolvemos msg y status
                    return Response({"message":"No se ha añadido ninguna IP, vuelva a intentarlo."}, status = status.HTTP_400_BAD_REQUEST)
                
                if delete_ips_allow in ips_allow or delete_ips_deny in ips_deny: # comprobamos que las ips recibidas en la peticion esten en el caddy.json
                    if delete_ips_allow:
                        ips_allow.remove(delete_ips_allow) # borramos las permitidas si nos las han pasado
                    if delete_ips_deny:
                        ips_deny.remove(delete_ips_deny) # borramos las denegadas si nos las han pasado
                    
                    # Sobreescribir el archivo JSON con los nuevos datos
                    f.seek(0)  # Ir al inicio del archivo
                    json.dump(data, f, indent=4) # dumpeamos los datos
                    f.truncate()  # Ajustar el tamaño del archivo
                    
                    return Response({"message": f"IPs permitidas: '{delete_ips_allow}' y IPs denegadas '{delete_ips_deny}' eliminadas correctamente"}, status=status.HTTP_201_CREATED) # si todo a ido bien devolvemos esto
                
                else: # si alguna de las ips que se pasan no existen en el caddy.json devolvemos este msg y status
                    return Response({"message":"Alguna de las ips añadidas no existe, porfavor vuelve a revisarlo y añade ips que esten añadidas"}, status = status.HTTP_400_BAD_REQUEST)
                
        except:
            
            Response({"message":"Ha ocurrido un error al intentar añadir las ips"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR) # si ocurre otro error en el proceso devolvemos esto
            
# 🛤️🛤️🛤️ CREAMOS CLASE Y FUNCIONES PARA AÑADIR Y ELIMINAR RUTAS PROTEGIDAS 🛤️🛤️🛤️
            
class AddRoutes(APIView): # ✅ clase para añadir rutas protegidas ✅
    
    def post(self, request):
        
        new_path = request.data.get("path")  # ruta que queremos agregar
        users = {user.username: user.password for user in User.objects.all()} # usuarios de la base de datos

        if not new_path:
            return Response({"error": "Añade alguna ruta"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            
            with open(JSON_PATH, "r+", encoding = "utf-8") as f:
                data = json.load(f)

                # Acceder a la lista de rutas en Caddy
                routes = data["apps"]["http"]["servers"]["Cloud_Guardian"]["routes"]

                # Comprobar si la ruta ya existe
                for route in routes:
                    for match in route.get("match", []):
                        if "path" in match and new_path in match["path"]:
                            return Response({"error": f"La ruta '{new_path}' ya existe"}, status=status.HTTP_400_BAD_REQUEST)

                # Crear la nueva ruta protegida
                new_route = {
                    "match": [{"path": [new_path]}],
                    "handle": [
                        {
                            "handler": "rate_limit",
                            "rate_limit": {
                                "requests": 5,  # Máximo de 5 requests por minuto
                                "window": "1m"
                            }
                        },
                        {
                            "handler": "authenticate",
                            "basic": {
                                "users": users
                            }
                        },
                        {
                            "handler": "static_response",
                            "body": f"Acceso permitido a {new_path}"
                        }
                    ]
                }

                # Agregar la nueva ruta al JSON
                routes.append(new_route)

                # Guardar cambios en el archivo JSON
                f.seek(0)
                json.dump(data, f, indent = 4)
                f.truncate()

            return Response({"message": f"Ruta segura '{new_path}' añadida correctamente"}, status=status.HTTP_201_CREATED)
        
        except:
            return Response({"error":"Ha ocurrido algún error en el proceso."}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteRoutes(APIView): # ❌ clase para eliminar rutas protegidas ❌
    
    def post(self, request): # definimos la funcion que recibe la peticion mediante el metodo post
        
        delete_path = request.data.get("path") # recibe el path de la peticion
        
        if not delete_path: # si se ha puesto ningun path se devuleve un msg y status
            return Response({"error":"No has añadido ninguna ruta, porfavor añade una ruta."}, status = status.HTTP_400_BAD_REQUEST)
        
        try:
            
            with open(JSON_PATH, "r+", encoding = "utf-8") as f:
                data = json.load(f)

                routes = data["apps"]["http"]["servers"]["Cloud_Guardian"]["routes"] # Acceder a la lista de rutas en Caddy

                # Ahora vamos a generar una lista de rutas en la cual no vamos a incluis la ruta que hemos pasado en la peticion, es decir que vamos a recorrer todas nuestras rutas y las vamos a ir metiendo en esta lista, en el momento que alguna ruta coincida con la ruta obtenida en la peticion esta no la va a incluir, de modo que estamos creando una lista de rutas con las mismas rutas que tenemos en nuestro caddy.json salvo la ruta que hemos obtenido en la peticion, es decir la ruta que contiene nuestra variable delete_path, una vez hecho esto para comprobar que se ha eliminado comparamos la lista que acabamos de generar con la lista de nuestro caddy.json, si el número de rutas es el mismo quiere decir que no se habrá eliminado ninguna ruta con lo cual la ruta que recibimos de la petición no existe en nuestro caddy.json y por lo tanto devolveremos un error
                new_routes = [route for route in routes if all(delete_path not in match.get("path", []) for match in route.get("match", []))] 

                if len(new_routes) == len(routes):
                    return Response({"error": f"La ruta '{delete_path}' no existe"}, status=status.HTTP_404_NOT_FOUND) # si tenemos las mismas rutas en el las nuevas(con la ruta ya eliminada, que en el otro es porque no existe la ruta)

                data["apps"]["http"]["servers"]["Cloud_Guardian"]["routes"] = new_routes # actualizamos la lista de rutas en el JSON

                # Guardar cambios en el archivo JSON
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

                return Response({"message": f"Ruta '{delete_path}' eliminada correctamente"}, status = status.HTTP_200_OK) # si todo está correcto devolvemos un msg y un status
                        
        except:
            
            return Response({"message": "Ha habido un error en el proceso."}, status = status.HTTP_500_INTERNAL_SERVER_ERROR) # por si ha habido algún error inesperado
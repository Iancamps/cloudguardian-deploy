#  API: Endpoints para el Backend

Este documento define los endpoints necesarios para la comunicación entre el frontend de CloudGuardian y el backend (Django).



##  Comunicación Frontend ↔ Backend

Se define una API que permite leer y actualizar el archivo `caddy_config.json` desde el backend mediante endpoints REST.

El **frontend utiliza Axios** para consumir esta API y mostrar los datos en la interfaz gráfica.

---

# Qué necesita saber el backend


GET	— = Ver config completa =	/api/config	
PUT = Actualizar config 	body JSON =	/api/config	
POST	= Añadir IP bloqueada =	/api/block-ip	= { "ip": "..." }
DELETE = Eliminar IP =	/api/block-ip/:ip		
POST = Añadir ruta protegida = /api/protected-route	=	{ "route": "/login" }
DELETE = Eliminar ruta	= /api/protected-route/:route		
- Control de acceso básico (solo usuarios autenticados pueden modificar)



# Testeos

- Probar con **Insomnia** o **Postman** para enviar GET y PUT.
- Validar que el archivo se actualice correctamente en el servidor.

---

# Notas para el equipo

- El backend debe tener permisos para leer y escribir en `deploy/caddy_config.json`
- Validar que el JSON sea correcto antes de sobrescribirlo

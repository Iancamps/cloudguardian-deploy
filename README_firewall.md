# 🚀 CloudGuardian - Despliegue DevOps

Este repositorio contiene la configuración de despliegue para el proyecto **CloudGuardian**, centrado en crear un sistema de firewall cloud y publicación de datos desde scraping, backend y frontend.

---

## 📁 Estructura del proyecto

cloudguardian-deploy/ 
├── deploy/ # Parte de DevOps 
│ ├── Dockerfile 
│ ├── caddy_config.json
│ └── www/ 
│ └── index.html 
├── backend/ # Backend Django (por añadir) 
├── frontend/ # Frontend React (por añadir) 
└── README.md


---

## 🔐 Parte DevOps (completada)

> Configuración desde cero de un servidor Ubuntu Cloud:

- [x] Acceso mediante SSH con clave pública (`ed25519`)
- [x] Creación de usuario `despliegue`
- [x] Copia de la clave SSH a `despliegue`
- [x] Instalación de Docker
- [x] Ejecución de contenedor Docker con **Caddy** (Hola Mundo)
- [x] Creación de archivo `Dockerfile`
- [x] Creación de archivo `caddy_config.json`
- [x] Creación y subida a rama `produccion` en GitHub

---

## 🌐 Despliegue actual

- Se ha desplegado un contenedor en el puerto `80`  que muestra un "Hola Mundo" desde `/www/index.html`
- Caddy se utiliza como servidor web dentro de Docker

---

## 🚧 Próximos pasos

- [ ] Crear interfaz con Django para editar `caddy_config.json` desde web
- [ ] Añadir el backend completo al directorio `backend/`
- [ ] Añadir frontend (React) al directorio `frontend/`
- [ ] Automatizar despliegue con GitHub Actions o scripts de CI/CD

---

## 👥 Autores

- Ian Camps – DevOps, estructura base y despliegue


---

## 🔗 Repositorio

> URL del proyecto:  
https://github.com/Iancamps/cloudguardian-deploy

> Rama de producción:  
https://github.com/Iancamps/cloudguardian-deploy/tree/produccion

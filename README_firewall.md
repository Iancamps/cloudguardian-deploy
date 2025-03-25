# 🔐 Configuración de Acceso SSH al Servidor Cloud (CloudGuardian)

Este documento explica **paso a paso** cómo configurar la conexión SSH, crear un nuevo usuario para despliegue y dejar un servidor Docker + Caddy corriendo un "Hola Mundo" en producción.

---

## ☁️ Datos del servidor

| IP               | Usuario por defecto | Contraseña |
| ---------------- | ------------------- | ---------- |
| `167.235.155.72` | `admin`             | `1234`     |

---

## 1️⃣ Generar una clave SSH en local (Windows)

Desde **PowerShell** o **Git Bash**:

ssh-keygen -t ed25519 -C "icg0012@alu.medac.es"

Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
obtenere clave publica



# Cloud Firewall - Proyecto Full Stack

## Descripción del proyecto
Cloud Firewall es una aplicación web que simula un sistema básico tipo Cloudflare. Ofrece protección, visualización y control del tráfico web con reglas, estadísticas y monitoreo.

## Funcionalidades principales
- 🔒 Reglas de firewall por IP, país o tipo de tráfico.
- 📊 Estadísticas y logs en tiempo real.
- 🚨 Modo seguro para bloquear tráfico sospechoso.
- 👥 Gestión de usuarios y roles.
- 🖥️ Panel de control responsivo.
- 📈 Integración con herramientas de monitoreo.

## Tecnologías utilizadas
### Frontend
- React.js
- Bootstrap o Tailwind
- Chart.js

### Backend
- Django (REST Framework)
- PostgreSQL
- Celery + Redis

### DevOps
- Docker & Docker Compose
- GitHub Actions
- NGINX + Gunicorn
- Kubernetes (opcional)

## Instalación
1. Clonar el repositorio.
2. Crear entorno virtual y activar.
3. Instalar dependencias.
4. Configurar variables de entorno.
5. Ejecutar `docker-compose up`.

## Uso
- Acceder al panel: `localhost:8000/dashboard`
- Crear reglas, ver tráfico y estadísticas.

## Créditos
Desarrollado por Ian Camps.

## Licencia
MIT License.

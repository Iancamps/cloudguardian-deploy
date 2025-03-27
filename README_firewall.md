# ☁️🛡️ CLOUD GUARDIAN — El escudo que nunca duerme

**CloudGuardian** es una plataforma full stack diseñada para ofrecer control, protección y visibilidad total sobre el tráfico web. Inspirado en soluciones como Cloudflare, permite gestionar reglas de firewall, monitorizar logs y mantener la nube segura 24/7.

---

## 🔐 Configuración de Acceso SSH al Servidor

| IP del servidor  | Usuario por defecto | Contraseña inicial |
| ---------------- | ------------------- | ------------------ |
| `167.235.155.72` | `admin`             | `1234`             |

---

### 1️⃣ Generar clave SSH (en local)

```bash
ssh-keygen -t ed25519 -C "icg0012@alu.medac.es"
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

---

## 🚀 Funcionalidades principales

- 🔒 Reglas de firewall (por IP, país o tipo de tráfico)
- 📄 Visualización de logs en tiempo real
- ⚙️ Panel de configuración dinámico (con edición JSON vía interfaz)
- 🧠 Estado del sistema: CPU, RAM, Disco, Red
- 👤 Gestión de usuarios y autenticación básica
- 📊 Dashboard con métricas y estadísticas
- 🔐 Seguridad: despliegue con Caddy, Docker y claves SSH

---

## 🧪 Tecnologías utilizadas

### 🖥️ Frontend
- React.js (con Vite)
- TailwindCSS (modo oscuro 🔴🖤)
- React Router Dom
- Iconografía Lucide y animaciones Framer Motion

### 🧠 Backend
- Django + Django REST Framework
- PostgreSQL
- Edición de configuración vía panel

### 🔧 DevOps
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Caddy Server como reverse proxy con JSON dinámico
- Usuario `despliegue` O IAN con llave SSH personalizada

---

## 📁 Estructura del proyecto

```
root/
├── frontend/        ← React con Vite, rutas, layouts
├── backend/         ← Django + API REST + seguridad
├── deploy/          ← Dockerfile, Caddy config, entrypoints
└── README.md
```

---

## 🛠️ Instalación local

```bash
git clone https://github.com/iancamps/cloudguardian.git
cd cloudguardian
# Configuración de entorno virtual, backend y frontend aquí...
docker compose up --build
```

Accede a: [http://localhost:8000](http://localhost:8000) o IP en cloud.

---

## 👨‍💻 Desarrollador
**Ian Camps** · Full Stack Dev y Ninja DevOps 🥷

---

## 📄 Licencia
MIT License.


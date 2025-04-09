# ./deploy.ps1

Write-Host "`n🛑 Parando contenedores antiguos..."
docker-compose down -v

Write-Host "`n🧹 Limpiando basura de Docker..."
docker system prune -f

Write-Host "`n🔨 Compilando imágenes sin caché..."
docker-compose build --no-cache

Write-Host "`n🚀 Levantando contenedores..."
docker-compose up -d

Write-Host "`n💻 Compilando frontend..."
cd frontend
npm install
npm run build
cd ..

Write-Host "`n📁 Copiando frontend compilado al contenedor Caddy..."
docker cp ./frontend/dist caddy:/srv

Write-Host "`n🔄 Reiniciando Caddy..."
docker restart caddy

Write-Host "`n✅ ¡Todo listo! Accede a: http://localhost"

# Etapa de build
FROM node:18 AS build

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Etapa final: servir con Nginx
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

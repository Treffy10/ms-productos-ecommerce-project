#!/bin/bash
set -e

# --- 1. Instalación de Docker y Herramientas ---
apt-get update
apt-get install -y git nginx docker.io docker-compose
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

# --- 2. Preparación de la Carpeta de la App ---
mkdir -p /home/ubuntu/app
cd /home/ubuntu/app

# --- 3. Crear el archivo .env dinámicamente ---
# Terraform inyectará estas variables aquí
cat > /home/ubuntu/app/.env <<EOF
DB_NAME=${db_name}
DB_USER=${db_user}
DB_PASSWORD=${db_password}
DB_HOST=db
SECRET_KEY=${django_secret_key}
DOCKER_IMAGE=${docker_image}
EOF

# --- 4. Crear el docker-compose.yml en el servidor ---
cat > /home/ubuntu/app/docker-compose.yml <<EOF
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: \${db_name}
      POSTGRES_USER: \${db_user}
      POSTGRES_PASSWORD: \${db_password}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    image: \${docker_image}
    restart: always
    depends_on:
      - db
    env_file:
      - .env
    ports:
      - "8000:8000"
    command: >
      sh -c "python manage.py migrate --noinput &&
             gunicorn --bind 0.0.0.0:8000 servicio_productos.wsgi:application"

volumes:
  postgres_data:
EOF

# --- 5. Configurar Nginx como Proxy Inverso ---
cat > /etc/nginx/sites-available/django <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

ln -sf /etc/nginx/sites-available/django /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl restart nginx

# --- 6. Lanzar la aplicación ---
# Esto descarga las imágenes de Docker Hub y levanta todo
docker-compose --env-file /home/ubuntu/app/.env up -d
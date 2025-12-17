#!/bin/bash
set -e

echo "🚀 Iniciando provisioning..."

################################
# 1️⃣ ACTUALIZAR SISTEMA
################################
apt-get update -y

################################
# 2️⃣ INSTALAR DOCKER Y GIT
################################
apt-get install -y docker.io git
systemctl start docker
systemctl enable docker

################################
# 3️⃣ INSTALAR POSTGRESQL
################################
apt-get install -y postgresql postgresql-contrib

################################
# 4️⃣ CONFIGURAR POSTGRES
################################
sudo -u postgres psql <<EOF
CREATE DATABASE productos_db_ecommerce;
ALTER USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE productos_db_ecommerce TO postgres;
EOF

################################
# 5️⃣ CONFIGURAR POSTGRES (HOST)
################################
PG_VERSION=$(ls /etc/postgresql)
PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"

sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/" $PG_CONF

echo "host    all             all             172.17.0.0/16          md5" >> $PG_HBA

systemctl restart postgresql

################################
# 6️⃣ CLONAR REPOSITORIO
################################
cd /home/ubuntu
git clone https://github.com/Treffy10/ms-productos-ecommerce-project.git servicio_productos
cd servicio_productos

################################
# 7️⃣ BUILD DE IMAGEN DOCKER
################################
docker build -t ms-productos:v1 .

################################
# 8️⃣ LEVANTAR CONTENEDOR DJANGO
################################
docker run -d \
  --name ms-productos \
  -p 8000:8000 \
  --add-host=host.docker.internal:host-gateway \
  -e DB_NAME=productos_db_ecommerce \
  -e DB_USER=postgres \
  -e DB_PASSWORD=postgres \
  -e DB_HOST=host.docker.internal \
  ms-productos:v1

echo "✅ Provisioning completado"

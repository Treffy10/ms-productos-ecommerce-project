#!/bin/bash
set -e

echo "🚀 Iniciando provisioning..."

################################
# 1️⃣ ACTUALIZAR SISTEMA
################################
apt-get update -y

################################
# 2️⃣ INSTALAR DOCKER
################################
apt-get install -y docker.io git
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

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
# 5️⃣ CONFIGURAR POSTGRES (LOCAL)
################################
PG_CONF="/etc/postgresql/14/main/postgresql.conf"
PG_HBA="/etc/postgresql/14/main/pg_hba.conf"

sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/" $PG_CONF

echo "local   all             all                                     md5" >> $PG_HBA

systemctl restart postgresql

################################
# 6️⃣ CLONAR REPOSITORIO
################################
cd /home/ubuntu
git clone https://github.com/Treffy10/ms-productos-ecommerce-project.git servicio_productos
cd servicio_productos

################################
# 7️⃣ BUILD DE IMAGEN DOCKER (LOCAL)
################################
docker build -t ms-productos .

################################
# 8️⃣ LEVANTAR CONTENEDOR DJANGO
################################
docker run -d \
  --name ms-productos \
  --network host \
  -e DB_NAME=productos_db_ecommerce \
  -e DB_USER=postgres \
  -e DB_PASSWORD=postgres \
  -e DB_HOST=127.0.0.1 \
  ms-productos

echo "✅ Provisioning completado"

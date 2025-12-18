resource "aws_instance" "app_server" {
  ami           = "ami-0c7217cdde317cfec" # Ubuntu 22.04 LTS (Verifica tu región)
  instance_type = "t2.micro"             # La opción gratuita (Free Tier)
  key_name      = "clavesecreta12345"         # El nombre de tu par de llaves en AWS

  # Seguridad: Abrir puertos 22 (SSH) y 80 (HTTP)
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  # INYECCIÓN DE VARIABLES AL SCRIPT
  user_data = templatefile("${path.module}/scripts/user_data.sh", {
    db_name           = var.db_name
    db_user           = var.db_user
    db_password       = var.db_password
    django_secret_key = var.django_secret_key
    docker_image      = var.docker_image
  })

  tags = {
    Name = "ServicioProductos"
  }
}

resource "aws_security_group" "app_sg" {
  name        = "productos-sg"
  description = "Permitir HTTP y SSH"

  # Puerto 80 para que tu App sea visible en la web
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Puerto 22 para que puedas entrar por SSH si es necesario
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Por seguridad, podrías poner solo tu IP aquí
  }

  # Permitir que el servidor salga a internet (para bajar Docker, etc.)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
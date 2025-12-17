terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "mi-bucket-terraform-ecommerce-project"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock"
  }
}


provider "aws" {
  region = "us-east-1"  
}

resource "aws_instance" "ms_productos" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.ms_productos_sg.id]

  user_data = file("user_data.sh")

  tags = {
    Name = "ms-productos"
  }
}
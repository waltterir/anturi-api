resource "aws_db_subnet_group" "anturi_api_db_subnets_group" {
  name       = "anturi-api-db-subnets"
  subnet_ids = data.aws_subnets.default_subnets.ids

  tags = {
    Name = "anturi-api-db-subnets"
  }
}

resource "aws_db_instance" "anturi_api_db_instance" {
  instance_class              = "db.t4g.micro"
  db_name                     = "anturi_api_db"
  identifier                  = "anturi-api-instance"
  engine                      = "postgres"
  engine_version              = "16"
  allocated_storage           = 20
  storage_encrypted           = true
  username                    = "waltterir"
  db_subnet_group_name        = aws_db_subnet_group.anturi_api_db_subnets_group.name
  vpc_security_group_ids      = [aws_security_group.rds.id]
  publicly_accessible         = false
  skip_final_snapshot         = true
  backup_retention_period     = 0
  manage_master_user_password = true
}

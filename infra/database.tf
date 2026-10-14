resource "aws_db_subnet_group" "anturi_api_db_subnets_group" {
  name       = "anturi-api-db-subnets"
  subnet_ids = data.aws_subnets.default_subnets.ids

  tags = {
    Name = "anturi-api-db-subnets"
  }
}
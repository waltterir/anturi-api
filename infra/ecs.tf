resource "aws_ecs_cluster" "anturi_api_cluster" {
  name = "anturi-api-cluster"

  tags = {
    Name = "anturi-api-cluster"
  }
}
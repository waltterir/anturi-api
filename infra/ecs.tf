resource "aws_ecs_cluster" "anturi_api_cluster" {
  name = "anturi-api-cluster"

  tags = {
    Name = "anturi-api-cluster"
  }
}

resource "aws_ecs_task_definition" "anturi_api_task_definition" {
  family                   = "anturi-api-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.anturi_api_role.arn
  container_definitions = jsonencode([{
    name      = "anturi-api-container"
    image     = "${aws_ecr_repository.anturi_api.repository_url}:latest"
    essential = true
    environment = [
      { name = "DB_HOST", value = aws_db_instance.anturi_api_db_instance.address },
      { name = "DB_NAME", value = aws_db_instance.anturi_api_db_instance.db_name },
      { name = "DB_USER", value = aws_db_instance.anturi_api_db_instance.username }
    ]
    secrets = [
      { name = "DB_PASSWORD", valueFrom = "${aws_db_instance.anturi_api_db_instance.master_user_secret[0].secret_arn}:password::" }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.ecs_anturi_api_task.name
        "awslogs-region"        = "eu-north-1"
        "awslogs-stream-prefix" = "ecs"
      }
    }
    portMappings = [
      {
        containerPort = 8000
        hostPort      = 8000
      }
    ]
  }])
}
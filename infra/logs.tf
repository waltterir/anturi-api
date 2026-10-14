resource "aws_cloudwatch_log_group" "ecs_anturi_api_task" {
  name              = "/ecs/anturi-api-task"
  retention_in_days = 3
  tags = {
    Name = "/ecs/anturi-api-task"
  }
}
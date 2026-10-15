# kuka saa käyttää roolia? = ecs taskit
resource "aws_iam_role" "anturi_api_role" {
  name = "anturi-api-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Name = "anturi-api-ecs-execution-role"
  }
}

# mitä roolilla saa tehdä? = hakea kuvat ecr:ästä
resource "aws_iam_role_policy_attachment" "anturi_api_role_policy" {
  role       = aws_iam_role.anturi_api_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# sallii execution rolen lukea RDS:n salasanan Secrets Managerista
resource "aws_iam_role_policy" "read_db_secret" {
  name = "anturi-api-read-db-secret"
  role = aws_iam_role.anturi_api_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Effect   = "Allow"
        Resource = aws_db_instance.anturi_api_db_instance.master_user_secret[0].secret_arn
      }
    ]
  })
}
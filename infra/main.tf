resource "aws_ecr_repository" "anturi_api" {
  name                 = "anturi-api"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

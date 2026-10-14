output "ecr_repository_url" {
  value = aws_ecr_repository.anturi_api.repository_url
}

output "vpc_id" {
  value = data.aws_vpc.default_vpc.id
}

output "subnets_ids" {
  value = data.aws_subnets.default_subnets.ids
}


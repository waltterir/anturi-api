terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  backend "s3" {
    bucket       = "waltteri-tf-test-bucket"
    key          = "anturi-api/terraform.tfstate"
    region       = "eu-north-1"
    use_lockfile = true
  }
}
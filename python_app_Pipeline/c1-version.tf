terraform {
  required_version = ">= 1.0.0"
   required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.48.0"
     }
   }

  # Adding Backend as S3 for Remote State Storage
  backend "s3" {
    bucket = "aws-eks-terraform"
    key    = "dev/py-pipelinee/terraform.tfstate"
    region = "us-east-1" 

    # For State Locking
    dynamodb_table = "py-pipeline"    
  }    



}

provider "aws" {
  region = var.aws_region
}
# AWS Configuration Variables
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "ci-cd-portfolio"
}

variable "environment" {
  description = "Environment (dev/prod)"
  type        = string
  default     = "dev"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "data-processor"
}
# AWS Configuration Variables
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-2"
}

variable "prefix" {
  description = "Prefix used to name AWS resources"
  type        = string
  default     = "ci-cd-portfolio-dev"
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

variable "glue_database_name" {
  description = "Name of the Glue database"
  type        = string
  default     = "log_data_catalog"
}

variable "glue_crawler_name" {
  description = "Name of the Glue crawler"
  type        = string
  default     = "log-data-crawler"
}

variable "glue_job_name" {
  default = "log-etl-job"
}

variable "lambda_role_arn" {
  description = "IAM role ARN used by Glue job"
  type        = string
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for Glue script and temp"
  type        = string
}


# Lambda role name (used in aws_lambda_permission)
variable "lambda_role_name" {
  description = "IAM role name for Lambda execution"
  type        = string
}

# AWS Provider Configuration
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
}

# S3 Bucket for data storage
resource "aws_s3_bucket" "data_bucket" {
  bucket = "${var.project_name}-${var.environment}-data"
  
  tags = {
    Name        = "${var.project_name}-${var.environment}-data"
    Environment = var.environment
    Project     = var.project_name
  }
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "data_bucket_versioning" {
  bucket = aws_s3_bucket.data_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_glue_catalog_database" "log_db" {
  name = var.glue_database_name
}



# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-${var.environment}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = [
            "lambda.amazonaws.com",
            "glue.amazonaws.com"
          ]
        },
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "${var.project_name}-${var.environment}-lambda-role"
    Environment = var.environment
    Project     = var.project_name
  }
}


# IAM Policy for Lambda
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-${var.environment}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Resource = [
          aws_s3_bucket.data_bucket.arn,
          "${aws_s3_bucket.data_bucket.arn}/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "glue:*"
        ],
        Resource = "*"
      }
    ]
  })
}


      resource "aws_glue_crawler" "log_crawler" {
  name         = var.glue_crawler_name
  role         = aws_iam_role.lambda_role.arn
  database_name = aws_glue_catalog_database.log_db.name

  s3_target {
    path = "s3://${aws_s3_bucket.data_bucket.bucket}/raw/"
  }

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }

  configuration = jsonencode({
    Version = 1.0,
    CrawlerOutput = {
      Partitions = { AddOrUpdateBehavior = "InheritFromTable" }
    }
  })

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_glue_job" "log_etl_job" {
  name     = "log-etl-job"
  role_arn = var.lambda_role_arn

  command {
    name            = "glueetl"
    script_location = "s3://${var.s3_bucket_name}/scripts/load_etl.py"
    python_version  = "3"
  }

  glue_version      = "4.0"
  max_retries       = 0
  timeout           = 10
  number_of_workers = 2
  worker_type       = "G.1X"

  default_arguments = {
    "--TempDir" = "s3://${var.s3_bucket_name}/temp/"
    "--job-language" = "python"
    "--enable-metrics" = "true"
  }

  depends_on = [aws_glue_crawler.log_crawler]
}

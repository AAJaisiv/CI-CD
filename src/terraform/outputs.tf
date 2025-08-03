# Terraform Outputs
output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.data_bucket.bucket
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.data_bucket.arn
}

output "lambda_role_arn" {
  description = "ARN of the Lambda IAM role"
  value       = aws_iam_role.lambda_role.arn
}

output "lambda_role_name" {
  description = "Name of the Lambda IAM role"
  value       = aws_iam_role.lambda_role.name
} 

output "glue_database_name" {
  description = "Glue database name"
  value       = aws_glue_catalog_database.log_db.name
}

output "glue_crawler_name" {
  description = "Glue crawler name"
  value       = aws_glue_crawler.log_crawler.name
}

output "glue_job_name" {
  value = aws_glue_job.log_etl_job.name
}


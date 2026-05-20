output "artifact_bucket_name" {
  description = "S3 bucket for model artifacts."
  value       = aws_s3_bucket.artifacts.bucket
}

output "ecr_repository_url" {
  description = "ECR repository URL for the API image."
  value       = aws_ecr_repository.api.repository_url
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name."
  value       = aws_lb.api.dns_name
}

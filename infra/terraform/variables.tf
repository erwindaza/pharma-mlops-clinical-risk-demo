variable "project_name" {
  description = "Project name used for AWS resource naming."
  type        = string
  default     = "pharma-mlops-clinical-risk-demo"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "demo"
}

variable "aws_region" {
  description = "AWS region for optional deployment."
  type        = string
  default     = "us-east-1"
}

variable "container_image" {
  description = "Container image URI for ECS task definitions."
  type        = string
  default     = "public.ecr.aws/docker/library/python:3.11-slim"
}

variable "ecs_desired_count" {
  description = "Desired ECS task count. Keep 0 or 1 for cost control."
  type        = number
  default     = 0
}

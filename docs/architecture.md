# Architecture

This demo is local-first and cloud-optional. The local path proves reproducible training, model artifact creation, API serving, tests, Docker packaging, and smoke testing without AWS credentials.

```mermaid
flowchart LR
  A[Synthetic data generator] --> B[Training pipeline]
  B --> C[MLflow local tracking]
  B --> D[Model artifact]
  D --> E[FastAPI service]
  E --> F[Docker image]
  F --> G[Local smoke test]
  F --> H[Optional ECR]
  H --> I[Optional ECS Fargate]
  I --> J[CloudWatch logs]
  I --> K[Application Load Balancer]
```

The AWS path is intentionally optional. Terraform defines S3, ECR, IAM, CloudWatch, ECS Fargate, security groups, and an ALB. `ecs_desired_count` defaults to `0` to avoid running compute by accident.

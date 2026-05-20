# Cost Control

Default execution is local and does not require AWS.

Optional AWS resources that can create costs:

- Application Load Balancer.
- ECS Fargate tasks.
- CloudWatch logs.
- S3 storage.
- ECR storage.

Cost controls:

- `ecs_desired_count` defaults to `0`.
- ECS task size is `256 CPU / 512 MB`.
- CloudWatch retention is 14 days.
- S3 lifecycle expiration is 30 days.
- ECR keeps only the latest 5 images.

Cleanup:

```bash
cd infra/terraform
terraform destroy
```

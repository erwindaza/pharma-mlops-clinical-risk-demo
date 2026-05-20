# MLOps Lifecycle

1. Generate synthetic non-PHI clinical trial operations data.
2. Train a binary classifier with a fixed seed.
3. Log parameters, metrics, and artifacts to local MLflow.
4. Export a model artifact for serving.
5. Serve predictions through FastAPI with explicit schemas.
6. Validate behavior with pytest and smoke tests.
7. Package the service in Docker.
8. Optionally publish the image to ECR and run on ECS Fargate.

Governance controls include dataset provenance, model version, metrics, training parameters, reproducibility seed, and a documented model card.

# Interview Pitch

This project demonstrates how I would productionize ML in a regulated pharma-style environment. The emphasis is not just model training; it is reproducibility, deployment, observability, security, cost control, and a clean path from local development to cloud infrastructure.

In an interview, the strongest points to show are:

- The model uses synthetic clinical trial operations data, avoiding PHI and credential risk.
- Training logs metrics and artifacts with MLflow.
- Serving is handled by a typed FastAPI service with health, metadata, metrics, and prediction endpoints.
- CI runs linting, tests, a training smoke test, Docker build, and container smoke test.
- Terraform defines optional AWS resources with low-cost defaults and least-privilege IAM.
- Documentation explains architecture, lifecycle, security, pharma context, and cost controls.

Senior framing: the model can evolve, but the platform already demonstrates production habits.

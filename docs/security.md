# Security And Compliance Notes

This repository must not contain AWS credentials, access keys, secrets, private keys, passwords, real patient records, PHI, or proprietary clinical data.

Controls included:

- `.env.example` documents configuration without secrets.
- `.gitignore` excludes `.env`, local artifacts, MLflow runs, state files, caches, and local databases.
- Terraform blocks public S3 access and enables server-side encryption.
- IAM is separated into ECS execution and task roles.
- The optional task role only reads the artifact bucket.
- AWS deployment is not part of default CI.

This is an engineering demo, not a medical device, diagnostic tool, or clinical recommendation system.

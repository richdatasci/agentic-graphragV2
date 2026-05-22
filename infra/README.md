# Infrastructure

This folder contains deployment assets for local and production environments.

Contents:

- `docker`: local development Docker assets
- `kubernetes`: Kubernetes manifests for API, workers and supporting services
- `terraform`: cloud infrastructure starter modules
- `helm`: Helm chart scaffold
- `grafana`: dashboard provisioning and dashboards

Secrets should not be committed. Use `.env`, Kubernetes secrets or a cloud secrets manager.

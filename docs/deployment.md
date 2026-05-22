# Deployment

## Local

```bash
docker compose up -d
uvicorn apps.api.main:app --reload
celery -A apps.worker.celery_app worker --loglevel=INFO
```

## Kubernetes

Apply manifests:

```bash
kubectl apply -f infra/kubernetes/namespace.yaml
kubectl apply -f infra/kubernetes/configmap.yaml
kubectl apply -f infra/kubernetes/secret.example.yaml
kubectl apply -f infra/kubernetes/api-deployment.yaml
kubectl apply -f infra/kubernetes/api-service.yaml
kubectl apply -f infra/kubernetes/worker-deployment.yaml
```

## Production Recommendations

- Use managed Postgres where possible.
- Use persistent storage for Neo4j, Qdrant and MinIO.
- Use a cloud secrets manager.
- Add CI/CD evaluation gates.
- Add backup and restore.
- Add horizontal autoscaling.

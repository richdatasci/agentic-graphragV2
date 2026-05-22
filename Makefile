.PHONY: setup up down logs bootstrap ingest-sample api worker frontend test clean pull-model pull-model-small shell

setup:
	cp -n .env.example .env || true
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev,ingestion]"

up:
	cp -n .env.example .env || true
	docker compose up -d --build

# FOR WINDOWS USERS

#setup:
	#powershell -NoProfile -Command "if (!(Test-Path .env)) { Copy-Item .env.example .env }"
	#python -m pip install --upgrade pip
	#python -m pip install -e ".[dev,ingestion]"

#up:
	#powershell -NoProfile -Command "if (!(Test-Path .env)) { Copy-Item .env.example .env }"
	#docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

bootstrap:
	docker compose exec api python scripts/bootstrap.py || python scripts/bootstrap.py

ingest-sample:
	docker compose exec api python scripts/ingest_sample.py || python scripts/ingest_sample.py

api:
	uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

worker:
	celery -A apps.worker.celery_app worker --loglevel=INFO

frontend:
	cd apps/frontend && npm install && npm run dev

test:
	pytest

pull-model:
	docker exec -it agentic-graphrag-ollama ollama pull llama3.1:8b

pull-model-small:
	docker exec -it agentic-graphrag-ollama ollama pull llama3.2:3b

shell:
	docker compose exec api bash

clean:
	docker compose down -v
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +

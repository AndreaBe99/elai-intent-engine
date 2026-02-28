# Makefile for ELAI Intent Engine

.PHONY: help setup start stop deploy run-docker stop-docker

# Show help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup        0. Setup uv, sync dependencies and install package in editable mode"
	@echo "  start        1. Start MongoDB (docker) and the application (uvicorn)"
	@echo "  stop         2. Stop the application and MongoDB container"
	@echo "  deploy       3. Deploy with Docker Compose (build and start in background)"
	@echo "  run-docker   4. Run with Docker Compose (foreground)"
	@echo "  stop-docker  5. Stop and remove Docker Compose containers"

# 0. setup uv
setup:
	uv sync --all-groups
	uv pip install -e .

# 1. start up the app with uvicorn and mongodb
start:
	docker compose -f docker/docker-compose.yml up -d mongo
	uv run uvicorn elai_intent_engine.main:app --host 0.0.0.0 --port 5000 --reload

# 2. Stop the app and mongodb
stop:
	@echo "Stopping application..."
	-taskkill /F /IM uvicorn.exe /T 2>/dev/null || pkill uvicorn 2>/dev/null || true
	docker compose -f docker/docker-compose.yml stop mongo

# 3. deploy docker compose
deploy:
	docker compose -f docker/docker-compose.yml up -d --build

# 4. run docker compose
run-docker:
	docker compose -f docker/docker-compose.yml up

# 5. stop docker compose
stop-docker:
	docker compose -f docker/docker-compose.yml down

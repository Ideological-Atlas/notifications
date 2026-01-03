ifneq ("$(wildcard .env)","")
    include .env
    export
endif

# --- Configuration ---
COMPOSE = docker compose
NOTIFICATIONS_SVC = $(PROJECT_NAME)_notifications
EXEC = docker exec -it $(NOTIFICATIONS_SVC)
TAIL_LOGS = 50

.DEFAULT_GOAL := up-logs

# --- System ---
.PHONY: help prepare-env clean-images remove-containers

help: ## Show this help message
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

prepare-env: ## Create .env from template
	@test -f .env || cp .env-dist .env

clean-images: ## Remove all project images
	@if [ -n "$(shell docker images -qa)" ]; then docker rmi $(shell docker images -qa) --force; fi

remove-containers: ## Remove all project containers
	@if [ -n "$(shell docker ps -qa)" ]; then docker rm $(shell docker ps -qa); fi

# --- Docker Orchestration ---
up-logs: up logs

up: prepare-env ## Start containers in background
	@$(COMPOSE) up --force-recreate -d --remove-orphans

down: ## Stop and remove containers
	@$(COMPOSE) down

restart: ## Restart containers
	@$(COMPOSE) restart

build: prepare-env ## Build images
	@$(COMPOSE) build

down-up: down up-logs ## Recreate services

complete-build: build down-up ## Full rebuild cycle

# --- Development & Logs ---
.PHONY: logs all-logs bash shell lint format

logs: ## Show notifications service logs
	@docker logs --tail $(TAIL_LOGS) -f $(NOTIFICATIONS_SVC)

bash: ## Access container bash
	@$(EXEC) bash

shell: ## Access IPython shell
	@$(EXEC) ipython


# --- Testing ---
.PHONY: trigger-test test install-dev-dependencies

install-dev-dependencies: ## Install dev dependencies
	@$(EXEC) uv sync --extra dev

clean-coverage: ## Clean previous coverage results
	@$(EXEC) rm -f .coverage coverage.xml

test: clean-coverage install-dev-dependencies ## Run tests with standard unittest
	@$(EXEC) uv run coverage run -m unittest discover -s tests -t . -p "test_*.py"
	@$(EXEC) uv run coverage xml
	@$(EXEC) uv run coverage report

trigger-test: ## Send a test email via Curl using .env variables
	@echo "Sending test email to $(TEST_EMAIL)..."
	@echo "Template: $(TEST_TEMPLATE)"
	@echo "Language: $(TEST_LANGUAGE)"
	@curl -X POST http://localhost:$(PORT)/notifications/send \
	   -H "Content-Type: application/json" \
	   -H "Authorization: Bearer $(API_KEY)" \
	   -d '{"to_email": "$(TEST_EMAIL)", "template_name": "$(TEST_TEMPLATE)", "language": "$(TEST_LANGUAGE)", "context": $(TEST_CONTEXT)}'
	@echo "\nDone."

include .env
export

.PHONY: server_mock server_lrs


install_python_dependencies:

server_mock:
	@echo "Starting server mock..."
	cd server_mock && uv sync && uv run uvicorn app:app --reload --host $(SERVER_HOST) --port $(SERVER_PORT)
	@echo "Server mock started."

server_lrs:
	@echo "Remove any LRSQL container..."
	-docker rm -f $(DOCKER_TAG) 2>/dev/null
	@echo "Starting LRSQL container..."
	docker run \
        -it \
        --name $(DOCKER_TAG) \
        -p $(SERVER_PORT):8080 \
        -e LRSQL_API_KEY_DEFAULT=$(LRSQL_API_KEY_DEFAULT) \
        -e LRSQL_API_SECRET_DEFAULT=$(LRSQL_API_SECRET_DEFAULT) \
        -e LRSQL_ADMIN_USER_DEFAULT=$(LRSQL_ADMIN_USER_DEFAULT) \
        -e LRSQL_ADMIN_PASS_DEFAULT=$(LRSQL_ADMIN_PASS_DEFAULT) \
        -e LRSQL_ALLOW_ALL_ORIGINS=$(LRSQL_ALLOW_ALL_ORIGINS) \
        -e LRSQL_DB_NAME=db/lrsql.sqlite.db \
        -v $(DB_VOLUME_NAME):/lrsql/db \
        yetanalytics/lrsql:latest
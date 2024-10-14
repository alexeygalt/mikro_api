.PHONY: install run test

run:
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .env

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

help:
	@echo "Available commands:"
	@echo "  run      - Run the FastAPI application"

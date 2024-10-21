.PHONY: install run test

run:
	poetry run gunicorn app.main:app -c gunicorn.conf.py

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

help:
	@echo "Available commands:"
	@echo "  run      - Run the FastAPI application"

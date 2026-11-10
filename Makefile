.PHONY: up down logs web makemigrations migrate createsuperuser

up:
	docker compose up -d --build

down:
	docker compose down

reset:
	docker compose down -v
	docker compose up -d --build
	@echo "♻️  Environment reset with clean DB."

logs:
	docker compose logs -f

web:
	docker compose exec web bash

makemigrations:
	docker compose exec web python manage.py makemigrations

migrate:
	docker compose exec web python manage.py migrate

createsuperuser:
	docker compose exec web python manage.py createsuperuser
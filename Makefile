.PHONY: setup dev down logs backend-shell trigger reset health clean

setup:
	cp -n .env.example .env || true
	cp -n backend/.env.example backend/.env || true
	cp -n frontend/.env.example frontend/.env || true
	@echo "Environment files created. Edit backend/.env to add QWEN_API_KEY when ready."

dev:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f backend frontend

backend-shell:
	docker compose exec backend sh

trigger:
	curl -s -X POST http://localhost:8000/api/v1/demo/trigger-alert | python -m json.tool

reset:
	curl -s -X POST http://localhost:8000/api/v1/demo/reset | python -m json.tool

health:
	curl -s http://localhost:8000/health | python -m json.tool

clean:
	docker compose down -v

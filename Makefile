# Makefile (Versión Simplificada)

# --- Entorno de Desarrollo (sin observabilidad) ---
up-dev:
	docker-compose --profile dev up -d --build

# --- Entorno de Desarrollo CON Observabilidad ---
up-obs:
	docker-compose --profile dev --profile obs up -d --build

# --- Entorno de Testing ---
up-test:
	docker-compose --profile test up -d --build

# --- Comandos Generales ---
# Detener todos los servicios
down:
	docker-compose down --remove-orphans

build:
	docker-compose build

rebuild:
	docker-compose build --no-cache

restart: down up-obs

logs:
	docker-compose logs -f

backend-shell:
	docker exec -it todolist_backend bash
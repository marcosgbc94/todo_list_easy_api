# Makefile para levantar todo el proyecto Todolist
# ================================================

# Variables
COMPOSE = ./docker-compose.yml

# Construir las imágenes sin levantar los contenedores
build:
	docker compose -f $(COMPOSE) build

# Reconstruir desde cero (ignora cache)
rebuild:
	docker compose -f $(COMPOSE) build --no-cache

# Levantar todos los servicios
up:
	docker compose -f $(COMPOSE) up -d

# Detener todos los servicios
down:
	docker compose -f $(COMPOSE) down

# Reiniciar todo
restart: down up

# Ver logs de todos los servicios
logs:
	docker compose -f $(COMPOSE) logs -f

# Entrar al contenedor de backend
backend-shell:
	docker exec -it todolist_backend bash

# Entrar al contenedor de DB
db-shell:
	docker exec -it todolist_db psql -U $(DB_USER) -d $(DB_NAME)

# Makefile
COMPOSE_BASE = docker-compose -f docker-compose.yml
COMPOSE_OBS = $(COMPOSE_BASE) -f docker-compose.observability.yml
COMPOSE_TEST = $(COMPOSE_BASE) -f docker-compose.test.yml

# Construir la imagen base
build:
	docker-compose build

# --- Entorno de Desarrollo ---
# Levantar solo backend y BD de desarrollo
up-dev:
	$(COMPOSE_BASE) up -d --build

# --- Entorno de Desarrollo con Observabilidad ---
# Levantar todo: backend, BD dev y stack de observabilidad
up-obs:
	$(COMPOSE_OBS) up -d --build

# --- Entorno de Testing ---
# Levantar backend y BD de pruebas
up-test:
	$(COMPOSE_TEST) up -d --build

# --- Comandos Generales ---
# Detener todos los servicios de todos los archivos
down:
	$(COMPOSE_OBS) -f docker-compose.test.yml down --remove-orphans

restart: down up-obs

logs:
	$(COMPOSE_OBS) logs -f

backend-shell:
	docker exec -it todolist_backend bash
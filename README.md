# TodoList API

Una API RESTful para gestionar listas de tareas, construida con Python y FastAPI, siguiendo los principios de Arquitectura Limpia y Diseño Guiado por el Dominio (DDD).

##  Arquitectura

Este proyecto está diseñado siguiendo una **Arquitectura Limpia** con influencias de la **Arquitectura Hexagonal (Puertos y Adaptadores)**. El objetivo principal es la separación de responsabilidades, creando un sistema desacoplado, mantenible y altamente testeable.

La regla fundamental es la **Regla de Dependencia**: las dependencias solo apuntan hacia adentro. La lógica de negocio (dominio) no sabe nada sobre la base de datos, el framework web o cualquier otro detalle de infraestructura.

---
## Flujo de una Petición: ¿Cómo interactúan las capas?

Para entender la arquitectura, sigamos el ciclo de vida de una petición HTTP, por ejemplo, `GET /users/{user_id}`:

1.  **Capa de Presentación (Entrada HTTP):**
    * La petición llega a **FastAPI** y es dirigida al `user_router` (`/presentation/api/routers/user_router.py`).
    * El decorador del endpoint (`@router.get("/{user_id}", ...)` coincide con la ruta.

2.  **Capa de Presentación (Inyección de Dependencias):**
    * Antes de ejecutar el código del endpoint, FastAPI resuelve las dependencias que este pide. En nuestro caso, pide `UserServiceDependency`.
    * El proveedor de dependencias (`/presentation/api/dependencies/user_dependencies.py`) construye una instancia de `UserService`.
    * Para construir `UserService`, el proveedor a su vez pide las dependencias que este necesita: `IUserRepository` (el puerto/interfaz) y `DataBaseSessionDependency`. Estas se resuelven desde `/presentation/api/dependencies/core_dependencies.py`. Aquí es donde se "conecta" la interfaz `IUserRepository` con su implementación concreta `UserRepository`.

3.  **Capa de Dominio (Ejecución de Lógica de Negocio):**
    * El endpoint del router, ya con una instancia de `UserService` lista para usar, llama al método correspondiente: `await user_service.get_user_by_id(user_id)`.
    * El `UserService` (`/domain/services/user_service.py`) contiene la lógica de negocio pura. No sabe qué es HTTP ni FastAPI.
    * El servicio utiliza el repositorio a través de la abstracción (`self.repo.get_user_by_id(...)`) que se le inyectó. Solo conoce el contrato definido en `IUserRepository` (`/domain/ports/i_user_repository.py`).

4.  **Capa de Datos (Acceso a la Base de Datos):**
    * La llamada al método del repositorio llega a la implementación concreta: `UserRepository` (`/data/repositories/user_repository.py`).
    * Este "adaptador" traduce la llamada del dominio a una consulta de **SQLAlchemy**.
    * Interactúa con el `UserModel` (`/data/models/user_model.py`) para consultar la base de datos a través de la sesión de SQLAlchemy.
    * Mapea el resultado de `UserModel` a una `UserEntity` (la entidad del dominio) y la devuelve.

5.  **El Flujo de Retorno:**
    * La `UserEntity` viaja de vuelta al `UserService`.
    * El `UserService` la retorna al `user_router` (envuelta en un objeto `Result`).
    * Finalmente, el `user_router` convierte la `UserEntity` en un `UserResponse` (un schema de Pydantic) y lo devuelve como una respuesta JSON al cliente.

Este flujo asegura que cada capa tenga una única responsabilidad y que el dominio permanezca aislado y puro.

---
## Estructura de Directorios

```
app/
├── core/                   # Lógica transversal: settings, excepciones, seguridad.
├── data/                   # Capa de Datos (Adaptadores)
│   ├── datasource/         # Configuración de la fuente de datos (ej: database.py).
│   ├── models/             # Modelos de SQLAlchemy (tablas).
│   └── repositories/       # Implementaciones concretas de los repositorios.
├── domain/                 # Capa de Dominio (Lógica de Negocio Pura)
│   ├── entities/           # Entidades de negocio.
│   ├── ports/              # Interfaces (Puertos) que definen los contratos.
│   └── services/           # Clases que orquestan la lógica de negocio.
├── presentation/           # Capa de Presentación (Interfaz con el exterior)
│   ├── api/
│   │   ├── dependencies/   # Proveedores para la inyección de dependencias.
│   │   └── routers/        # Endpoints de la API (FastAPI).
│   └── schemas/            # Schemas de Pydantic (modelos de Request/Response).
└── utils/                  # Utilidades generales.
```

---
## Cómo Empezar

1.  **Clonar el repositorio:**
    ```bash
    git clone <url-del-repositorio>
    cd todo_list_easy_api
    ```

2.  **Configurar el entorno:**
    * Crea un archivo `.env` a partir del ejemplo: `cp .env.example .env`.
    * Modifica las variables en `.env` según tu configuración local.

3.  **Levantar los servicios con Docker:**
    El proyecto utiliza Docker Compose para orquestar la aplicación y la base de datos.
    ```bash
    docker-compose up -d --build
    ```
    Puedes usar los comandos del `Makefile` para una gestión más sencilla (ej: `make up`, `make down`).

4.  **Acceder a la API:**
    * La API estará disponible en `http://localhost:8000` (o el puerto que hayas configurado).
    * La documentación interactiva de Swagger UI se encuentra en `http://localhost:8000/docs`.

---
## Stack Tecnológico

* **Framework:** FastAPI
* **Base de Datos:** PostgreSQL
* **ORM:** SQLAlchemy (con `asyncpg` para modo asíncrono)
* **Validación de Datos:** Pydantic
* **Contenerización:** Docker & Docker Compose
```
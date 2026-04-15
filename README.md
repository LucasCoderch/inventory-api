# inventory-api

API REST de gestión de inventario construida con FastAPI y PostgreSQL. Incluye autenticación JWT, control de roles y datos reales del dataset [Online Retail Transaction Data](https://www.kaggle.com/datasets/thedevastator/online-retail-transaction-data) de Kaggle (~3900 productos).

## Stack

| Capa | Tecnología |
|---|---|
| Framework | FastAPI 0.135 + Uvicorn |
| Base de datos | PostgreSQL 16 (Docker) |
| ORM | SQLAlchemy 2.0 async (asyncpg) |
| Validación | Pydantic v2 |
| Migraciones | Alembic |
| Auth | JWT via python-jose + passlib/bcrypt |
| Tests | pytest + pytest-asyncio |
| CI/CD | GitHub Actions |

## Modelo de datos

```
users ──────────── orders ──────────── order_items
  id                 id                    id
  email              user_id (FK)          order_id (FK)
  hashed_password    status                product_id (FK)
  role               total                 qty
  is_active          created_at            unit_price
  created_at
                                       products
                                           id
                                           sku (único)
                                           name
                                           description
                                           price
                                           stock
                                           created_at
```

## Setup local

### Requisitos previos
- Python 3.12
- Docker Desktop

### 1. Clonar y configurar entorno

```bash
git clone <repo-url>
cd inventory-api
python -m venv .venv
.venv/Scripts/activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

### 2. Variables de entorno

```bash
cp .env.example .env
# Editar .env y cambiar SECRET_KEY por un valor seguro
```

### 3. Levantar base de datos

```bash
docker-compose up -d
```

### 4. Correr migraciones

```bash
alembic upgrade head
```

### 5. Cargar datos de Kaggle

```bash
python scripts/download_dataset.py   # descarga el CSV
python scripts/seed.py               # inserta ~3900 productos
```

### 6. Iniciar servidor

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en `http://127.0.0.1:8000`
Documentación interactiva: `http://127.0.0.1:8000/docs`

---

## Prueba manual (Swagger UI)

La forma más rápida de probar la API es desde el Swagger en `http://127.0.0.1:8000/docs`.

### Crear un usuario administrador

Los endpoints de admin requieren un usuario con `role: admin`. Para crearlo desde la DB:

```bash
# 1. Generar el hash de la contraseña
python -c "from app.core.security import hash_password; print(hash_password('tu_password'))"

# 2. Insertar el admin en la DB
docker exec inventory_db psql -U inventory -d inventory -c "
INSERT INTO users (email, hashed_password, role, is_active, created_at)
VALUES ('admin@miapi.com', '<hash_del_paso_1>', 'admin', true, NOW());"
```

### Flujo de autenticación en Swagger

1. Ir a `http://127.0.0.1:8000/docs`
2. Usar `POST /api/v1/auth/login` con email y password
3. Copiar el `access_token` de la respuesta
4. Hacer clic en el botón **Authorize** (candado arriba a la derecha)
5. Pegar el token en el campo `Value` con el formato: `Bearer <token>`
6. Confirmar con **Authorize** — todos los endpoints protegidos quedan habilitados

---

## Endpoints

### Auth
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | No | Registrar nuevo usuario |
| POST | `/api/v1/auth/login` | No | Login — devuelve JWT |
| GET | `/api/v1/auth/me` | Token | Perfil del usuario autenticado |

### Usuarios (solo admin)
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/v1/users` | Admin | Listar todos los usuarios |
| GET | `/api/v1/users/{id}` | Admin | Obtener usuario por ID |
| PATCH | `/api/v1/users/{id}` | Admin | Cambiar role o is_active |
| DELETE | `/api/v1/users/{id}` | Admin | Desactivar usuario (soft delete) |

### Productos
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/v1/products` | No | Listar productos |
| GET | `/api/v1/products/{id}` | No | Obtener producto por ID |
| POST | `/api/v1/products` | Admin | Crear producto |
| PATCH | `/api/v1/products/{id}` | Admin | Actualizar producto |
| DELETE | `/api/v1/products/{id}` | Admin | Eliminar producto |

### Sistema
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/health` | No | Estado de la API y la DB |

---

## Correr tests

```bash
pytest
```

---

## Setup con Docker completo

> Próximamente — se agregará Dockerfile y docker-compose con servicio de la API incluido (paso 7 del roadmap).

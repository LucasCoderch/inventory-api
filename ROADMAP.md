# Roadmap — inventory-api

## 1. Autenticación y Autorización (JWT)
- [x] 1.1 Instalar dependencias: `python-jose[cryptography]` y `passlib[bcrypt]` ✓
- [x] 1.2 Crear `app/core/security.py` — hash de password, verificación, generación/validación de JWT ✓
- [x] 1.3 Agregar a `Settings` (`config.py`): `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` ✓
- [x] 1.4 Actualizar `.env` y `.env.example` con las nuevas variables ✓
- [x] 1.5 Crear `app/schemas/user.py` — `UserCreate`, `UserOut`, `TokenOut`, `LoginIn` ✓
- [x] 1.6 Crear `app/services/users.py` — `register`, `authenticate`, `get_by_email`, `get_by_id` ✓
- [x] 1.7 Crear `app/api/v1/routers/auth.py` — endpoints: ✓
  - [x] 1.7.1 `POST /auth/register` ✓
  - [x] 1.7.2 `POST /auth/login` ✓
  - [x] 1.7.3 `GET /auth/me` ✓
- [x] 1.8 Crear `app/api/deps.py` — `get_current_user` y `require_admin` ✓
- [x] 1.9 Registrar el router de auth en `app/api/v1/api.py` ✓

## 2. CRUD de Usuarios (admin)
- [ ] 2.1 Completar `app/services/users.py` — `list_users`, `get_user`, `deactivate_user`
- [ ] 2.2 Crear `app/api/v1/routers/users.py`:
  - [ ] 2.2.1 `GET /users`
  - [ ] 2.2.2 `GET /users/{id}`
  - [ ] 2.2.3 `PATCH /users/{id}`
  - [ ] 2.2.4 `DELETE /users/{id}`
- [ ] 2.3 Agregar schema `UserUpdate`
- [ ] 2.4 Registrar router en `api.py`

## 3. Proteger endpoints de Productos con roles
- [ ] 3.1 Agregar `get_current_user` a `POST`, `PATCH`, `DELETE` de productos
- [ ] 3.2 Agregar `require_admin` a escritura de productos
- [ ] 3.3 Mantener `GET` de productos públicos

## 4. Paginación y Filtros en Productos
- [ ] 4.1 Query params: `skip`, `limit`
- [ ] 4.2 Filtro por nombre: `?search=`
- [ ] 4.3 Filtro por rango de precio: `?min_price=` y `?max_price=`
- [ ] 4.4 Ordenamiento: `?order_by=` y `?order_dir=`
- [ ] 4.5 Schema `ProductListOut` con paginación
- [ ] 4.6 Actualizar `ProductService.list()`

## 5. CRUD de Órdenes con lógica de negocio
- [ ] 5.1 Crear `app/schemas/order.py`
- [ ] 5.2 Crear `app/services/orders.py`:
  - [ ] 5.2.1 `create_order` — valida stock, descuenta, calcula total
  - [ ] 5.2.2 `list_orders`
  - [ ] 5.2.3 `get_order` con items
  - [ ] 5.2.4 `cancel_order` — devuelve stock
- [ ] 5.3 Crear `app/api/v1/routers/orders.py`:
  - [ ] 5.3.1 `POST /orders`
  - [ ] 5.3.2 `GET /orders`
  - [ ] 5.3.3 `GET /orders/{id}`
  - [ ] 5.3.4 `PATCH /orders/{id}/cancel`
- [ ] 5.4 Validación de stock insuficiente
- [ ] 5.5 Registrar router en `api.py`

## 6. Tests de Integración Completos
- [ ] 6.1 Crear `tests/conftest.py` con fixtures: `db`, `client`, `admin_token`, `user_token`, `sample_product`
- [ ] 6.2 Crear `tests/test_auth.py` (register, login, me, errores)
- [ ] 6.3 Ampliar `tests/test_products.py` (paginación, filtros, roles, errores)
- [ ] 6.4 Crear `tests/test_orders.py` (crear, listar, cancelar, validaciones)
- [ ] 6.5 Actualizar GitHub Actions CI

## 7. Infraestructura — Dockerfile + docker-compose completo
- [ ] 7.1 Crear `Dockerfile` para la app
- [ ] 7.2 Actualizar `docker-compose.yml` con servicio `api`
- [ ] 7.3 Agregar `.dockerignore`
- [ ] 7.4 Migraciones automáticas al arranque

## 8. Logging estructurado
- [ ] 8.1 Crear `app/core/logging.py`
- [ ] 8.2 Formato estructurado (nivel, timestamp, ruta)
- [ ] 8.3 Agregar `lifespan` en `app/main.py`
- [ ] 8.4 Loguear eventos clave en servicios

## 9. README completo
- [ ] 9.1 Descripción y stack
- [ ] 9.2 Modelo de datos
- [ ] 9.3 Instrucciones de setup local
- [ ] 9.4 Tabla de endpoints
- [ ] 9.5 Instrucciones de tests
- [ ] 9.6 Setup con Docker completo
- [ ] 9.7 Link a Swagger UI

## 10. Pulido final
- [ ] 10.1 `.env.example` completo
- [ ] 10.2 OpenAPI personalizado (descripción, tags, contact)
- [ ] 10.3 Verificar `alembic upgrade head` desde cero
- [ ] 10.4 Suite de tests en verde
- [ ] 10.5 Linter y formatter sin errores
- [ ] 10.6 Push final con CI en verde
- [ ] 10.7 Deploy en Railway/Render (opcional)

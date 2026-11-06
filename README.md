# Tienda Online - Class 5

Proyecto desarrollado con FastAPI, SQLModel, SQLite y autenticación JWT.

## Funcionalidades

- Registro de usuarios
- Inicio de sesión
- Contraseñas almacenadas mediante hash seguro
- Generación y validación de tokens JWT
- Endpoints de productos protegidos
- Crear productos
- Listar productos
- Consultar productos por ID
- Editar productos
- Eliminar productos
- Persistencia de datos con SQLite
- Frontend desarrollado con HTML, CSS y JavaScript
- Comunicación con el backend mediante Fetch API

## Tecnologías utilizadas

- Python
- FastAPI
- SQLModel
- SQLite
- JWT
- Argon2
- HTML
- CSS
- JavaScript

## Estructura del proyecto

```text
tienda/
├── controller/
├── core/
├── db/
├── dependencies/
├── frontend/
├── models/
├── schemas/
├── services/
├── database.db
├── main.py
├── requirements.txt
└── README.md
```

## Ejecutar el proyecto

Crear y activar un entorno virtual e instalar las dependencias:

```bash
pip install -r requirements.txt
```

Crear un archivo `.env` con las variables de configuración necesarias.

Ejecutar el backend:

```bash
python -m uvicorn main:app --reload
```

La documentación Swagger estará disponible en:

```text
http://127.0.0.1:8000/docs
```

Para utilizar el frontend, abrir:

```text
frontend/index.html
```

con Live Server.

## Autenticación

Los endpoints de productos requieren un token JWT.

El flujo utilizado es:

1. Registrar un usuario.
2. Iniciar sesión.
3. Obtener el token JWT.
4. Enviar el token como Bearer Token para acceder al CRUD de productos.

## Base de datos

La aplicación utiliza SQLite mediante el archivo:

```text
database.db
```

Los usuarios y productos permanecen almacenados aunque el servidor sea reiniciado.

## Seguridad

El archivo `.env` no se incluye en el repositorio.

Las contraseñas no se almacenan directamente. Se guarda únicamente su hash utilizando Argon2.
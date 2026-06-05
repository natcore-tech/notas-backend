# Sistema de Notas - Backend (API REST)

Este es el repositorio del backend para mi proyecto universitario de la Universidad Tecnológica Equinoccial (UTE). Es una API REST diseñada para gestionar estudiantes, materias, periodos académicos y calificaciones.

#### Enlace del repositorio: https://github.com/natcore-tech/notas-backend

## ¿Qué hace este proyecto?

### El sistema separa los permisos dependiendo del tipo de usuario usando tokens JWT:
* **Estudiantes:** Tienen acceso de solo lectura. Cuando inician sesión, el sistema filtra la base de datos para que solo puedan ver sus propias materias y calificaciones. No pueden modificar nada ni ver los datos de otros compañeros.
* **Administradores / Docentes (Staff):** Tienen acceso total (CRUD) para registrar materias, crear periodos académicos, matricular estudiantes y subir las notas.

## Tecnologías utilizadas

* Python 3.12+
* Django 5 y Django REST Framework
* PostgreSQL (Base de datos relacional)
* uv (Para instalar paquetes y manejar el entorno virtual)

## Instalación

### **1. Clonar el repositorio**
```bash
git clone [https://github.com/natcore-tech/notas-backend.git](https://github.com/natcore-tech/notas-backend.git)
cd notas-backend
```
### **2. Crear el archivo de variables de entorno:** Crea un archivo llamado `.env` en la raíz del proyecto para conectar la base de datos

```env
# Django
SECRET_KEY=tu_clave_secreta_de_django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Postgres
DB_NAME=nombre_base_datos
DB_USER=usuario_de_postgres
DB_PASSWORD=tu_contraseña_de_postgres
DB_HOST=localhost
DB_PORT=5432
TEST_DB_NAME=notas_test_db

# Cors
CORS_ALLOW_ALL_ORIGINS=True
```

### **3. Crear base de datos y credenciales:** Accede a la consola de postgres, crea el usuario y la base de datos, las credenciales creadas se deben adjuntar al `.env`

```bash
psql -U postgres
```

```sql
CREATE DATABASE example_db;
CREATE USER example_user WITH PASSWORD 'your_postgres_password';

ALTER ROLE example_user SET client_encoding TO 'utf8';
ALTER ROLE example_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE example_user SET default_transaction_deferrable TO on;
ALTER ROLE example_user SET timezone TO 'America/Lima';

GRANT ALL PRIVILEGES ON DATABASE example_db TO example_user;
```

Salir:

```sql
\q
```

### **4. Instalar las dependencias** Utiliza uv para sincronizar el entorno virtual de forma rápida 

```
uv sync
```

### **5. Migraciones y Superusuario** Crea las tablas en PostgreSQL y cuenta de administrador principal

```
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

## Levantar el Servidor

### Ejecutar el siguiente comando

```
uv run python manage.py runserver
```

### El servidor esta disponible en la siguiente ruta

```
http://127.0.0.1:8000/api/
```

### Para verificar funcionamiento podemos acceder a la siguiente ruta

```
http://127.0.0.1:8000/api/health/
```

## Documentación de la API

### 1. Panel de Administración de Django
* **`GET`** `/admin/` - Acceso al panel nativo de administrador.

### 2. Estado del Servidor
* **`GET`** `/api/health/` - Endpoint para verificar que la API está funcionando.

### 3. Autenticación y Tokens
* **`POST`** `/api/auth/register/` - Registro de nuevos usuarios.
* **`POST`** `/api/auth/login/` - Inicio de sesión y generación de token JWT.
* **`POST`** `/api/auth/token/refresh/` - Renovación de un token de acceso expirado.
* **`POST`** `/api/auth/token/verify/` - Verificación de validez de un token.
* **`POST`** `/api/auth/logout/` - Cierre de sesión (invalidación del token).

### 4. Gestión de Cuentas (Usuarios)
* **`GET`, `POST`** `/api/users/` - Listar todos los usuarios o crear uno nuevo.
* **`GET`, `PUT`, `PATCH`, `DELETE`** `/api/users/<id>/` - Ver, editar o eliminar un usuario específico.

### 5. Periodos Académicos
* **`GET`, `POST`** `/api/periods/` - Listar o crear periodos académicos.
* **`GET`, `PUT`, `PATCH`, `DELETE`** `/api/periods/<id>/` - Ver, editar o eliminar un periodo específico.

### 6. Materias (Cursos)
* **`GET`, `POST`** `/api/courses/` - Listar o crear materias.
* **`GET`, `PUT`, `PATCH`, `DELETE`** `/api/courses/<id>/` - Ver, editar o eliminar una materia específica.

### 7. Perfiles de Estudiantes
* **`GET`, `POST`** `/api/students/` - Listar o registrar estudiantes.
* **`GET`, `PUT`, `PATCH`, `DELETE`** `/api/students/<id>/` - Ver, editar o eliminar el perfil de un estudiante.

### 8. Matrículas
* **`GET`, `POST`** `/api/enrollments/` - Listar matrículas o inscribir a un estudiante en una materia.
* **`GET`, `PUT`, `PATCH`, `DELETE`** `/api/enrollments/<id>/` - Ver, editar o anular una matrícula específica.

### 9. Calificaciones
* **`GET`, `POST`** `/api/grades/` - Listar todas las notas o registrar una nueva.
* **`GET`, `PUT`, `PATCH`, `DELETE`** `/api/grades/<id>/` - Ver, editar o eliminar una calificación específica.

## Estructura del Proyecto

```txt
notas-backend/
├── config/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── notas/
│   ├── models/
│   ├── serializers/
│   ├── tests/
│   ├── views/
│   ├── admin.py
│   ├── apps.py
│   ├── filters.py
│   ├── models.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── urls.py
│   └── views.py
├── .env
├── .gitignore
├── .python-version
├── main.py
├── manage.py
├── pyproject.toml
├── README.md
└── uv.lock
```

## Ejemplos de uso de la API

Para interactuar con las rutas protegidas del sistema, es obligatorio enviar el token de acceso (`access token`) en los headers de la petición HTTP. El formato debe ser `Bearer <tu_token>`.

A continuación, se muestran algunos ejemplos prácticos:


### 1. Iniciar sesión para obtener el token

**Usando cURL (Terminal):**
```bash
curl -X POST [http://127.0.0.1:8000/api/auth/login/](http://127.0.0.1:8000/api/auth/login/) \
     -H "Content-Type: application/json" \
     -d '{
           "username": "nuevo_alumno",
           "password": "Password123!"
         }'
```

### 2. Obtener la lista de materias

**Usando cURL (Terminal):**
```bash
curl -X GET [http://127.0.0.1:8000/api/courses/](http://127.0.0.1:8000/api/courses/) \
     -H "Authorization: Bearer tu_access_token_aqui"
```

### 3. Crear una nueva materia

**Usando cURL (Terminal):**
```bash
curl -X POST [http://127.0.0.1:8000/api/courses/](http://127.0.0.1:8000/api/courses/) \
     -H "Authorization: Bearer tu_access_token_aqui" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Seguridad Informática",
           "description": "Laboratorio de redes",
           "credits": 4,
           "is_active": true
         }'
```

### 4. Consultar calificaciones personales

**Usando cURL (Terminal):**
```bash
curl -X GET [http://127.0.0.1:8000/api/grades/](http://127.0.0.1:8000/api/grades/) \
     -H "Authorization: Bearer tu_access_token_aqui"
```


## Autor y Contacto

Desarrollado por **Elihú Natanael** bajo la firma de **Natcore Tech**.

Este proyecto fue construido y estructurado desde cero como parte de mi formación académica en la Universidad Tecnológica Equinoccial (UTE). La intención de este repositorio es demostrar la implementación de buenas prácticas en arquitecturas backend, seguridad de APIs y bases de datos relacionales.

Siéntete libre de hacer un fork, clonar el proyecto o usarlo como base para tus propias prácticas de laboratorio. Si encuentras algún bug (esperemos que no explote nada) o tienes sugerencias para optimizar el código, ¡los pull requests son totalmente bienvenidos!

---
*El código es como el humor: cuando tienes que explicarlo, es porque algo salió mal.*


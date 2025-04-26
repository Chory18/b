# API de Tienda con Flask

API RESTful para gestionar una tienda en línea, desarrollada con Flask y SQLAlchemy.

## Características

- Autenticación JWT
- Gestión de usuarios
- Gestión de categorías
- Gestión de productos
- Base de datos MySQL
- API RESTful

## Requisitos

- Python 3.8+
- MySQL
- pip

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/TU_USUARIO/tienda-api.git
cd tienda-api
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
Crear un archivo `.env` con las siguientes variables:
```
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost/tienda
SECRET_KEY=tu-secreto-super-seguro
```

5. Inicializar la base de datos:
```sql
CREATE DATABASE tienda;
USE tienda;

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

6. Ejecutar la aplicación:
```bash
python main.py
```

## Endpoints

### Autenticación
- `POST /api/login` - Iniciar sesión

### Categorías
- `GET /api/categorias` - Listar categorías
- `GET /api/categorias/<id>` - Obtener categoría
- `POST /api/categorias` - Crear categoría
- `PUT /api/categorias/<id>` - Actualizar categoría
- `DELETE /api/categorias/<id>` - Eliminar categoría

### Productos
- `GET /api/productos` - Listar productos
- `GET /api/productos/<id>` - Obtener producto
- `POST /api/productos` - Crear producto
- `PUT /api/productos/<id>` - Actualizar producto
- `DELETE /api/productos/<id>` - Eliminar producto

### Usuarios
- `GET /api/usuarios` - Listar usuarios
- `GET /api/usuarios/<id>` - Obtener usuario
- `POST /api/usuarios` - Crear usuario
- `PUT /api/usuarios/<id>` - Actualizar usuario
- `DELETE /api/usuarios/<id>` - Eliminar usuario

## Ejemplos de uso

### Crear un usuario
```bash
curl -X POST http://localhost:5000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan Pérez", "correo": "juan@example.com", "contraseña": "123456"}'
```

### Iniciar sesión
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"correo": "juan@example.com", "contraseña": "123456"}'
```

### Crear una categoría
```bash
curl -X POST http://localhost:5000/api/categorias \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_JWT" \
  -d '{"nombre": "Electrónicos"}'
```

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 
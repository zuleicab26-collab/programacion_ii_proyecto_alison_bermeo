# Concesionaria de motos

Aplicación web en Django para gestionar marcas, motos, clientes y ventas,
con autenticación y control de acceso por grupos.

## Requisitos
- Python 3.10 o superior
- Git

## Instalación

1. Clonar el repositorio y entrar en la carpeta:
   ```
   https://github.com/zuleicab26-collab/programacion_ii_proyecto_alison_bermeo.git
   programacion_ii_proyecto_alison_bermeo
   ```
2. Crear y activar el entorno virtual:
   ```
   python -m venv venv
   venv\Scripts\activate          (Windows)
   source venv/bin/activate       (Linux / Mac)
   ```
3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Crear la base de datos:
   ```
   python manage.py migrate
   ```
5. Cargar grupos, usuarios y datos de prueba:
   ```
   python manage.py cargar_datos
   ```
6. Iniciar el servidor:
   ```
   python manage.py runserver
   ```
   Abrir http://127.0.0.1:8000/

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | Admin12345 | Superusuario (también entra a /admin/) |
| gerente | Gerente12345 | Grupo administradores |
| vendedor | Vendedor12345 | Grupo vendedores |

## Grupos y permisos

| Grupo | Puede | No puede |
|---|---|---|
| administradores | Crear, editar y eliminar en las 4 entidades (marcas, clientes, motos y ventas) | — |
| vendedores | Ver todo; crear clientes; crear ventas, y editar o eliminar solo las que registró | Crear o modificar marcas y motos; editar o eliminar ventas ajenas; editar o eliminar clientes |

Los usuarios que se registran en `/registro/` entran al grupo vendedores.

## Regla de propiedad
Una venta solo puede ser editada o eliminada por quien la creó o por un administrador. Se aplica en la vista (responde 403) y en la plantilla (oculta los botones).

En los datos de prueba, las ventas #3 y #4 las registró `gerente`, por lo que el usuario `vendedor` no puede modificarlas.

## Estructura
Un archivo por entidad en `models/`, `forms/`, `views/` y `urls/`, con
`__init__.py` que re-exportan. Las plantillas usan doble carpeta:
`concesionaria/templates/concesionaria/<entidad>/`.

Los estilos están en `concesionaria/static/concesionaria/css/estilos.css`
(CSS propio, sin frameworks externos).

## Comandos de gestión
- `python manage.py crear_grupos`: crea los grupos y sus permisos.
- `python manage.py cargar_datos`: crea grupos, usuarios y datos de prueba
  (se puede ejecutar varias veces sin duplicar).
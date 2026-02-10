# Práctica 3.1: Desarrollo de una API REST con FastAPI

**Nombre.** Sofía Rodríguez Ramírez

## Dominio de datos elegido
La API trata sobre una videojuegos y sus plataformas

En cada videojuego hay estos campos:

- id (entero, generado automáticamente)

- nombre (texto)

- genero (texto)

- precio (float, mayor que 0)

- plataformas (lista de textos)

- fecha_lanzamiento (fecha)

En cada lataforma hay estos campos:

- id (entero, generado automáticamente)

- nombre (texto)

- descripcion (texto)

- precio (float, mayor que 0)

- empresa que lo sacó al mercado (texto)

- fecha de lanzamiento (fecha)

- Si la tengo en mi colección (boolean)

Cabe resaltar que hay una tabla de asociación entre videojuegos y plataformas, ya que solo se podrán añadir videojuegos de una plataforma que haya sido registrada anteriormente

He elegido este dominio porque me parece interesante poder tener información de manera rápida como el precio o las plataformas disponibles sobre los videojuegos, además puede ser útil para otra práctica en un futuro.

## Cómo ejecutar el servidor FastAPI

1. **Crear el entorno virtual** (Solo se hace una vez): python -m venv .venv

2. **Activar el entorno virtual** (Se debe hacer siempre que vayamos a usar la API): .venv\Scripts\Activate.ps1 (Este comando es para Powershell)

3. **Instalar dependencias:** pip install -r requirements.txt

4. **Ejecutar el servidor:** fastapi dev main.py


## Documentación:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

## Link de web pública en render
https://videogames-api-52uc.onrender.com/

# Demo_Task -- Práctica Python

Este proyecto consiste en desarrollar un sistema de gestión de tareas para una empresa, permitiendo administrar las tareas pendientes de los empleados mediante una aplicación de consola en Python.

El sistema permite registrar tareas, consultar las existentes, buscar tareas por responsable, actualizar estados y obtener estadísticas generales del trabajo realizado.

El objetivo principal es poner en práctica estructuras de datos fundamentales de Python, así como conceptos de programación modular, control de flujo y manejo de errores.

## Requisitos

- Python 3.
- No requiere bibliotecas externas ni base de datos.

## Ejecución

Desde la carpeta raíz del proyecto, ejecuta:

```bash
python3 codigo/Control_task.py
```

## Opciones del menú

1. Registrar una tarea con descripción, responsable y prioridad (Alta, Media o Baja). Las nuevas tareas comienzan como Pendiente.
2. Mostrar todas las tareas en columnas, ordenadas por prioridad.
3. Buscar tareas por nombre del responsable. La búsqueda no distingue mayúsculas y minúsculas y acepta coincidencias parciales.
4. Cambiar el estado de una tarea seleccionándola por ID (Pendiente, En progreso o Finalizada).
5. Consultar el total de tareas, cantidades por estado y porcentaje finalizado.
6. Mostrar únicamente las tareas pendientes.
7. Salir.

Las tareas se almacenan en `codigo/tareas.json`, junto al programa. El archivo se crea al registrar la primera tarea y se actualiza al cambiar un estado; al iniciar, el programa carga las tareas guardadas para conservarlas entre ejecuciones.

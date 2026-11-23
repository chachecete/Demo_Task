"""Gestor de tareas de empleados para uso exclusivo en consola."""

import json
from pathlib import Path


PRIORIDADES = ("Alta", "Media", "Baja")
ESTADOS = ("Pendiente", "En progreso", "Finalizada")
ORDEN_PRIORIDAD = {"Alta": 1, "Media": 2, "Baja": 3}
ARCHIVO_TAREAS = Path(__file__).with_name("tareas.json")


def cargar_tareas():
    """Carga las tareas guardadas o devuelve una lista vacía si aún no existen."""
    try:
        tareas = json.loads(ARCHIVO_TAREAS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            f"El archivo {ARCHIVO_TAREAS} contiene JSON inválido "
            f"(línea {error.lineno})."
        ) from error

    if not isinstance(tareas, list):
        raise ValueError(f"El contenido de {ARCHIVO_TAREAS} debe ser una lista.")

    ids = set()
    campos = {"id", "descripcion", "responsable", "prioridad", "estado"}
    for indice, tarea in enumerate(tareas, start=1):
        if not isinstance(tarea, dict) or not campos.issubset(tarea):
            raise ValueError(f"La tarea número {indice} tiene un formato inválido.")
        if type(tarea["id"]) is not int or tarea["id"] < 1 or tarea["id"] in ids:
            raise ValueError(f"La tarea número {indice} tiene un ID inválido o duplicado.")
        if not isinstance(tarea["descripcion"], str) or not tarea["descripcion"].strip():
            raise ValueError(f"La descripción de la tarea número {indice} no es válida.")
        if not isinstance(tarea["responsable"], str) or not tarea["responsable"].strip():
            raise ValueError(f"El responsable de la tarea número {indice} no es válido.")
        if tarea["prioridad"] not in PRIORIDADES or tarea["estado"] not in ESTADOS:
            raise ValueError(f"La prioridad o el estado de la tarea número {indice} no es válido.")
        ids.add(tarea["id"])

    return tareas


def guardar_tareas(tareas):
    """Guarda todas las tareas en un archivo JSON local."""
    archivo_temporal = ARCHIVO_TAREAS.with_suffix(".tmp")
    try:
        archivo_temporal.write_text(
            json.dumps(tareas, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        archivo_temporal.replace(ARCHIVO_TAREAS)
    except OSError as error:
        raise OSError(f"No se pudieron guardar las tareas en {ARCHIVO_TAREAS}: {error}") from error


def solicitar_opcion(mensaje, opciones):
    """Solicita una opción numérica perteneciente a las opciones permitidas."""
    while True:
        try:
            opcion = int(input(mensaje))
            if opcion in opciones:
                return opcion
            print(f"Selecciona un número entre {min(opciones)} y {max(opciones)}.")
        except ValueError:
            print("Entrada no válida. Escribe un número.")


def mostrar_tabla(tareas):
    """Imprime las tareas en columnas."""
    if not tareas:
        print("No hay tareas para mostrar.")
        return

    columnas = (
        ("ID", 5),
        ("Descripción", 36),
        ("Responsable", 22),
        ("Prioridad", 12),
        ("Estado", 16),
    )
    separador = "+-" + "-+-".join("-" * ancho for _, ancho in columnas) + "-+"

    print(separador)
    print("| " + " | ".join(nombre.ljust(ancho) for nombre, ancho in columnas) + " |")
    print(separador)
    for tarea in tareas:
        valores = (
            str(tarea["id"]),
            tarea["descripcion"],
            tarea["responsable"],
            tarea["prioridad"],
            tarea["estado"],
        )
        celdas = [
            valor if len(valor) <= ancho else valor[: ancho - 3] + "..."
            for valor, (_, ancho) in zip(valores, columnas)
        ]
        print("| " + " | ".join(valor.ljust(ancho) for valor, (_, ancho) in zip(celdas, columnas)) + " |")
    print(separador)


def registrar_tarea(tareas, siguiente_id):
    """Pide los datos y agrega una tarea a la lista."""
    while True:
        descripcion = input("Descripción: ").strip()
        if descripcion:
            break
        print("La descripción no puede estar vacía.")

    while True:
        responsable = input("Responsable: ").strip()
        if responsable:
            break
        print("El responsable no puede estar vacío.")

    print("\nPrioridad:")
    for numero, prioridad in enumerate(PRIORIDADES, start=1):
        print(f"{numero}. {prioridad}")
    prioridad = PRIORIDADES[solicitar_opcion("Selecciona la prioridad: ", range(1, 4)) - 1]

    tareas.append(
        {
            "id": siguiente_id,
            "descripcion": descripcion,
            "responsable": responsable,
            "prioridad": prioridad,
            "estado": ESTADOS[0],
        }
    )
    try:
        guardar_tareas(tareas)
    except OSError as error:
        tareas.pop()
        print(error)
        return siguiente_id

    print(f"Tarea {siguiente_id} registrada correctamente.")
    return siguiente_id + 1


def mostrar_tareas(tareas):
    """Muestra todas las tareas, ordenadas de mayor a menor prioridad."""
    tareas_ordenadas = sorted(tareas, key=lambda tarea: ORDEN_PRIORIDAD[tarea["prioridad"]])
    mostrar_tabla(tareas_ordenadas)


def buscar_por_responsable(tareas):
    """Busca y muestra tareas asociadas al nombre de un responsable."""
    nombre = input("Nombre del responsable: ").strip().casefold()
    if not nombre:
        print("Debes escribir un nombre para realizar la búsqueda.")
        return

    resultados = [
        tarea
        for tarea in tareas
        if nombre in tarea["responsable"].casefold()
    ]
    mostrar_tabla(resultados)


def mostrar_pendientes(tareas):
    """Filtra las tareas pendientes mediante una comprensión de listas."""
    pendientes = [tarea for tarea in tareas if tarea["estado"] == "Pendiente"]
    mostrar_tabla(pendientes)


def cambiar_estado(tareas):
    """Busca una tarea por ID y permite actualizar su estado."""
    if not tareas:
        print("No hay tareas registradas.")
        return

    try:
        id_tarea = int(input("ID de la tarea que deseas actualizar: "))
    except ValueError:
        print("ID no válido. Escribe un número.")
        return

    tarea = next((elemento for elemento in tareas if elemento["id"] == id_tarea), None)
    if tarea is None:
        print(f"No existe una tarea con el ID {id_tarea}.")
        return

    print(f"Estado actual: {tarea['estado']}")
    for numero, estado in enumerate(ESTADOS, start=1):
        print(f"{numero}. {estado}")
    nuevo_estado = ESTADOS[solicitar_opcion("Selecciona el nuevo estado: ", range(1, 4)) - 1]
    estado_anterior = tarea["estado"]
    tarea["estado"] = nuevo_estado
    try:
        guardar_tareas(tareas)
    except OSError as error:
        tarea["estado"] = estado_anterior
        print(error)
        return

    print(f"El estado de la tarea {id_tarea} ahora es «{nuevo_estado}».")


def mostrar_estadisticas(tareas):
    """Calcula y presenta el resumen de estados de las tareas."""
    total = len(tareas)
    pendientes = sum(tarea["estado"] == "Pendiente" for tarea in tareas)
    en_progreso = sum(tarea["estado"] == "En progreso" for tarea in tareas)
    finalizadas = sum(tarea["estado"] == "Finalizada" for tarea in tareas)
    porcentaje_finalizadas = (finalizadas / total * 100) if total else 0

    print("\n--- Estadísticas ---")
    print(f"Cantidad total de tareas:       {total}")
    print(f"Cantidad de tareas pendientes:  {pendientes}")
    print(f"Cantidad en progreso:           {en_progreso}")
    print(f"Cantidad finalizadas:           {finalizadas}")
    print(f"Porcentaje finalizadas:         {porcentaje_finalizadas:.2f}%")


def main():
    """Ejecuta el menú principal del gestor."""
    try:
        tareas = cargar_tareas()
    except (OSError, ValueError) as error:
        print(f"No se pudieron cargar las tareas: {error}")
        return

    siguiente_id = max((tarea["id"] for tarea in tareas), default=0) + 1

    while True:
        print(
            "\n=== Gestor de tareas ===\n"
            "1. Registrar una tarea\n"
            "2. Mostrar todas las tareas\n"
            "3. Buscar tareas por responsable\n"
            "4. Cambiar estado de una tarea\n"
            "5. Mostrar estadísticas\n"
            "6. Mostrar tareas pendientes\n"
            "7. Salir"
        )
        opcion = solicitar_opcion("Selecciona una opción: ", range(1, 8))

        if opcion == 1:
            siguiente_id = registrar_tarea(tareas, siguiente_id)
        elif opcion == 2:
            mostrar_tareas(tareas)
        elif opcion == 3:
            buscar_por_responsable(tareas)
        elif opcion == 4:
            cambiar_estado(tareas)
        elif opcion == 5:
            mostrar_estadisticas(tareas)
        elif opcion == 6:
            mostrar_pendientes(tareas)
        else:
            print("Hasta luego.")
            break


if __name__ == "__main__":
    main()
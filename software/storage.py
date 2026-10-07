import csv
import shutil

from config import (PROGRESS_FILE,RESULTS_DIR,CLASS_FOLDERS,VALID_EXTENSIONS,)

def guardar_etiquetas(etiquetas):
    PROGRESS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with PROGRESS_FILE.open(
        mode="w",
        newline="",
        encoding="utf-8-sig",
    ) as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["nombre", "etiqueta"])

        for nombre, etiqueta in sorted(etiquetas.items()):
            escritor.writerow([nombre, etiqueta])


def cargar_etiquetas(rutas_imagenes):
    etiquetas = {}

    if not PROGRESS_FILE.exists():
        return etiquetas

    nombres_validos = {
        ruta.name
        for ruta in rutas_imagenes
    }

    with PROGRESS_FILE.open(
        mode="r",
        newline="",
        encoding="utf-8-sig",
    ) as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            nombre = fila["nombre"]
            etiqueta = fila["etiqueta"]

            if nombre not in nombres_validos or not etiqueta:
                continue

            etiquetas[nombre] = etiqueta

    return etiquetas


def exportar_resultados(etiquetas, rutas_imagenes):
    rutas_por_nombre = {
        ruta.name: ruta
        for ruta in rutas_imagenes
    }

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    carpetas_clases = {}

    for etiqueta, nombre_carpeta in CLASS_FOLDERS.items():
        carpeta_clase = RESULTS_DIR / nombre_carpeta

        carpeta_clase.mkdir(
            parents=True,
            exist_ok=True,
        )

        carpetas_clases[etiqueta] = carpeta_clase

        for archivo in carpeta_clase.iterdir():
            if (
                archivo.is_file()
                and archivo.suffix.lower() in VALID_EXTENSIONS
            ):
                archivo.unlink()

    for nombre, etiqueta in etiquetas.items():
        origen = rutas_por_nombre[nombre]
        destino = carpetas_clases[etiqueta] / nombre

        shutil.copy2(origen, destino)

    ruta_csv = RESULTS_DIR / "etiquetas_galaxias.csv"

    with ruta_csv.open(
        mode="w",
        newline="",
        encoding="utf-8-sig",
    ) as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["nombre", "etiqueta"])

        for nombre, etiqueta in sorted(etiquetas.items()):
            escritor.writerow([nombre, etiqueta])

    return RESULTS_DIR
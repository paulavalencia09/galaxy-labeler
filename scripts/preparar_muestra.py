from pathlib import Path
from zipfile import ZipFile
import random
from PIL import Image, UnidentifiedImageError
import shutil

#Obtener imágenes zip

def obtener_imagenes(zip_path):
    with ZipFile(zip_path, 'r') as zf:
        #Extraer 30 archivos aleatorios del archivo zip
        zip_names = zf.namelist()

        print(f"Archivos dentro del ZIP: {len(zip_names)}")
        imagenes = []

        for info in zf.infolist():
            # Ignorar las carpetas internas del ZIP
            if info.is_dir():
                continue

            nombre = info.filename
            extension = Path(nombre).suffix.lower()

            # Guardar solamente archivos JPG o JPEG
            if extension == ".jpg" or extension == ".jpeg":
                imagenes.append(nombre)

    imagenes.sort(key=lambda nombre: int(Path(nombre).stem))

    return imagenes

#------------------------------------------------------------------

def seleccionar_img(imagenes,SEED, SAMPLE_SIZE):
    imagenes_mezcladas = imagenes.copy()

    generador = random.Random(SEED)
    generador.shuffle(imagenes_mezcladas)

    muestra_piloto = imagenes_mezcladas[:SAMPLE_SIZE]

    print(f"Imágenes seleccionadas: {len(muestra_piloto)}")

    for nombre in muestra_piloto:
        print(Path(nombre).name)

    return muestra_piloto

#------------------------------------------------------------------

def validar_img(muestra_piloto, zip_path):
    imagenes_validas = []
    imagenes_invalidas = []

    with ZipFile(zip_path, mode="r") as archivo_zip:
        for nombre in muestra_piloto:
            try:
                with archivo_zip.open(nombre) as archivo:
                    with Image.open(archivo) as imagen:
                        imagen.verify()

                imagenes_validas.append(nombre)

            except (UnidentifiedImageError, OSError, KeyError) as error:
                imagenes_invalidas.append((nombre, str(error)))

    print(f"Imágenes revisadas: {len(muestra_piloto)}")
    print(f"Imágenes válidas: {len(imagenes_validas)}")
    print(f"Imágenes inválidas: {len(imagenes_invalidas)}")

    return imagenes_validas

#------------------------------------------------------------------

def extraer_img(carpeta_test, zip_path, imagenes_validas):
    carpeta_test.mkdir(parents=True, exist_ok=True)

    extraidas = []

    with ZipFile(zip_path, mode="r") as archivo_zip:
        for nombre_interno in imagenes_validas:
            nombre_archivo = Path(nombre_interno).name
            destino = carpeta_test / nombre_archivo

            if destino.exists():
                print(f"Ya existe, se omite: {nombre_archivo}")
                continue

            with archivo_zip.open(nombre_interno) as origen:
                with destino.open("wb") as salida:
                    shutil.copyfileobj(origen, salida)

            extraidas.append(destino)

    imagenes_en_carpeta = list(carpeta_test.glob("*.jpg"))

    print(f"Imágenes extraídas ahora: {len(extraidas)}")
    print(f"Total en carpeta test: {len(imagenes_en_carpeta)}")
    print(f"Destino: {carpeta_test}")

    #------------------------------------------------------------------

def main():

    ZIP_PATH = "data/raw/images_test_rev1.zip"
    OUTPUT_DIR = "data/img"
    SAMPLE_SIZE = 350
    SEED = 20261005

    zip_path = Path(ZIP_PATH).resolve()
    carpeta_test = Path(OUTPUT_DIR).resolve()

    imagenes = obtener_imagenes(zip_path)
    muestra_piloto = seleccionar_img(imagenes, SEED, SAMPLE_SIZE)
    imagenes_validas = validar_img(muestra_piloto, zip_path)
    extraer_img(carpeta_test, zip_path, imagenes_validas)

    #------------------------------------------------------------------

if __name__ == "__main__":
    main()
from pathlib import Path
from zipfile import ZipFile
import random
from PIL import Image, UnidentifiedImageError
import shutil
import hashlib
from io import BytesIO

#Obtener imágenes zip

def obtener_imagenes(zip_path):
    with ZipFile(zip_path, 'r') as zf:
        #Extraer 350 archivos aleatorios del archivo zip
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

def seleccionar_img(imagenes,SEED):
    imagenes_mezcladas = imagenes.copy()

    generador = random.Random(SEED)
    generador.shuffle(imagenes_mezcladas)

    return imagenes_mezcladas

#------------------------------------------------------------------

def validar_img(imagenes_candidatas,zip_path,sample_size,):
    imagenes_validas = []
    imagenes_invalidas = []
    imagenes_duplicadas = []

    hashes_encontrados = {}

    with ZipFile(zip_path, mode="r") as archivo_zip:
        for nombre in imagenes_candidatas:
            if len(imagenes_validas) == sample_size:
                break

            try:
                datos = archivo_zip.read(nombre)

                hash_imagen = hashlib.sha256(datos).hexdigest()

                if hash_imagen in hashes_encontrados:
                    imagenes_duplicadas.append((nombre,hashes_encontrados[hash_imagen],))
                    continue

                with Image.open(BytesIO(datos)) as imagen:
                    imagen.verify()

                hashes_encontrados[hash_imagen] = nombre
                imagenes_validas.append(nombre)

            except (UnidentifiedImageError,OSError,KeyError,) as error:
                imagenes_invalidas.append((nombre, str(error)))

    print(f"Imágenes válidas: {len(imagenes_validas)}")
    print(f"Imágenes inválidas: {len(imagenes_invalidas)}")
    print(f"Duplicados exactos: "f"{len(imagenes_duplicadas)}")

    if len(imagenes_validas) < sample_size:
        raise RuntimeError(f"No fue posible obtener {sample_size} ""imágenes válidas y únicas.")

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

    imagenes_en_carpeta = [archivo for archivo in carpeta_test.iterdir() if archivo.is_file() and archivo.suffix.lower() in {".jpg", ".jpeg"}]

    if len(imagenes_en_carpeta) != len(imagenes_validas):
        raise RuntimeError(
            "La cantidad final de archivos no coincide "
            "con la muestra validada.")

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
    imagenes_candidatas = seleccionar_img(imagenes,SEED,)

    imagenes_validas = validar_img(imagenes_candidatas,zip_path,SAMPLE_SIZE,)
    extraer_img(carpeta_test, zip_path, imagenes_validas)

    #------------------------------------------------------------------

if __name__ == "__main__":
    main()
# Galaxy Labeler

Aplicación de escritorio para etiquetar manualmente imágenes de galaxias y generar un dataset clasificado en formato CSV, acompañado de carpetas organizadas por clase.

## Integrante

- Paula Valencia — [@paulavalencia09](https://github.com/paulavalencia09)

## Objetivo

Galaxy Labeler permite construir un dataset etiquetado para un problema de clasificación morfológica de galaxias. La aplicación muestra una imagen a la vez y permite asignarle una de cinco clases:

- Elíptica
- Lenticular
- Espiral
- Irregular
- No clasificable

El software fue desarrollado para trabajar con una muestra de 350 imágenes obtenidas de [Galaxy Zoo: The Galaxy Challenge](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge). El etiquetado generado puede utilizarse posteriormente en la exploración de datos y en el entrenamiento de modelos de clasificación de imágenes.

> Las imágenes del dataset no se incluyen en este repositorio. Deben descargarse directamente desde Kaggle, respetando sus condiciones de acceso y uso.

## Funcionalidades

- Selección de una carpeta local de imágenes.
- Compatibilidad con archivos `.jpg`, `.jpeg` y `.png`.
- Visualización individual de cada galaxia.
- Navegación circular entre imágenes mediante botones anterior y siguiente.
- Avance automático después de asignar una etiqueta.
- Inicio desde la primera imagen que aún no ha sido clasificada.
- Modificación o eliminación de una etiqueta existente.
- Tabla paginada con seis registros por página.
- Acciones para mostrar una imagen de la tabla o eliminar su clasificación.
- Contador de imágenes etiquetadas respecto del total cargado.
- Guardado automático del progreso en un archivo CSV local.
- Recuperación del progreso al volver a abrir la aplicación.
- Eliminación completa del progreso mediante confirmación.
- Exportación de un CSV con las columnas `nombre` y `etiqueta`.
- Copia de las imágenes etiquetadas a carpetas separadas por clase.

## Requisitos

El proyecto fue desarrollado y probado con:

- Python 3.14.5
- CustomTkinter 6.0.0
- Pillow 12.3.0
- Darkdetect 0.8.0
- Packaging 26.3
- Tkinter, incluido con la instalación estándar de Python para Windows

Las versiones exactas se encuentran en [`requirements.txt`](requirements.txt).

## Instalación

### 1. Clonar el repositorio

```powershell
git clone https://github.com/paulavalencia09/galaxy-labeler.git
cd galaxy-labeler
```

### 2. Crear un entorno virtual

En Windows PowerShell:

```powershell
python -m venv label_env
.\label_env\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
python3 -m venv label_env
source label_env/bin/activate
```

### 3. Instalar las dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Preparación del dataset

La aplicación puede trabajar con cualquier carpeta que contenga imágenes compatibles. Para reproducir la muestra utilizada en el proyecto:

1. Iniciar sesión en Kaggle y acceder a [Galaxy Zoo: The Galaxy Challenge](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge/data).
2. Descargar el archivo `images_test_rev1.zip`.
3. Crear la carpeta `data/raw/` en la raíz del repositorio.
4. Guardar el ZIP con esta ruta exacta:

```text
data/raw/images_test_rev1.zip
```

5. Con el entorno virtual activado, ejecutar desde la raíz del repositorio:

```powershell
python .\scripts\preparar_muestra.py
```

El script:

- Busca imágenes JPG y JPEG dentro del ZIP.
- Mezcla los registros con una semilla fija para obtener una muestra reproducible.
- Verifica que cada imagen pueda abrirse correctamente con Pillow.
- Detecta archivos duplicados exactos mediante SHA-256.
- Descarta imágenes inválidas o repetidas.
- Extrae 350 imágenes válidas y únicas en `data/img/`.

La semilla utilizada es `20261005`.

## Ejecución

Desde la raíz del repositorio y con el entorno virtual activado:

```powershell
python .\software\main.py
```

La aplicación se abrirá sin cargar imágenes automáticamente.

## Uso

1. Presionar **Seleccionar carpeta**.
2. Elegir la carpeta que contiene las imágenes, por ejemplo `data/img/`.
3. Verificar que la ruta, el nombre de la imagen y el contador aparezcan en la interfaz.
4. Examinar la galaxia mostrada.
5. Seleccionar una de las cinco etiquetas disponibles.
6. La clasificación se guardará automáticamente y la aplicación avanzará a la imagen siguiente.
7. Utilizar los botones laterales para recorrer las imágenes manualmente cuando sea necesario.
8. Revisar las clasificaciones en la tabla inferior:
   - El botón celeste muestra la imagen correspondiente.
   - La `X` rosada elimina su clasificación.
9. Utilizar **Borrar etiqueta** para quitar la clasificación de la imagen actual.
10. Utilizar **Borrar todo** solamente si se desea eliminar todo el progreso guardado.
11. Presionar **Exportar CSV** para generar el archivo final y las carpetas por clase.
12. Para finalizar, cerrar normalmente la ventana. No es necesario guardar manualmente.

Si la carpeta seleccionada no contiene imágenes compatibles, la interfaz mostrará un mensaje y no intentará cargar una imagen.

## Guardado del progreso

El progreso se guarda automáticamente en:

```text
db/progreso_etiquetas.csv
```

El archivo se actualiza al asignar, modificar o eliminar etiquetas. Al seleccionar nuevamente la carpeta de imágenes, la aplicación recupera las clasificaciones cuyos nombres coincidan con archivos existentes.

Este archivo representa estado local de ejecución y está excluido del repositorio mediante `.gitignore`.

## Exportación

Al presionar **Exportar CSV**, la aplicación crea la siguiente estructura:

```text
resultados/
├── etiquetas_galaxias.csv
├── eliptica/
├── lenticular/
├── espiral/
├── irregular/
└── no_clasificable/
```

El archivo `etiquetas_galaxias.csv` contiene:

```csv
nombre,etiqueta
101011.jpg,Espiral
101780.jpg,Lenticular
```

Las imágenes originales no se mueven ni se eliminan. La aplicación crea copias dentro de la carpeta correspondiente a cada clase. Las exportaciones anteriores de esas carpetas se reemplazan al realizar una nueva exportación.

## Estructura del proyecto

```text
galaxy-labeler/
├── scripts/
│   └── preparar_muestra.py
├── software/
│   ├── widgets/
│   │   ├── __init__.py
│   │   └── label_table.py
│   ├── app.py
│   ├── config.py
│   ├── img_effects.py
│   ├── main.py
│   └── storage.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

### Responsabilidad de los módulos

- `main.py`: punto de entrada de la aplicación.
- `app.py`: ventana principal, flujo de etiquetado y coordinación de componentes.
- `config.py`: rutas, clases, extensiones y colores compartidos.
- `img_effects.py`: generación de degradados y efectos de iluminación con Pillow.
- `storage.py`: lectura del progreso, escritura de CSV y exportación de resultados.
- `widgets/label_table.py`: tabla personalizada y paginada de clasificaciones.
- `scripts/preparar_muestra.py`: selección, validación y extracción reproducible de la muestra.

## Consideraciones

- La clasificación es manual y puede contener decisiones subjetivas.
- La clase **No clasificable** debe utilizarse cuando la morfología no pueda determinarse con suficiente seguridad.
- El programa etiqueta imágenes; no permite editar ni eliminar los archivos originales de la carpeta seleccionada.
- El nombre `test` corresponde al rol original de las imágenes en la competencia de Kaggle. Después del etiquetado, cualquier proyecto de aprendizaje automático debe crear sus propias particiones de entrenamiento, validación y prueba.
- Las carpetas `data/`, `db/` y `resultados/` contienen datos locales o generados y no se publican en Git.

## Licencia

El código de este proyecto se distribuye bajo la licencia MIT. Consulta [`LICENSE`](LICENSE) para más información.

from pathlib import Path

VALID_EXTENSIONS = [".jpg", ".jpeg", ".png"]
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROGRESS_FILE = PROJECT_ROOT / "db" / "progreso_etiquetas.csv"
RESULTS_DIR = PROJECT_ROOT / "resultados"

CLASS_FOLDERS = {
    "Elíptica": "eliptica",
    "Lenticular": "lenticular",
    "Espiral": "espiral",
    "Irregular": "irregular",
    "No clasificable": "no_clasificable",
}

#-----------------------------------------------------------------------------
COLOR_FONDO = "#080617"
COLOR_SUPERFICIE = "#14102E"
COLOR_PRIMARIO = "#7C3AED"
COLOR_PRIMARIO_HOVER = "#9333EA"
COLOR_CELESTE = "#38BDF8"
COLOR_ROSADO = "#EC4899"
COLOR_TEXTO = "#F8FAFC"
COLOR_TEXTO_SECUNDARIO = "#8F8AA8"
COLOR_PELIGRO = "#F43F5E"
COLOR_BORDE = "#4C1D95"

COLOR_GLOW_EXTERIOR = "#4C1D95"
COLOR_GLOW_MEDIO = "#8B5CF6"
COLOR_GLOW_CLARO = "#D8B4FE"

COLORES_ETIQUETAS = {
    "Elíptica": ("#123A5A", "#38BDF8"),
    "Lenticular": ("#3B2A68", "#C4B5FD"),
    "Espiral": ("#4C1D95", "#D8B4FE"),
    "Irregular": ("#701A4F", "#F9A8D4"),
    "No clasificable": ("#1F2937", "#8F8AA8"),
}

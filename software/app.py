from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFilter, ImageColor
import csv
import shutil


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


#-----------------------------------------------------------------------------

class GalaxyLabeler(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Galaxy Labeler")
        self.geometry("900x800")

        self.configure(fg_color=COLOR_FONDO)
        self.minsize(800, 700)

        self.rutas_imagenes = []
        self.indice_actual = 0
        self.etiquetas = {}
        self.etiqueta_actual = ctk.StringVar(value="")
        self.ruta_carpeta = ctk.StringVar(value="")

        self.contenido = ctk.CTkScrollableFrame(self,fg_color=COLOR_FONDO,corner_radius=0,scrollbar_button_color=COLOR_BORDE,scrollbar_button_hover_color=COLOR_PRIMARIO,)
        self.contenido.pack(fill="both",expand=True,)

        self.title_labeler = ctk.CTkLabel(self.contenido,text="✧  Galaxy Labeler  ✧",text_color=COLOR_TEXTO,font=ctk.CTkFont(family="Segoe UI",size=28,weight="bold",),)
        self.title_labeler.pack(pady=(24, 2),)

        self.estado = ctk.CTkLabel(
        self.contenido,text="No se ha seleccionado ninguna carpeta.",text_color=COLOR_TEXTO_SECUNDARIO,font=ctk.CTkFont(family="Segoe UI",size=11,),)
        self.estado.pack(pady=(0, 14),)

        self.frame_carpeta = ctk.CTkFrame(self.contenido,fg_color="transparent",)
        self.frame_carpeta.pack(fill="x",padx=32,pady=(4, 14),)

        self.boton_carpeta = ctk.CTkButton(self.frame_carpeta,
                            text="▣  Seleccionar carpeta",
                            command=self.seleccionar_carpeta,
                            width=155,
                            height=34,
                            corner_radius=8,
                            fg_color=COLOR_PRIMARIO,
                            hover_color=COLOR_PRIMARIO_HOVER,
                            text_color=COLOR_TEXTO,
                            font=ctk.CTkFont(
                                family="Segoe UI",
                                size=12,
                                weight="bold",),)
        self.boton_carpeta.pack(side="left",padx=(0, 12),)

        self.input_carpeta = ctk.CTkEntry(self.frame_carpeta,
            textvariable=self.ruta_carpeta,
            state="disabled",
            height=34,
            corner_radius=7,
            fg_color=COLOR_SUPERFICIE,
            border_color=COLOR_BORDE,
            border_width=1,
            text_color=COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,),)
        self.input_carpeta.pack(side="left",fill="x",expand=True,)

        self.nombre_imagen = ctk.CTkLabel(self.contenido,
            text="",
            text_color="#D8B4FE",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=18,
                weight="bold",),
                )
        self.nombre_imagen.pack(pady=(4, 10),)



        self.frame_visualizador = ctk.CTkFrame(self.contenido,fg_color="transparent",)
        self.frame_visualizador.pack(pady=(4, 14),)



        #-----------------------------------------------------------------------------

        self.seccion_etiqueta = ctk.CTkFrame(self.contenido,fg_color="transparent",)
        self.seccion_etiqueta.pack(pady=(10, 0))

        self.label_etiqueta = ctk.CTkLabel(self.seccion_etiqueta,
                                text="ETIQUETA",
                                text_color=COLOR_TEXTO_SECUNDARIO,
                                font=ctk.CTkFont(
                                        family="Segoe UI",
                                        size=10,
                                        weight="bold",),)
        self.label_etiqueta.pack(anchor="w",pady=(10, 0),)

        self.frame_etiquetas_actual = ctk.CTkFrame(self.seccion_etiqueta,fg_color="transparent",)
        self.frame_etiquetas_actual.pack(pady=(4,10))
        
        self.campo_etiqueta = ctk.CTkEntry(self.frame_etiquetas_actual,
                            textvariable=self.etiqueta_actual,
                            state="disabled",
                            width=395,
                            height=36,
                            corner_radius=7,
                            fg_color=COLOR_SUPERFICIE,
                            border_color=COLOR_PRIMARIO,
                            border_width=2,
                            text_color="#D8B4FE",)
        self.campo_etiqueta.pack(side="left",padx=5,)
        
        self.boton_borrar = ctk.CTkButton(self.frame_etiquetas_actual,
                            text="✕  Borrar etiqueta",
                            command=self.borrar_etiqueta,
                            width=140,
                            height=34,
                            corner_radius=7,
                            fg_color="#6B164F",
                            hover_color=COLOR_PELIGRO,
                            border_width=1,
                            border_color=COLOR_ROSADO,
                            text_color="#FBCFE8",)
        self.boton_borrar.pack(side="left",padx=5,)

        self.boton_borrar_todo = ctk.CTkButton(self.frame_etiquetas_actual,
                            text="⊘  Borrar todo",
                            command=self.borrar_todo,
                            width=125,
                            height=34,
                            corner_radius=7,
                            fg_color=COLOR_SUPERFICIE,
                            hover_color="#312E5B",
                            border_width=1,
                            border_color=COLOR_BORDE,
                            text_color=COLOR_TEXTO_SECUNDARIO,)
        self.boton_borrar_todo.pack(side="left",padx=5,)

        #-----------------------------------------------------------------------------

        self.seccion_clasificar = ctk.CTkFrame(self.contenido,fg_color="transparent",)
        self.seccion_clasificar.pack(pady=(14, 5))
        
        self.label_clasificar = ctk.CTkLabel(self.seccion_clasificar,
                                text="CLASIFICAR COMO",
                                text_color=COLOR_TEXTO_SECUNDARIO,
                                font=ctk.CTkFont(
                                        family="Segoe UI",
                                        size=10,
                                        weight="bold",),)
        self.label_clasificar.pack(anchor="w",pady=(0, 6),)

        self.frame_etiquetas = ctk.CTkFrame(self.seccion_clasificar,fg_color="transparent",)
        self.frame_etiquetas.pack(pady=(6,5))
        
        self.boton_etiqueta1 = ctk.CTkButton(self.frame_etiquetas,text="Elíptica",command=lambda: self.asignar_etiqueta("Elíptica"),)
        self.boton_etiqueta1.pack(side="left",padx=5)

        self.boton_etiqueta2 = ctk.CTkButton(self.frame_etiquetas,text="Lenticular",command=lambda: self.asignar_etiqueta("Lenticular"),)
        self.boton_etiqueta2.pack(side="left",padx=5)

        self.boton_etiqueta3 = ctk.CTkButton(self.frame_etiquetas,text="Espiral",command=lambda: self.asignar_etiqueta("Espiral"),)
        self.boton_etiqueta3.pack(side="left",padx=5)

        self.boton_etiqueta4 = ctk.CTkButton(self.frame_etiquetas,text="Irregular",command=lambda: self.asignar_etiqueta("Irregular"),)
        self.boton_etiqueta4.pack(side="left",padx=5)

        self.boton_etiqueta5 = ctk.CTkButton(self.frame_etiquetas,text="No clasificable",command=lambda: self.asignar_etiqueta("No clasificable"),)
        self.boton_etiqueta5.pack(side="left",padx=5)

        #------------------estilos------------------------------------

        self.boton_etiqueta1.configure(
                text="Elíptica",
                width=120,
                height=34,
                corner_radius=7,
                fg_color=COLOR_SUPERFICIE,
                hover_color="#123A5A",
                border_width=2,
                border_color=COLOR_CELESTE,
                text_color=COLOR_CELESTE,)

        self.boton_etiqueta2.configure(
                text="Lenticular",
                width=125,
                height=34,
                corner_radius=7,
                fg_color=COLOR_SUPERFICIE,
                hover_color="#3B2A68",
                border_width=2,
                border_color="#A78BFA",
                text_color="#C4B5FD",)

        self.boton_etiqueta3.configure(
                text="Espiral",
                width=120,
                height=34,
                corner_radius=7,
                fg_color=COLOR_SUPERFICIE,
                hover_color="#4C1D95",
                border_width=2,
                border_color=COLOR_PRIMARIO,
                text_color="#D8B4FE",)

        self.boton_etiqueta4.configure(
                text="Irregular",
                width=120,
                height=34,
                corner_radius=7,
                fg_color=COLOR_SUPERFICIE,
                hover_color="#701A4F",
                border_width=2,
                border_color=COLOR_ROSADO,
                text_color="#F9A8D4",)

        self.boton_etiqueta5.configure(
    text="No clasificable",
    width=155,
    height=34,
    corner_radius=7,
    fg_color=COLOR_SUPERFICIE,
    hover_color="#312E5B",
    border_width=1,
    border_color=COLOR_BORDE,
    text_color=COLOR_TEXTO_SECUNDARIO,)

        #-----------------------------------------------------------------------------

        fondo_navegacion = self.crear_fondo_boton_navegacion(
            "#211F5A",
            "#7C3AED",
        )
        fondo_navegacion_hover = self.crear_fondo_boton_navegacion(
            "#312E81",
            "#A855F7",
        )

        self.imagen_navegacion = ctk.CTkImage(
            light_image=fondo_navegacion,
            dark_image=fondo_navegacion,
            size=(82, 82),
        )
        self.imagen_navegacion_hover = ctk.CTkImage(
            light_image=fondo_navegacion_hover,
            dark_image=fondo_navegacion_hover,
            size=(82, 82),
        )

        self.boton_anterior = ctk.CTkLabel(
            self.frame_visualizador,
            text="❮",
            image=self.imagen_navegacion,
            compound="center",
            fg_color="transparent",
            text_color="#C084FC",
            font=ctk.CTkFont(
                family="Segoe UI Symbol",
                size=25,
                weight="bold",
            ),
            cursor="hand2",
        )
        self.boton_anterior.pack(side="left",padx=(0, 28),)

        """self.frame_glow_imagen = ctk.CTkFrame(self.frame_visualizador,
                                    fg_color=COLOR_GLOW_EXTERIOR,
                                    border_width=3,
                                    border_color=COLOR_GLOW_MEDIO,
                                    corner_radius=17,)
        self.frame_glow_imagen.pack(side="left")


        self.frame_borde_imagen = ctk.CTkFrame(self.frame_glow_imagen,
                                    fg_color=COLOR_SUPERFICIE,
                                    border_width=3,
                                    border_color=COLOR_GLOW_CLARO,
                                    corner_radius=12,)
        self.frame_borde_imagen.pack(padx=8,pady=8,)"""

        self.visor_imagen = ctk.CTkLabel(self.frame_visualizador,
                            text="Aquí se mostrará la imagen",
                            text_color=COLOR_TEXTO_SECUNDARIO,
                            fg_color=COLOR_FONDO,
                            corner_radius=9,)
        self.visor_imagen.pack(side="left", padx=6, pady=6)

        self.boton_siguiente = ctk.CTkLabel(
                            self.frame_visualizador,
                            text="❯",
                            image=self.imagen_navegacion,
                            compound="center",
                            fg_color="transparent",
                            text_color="#C084FC",
                            font=ctk.CTkFont(
                                    family="Segoe UI Symbol",
                                    size=25,
                                    weight="bold",),
                            cursor="hand2",)
        self.boton_siguiente.pack(side="left",padx=(28, 0),)

        self.boton_anterior.bind(
            "<Button-1>",
            lambda evento: self.imagen_anterior(),
        )
        self.boton_siguiente.bind(
            "<Button-1>",
            lambda evento: self.imagen_siguiente(),
        )

        for boton in (self.boton_anterior, self.boton_siguiente):
            boton.bind(
                "<Enter>",
                lambda evento, boton=boton: boton.configure(
                    image=self.imagen_navegacion_hover
                ),
            )
            boton.bind(
                "<Leave>",
                lambda evento, boton=boton: boton.configure(
                    image=self.imagen_navegacion
                ),
            )

        

#-----------------------------------------------------------------------------

        # Tabla personalizada paginada.
        self.registros_por_pagina = 6
        self.pagina_tabla = 0

        self.frame_tabla_nueva = ctk.CTkFrame(
            self.contenido,
            fg_color="#0D0A20",
            border_width=1,
            border_color="#3B2C7A",
            corner_radius=9,
        )
        self.frame_tabla_nueva.pack(
            padx=32,
            pady=(0, 20),
            fill="x",
        )

        self.encabezado_tabla_nueva = ctk.CTkFrame(
            self.frame_tabla_nueva,
            fg_color="#211A4A",
            corner_radius=8,
            height=32,
        )
        self.encabezado_tabla_nueva.pack(
            padx=1,
            pady=1,
            fill="x",
        )
        self.encabezado_tabla_nueva.grid_propagate(False)
        self.encabezado_tabla_nueva.grid_columnconfigure(0, weight=43)
        self.encabezado_tabla_nueva.grid_columnconfigure(1, weight=42)
        self.encabezado_tabla_nueva.grid_columnconfigure(2, weight=15)

        ctk.CTkLabel(
            self.encabezado_tabla_nueva,
            text="nombre",
            anchor="w",
            text_color="#D8B4FE",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
        ).grid(row=0, column=0, sticky="ew", padx=(14, 4))

        ctk.CTkLabel(
            self.encabezado_tabla_nueva,
            text="etiqueta",
            anchor="w",
            text_color="#D8B4FE",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
        ).grid(row=0, column=1, sticky="ew", padx=4)

        ctk.CTkLabel(
            self.encabezado_tabla_nueva,
            text="acción",
            text_color="#D8B4FE",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
        ).grid(row=0, column=2, sticky="ew", padx=4)

        self.contenedor_filas = ctk.CTkFrame(
            self.frame_tabla_nueva,
            height=192,
            fg_color="#0D0A20",
            corner_radius=0,
        )
        self.contenedor_filas.pack(
            padx=1,
            pady=(0, 1),
            fill="x",
        )
        self.contenedor_filas.grid_columnconfigure(0, weight=1)
        self.contenedor_filas.grid_propagate(False)

        self.frame_paginacion = ctk.CTkFrame(
            self.frame_tabla_nueva,
            fg_color="#0D0A20",
            corner_radius=0,
        )
        self.frame_paginacion.pack(
            padx=10,
            pady=(2, 6),
            fill="x",
        )
        self.frame_paginacion.grid_columnconfigure(0, weight=1)
        self.frame_paginacion.grid_columnconfigure(1, weight=0)
        self.frame_paginacion.grid_columnconfigure(2, weight=0)
        self.frame_paginacion.grid_columnconfigure(3, weight=1)

        self.boton_pagina_anterior = ctk.CTkButton(
            self.frame_paginacion,
            text="‹",
            width=28,
            height=24,
            corner_radius=6,
            fg_color=COLOR_SUPERFICIE,
            hover_color=COLOR_PRIMARIO,
            border_width=1,
            border_color=COLOR_BORDE,
            text_color="#D8B4FE",
            command=lambda: self.cambiar_pagina_tabla(-1),
        )
        self.boton_pagina_anterior.grid(row=0, column=1, padx=4)

        self.indicador_pagina = ctk.CTkLabel(
            self.frame_paginacion,
            text="1 / 1",
            width=60,
            text_color=COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(family="Segoe UI", size=10),
        )
        self.indicador_pagina.grid(row=0, column=2, padx=4)

        self.boton_pagina_siguiente = ctk.CTkButton(
            self.frame_paginacion,
            text="›",
            width=28,
            height=24,
            corner_radius=6,
            fg_color=COLOR_SUPERFICIE,
            hover_color=COLOR_PRIMARIO,
            border_width=1,
            border_color=COLOR_BORDE,
            text_color="#D8B4FE",
            command=lambda: self.cambiar_pagina_tabla(1),
        )
        self.boton_pagina_siguiente.grid(row=0, column=3, sticky="w", padx=4)
#------------------------------------------------------------------------------

        fondo_csv = self.crear_fondo_boton_csv("#9D7BFF","#E65AC5",)
        fondo_csv_hover = self.crear_fondo_boton_csv("#B69AFF","#F472D0",)

        self.imagen_csv = ctk.CTkImage(light_image=fondo_csv,dark_image=fondo_csv,size=(180, 78),)
        self.imagen_csv_hover = ctk.CTkImage(light_image=fondo_csv_hover,dark_image=fondo_csv_hover,size=(180, 78),)

        self.boton_csv = ctk.CTkLabel(self.contenido,
                        text="↓  Exportar CSV",
                        image=self.imagen_csv,
                        compound="center",
                        fg_color="transparent",
                        text_color="#FFFFFF",
                        font=ctk.CTkFont(
                            family="Segoe UI",
                            size=12,
                            weight="bold",),
                        cursor="hand2",)

        self.boton_csv.pack(anchor="e",padx=12,pady=(0, 5),)

        self.boton_csv.bind(
            "<Button-1>",
            lambda evento: self.exportar_csv(),
        )
        self.boton_csv.bind(
            "<Enter>",
            lambda evento: self.boton_csv.configure(
                image=self.imagen_csv_hover
            ),
        )
        self.boton_csv.bind(
            "<Leave>",
            lambda evento: self.boton_csv.configure(
                image=self.imagen_csv
            ),
        )

        

    def crear_fila_tabla_nueva(self, nombre, etiqueta, indice):
        color_fondo, color_texto = COLORES_ETIQUETAS.get(
            etiqueta,
            ("#1F2937", COLOR_TEXTO_SECUNDARIO),
        )
        color_fila = "#100D2B" if indice % 2 == 0 else "#0B091D"

        fila = ctk.CTkFrame(
            self.contenedor_filas,
            height=31,
            fg_color=color_fila,
            corner_radius=0,
        )
        fila.grid(row=indice, column=0, sticky="ew", pady=(0, 1))
        fila.grid_propagate(False)
        fila.grid_columnconfigure(0, weight=43)
        fila.grid_columnconfigure(1, weight=42)
        fila.grid_columnconfigure(2, weight=15)

        ctk.CTkLabel(
            fila,
            text=nombre,
            anchor="w",
            text_color="#E5E7EB",
            font=ctk.CTkFont(family="Segoe UI", size=10),
        ).grid(row=0, column=0, sticky="ew", padx=(14, 4))

        contenedor_etiqueta = ctk.CTkFrame(
            fila,
            fg_color="transparent",
        )
        contenedor_etiqueta.grid(row=0, column=1, sticky="w", padx=4)

        etiqueta_visual = ctk.CTkLabel(
            contenedor_etiqueta,
            text=etiqueta,
            height=20,
            corner_radius=5,
            fg_color=color_fondo,
            text_color=color_texto,
            font=ctk.CTkFont(family="Segoe UI", size=9),
        )
        etiqueta_visual.pack(ipadx=7)

        acciones = ctk.CTkFrame(fila, fg_color="transparent")
        acciones.grid(row=0, column=2)

        boton_ver = ctk.CTkButton(
            acciones,
            text="◉",
            width=24,
            height=24,
            corner_radius=6,
            fg_color="transparent",
            hover_color="#123A5A",
            text_color=COLOR_CELESTE,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            command=lambda nombre=nombre: self.mostrar_desde_tabla(nombre),
        )
        boton_ver.pack(side="left", padx=(0, 1))

        boton_borrar = ctk.CTkButton(
            acciones,
            text="✕",
            width=24,
            height=24,
            corner_radius=6,
            fg_color="transparent",
            hover_color="#701A4F",
            text_color=COLOR_ROSADO,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda nombre=nombre: self.borrar_desde_tabla(nombre),
        )
        boton_borrar.pack(side="left", padx=(1, 0))

    def refrescar_tabla_nueva(self):
        for widget in self.contenedor_filas.winfo_children():
            widget.destroy()

        registros = list(self.etiquetas.items())
        total_registros = len(registros)
        total_paginas = max(
            1,
            (total_registros + self.registros_por_pagina - 1)
            // self.registros_por_pagina,
        )

        self.pagina_tabla = min(self.pagina_tabla, total_paginas - 1)
        self.pagina_tabla = max(self.pagina_tabla, 0)

        inicio = self.pagina_tabla * self.registros_por_pagina
        fin = inicio + self.registros_por_pagina

        for indice, (nombre, etiqueta) in enumerate(registros[inicio:fin]):
            self.crear_fila_tabla_nueva(nombre, etiqueta, indice)

        self.indicador_pagina.configure(
            text=f"{self.pagina_tabla + 1} / {total_paginas}"
        )

        estado_anterior = "normal" if self.pagina_tabla > 0 else "disabled"
        estado_siguiente = (
            "normal" if self.pagina_tabla < total_paginas - 1 else "disabled"
        )

        self.boton_pagina_anterior.configure(state=estado_anterior)
        self.boton_pagina_siguiente.configure(state=estado_siguiente)

    def cambiar_pagina_tabla(self, desplazamiento):
        total_registros = len(self.etiquetas)
        total_paginas = max(
            1,
            (total_registros + self.registros_por_pagina - 1)
            // self.registros_por_pagina,
        )

        nueva_pagina = self.pagina_tabla + desplazamiento

        if 0 <= nueva_pagina < total_paginas:
            self.pagina_tabla = nueva_pagina
            self.refrescar_tabla_nueva()

    def actualizar_fila_tabla_nueva(self, nombre, etiqueta):
        total_registros = len(self.etiquetas)
        self.pagina_tabla = max(
            0,
            (total_registros - 1) // self.registros_por_pagina,
        )
        self.refrescar_tabla_nueva()

    def eliminar_fila_tabla_nueva(self, nombre):
        self.refrescar_tabla_nueva()

    def limpiar_tabla_nueva(self):
        self.pagina_tabla = 0
        self.refrescar_tabla_nueva()

    def crear_fondo_boton_navegacion(self, color_circulo, color_glow):
        escala = 2
        diametro = 54 * escala
        margen = 14 * escala
        tamaño = diametro + margen * 2

        mascara = Image.new("L", (tamaño, tamaño), 0)
        dibujo_mascara = ImageDraw.Draw(mascara)
        dibujo_mascara.ellipse(
            (margen, margen, margen + diametro, margen + diametro),
            fill=255,
        )

        mascara_glow = mascara.filter(
            ImageFilter.GaussianBlur(8 * escala)
        )
        mascara_glow = mascara_glow.point(
            lambda valor: int(valor * 0.55)
        )

        rgb_glow = ImageColor.getrgb(color_glow)
        capa_glow = Image.new(
            "RGBA",
            (tamaño, tamaño),
            (*rgb_glow, 0),
        )
        capa_glow.putalpha(mascara_glow)

        resultado = Image.new("RGBA", (tamaño, tamaño), (0, 0, 0, 0))
        resultado = Image.alpha_composite(resultado, capa_glow)

        rgb_circulo = ImageColor.getrgb(color_circulo)
        circulo = Image.new(
            "RGBA",
            (diametro, diametro),
            (*rgb_circulo, 255),
        )
        mascara_circulo = Image.new("L", (diametro, diametro), 0)
        ImageDraw.Draw(mascara_circulo).ellipse(
            (0, 0, diametro - 1, diametro - 1),
            fill=255,
        )
        resultado.paste(
            circulo,
            (margen, margen),
            mascara_circulo,
        )

        ImageDraw.Draw(resultado).ellipse(
            (
                margen,
                margen,
                margen + diametro - 1,
                margen + diametro - 1,
            ),
            outline=(49, 46, 129, 255),
            width=escala,
        )

        return resultado

    def crear_fondo_boton_csv(self, color_superior, color_inferior):
        escala = 2
        ancho = 140 * escala
        alto = 38 * escala
        margen = 20 * escala
        radio = 8 * escala

        tamaño = (ancho + margen * 2,alto + margen * 2,)

        # Máscara con la forma redondeada del botón
        mascara = Image.new("L", tamaño, 0)
        dibujo_mascara = ImageDraw.Draw(mascara)

        dibujo_mascara.rounded_rectangle((margen,margen,margen + ancho,margen + alto,),radius=radio,fill=255,)

        # Glow difuminado
        mascara_glow = mascara.filter(ImageFilter.GaussianBlur(8 * escala))

        mascara_glow = mascara_glow.point(lambda valor: int(valor * 0.45))

        capa_glow = Image.new("RGBA",tamaño,(168, 85, 247, 0),)
        capa_glow.putalpha(mascara_glow)

        resultado = Image.new("RGBA", tamaño, (0, 0, 0, 0))
        resultado = Image.alpha_composite(resultado, capa_glow)

        # Degradado violeta a rosado
        color_inicio = ImageColor.getrgb(color_superior)
        color_final = ImageColor.getrgb(color_inferior)

        degradado = Image.new("RGBA", (ancho, alto))
        dibujo_degradado = ImageDraw.Draw(degradado)

        for y in range(alto):
            proporcion = y / (alto - 1)

            color = tuple(int(color_inicio[i]+ (color_final[i] - color_inicio[i]) * proporcion) for i in range(3))

            dibujo_degradado.line((0, y, ancho, y),fill=(*color, 255),)

        mascara_boton = Image.new("L", (ancho, alto), 0)
        dibujo_boton = ImageDraw.Draw(mascara_boton)

        dibujo_boton.rounded_rectangle((0, 0, ancho - 1, alto - 1),radius=radio,fill=255,)

        resultado.paste(degradado,(margen, margen),mascara_boton,)

        # Borde luminoso
        dibujo_resultado = ImageDraw.Draw(resultado)

        dibujo_resultado.rounded_rectangle((margen,margen,margen + ancho - 1,margen + alto - 1,),radius=radio,outline=(233, 184, 255, 255),width=escala,)

        return resultado

    def seleccionar_carpeta(self):
        carpeta_seleccionada = filedialog.askdirectory(title="Seleccionar carpeta de imágenes")
        #carpeta_seleccionada = Path(__file__).resolve().parent.parent / "data" / "img"

        if not carpeta_seleccionada:
            return

        carpeta = Path(carpeta_seleccionada)

        self.ruta_carpeta.set(str(carpeta))

        self.rutas_imagenes = sorted(
            [
                archivo
                for archivo in carpeta.iterdir()
                if archivo.is_file()
                and archivo.suffix.lower() in VALID_EXTENSIONS
            ],
            key=lambda archivo: archivo.name.lower(),
        )

        if not self.rutas_imagenes:
            self.estado.configure(
                text="No se encontraron imágenes en la carpeta seleccionada."
            )
            self.nombre_imagen.configure(text="")
            self.visor_imagen.configure(
                image=None,
                text="No hay imágenes para mostrar",
            )
            self.imagen_ctk = None
            self.etiqueta_actual.set("")
            self.etiquetas.clear()
            self.limpiar_tabla_nueva()
            return

        self.cargar_progreso()
        self.actualizar_contador()

        if self.rutas_imagenes:
            self.indice_actual = 0

        for indice, ruta in enumerate(self.rutas_imagenes):
            if ruta.name not in self.etiquetas:
                self.indice_actual = indice
                break

        self.mostrar_imagen()


    def crear_imagen_con_glow(self, imagen):
        margen = 28
        desenfoque = 14

        ancho, alto = imagen.size
        tamaño_final = (
            ancho + margen * 2,
            alto + margen * 2,
        )

        mascara_glow = Image.new(
            "L",
            tamaño_final,
            0,
        )

        dibujo_mascara = ImageDraw.Draw(mascara_glow)

        dibujo_mascara.rounded_rectangle(
            (
                margen - 4,
                margen - 4,
                margen + ancho + 4,
                margen + alto + 4,
            ),
            radius=16,
            fill=230,
        )

        mascara_glow = mascara_glow.filter(
            ImageFilter.GaussianBlur(desenfoque)
        )

        capa_glow = Image.new(
            "RGBA",
            tamaño_final,
            (139, 92, 246, 0),
        )
        capa_glow.putalpha(mascara_glow)

        resultado = Image.new(
            "RGBA",
            tamaño_final,
            (0, 0, 0, 0),
        )
        resultado = Image.alpha_composite(
            resultado,
            capa_glow,
        )

        mascara_imagen = Image.new(
            "L",
            imagen.size,
            0,
        )

        dibujo_imagen = ImageDraw.Draw(mascara_imagen)
        dibujo_imagen.rounded_rectangle(
            (0, 0, ancho - 1, alto - 1),
            radius=10,
            fill=255,
        )

        resultado.paste(
            imagen.convert("RGBA"),
            (margen, margen),
            mascara_imagen,
        )

        dibujo_resultado = ImageDraw.Draw(resultado)
        dibujo_resultado.rounded_rectangle(
            (
                margen - 2,
                margen - 2,
                margen + ancho + 1,
                margen + alto + 1,
            ),
            radius=12,
            outline=(192, 132, 252, 255),
            width=3,
        )

        return resultado

    def mostrar_imagen(self):
        ruta_actual = self.rutas_imagenes[self.indice_actual]
        self.nombre_imagen.configure(text=ruta_actual.name)

        etiqueta = self.etiquetas.get(ruta_actual.name, "")
        self.etiqueta_actual.set(etiqueta)

        with Image.open(ruta_actual) as imagen:
            imagen = imagen.copy()

            imagen.thumbnail((300, 300), Image.Resampling.LANCZOS)
            imagen = self.crear_imagen_con_glow(imagen)

            self.imagen_ctk = ctk.CTkImage(light_image=imagen,dark_image=imagen,size=imagen.size,)
            self.visor_imagen.configure(image=self.imagen_ctk,text="",)

    def imagen_anterior(self):
        if self.rutas_imagenes:
            self.indice_actual = (self.indice_actual - 1) % len(self.rutas_imagenes)
            self.mostrar_imagen()

    def asignar_etiqueta(self,etiqueta):
        if not self.rutas_imagenes:
            return
           
        ruta_actual = self.rutas_imagenes[self.indice_actual]
        self.etiquetas[ruta_actual.name] = etiqueta
        self.etiqueta_actual.set(etiqueta)

        nombre = ruta_actual.name

        self.actualizar_fila_tabla_nueva(nombre, etiqueta)

        self.actualizar_contador()
        self.guardar_progreso()
        self.imagen_siguiente()

    def borrar_etiqueta(self):
        if not self.rutas_imagenes:
            return

        ruta_actual = self.rutas_imagenes[self.indice_actual]

        self.etiquetas.pop(ruta_actual.name, None)
        self.etiqueta_actual.set("")

        self.eliminar_fila_tabla_nueva(ruta_actual.name)

        self.actualizar_contador()
        self.guardar_progreso()

    def imagen_siguiente(self):
        if self.rutas_imagenes:
            self.indice_actual = (self.indice_actual + 1) % len(self.rutas_imagenes)
            self.mostrar_imagen()

    def mostrar_desde_tabla(self,name):
        for indice, ruta in enumerate(self.rutas_imagenes):
            if ruta.name == name:
                self.indice_actual = indice
                self.mostrar_imagen()
                return

    def borrar_desde_tabla(self,name):
        self.etiquetas.pop(name, None)

        self.eliminar_fila_tabla_nueva(name)

        if self.rutas_imagenes:
            ruta_actual= self.rutas_imagenes[self.indice_actual]
            if ruta_actual.name == name:
                self.etiqueta_actual.set("")

        self.actualizar_contador()
        self.guardar_progreso()

    def exportar_csv(self):
        if not self.etiquetas:
            messagebox.showwarning("Sin etiquetas","No hay imágenes etiquetadas para exportar.",)
            return

        etiquetas_desconocidas = (set(self.etiquetas.values()) - set(CLASS_FOLDERS))

        if etiquetas_desconocidas:
            messagebox.showerror("Etiquetas desconocidas","Existen etiquetas antiguas o no reconocidas: "+ ", ".join(sorted(etiquetas_desconocidas)),)
            return

        rutas_por_nombre = {ruta.name: ruta for ruta in self.rutas_imagenes}

        imagenes_faltantes = [ nombre for nombre in self.etiquetas if nombre not in rutas_por_nombre]

        if imagenes_faltantes:
            messagebox.showerror("Imágenes faltantes","No se encontraron algunas imágenes etiquetadas.",)
            return

        RESULTS_DIR.mkdir(parents=True,exist_ok=True,)

        carpetas_clases = {}

        for etiqueta, nombre_carpeta in CLASS_FOLDERS.items():
            carpeta_clase = RESULTS_DIR / nombre_carpeta

            carpeta_clase.mkdir(parents=True,exist_ok=True,)

            carpetas_clases[etiqueta] = carpeta_clase

            # Eliminar solamente copias de exportaciones anteriores.
            for archivo in carpeta_clase.iterdir():
                if (archivo.is_file()and archivo.suffix.lower()in VALID_EXTENSIONS):
                    archivo.unlink()

        try:
            for nombre, etiqueta in self.etiquetas.items():
                origen = rutas_por_nombre[nombre]
                destino = carpetas_clases[etiqueta] / nombre

                shutil.copy2(origen, destino)

            ruta_csv = RESULTS_DIR / "etiquetas_galaxias.csv"

            with ruta_csv.open(mode="w",newline="",encoding="utf-8-sig",) as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(["nombre", "etiqueta"])

                for nombre, etiqueta in sorted(self.etiquetas.items()):
                    escritor.writerow([nombre, etiqueta])

        except OSError as error:
            messagebox.showerror("Error de exportación",f"No se pudo completar la exportación:\n{error}",)
            return

        messagebox.showinfo(
            "Exportación completada",
            (f"Se exportaron {len(self.etiquetas)} imágenes "f"en:\n{RESULTS_DIR}"),)

    def actualizar_contador(self):
        cantidad_etiquetadas = len(self.etiquetas)
        total_img = len(self.rutas_imagenes)

        self.estado.configure(text=(f"{cantidad_etiquetadas} de {total_img} imágenes etiquetadas"))

    def guardar_progreso(self):
        with PROGRESS_FILE.open(mode="w",newline="",encoding="utf-8-sig",) as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["nombre", "etiqueta"])

            for nombre, etiqueta in sorted(self.etiquetas.items()):
                escritor.writerow([nombre, etiqueta])

    def cargar_progreso(self):
        self.etiquetas.clear()

        self.limpiar_tabla_nueva()

        if not PROGRESS_FILE.exists():
            return

        nombres_validos = {ruta.name for ruta in self.rutas_imagenes}

        with PROGRESS_FILE.open(mode="r",newline="",encoding="utf-8-sig",) as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                nombre = fila["nombre"]
                etiqueta = fila["etiqueta"]

                if nombre not in nombres_validos or not etiqueta:
                    continue

                self.etiquetas[nombre] = etiqueta

        self.refrescar_tabla_nueva()

    def borrar_todo(self):
        if not self.etiquetas:
            messagebox.showinfo("Sin etiquetas","No hay etiquetas para borrar.",)
            return

        confirmar = messagebox.askyesno("Confirmar borrado","¿Deseas borrar todas las etiquetas guardadas?",)

        if not confirmar:
            return

        self.etiquetas.clear()

        self.limpiar_tabla_nueva()

        self.etiqueta_actual.set("")
        self.actualizar_contador()
        self.guardar_progreso()

        messagebox.showinfo("Progreso eliminado","Todas las etiquetas fueron borradas.",)

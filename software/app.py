from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
from storage import (guardar_etiquetas,cargar_etiquetas,exportar_resultados,)
from widgets.label_table import LabelTable


from config import (
    VALID_EXTENSIONS,
    CLASS_FOLDERS,
    COLOR_FONDO,
    COLOR_SUPERFICIE,
    COLOR_PRIMARIO,
    COLOR_PRIMARIO_HOVER,
    COLOR_CELESTE,
    COLOR_ROSADO,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_PELIGRO,
    COLOR_BORDE,
)

from img_effects import (crear_fondo_boton_navegacion,crear_fondo_boton_csv,crear_imagen_con_glow,
)
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

        fondo_navegacion = crear_fondo_boton_navegacion(
            "#211F5A",
            "#7C3AED",
        )
        fondo_navegacion_hover = crear_fondo_boton_navegacion(
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
        self.tabla_etiquetas = LabelTable(
            self.contenido,
            on_ver=self.mostrar_desde_tabla,
            on_borrar=self.borrar_desde_tabla,
            registros_por_pagina=6,
        )
        self.tabla_etiquetas.pack(
            padx=32,
            pady=(0, 20),
            fill="x",
        )
#------------------------------------------------------------------------------

        fondo_csv = crear_fondo_boton_csv("#9D7BFF","#E65AC5",)
        fondo_csv_hover = crear_fondo_boton_csv("#B69AFF","#F472D0",)

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
            self.tabla_etiquetas.limpiar()
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

    def mostrar_imagen(self):
        ruta_actual = self.rutas_imagenes[self.indice_actual]
        self.nombre_imagen.configure(text=ruta_actual.name)

        etiqueta = self.etiquetas.get(ruta_actual.name, "")
        self.etiqueta_actual.set(etiqueta)

        with Image.open(ruta_actual) as imagen:
            imagen = imagen.copy()

            imagen.thumbnail((300, 300), Image.Resampling.LANCZOS)
            imagen = crear_imagen_con_glow(imagen)

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

        self.tabla_etiquetas.actualizar(
            self.etiquetas,
            mostrar_ultima=True,
        )

        self.actualizar_contador()
        self.guardar_progreso()
        self.imagen_siguiente()

    def borrar_etiqueta(self):
        if not self.rutas_imagenes:
            return

        ruta_actual = self.rutas_imagenes[self.indice_actual]

        self.etiquetas.pop(ruta_actual.name, None)
        self.etiqueta_actual.set("")

        self.tabla_etiquetas.actualizar(self.etiquetas)

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

        self.tabla_etiquetas.actualizar(self.etiquetas)

        if self.rutas_imagenes:
            ruta_actual= self.rutas_imagenes[self.indice_actual]
            if ruta_actual.name == name:
                self.etiqueta_actual.set("")

        self.actualizar_contador()
        self.guardar_progreso()

    def exportar_csv(self):
        if not self.etiquetas:
            messagebox.showwarning(
                "Sin etiquetas",
                "No hay imágenes etiquetadas para exportar.",
            )
            return

        etiquetas_desconocidas = (
            set(self.etiquetas.values())
            - set(CLASS_FOLDERS)
        )

        if etiquetas_desconocidas:
            messagebox.showerror(
                "Etiquetas desconocidas",
                (
                    "Existen etiquetas antiguas o no reconocidas: "
                    + ", ".join(sorted(etiquetas_desconocidas))
                ),
            )
            return

        rutas_por_nombre = {
            ruta.name: ruta
            for ruta in self.rutas_imagenes
        }

        imagenes_faltantes = [
            nombre
            for nombre in self.etiquetas
            if nombre not in rutas_por_nombre
        ]

        if imagenes_faltantes:
            messagebox.showerror(
                "Imágenes faltantes",
                "No se encontraron algunas imágenes etiquetadas.",
            )
            return

        try:
            ruta_resultados = exportar_resultados(
                self.etiquetas,
                self.rutas_imagenes,
            )

        except OSError as error:
            messagebox.showerror(
                "Error de exportación",
                f"No se pudo completar la exportación:\n{error}",
            )
            return

        messagebox.showinfo(
            "Exportación completada",
            (
                f"Se exportaron {len(self.etiquetas)} imágenes "
                f"en:\n{ruta_resultados}"
            ),
        )



    def actualizar_contador(self):
        cantidad_etiquetadas = len(self.etiquetas)
        total_img = len(self.rutas_imagenes)

        self.estado.configure(text=(f"{cantidad_etiquetadas} de {total_img} imágenes etiquetadas"))

    def guardar_progreso(self):
        guardar_etiquetas(self.etiquetas)

    def cargar_progreso(self):
        self.etiquetas.clear()
        self.tabla_etiquetas.limpiar()

        etiquetas_guardadas = cargar_etiquetas(self.rutas_imagenes)

        self.etiquetas.update(etiquetas_guardadas)
        self.tabla_etiquetas.actualizar(self.etiquetas)

    def borrar_todo(self):
        if not self.etiquetas:
            messagebox.showinfo("Sin etiquetas","No hay etiquetas para borrar.",)
            return

        confirmar = messagebox.askyesno("Confirmar borrado","¿Deseas borrar todas las etiquetas guardadas?",)

        if not confirmar:
            return

        self.etiquetas.clear()

        self.tabla_etiquetas.limpiar()

        self.etiqueta_actual.set("")
        self.actualizar_contador()
        self.guardar_progreso()

        messagebox.showinfo("Progreso eliminado","Todas las etiquetas fueron borradas.",)

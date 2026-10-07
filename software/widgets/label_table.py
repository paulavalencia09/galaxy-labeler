import customtkinter as ctk

from config import (
    COLORES_ETIQUETAS,
    COLOR_BORDE,
    COLOR_CELESTE,
    COLOR_PRIMARIO,
    COLOR_ROSADO,
    COLOR_SUPERFICIE,
    COLOR_TEXTO_SECUNDARIO,
)


class LabelTable(ctk.CTkFrame):
    def __init__(
        self,
        master,
        on_ver,
        on_borrar,
        registros_por_pagina=6,
    ):
        super().__init__(
            master,
            fg_color="#0D0A20",
            border_width=1,
            border_color="#3B2C7A",
            corner_radius=9,
        )

        self.on_ver = on_ver
        self.on_borrar = on_borrar
        self.registros_por_pagina = registros_por_pagina
        self.pagina_actual = 0
        self.etiquetas = {}

        self._crear_encabezado()
        self._crear_contenedor_filas()
        self._crear_paginacion()
        self._refrescar()

    def _crear_encabezado(self):
        encabezado = ctk.CTkFrame(
            self,
            fg_color="#211A4A",
            corner_radius=8,
            height=32,
        )
        encabezado.pack(
            padx=1,
            pady=1,
            fill="x",
        )
        encabezado.grid_propagate(False)

        encabezado.grid_columnconfigure(0, weight=43)
        encabezado.grid_columnconfigure(1, weight=42)
        encabezado.grid_columnconfigure(2, weight=15)

        ctk.CTkLabel(
            encabezado,
            text="nombre",
            anchor="w",
            text_color="#D8B4FE",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(14, 4),
        )

        ctk.CTkLabel(
            encabezado,
            text="etiqueta",
            anchor="w",
            text_color="#D8B4FE",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=4,
        )

        ctk.CTkLabel(
            encabezado,
            text="acción",
            text_color="#D8B4FE",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=2,
            sticky="ew",
            padx=4,
        )

    def _crear_contenedor_filas(self):
        self.contenedor_filas = ctk.CTkFrame(
            self,
            height=192,
            fg_color="#0D0A20",
            corner_radius=0,
        )
        self.contenedor_filas.pack(
            padx=1,
            pady=(0, 1),
            fill="x",
        )
        self.contenedor_filas.grid_columnconfigure(
            0,
            weight=1,
        )
        self.contenedor_filas.grid_propagate(False)

    def _crear_paginacion(self):
        paginacion = ctk.CTkFrame(
            self,
            fg_color="#0D0A20",
            corner_radius=0,
        )
        paginacion.pack(
            padx=10,
            pady=(2, 6),
            fill="x",
        )

        paginacion.grid_columnconfigure(0, weight=1)
        paginacion.grid_columnconfigure(1, weight=0)
        paginacion.grid_columnconfigure(2, weight=0)
        paginacion.grid_columnconfigure(3, weight=1)

        self.boton_anterior = ctk.CTkButton(
            paginacion,
            text="‹",
            width=28,
            height=24,
            corner_radius=6,
            fg_color=COLOR_SUPERFICIE,
            hover_color=COLOR_PRIMARIO,
            border_width=1,
            border_color=COLOR_BORDE,
            text_color="#D8B4FE",
            command=lambda: self._cambiar_pagina(-1),
        )
        self.boton_anterior.grid(
            row=0,
            column=1,
            padx=4,
        )

        self.indicador_pagina = ctk.CTkLabel(
            paginacion,
            text="1 / 1",
            width=60,
            text_color=COLOR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
            ),
        )
        self.indicador_pagina.grid(
            row=0,
            column=2,
            padx=4,
        )

        self.boton_siguiente = ctk.CTkButton(
            paginacion,
            text="›",
            width=28,
            height=24,
            corner_radius=6,
            fg_color=COLOR_SUPERFICIE,
            hover_color=COLOR_PRIMARIO,
            border_width=1,
            border_color=COLOR_BORDE,
            text_color="#D8B4FE",
            command=lambda: self._cambiar_pagina(1),
        )
        self.boton_siguiente.grid(
            row=0,
            column=3,
            sticky="w",
            padx=4,
        )

    def _crear_fila(self, nombre, etiqueta, indice):
        color_fondo, color_texto = COLORES_ETIQUETAS.get(
            etiqueta,
            ("#1F2937", COLOR_TEXTO_SECUNDARIO),
        )

        color_fila = (
            "#100D2B"
            if indice % 2 == 0
            else "#0B091D"
        )

        fila = ctk.CTkFrame(
            self.contenedor_filas,
            height=31,
            fg_color=color_fila,
            corner_radius=0,
        )
        fila.grid(
            row=indice,
            column=0,
            sticky="ew",
            pady=(0, 1),
        )
        fila.grid_propagate(False)

        fila.grid_columnconfigure(0, weight=43)
        fila.grid_columnconfigure(1, weight=42)
        fila.grid_columnconfigure(2, weight=15)

        ctk.CTkLabel(
            fila,
            text=nombre,
            anchor="w",
            text_color="#E5E7EB",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=10,
            ),
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(14, 4),
        )

        contenedor_etiqueta = ctk.CTkFrame(
            fila,
            fg_color="transparent",
        )
        contenedor_etiqueta.grid(
            row=0,
            column=1,
            sticky="w",
            padx=4,
        )

        etiqueta_visual = ctk.CTkLabel(
            contenedor_etiqueta,
            text=etiqueta,
            height=20,
            corner_radius=5,
            fg_color=color_fondo,
            text_color=color_texto,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=9,
            ),
        )
        etiqueta_visual.pack(ipadx=7)

        acciones = ctk.CTkFrame(
            fila,
            fg_color="transparent",
        )
        acciones.grid(row=0, column=2)

        ctk.CTkButton(
            acciones,
            text="◉",
            width=24,
            height=24,
            corner_radius=6,
            fg_color="transparent",
            hover_color="#123A5A",
            text_color=COLOR_CELESTE,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
            command=lambda: self.on_ver(nombre),
        ).pack(side="left", padx=(0, 1))

        ctk.CTkButton(
            acciones,
            text="✕",
            width=24,
            height=24,
            corner_radius=6,
            fg_color="transparent",
            hover_color="#701A4F",
            text_color=COLOR_ROSADO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold",
            ),
            command=lambda: self.on_borrar(nombre),
        ).pack(side="left", padx=(1, 0))

    def actualizar(self, etiquetas, mostrar_ultima=False):
        self.etiquetas = dict(etiquetas)

        if mostrar_ultima and self.etiquetas:
            self.pagina_actual = (
                (len(self.etiquetas) - 1)
                // self.registros_por_pagina
            )

        self._refrescar()

    def limpiar(self):
        self.etiquetas.clear()
        self.pagina_actual = 0
        self._refrescar()

    def _cambiar_pagina(self, desplazamiento):
        total_paginas = self._calcular_total_paginas()
        nueva_pagina = self.pagina_actual + desplazamiento

        if 0 <= nueva_pagina < total_paginas:
            self.pagina_actual = nueva_pagina
            self._refrescar()

    def _calcular_total_paginas(self):
        return max(
            1,
            (
                len(self.etiquetas)
                + self.registros_por_pagina
                - 1
            )
            // self.registros_por_pagina,
        )

    def _refrescar(self):
        for widget in self.contenedor_filas.winfo_children():
            widget.destroy()

        total_paginas = self._calcular_total_paginas()

        self.pagina_actual = min(
            self.pagina_actual,
            total_paginas - 1,
        )
        self.pagina_actual = max(
            self.pagina_actual,
            0,
        )

        registros = list(self.etiquetas.items())

        inicio = (
            self.pagina_actual
            * self.registros_por_pagina
        )
        fin = inicio + self.registros_por_pagina

        for indice, (nombre, etiqueta) in enumerate(
            registros[inicio:fin]
        ):
            self._crear_fila(
                nombre,
                etiqueta,
                indice,
            )

        self.indicador_pagina.configure(
            text=(
                f"{self.pagina_actual + 1} "
                f"/ {total_paginas}"
            )
        )

        estado_anterior = (
            "normal"
            if self.pagina_actual > 0
            else "disabled"
        )
        estado_siguiente = (
            "normal"
            if self.pagina_actual < total_paginas - 1
            else "disabled"
        )

        self.boton_anterior.configure(
            state=estado_anterior
        )
        self.boton_siguiente.configure(
            state=estado_siguiente
        )
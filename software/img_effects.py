from PIL import Image, ImageDraw, ImageFilter, ImageColor

def crear_fondo_boton_navegacion(color_circulo, color_glow):
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

def crear_fondo_boton_csv(color_superior, color_inferior):
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


def crear_imagen_con_glow(imagen):
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


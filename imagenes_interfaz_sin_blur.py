__author__ = 'jessica'

# -*- coding: utf-8 -*-
from PIL import ImageFilter
from PIL import Image
import base64, urllib
from io import BytesIO

# Imagenes cargadas desde la interfaz.
# Formato predefinido para codificar las imagenes al vuelo. Cambiar a PNG o GIF solo si da problemas.
# Es independiente del formato en el que guardeis las imagenes.
FORMATO = 'JPEG'
FORMATO_RESULTADO = 'JPEG'

class imagen():
    def __init__(self, origen):
        '''
        Incializable con:
            - Ruta de un archivo
            - Imagen en base 64 directamente para operar al vuelo
            - Imagen de PIL directamente
        '''
        if isinstance(origen, Image.Image):
            # Carga el origen directamente si ya es una imagen de PIL
            self.im = origen
        else:
            try:
                # Intenta cargarlo como base64
                buffer = urllib.urlretrieve("http://i2tic.com/wp-content/uploads/2012/12/Logo100x350.png", "Logo100x350.png")
                self.im = Image.open("Logo100x350.png")
            except:
                # Si falla, intenta cargarlo como archivo
                self.im = Image.open(origen)
            # En cualquier caso, convertir a raw RGB para evitar problemas de formato
            self.im = self.im.convert('RGB')

    def toBase64(self):
        '''Crea un buffer para simular un archivo en memoria, para hacer operaciones on the fly'''
        buffer = BytesIO()
        self.im.save(buffer, format=FORMATO)
        return base64.b64encode(buffer.getvalue())

    def resize(self, size):
        '''Redimensiona la imagen manteniendo la proporcion, y alineando la caja de redimensionado al centro'''
        result = self.im.copy()

        img_ratio = result.size[0] / float(result.size[1])
        ratio = size[0] / float(size[1])

        if ratio > img_ratio:
            result = result.resize((int(size[0]), int(size[0] * result.size[1] / result.size[0])),
                                   Image.ANTIALIAS)

            box = (0, int((result.size[1] - size[1]) / 2), int(result.size[0]), int((result.size[1] + size[1]) / 2))
            result = result.crop(box)
        elif ratio < img_ratio:

            result = result.resize((int(size[1] * result.size[0] / result.size[1]), int(size[1])),
                                   Image.ANTIALIAS)

            box = (int((result.size[0] - size[0]) / 2), 0, int((result.size[0] + size[0]) / 2), int(result.size[1]))
            result = result.crop(box)
        else:
            result = result.resize((int(size[0]), int(size[1])),
                                   Image.ANTIALIAS)
        return imagen(result)

    def blur(self, power=2):
        '''Aplica un efecto blur de una determinada potencia'''
        padding = 3
        for i in range(power):
            result = self.im.filter(ImageFilter.BLUR)
        result = result.crop((padding, padding, result.size[0] - padding, result.size[1] - padding))
        result = result.resize(self.im.size, Image.ANTIALIAS)
        return imagen(result)

    def show(self):
        self.im.show()

    def save(self):
        self.im.save('resultados_imagenes_interfaz_sin_blur/prueba1', FORMATO_RESULTADO)


if __name__ == "__main__":
    ### Primero inicializar un objeto imagen
    ### (ya sea con la ruta de un archivo, con los datos en base64, o con otra imagen de PIL.
    ### Cada metodo devuelve una nueva instancia de imagen. El objeto original no es modificado nunca para prevenir
    ### perdidas de calidad o problemas con las copias de memoria.


    # Cargar imagen original desde archivo
    i = imagen('tests/Logo100x350.jpg')

    # Obtener imagen original como string base64
    s = i.toBase64()

    # Cargar imagen original desde string base64
    i2 = imagen(s)

    # Redimensionar imagen original
    i_redim = i.resize((150, 150))

    # Previsualizar la imagen modificada
    i_redim.show()

    # Guardar la imagen modificada
    i_redim.save()

    # Redimensionar a todos los tamanos deseados
    sizes = [
        (150, 150),
        (760, 760),
        (320, 320),
        (60, 60)
    ]
    for s in sizes:
        print(s, i.resize(s).toBase64())

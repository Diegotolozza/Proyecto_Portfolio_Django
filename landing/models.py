# from django.db import models
# from django.core.exceptions import ValidationError
# import os
# from django.utils.text import slugify

# class Categoria(models.Model):
#     nombre = models.CharField(max_length=100)
#     imagen_portada = models.ImageField(upload_to="categorias/", blank=True, null=True)
#     slug = models.SlugField(unique=True, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.nombre)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.nombre

# class Foto(models.Model):
#     categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='fotos')
#     imagen = models.ImageField(upload_to="fotos/")
#     titulo = models.CharField(max_length=100, blank=True)
#     descripcion = models.TextField(blank=True)

#     def __str__(self):
#         return self.titulo or f"Foto de {self.categoria.nombre}"

from django.db import models
from django.core.exceptions import ValidationError
import os
from django.utils.text import slugify
from PIL import Image                 # Para manipular imágenes
from io import BytesIO                # Para crear buffer en memoria
from django.core.files.base import ContentFile  # Para guardar la miniatura en ImageField

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    imagen_portada = models.ImageField(upload_to="categorias/", blank=True, null=True)
    miniatura_portada = models.ImageField(upload_to="categorias/miniaturas/", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)

        super().save(*args, **kwargs)  # Guarda primero para tener self.imagen_portada.path

        # Generar miniatura si hay imagen
        if self.imagen_portada:
            img = Image.open(self.imagen_portada.path)
            img.thumbnail((600, 400), Image.LANCZOS)  # tamaño para web
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)

            miniatura_name = f"mini_{os.path.basename(self.imagen_portada.name)}"
            self.miniatura_portada.save(miniatura_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Foto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to="fotos/")
    titulo = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.titulo or f"Foto de {self.categoria.nombre}"

    def delete(self, *args, **kwargs):
        # Elimina también el archivo físico
        if self.imagen and os.path.isfile(self.imagen.path):
            os.remove(self.imagen.path)
        super().delete(*args, **kwargs)

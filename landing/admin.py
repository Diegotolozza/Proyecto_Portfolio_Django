# from django.contrib import admin
# from .models import *

# # Register your models here.
# # admin.site.register(Categoria)
# # admin.site.register(Foto)

# @admin.register(Categoria)
# class CategoriaAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'slug')
#     prepopulated_fields = {'slug': ('nombre',)}

# @admin.register(Foto)
# class FotoAdmin(admin.ModelAdmin):
#     list_display = ('titulo', 'categoria')
#     list_filter = ('categoria',)

from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Foto

# Inline para gestionar fotos desde la categoría
class FotoInline(admin.TabularInline):
    model = Foto
    extra = 1
    fields = ("imagen", "titulo", "descripcion", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.imagen.url)
        return "Sin imagen"

    preview.short_description = "Vista previa"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "preview")
    prepopulated_fields = {"slug": ("nombre",)}
    inlines = [FotoInline]

    def preview(self, obj):
        if obj.imagen_portada:
            return format_html('<img src="{}" style="width: 120px; height:auto;" />', obj.imagen_portada.url)
        return "Sin portada"

    preview.short_description = "Portada"


@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "preview")
    list_filter = ("categoria",)
    search_fields = ("titulo", "descripcion")

    def preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.imagen.url)
        return "Sin imagen"

    preview.short_description = "Vista previa"

from django.contrib import admin
from .models import Pelicula, Serie, Categoria, Director, ContenidoUsuario

# Register your models here.

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'anio', 'director')
    search_fields = ('titulo', 'director')
    list_filter = ('categoria', 'anio')
    
@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'anio', 'director', 'temporadas', 'capitulos')
    search_fields = ('titulo', 'director')
    list_filter = ('categoria', 'anio')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    
@admin.register(ContenidoUsuario)
class ContenidoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pelicula', 'serie', 'favorito', 'visto', 'fecha_visto')
    search_fields = ('usuario', 'pelicula', 'serie', 'favorito', 'visto', 'fecha_visto')
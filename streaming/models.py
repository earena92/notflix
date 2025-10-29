from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    '''Clase Categoría
    Enlista las distintas categorías cinematográficas para clasificar los títulos de series y películas
    '''
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['nombre']
    
class Director(models.Model):
    '''Clase Director
    Nombre y/o Apellidos de los directores asociados a los títulos de películas y series
    '''
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['nombre']

class Pelicula(models.Model):
    '''Clase Película
    Contiene toda la información de las películas del catálogo, incluyendo el título, la categoría(FK), el director(FK), comentario o sinopsis, año de producción, duración, una imágen de portada(URL) y un trailer(URL) 
    '''
    titulo = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    comentario = models.TextField(blank=True)
    anio = models.IntegerField()
    duracion = models.DurationField()
    imagen_portada = models.URLField(blank=True)
    trailer = models.URLField(blank=True)
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['titulo']
    
class Serie(models.Model):
    '''Clase Serie
    Contiene toda la información de las series del catálogo, incluyendo el título, la categoría(FK), el director(FK), comentario o sinopsis, año de producción, cantidad de temporadas, cantidad de capítulos, duración de cada capítulos, una imágen de portada(URL) y un trailer(URL) 
    '''
    titulo = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True)
    comentario = models.TextField(blank=True)
    anio = models.IntegerField()
    temporadas = models.IntegerField()
    capitulos = models.IntegerField()
    duracion_capitulo = models.DurationField()
    imagen_portada = models.URLField(blank=True)
    trailer = models.URLField(blank=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['titulo']
    
class ContenidoUsuario(models.Model):
    '''Clase ContenidoUsuario
    Relaciona la información del usuario con las películas y series, incluye los atributos de visto y favorito. También almacena la fecha_visto'''
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, null=True, blank=True)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True, blank=True)
    favorito = models.BooleanField(default=False)
    visto = models.BooleanField(default=False)
    fecha_visto = models.DateTimeField(auto_now=True)

    def __str__(self):
        contenido = self.pelicula.titulo if self.pelicula else self.serie.titulo
        return f"{self.usuario.username} - {contenido}"
    

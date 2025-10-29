from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreacionUsuario
from .models import Pelicula, Serie, ContenidoUsuario
from django.db.models import Q
from datetime import timedelta


def home(request):
    return render(request, 'home.html')


def signup(request):
    # Si se accede mediante un método GET se renderiza la página con el formulario
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CreacionUsuario
        })
    # Si se accede mediante el método post, enviando el formulario, se crea el nuevo usuario y se logea
    else:
        form = CreacionUsuario(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'signup.html', {
                'form': form})


def signin(request):
    if request.method == 'GET':
        # Si el usuario viene redirigido de otra página con login_required mostramos error
        if 'next' in request.GET:
            messages.error(
                request, 'Debes iniciar sesión para ver series o películas')
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        # Si no se encuentra al user (devuelve nulo) y mostramos un error
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecto'
            })
        else:
            login(request, user)
            return redirect('index')


def signout(request):
    logout(request)
    return redirect('index')

@login_required
def perfil(request):
    # Accedemos al contenido del usuario que indica favoritos y vistos
    contenido_usuario = ContenidoUsuario.objects.filter(
        usuario=request.user)

    # Filtramos y guardamos en una variable las peliculas y series vistas
    peliculas_vistas = contenido_usuario.filter(
        pelicula__isnull=False, visto=True)

    series_vistas = contenido_usuario.filter(serie__isnull=False, visto=True)

    # Calculamos el tiempo de visualización a partir del atributo duracion y duracion_capitulo
    tiempo_peliculas = timedelta()
    tiempo_series = timedelta()
    for item in peliculas_vistas:
        tiempo_peliculas += item.pelicula.duracion
    for item in series_vistas:
        tiempo_series += item.serie.duracion_capitulo * item.serie.capitulos
    tiempo_total = tiempo_peliculas+tiempo_series

    # Pasamos al html el contexto incluyendo el tiempo de películas y series en minutos para que lo procese el gráfico en JS
    context = {
        'peliculas_vistas': peliculas_vistas,
        'series_vistas': series_vistas,
        'tiempo_peliculas': tiempo_peliculas,
        'tiempo_series': tiempo_series,
        'tiempo_total': tiempo_total,
        'tiempo_peliculas_minutos': tiempo_peliculas.total_seconds() / 60,
        'tiempo_series_minutos': tiempo_series.total_seconds() / 60,
    }

    return render(request, 'perfil.html', context)

@login_required
def cambiar_contrasenia(request):
    # Icluimos un mensaje de éxito si el usuario ha podido cambiar la contraseña y lo mostramos en 'perfil' donde es redirigido nuevamente
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña se ha actualizado con éxito.')
            return redirect('perfil')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiar_contrasenia.html', {
        'form': form
    })


def peliculas(request):
    # Primero accedemos a todas las películas de la DB y las pasamos al html
    peliculas = Pelicula.objects.all().order_by('titulo')
    context = {'peliculas': peliculas}

    # Si el usuario está logeado accedemos a la información de sus favoritos y sus vistos
    if request.user.is_authenticated:
        favoritos = ContenidoUsuario.objects.filter(
            usuario=request.user,
            pelicula__isnull=False,
            favorito=True
        ).values_list('pelicula__id', flat=True) # flat=True para enviar una lista plana de los ids sin tuplas

        vistos = ContenidoUsuario.objects.filter(
            usuario=request.user,
            pelicula__isnull=False,
            visto=True
        ).values_list('pelicula__id', flat=True)

        context.update({
            'favoritos': favoritos,
            'vistos': vistos
        })

    return render(request, 'peliculas.html', context)


# Si el usuario intenta acceder sin estar logeado se le redirige a 'login'
@login_required(login_url='login')
# Accedemos a la película con el id a la que el user quiere acceder
def pelicula_detalle(request, pelicula_id):
    pelicula = get_object_or_404(Pelicula, id=pelicula_id)

    # Se inicilizan las variables favorito y visto por si no hay un contenido_usuario para esa película
    favorito = False
    visto = False
    # Se intenta acceder al contenido, si existe se sobreescriben favorito y visto
    if request.user.is_authenticated:
        contenido_usuario = ContenidoUsuario.objects.filter(
            usuario=request.user,
            pelicula=pelicula
        ).first()
        if contenido_usuario:
            favorito = contenido_usuario.favorito
            visto = contenido_usuario.visto

    context = {
        'pelicula': pelicula,
        'favorito': favorito,
        'visto': visto,
    }
    return render(request, 'pelicula_detalle.html', context)


def series(request):
    # Igual que def peliculas()
    series = Serie.objects.all().order_by('titulo')
    context = {'series': series}

    if request.user.is_authenticated:
        favoritos = ContenidoUsuario.objects.filter(
            usuario=request.user,
            serie__isnull=False,
            favorito=True
        ).values_list('serie__id', flat=True)

        vistos = ContenidoUsuario.objects.filter(
            usuario=request.user,
            serie__isnull=False,
            visto=True
        ).values_list('serie__id', flat=True)

        context.update({
            'favoritos': favoritos,
            'vistos': vistos
        })
    return render(request, 'series.html', context)


@login_required(login_url='login')
# Igual que en def pelicula_detalle
def serie_detalle(request, serie_id):
    serie = get_object_or_404(Serie, id=serie_id)

    favorito = False
    visto = False
    if request.user.is_authenticated:
        contenido_usuario = ContenidoUsuario.objects.filter(
            usuario=request.user,
            serie=serie
        ).first()
        if contenido_usuario:
            favorito = contenido_usuario.favorito
            visto = contenido_usuario.visto

    context = {
        'serie': serie,
        'favorito': favorito,
        'visto': visto,
    }
    return render(request, 'serie_detalle.html', context)


@login_required
# Accedemos a peliculas y series marcadas como favoritas en ContenidoUsuario
def favoritos(request):
    peliculas_favoritas = ContenidoUsuario.objects.filter(
        usuario=request.user,
        pelicula__isnull=False,
        favorito=True
    ).select_related('pelicula', 'pelicula__director') # En la misma consulta carga las FK pelicula y director

    series_favoritas = ContenidoUsuario.objects.filter(
        usuario=request.user,
        serie__isnull=False,
        favorito=True
    ).select_related('serie', 'serie__director')

    context = {
        'peliculas_favoritas': peliculas_favoritas,
        'series_favoritas': series_favoritas,
    }
    return render(request, 'favoritos.html', context)


@login_required
# Recibe los argumentos tipo y el id de la pelicula o serie desde el html
def marcar_favorito(request, tipo, id):
    if tipo == 'pelicula':
        # Accedemos a la pelicula por su id
        contenido = get_object_or_404(Pelicula, id=id)
        # Accedemos al contenido o si no existe lo creamos
        item, created = ContenidoUsuario.objects.get_or_create(
            usuario=request.user,
            pelicula=contenido
        )
    elif tipo == 'serie':
        contenido = get_object_or_404(Serie, id=id)
        # get_or_create devuelve dos variables: el objeto (item) y un booleano (created) para saber si se creó (True) o se recuperó (False)
        item, created = ContenidoUsuario.objects.get_or_create(
            usuario=request.user,
            serie=contenido
        )

    # Cambiamos el estado de favorito cada vez que se accede
    item.favorito = not item.favorito
    item.save()
    
    #Redirigimos a la página desde donde se venía, o si no se puede acceder va a 'index' 
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
# Igual que def marcar_favorito()
def marcar_visto(request, tipo, id):
    if tipo == 'pelicula':
        contenido = get_object_or_404(Pelicula, id=id)
        item, created = ContenidoUsuario.objects.get_or_create(
            usuario=request.user,
            pelicula=contenido
        )
    else:
        contenido = get_object_or_404(Serie, id=id)
        item, created = ContenidoUsuario.objects.get_or_create(
            usuario=request.user,
            serie=contenido
        )

    item.visto = not item.visto
    item.save()

    return redirect(request.META.get('HTTP_REFERER', 'index'))

def buscar(request):
    query = request.GET.get('busqueda', '')
    resultados_peliculas = []
    resultados_series = []
    
    if query:
        # Búsqueda en películas
        resultados_peliculas = Pelicula.objects.filter(
            Q(titulo__icontains=query) |  # Búsqueda por título
            Q(director__nombre__icontains=query) |  # Búsqueda por director
            Q(categoria__nombre__icontains=query) # Búsqueda por categoría
        ).distinct() # .distinct() elimina resultados duplicados
        
        # Búsqueda en series
        resultados_series = Serie.objects.filter(
            Q(titulo__icontains=query) |
            Q(director__nombre__icontains=query) |
            Q(categoria__nombre__icontains=query)
        ).distinct()
        
    # Si el usuario está logeado, obtenemos sus favoritos y vistos
    favoritos_peliculas = []
    favoritos_series = []
    vistos_peliculas = []
    vistos_series = []
    
    if request.user.is_authenticated:
        from .models import ContenidoUsuario
        
        favoritos_peliculas = ContenidoUsuario.objects.filter(
            usuario=request.user,
            pelicula__isnull=False,
            favorito=True
        ).values_list('pelicula__id', flat=True)
        
        favoritos_series = ContenidoUsuario.objects.filter(
            usuario=request.user,
            serie__isnull=False,
            favorito=True
        ).values_list('serie__id', flat=True)
        
        vistos_peliculas = ContenidoUsuario.objects.filter(
            usuario=request.user,
            pelicula__isnull=False,
            visto=True
        ).values_list('pelicula__id', flat=True)
        
        vistos_series = ContenidoUsuario.objects.filter(
            usuario=request.user,
            serie__isnull=False,
            visto=True
        ).values_list('serie__id', flat=True)
    
    context = {
        'query': query,
        'resultados_peliculas': resultados_peliculas,
        'resultados_series': resultados_series,
        'favoritos_peliculas': favoritos_peliculas,
        'favoritos_series': favoritos_series,
        'vistos_peliculas': vistos_peliculas,
        'vistos_series': vistos_series,
    }
    
    return render(request, 'buscar.html', context)

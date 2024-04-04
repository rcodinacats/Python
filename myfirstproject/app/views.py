from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Jornada


@login_required
def home(request):
    return render(request, 'plantilla/base.html')

def salir(request):
    logout(request)
    return redirect('/')

from django.shortcuts import redirect
from django.utils import timezone
from .models import Jornada

def iniciar_jornada(request):
    if request.user.is_authenticated:
        Jornada.objects.create(usuari=request.user, data_hora_inici=timezone.now())
        # Redirigeix a la pàgina que prefereixis
        return redirect('veure_registres')
        return redirect('home')
    else:
        # Redirigeix a la pàgina de login si no està logejat
        return redirect('login')

def finalitzar_jornada(request):
    if request.user.is_authenticated:
        jornada = Jornada.objects.filter(usuari=request.user).last()
        if jornada and not jornada.data_hora_fi:
            jornada.data_hora_fi = timezone.now()
            jornada.save()
        return redirect('veure_registres')
        return redirect('home')
    else:
        return redirect('login')
    
@login_required
def veure_registres(request):
    registres = Jornada.objects.filter(usuari=request.user).order_by('-data_hora_inici')
    jornada_en_curs = registres.first() and not registres.first().data_hora_fi
    return render(request, 'plantilla/veure_registres.html', {'registres': registres, 'jornada_en_curs': jornada_en_curs})
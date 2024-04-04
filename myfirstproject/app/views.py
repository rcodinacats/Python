from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Jornada
from django.utils import timezone
from django.http import JsonResponse
from django.core.serializers import serialize
import csv
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

@login_required
def home(request):
    registres = Jornada.objects.filter(usuari=request.user).order_by('-data_hora_inici')
    jornada_en_curs = registres.first() and not registres.first().data_hora_fi
    return render(request, 'plantilla/veure_registres.html', {'registres': registres, 'jornada_en_curs': jornada_en_curs})
    return render(request, 'plantilla/base.html')

def salir(request):
    logout(request)
    return redirect('/')

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

@login_required
def exportar_jornades_json(request):
    jornades = Jornada.objects.all()
    jornades_json = serialize('json', jornades)
    
    response = HttpResponse(jornades_json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="jornades.json"'
    
    return response
@login_required
def exportar_jornades_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="jornades.csv"'

    escriptor = csv.writer(response)
    escriptor.writerow(['Usuari', 'Data Hora Inici', 'Data Hora Fi'])

    for jornada in Jornada.objects.all():
        escriptor.writerow([jornada.usuari.username, jornada.data_hora_inici, jornada.data_hora_fi])

    return response

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirigir a la pàgina d'inici de sessió després del registre
    template_name = 'registration/signup.html'
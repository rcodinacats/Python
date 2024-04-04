"""
URL configuration for myfirstproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from app import views as v
from app.views import SignUpView
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',v.veure_registres, name='veure_registres'),
    path('', include("app.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('iniciar_jornada/', v.iniciar_jornada, name='iniciar_jornada'),
    path('finalitzar_jornada/', v.finalitzar_jornada, name='finalitzar_jornada'),
    path('veure_registres/', v.veure_registres, name='veure_registres'),
    path('exportar/json/', v.exportar_jornades_json, name='exportar_jornades_json'),
    path('exportar/csv/', v.exportar_jornades_csv, name='exportar_jornades_csv'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]


from django.db import models
from django.contrib.auth.models import User

class Jornada(models.Model):
    usuari = models.ForeignKey(User, on_delete=models.CASCADE)
    data_hora_inici = models.DateTimeField(null=True, blank=True)
    data_hora_fi = models.DateTimeField(null=True, blank=True)
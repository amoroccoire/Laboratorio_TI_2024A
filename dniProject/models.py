from django.db import models

class Persona(models.Model):
    dni = models.CharField(max_length=8, primary_key=True)
    nombre = models.CharField(max_length=100)
    apePaterno = models.CharField(max_length=100)
    apeMaterno = models.CharField(max_length=100)
    fecRegistro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} {self.apePaterno} {self.apeMaterno}'


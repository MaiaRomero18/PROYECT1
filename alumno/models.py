from django.db import models
from django.contrib.auth.models import User

class Tarea(models.Model):
    title = models.CharField(max_length=100)
    adjunto= models.FileField(upload_to="archivos/", null=True, blank=True)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    dateCompleted = models.DateTimeField(null=True)
    user = models.name = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + '- by ' + self.user.username


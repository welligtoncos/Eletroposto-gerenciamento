from django.db import models

class Carregador(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('carregando', 'Carregando'),
        ('ocupado', 'Ocupado'),
    ]

    id_tag = models.CharField(max_length=100, unique=True, verbose_name="Identificador")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='disponivel', 
        verbose_name="Status"
    )

    def __str__(self):
        return f"Carregador {self.id_tag} - {self.status}"

from django.db import models


class Juego(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    genero = models.CharField(max_length=50)
    desarrollador = models.CharField(max_length=100)
    fecha_lanzamiento = models.DateField()
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'juegos'

    def __str__(self):
        return self.nombre


class Torneo(models.Model):
    class Estado(models.TextChoices):
        PROXIMO = 'PROXIMO', 'Próximo'
        EN_CURSO = 'EN_CURSO', 'En curso'
        FINALIZADO = 'FINALIZADO', 'Finalizado'

    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE,
        related_name='torneos',
    )
    nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    premio = models.PositiveIntegerField(help_text='Premio en CLP')
    max_participantes = models.PositiveSmallIntegerField()
    estado = models.CharField(
        max_length=12,
        choices=Estado.choices,
        default=Estado.PROXIMO,
    )

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name_plural = 'torneos'

    def __str__(self):
        return f'{self.nombre} ({self.juego})'
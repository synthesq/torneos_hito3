from django.db import models
from django.utils import timezone


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
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name_plural = 'torneos'

    def __str__(self):
        return f'{self.nombre} ({self.juego})'

    # --- Propiedades de presentación (no crean columnas ni migraciones) ---
    @property
    def duracion_dias(self):
        return (self.fecha_fin - self.fecha_inicio).days + 1

    @property
    def progreso(self):
        """Avance del torneo (0-100) según las fechas de hoy."""
        hoy = timezone.localdate()
        if hoy <= self.fecha_inicio:
            return 0
        if hoy >= self.fecha_fin:
            return 100
        total = max((self.fecha_fin - self.fecha_inicio).days, 1)
        return int((hoy - self.fecha_inicio).days / total * 100)

    @property
    def texto_tiempo(self):
        hoy = timezone.localdate()
        if hoy < self.fecha_inicio:
            d = (self.fecha_inicio - hoy).days
            if d == 1:
                return 'Comienza mañana'
            return f'Comienza en {d} días'
        if hoy <= self.fecha_fin:
            d = (self.fecha_fin - hoy).days
            if d == 0:
                return 'Termina hoy'
            return f'Termina en {d} días'
        d = (hoy - self.fecha_fin).days
        return 'Terminó ayer' if d == 1 else f'Terminó hace {d} días'

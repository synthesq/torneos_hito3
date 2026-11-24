from datetime import date, timedelta

from django.core.management.base import BaseCommand

from torneos.models import Juego, Torneo

JUEGOS = [
    ('Overwatch 2', 'Shooter de héroes', 'Blizzard Entertainment', date(2022, 10, 4)),
    ('Valorant', 'Shooter táctico', 'Riot Games', date(2020, 6, 2)),
    ('Rocket League', 'Deportes / Carreras', 'Psyonix', date(2015, 7, 7)),
    ('Counter-Strike 2', 'Shooter táctico', 'Valve', date(2023, 9, 27)),
]

# (juego, nombre, días desde hoy hasta el inicio, duración en días, premio CLP, cupos, activo)
TORNEOS = [
    ('Overwatch 2', 'Copa Patagonia OW2', -40, 3, 800000, 32, True),
    ('Overwatch 2', 'Liga Invierno OW2', -3, 10, 1500000, 16, True),
    ('Overwatch 2', 'Desafío Lagos OW2', 12, 2, 500000, 24, True),
    ('Valorant', 'Valorant Open Osorno', -25, 2, 1200000, 64, True),
    ('Valorant', 'Copa Volcán Valorant', 5, 4, 2000000, 32, True),
    ('Valorant', 'Ascenso Sur Valorant', 30, 3, 900000, 16, False),
    ('Rocket League', 'Rocket Cup Austral', -60, 2, 400000, 16, True),
    ('Rocket League', 'Liga 3v3 Rocket', -1, 14, 700000, 12, True),
    ('Rocket League', 'Aerial Masters', 20, 1, 350000, 8, True),
    ('Counter-Strike 2', 'CS2 Torneo Aniversario', -15, 3, 1000000, 32, True),
    ('Counter-Strike 2', 'Major Estudiantil CS2', 2, 5, 2500000, 48, True),
    ('Counter-Strike 2', 'CS2 Clasificatoria', 45, 2, 600000, 24, False),
]


class Command(BaseCommand):
    help = 'Carga datos de demostración (4 juegos y 12 torneos). Se puede repetir sin duplicar.'

    def handle(self, *args, **options):
        hoy = date.today()
        juegos = {}
        for nombre, genero, dev, lanzamiento in JUEGOS:
            juegos[nombre], _ = Juego.objects.get_or_create(
                nombre=nombre,
                defaults={'genero': genero, 'desarrollador': dev,
                          'fecha_lanzamiento': lanzamiento, 'activo': True},
            )
        for juego, nombre, offset, dias, premio, cupos, activo in TORNEOS:
            inicio = hoy + timedelta(days=offset)
            fin = inicio + timedelta(days=dias - 1)
            if fin < hoy:
                estado = Torneo.Estado.FINALIZADO
            elif inicio <= hoy:
                estado = Torneo.Estado.EN_CURSO
            else:
                estado = Torneo.Estado.PROXIMO
            Torneo.objects.get_or_create(
                juego=juegos[juego], nombre=nombre,
                defaults={'fecha_inicio': inicio, 'fecha_fin': fin, 'premio': premio,
                          'max_participantes': cupos, 'estado': estado, 'activo': activo},
            )
        self.stdout.write(self.style.SUCCESS(
            f'Listo. Juegos: {Juego.objects.count()} | Torneos: {Torneo.objects.count()}'))

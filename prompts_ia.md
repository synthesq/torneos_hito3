# Bitácora de prompts de IA — Hito 3 (TI3041)

## Prompt 1 — Modelado relacional
- **Rol:** Actúa como un desarrollador back end experto en Django.
- **Tarea:** Diseña dos modelos relacionales 1:N para un sistema de torneos de videojuegos.
- **Contexto:** Proyecto individual de INACAP. Juego es la entidad padre (clasificadora, gestionada en Django Admin) y Torneo es la entidad hija con ForeignKey, on_delete explícito y al menos 4 atributos de tipos variados.
- **Formato:** Código Python de models.py con comentarios breves.
- **Resultado:** (describe qué usaste y qué ajustaste)

## Prompt 2 — Optimización y seguridad de las vistas
- **Rol:** Actúa como revisor de código Django.
- **Tarea:** Revisa mis vistas basadas en clases y señala problemas de rendimiento y seguridad.
- **Contexto:** ListView con filtros, CRUD con CreateView/UpdateView/DeleteView, MySQL local, autenticación nativa de Django.
- **Formato:** Lista de hallazgos con la línea afectada y la corrección propuesta.
- **Resultado:** (describe qué usaste y qué ajustaste)
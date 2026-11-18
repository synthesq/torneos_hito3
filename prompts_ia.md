# Bitácora de Inteligencia Artificial - Hito 3
**Proyecto:** SynthesQ Torneos

A continuación se documentan los prompts utilizados en el desarrollo del sistema, estructurados bajo el marco **RTCF** (Rol, Tarea, Contexto, Formato).

## Prompt 1: Generación de Vistas y UI (Front-End)
* **Rol:** Eres un desarrollador experto en Django y Bootstrap 5.
* **Tarea:** Escribe el código HTML para una plantilla `torneo_list.html` que muestre una tabla responsiva con un botón para crear nuevos registros.
* **Contexto:** Estoy desarrollando la Fase 3 de mi proyecto de gestión de Torneos (Modelo Hijo) y necesito que la tabla se vea moderna usando clases tipo "card" de Bootstrap, e implemente un bloque "empty" si no hay datos.
* **Formato:** Entrega únicamente el código de la plantilla HTML listo para ser ejecutado mediante un script de PowerShell (Write-Utf8).

## Prompt 2: Depuración y Seguridad (Back-End)
* **Rol:** Eres un tutor especialista en seguridad y arquitectura Django.
* **Tarea:** Protege mis Vistas Basadas en Clases (CreateView, UpdateView, DeleteView) para evitar accesos anónimos.
* **Contexto:** El proyecto debe cumplir con la pauta de evaluación que exige usar `LoginRequiredMixin` respetando la regla MRO (a la izquierda), y necesito ocultar los botones de acción en la interfaz DTL si el usuario no está autenticado (`user.is_authenticated`).
* **Formato:** Proporciona el código de `views.py` actualizado y el fragmento modificado del `base.html` con las sentencias de validación correspondientes.
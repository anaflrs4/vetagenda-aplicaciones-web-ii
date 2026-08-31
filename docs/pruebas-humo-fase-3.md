# Pruebas de humo de VetAgenda — Fase 3

## Objetivo

Las pruebas de humo comprueban que el backend pueda iniciar, que el esquema de datos esté actualizado, que el flujo principal de la aplicación responda y que los componentes nuevos de la fase 3 puedan reproducirse.

## Comandos ejecutados

```bash
python manage.py migrate
python manage.py configurar_roles
python manage.py cargar_demo
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Resultados

| Verificación | Resultado |
|---|---|
| Migraciones | `0001_initial`, `0002_cita_duracion_minutos` y `0003` se aplican correctamente. |
| Configuración Django | `System check identified no issues (0 silenced).` |
| Migraciones pendientes | `No changes detected`. |
| Grupos y permisos | Se crearon o actualizaron los grupos `Propietario` con 7 permisos, `Personal veterinario` con 5 y `Administrador` con 16. |
| Datos de demostración | `cargar_demo` terminó correctamente con datos ficticios. |
| Suite automatizada | 11 pruebas ejecutadas y aprobadas. Incluye navegación, modelos, formularios, solapamientos, agenda diaria, dashboard y grupos de permisos. |
| Dashboard | Se verificaron los conteos generales y los estados con código de colores. |
| Agenda diaria | Se verificó `/citas/hoy/` con la fecha actual y filtro por veterinario activo. |
| Solapamiento | Se verificó el rechazo de citas duplicadas y de intervalos parcialmente cruzados. |

## Reproducción limpia recomendada

Para una demostración sin datos locales previos, realiza una copia de seguridad, crea un entorno virtual nuevo y ejecuta las migraciones. Después carga el fixture o los datos ficticios, configura los grupos y ejecuta el servidor:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata citas/fixtures/vetagenda_demo.json
python manage.py configurar_roles
python manage.py runserver
```

La aplicación se consulta en `http://127.0.0.1:8000/`, la agenda diaria en `http://127.0.0.1:8000/citas/hoy/` y el panel administrativo en `http://127.0.0.1:8000/admin/`.

# Verificación visual de la fase 2

La aplicación se ejecutó localmente con `python3 manage.py runserver 0.0.0.0:8000` y se verificaron las siguientes pantallas:

| Ruta | Resultado |
|---|---|
| `/` | El panel muestra la propuesta, la problemática, contadores, roles y próximas citas. |
| `/propietarios/` | Se muestran dos propietarios ficticios, búsqueda y acciones de edición/eliminación. |
| `/citas/nueva/` | El formulario carga las mascotas, veterinarios, fecha, hora, motivo, estado y observaciones. |

Los datos mostrados fueron generados con el comando `python3 manage.py cargar_demo` y son completamente ficticios. No se utilizaron datos reales de pacientes ni propietarios.

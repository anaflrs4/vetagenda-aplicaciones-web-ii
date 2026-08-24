# Verificación visual de la fase 2

La aplicación se ejecutó localmente con `python3 manage.py runserver 0.0.0.0:8000` y se verificaron las siguientes pantallas:

| Ruta | Resultado |
|---|---|
| `/` | El panel muestra la propuesta, la problemática, contadores, roles y próximas citas. |
| `/propietarios/` | Se muestran dos propietarios ficticios, búsqueda y acciones de edición/eliminación. |
| `/citas/nueva/` | El formulario carga las mascotas, veterinarios, fecha, hora, motivo, estado y observaciones. |

Los datos mostrados fueron generados con el comando `python3 manage.py cargar_demo` y son completamente ficticios. No se utilizaron datos reales de pacientes ni propietarios.

## Verificación de la retroalimentación docente

| Mejora solicitada | Evidencia verificada |
|---|---|
| Dashboard intuitivo con colores | El panel muestra tarjetas separadas para Solicitada, Confirmada, Atendida y Cancelada, cada una con un color lateral diferente. |
| Agenda del personal veterinario | La ruta `/citas/hoy/` limita la consulta a la fecha actual y permite filtrar por veterinario activo. |
| Control de duración y horarios | El formulario permite elegir 30, 45 o 60 minutos y el modelo rechaza horarios que se solapan para el mismo veterinario. |

La agenda diaria se verificó con una cita ficticia del día actual. El dashboard mostró los totales por estado y la navegación incluyó el acceso “Agenda de hoy”.

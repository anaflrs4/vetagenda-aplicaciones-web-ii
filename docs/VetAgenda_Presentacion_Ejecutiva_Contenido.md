## Cover

# VetAgenda

Gestión inteligente de citas veterinarias

Ana Paula Flores Escalona · Aplicaciones Web II

## Slide 1 — La agenda dispersa genera fricción

- Los datos de propietarios y mascotas se encuentran en medios separados.
- Confirmar disponibilidad y localizar información requiere tiempo adicional.
- Los cambios de estado no siempre son visibles para todo el personal.
- Un cruce de horarios afecta la atención y la experiencia del cliente.

## Slide 2 — Una sola aplicación conecta la operación

- VetAgenda centraliza propietarios, mascotas, veterinarios y citas.
- La agenda diaria muestra la atención programada para cada profesional.
- Los estados por color permiten reconocer solicitudes, confirmaciones, atenciones y cancelaciones.
- Las reglas de negocio protegen la disponibilidad de los horarios.

## Slide 3 — El proceso fluye de principio a fin

1. Registrar al propietario y a su mascota.
2. Configurar al personal veterinario disponible.
3. Programar una cita con fecha, hora, duración y motivo.
4. Confirmar, atender o cancelar mediante transiciones válidas.

## Slide 4 — CRUD completo con una interfaz clara

- Altas mediante formularios validados.
- Consultas con listados, filtros, búsqueda y detalle.
- Cambios de información y estado con mensajes de confirmación.
- Bajas controladas con una advertencia antes de eliminar.

## Slide 5 — Cuatro entidades sostienen el negocio

- Propietario concentra la información de contacto.
- Mascota representa al paciente y pertenece a un propietario.
- Veterinario contiene especialidad y disponibilidad.
- Cita relaciona paciente, profesional, horario, motivo y estado.

## Slide 6 — La arquitectura separa responsabilidades

- Las plantillas presentan los datos y reciben acciones del usuario.
- Las vistas procesan solicitudes sin consultar directamente el ORM.
- Los DAO centralizan consultas, guardado, baja, agenda y estados.
- El ORM preserva la persistencia y las relaciones de la base de datos.

## Slide 7 — Las reglas previenen errores operativos

- Cada turno dura 30, 45 o 60 minutos.
- Los intervalos activos no pueden solaparse para el mismo veterinario.
- Una cancelación libera el horario.
- Solo se permiten transiciones coherentes entre estados.

## Slide 8 — Frontend y backend ya están integrados

- Los formularios ejecutan altas, cambios y bajas mediante solicitudes HTTP.
- El dashboard resume registros y estados de la operación.
- La agenda diaria permite actualizar la atención desde la interfaz.
- La API REST publica las citas activas en formato JSON.

## Slide 9 — La calidad se demuestra con evidencia

- 7 pruebas unitarias.
- 5 pruebas de componentes.
- 6 pruebas de integración.
- 1 prueba E2E; total: 19 pruebas aprobadas.

## Slide 10 — VetAgenda crea valor desde la primera versión

- Reduce la dispersión de información.
- Disminuye el riesgo de cruces de horario.
- Facilita el seguimiento diario de las consultas.
- Su arquitectura permite incorporar autenticación, notificaciones e historial clínico.

## Closing

# Menos confusión. Más cuidado.

VetAgenda convierte la agenda veterinaria en un proceso claro, verificable y escalable.

Repositorio: github.com/anaflrs4/vetagenda-aplicaciones-web-ii

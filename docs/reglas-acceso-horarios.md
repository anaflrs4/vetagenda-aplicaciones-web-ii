# Reglas de acceso, estados y horarios de VetAgenda

Este documento incorpora la retroalimentación recibida en la evaluación de la fase 1 y define con mayor precisión el comportamiento esperado de cada rol.

## 1. Límites de acceso por rol

| Rol | Puede consultar | Puede crear | Puede modificar | Puede cancelar o eliminar |
|---|---|---|---|---|
| Propietario de mascota | Únicamente sus mascotas y sus propias citas. | Solicitudes de cita para sus mascotas. | Puede corregir datos de contacto y modificar una solicitud mientras siga en estado `solicitada`. | Puede cancelar sus propias solicitudes `solicitada` o citas `confirmada` antes de la hora de atención. No puede eliminar registros históricos ni cambiar una cita a `atendida`. |
| Personal veterinario | Su agenda del día y la información necesaria de las mascotas asignadas a sus citas. | Puede registrar observaciones de atención cuando corresponda. | Puede actualizar el estado de sus citas y agregar observaciones. | Puede marcar una cita como `cancelada` cuando exista un motivo operativo, pero no elimina el registro histórico. |
| Administrador | Toda la información de la clínica. | Propietarios, mascotas, veterinarios y citas. | Puede editar cualquier registro y configurar el catálogo operativo. | Puede cancelar citas y eliminar registros administrativos bajo control. Se recomienda conservar el historial de citas atendidas. |

En la fase 2 estas reglas quedan documentadas y se implementa la separación funcional mediante la vista de agenda diaria y el panel administrativo. La autenticación y los permisos específicos por usuario se desarrollarán cuando la asignatura indique la fase de seguridad.

## 2. Estados de una cita

| Estado | Significado | Color del dashboard | Transiciones permitidas |
|---|---|---|---|
| `solicitada` | La solicitud fue registrada y está pendiente de revisión. | Verde azulado | `confirmada` o `cancelada`. |
| `confirmada` | La clínica aceptó la fecha y hora. | Amarillo | `atendida` o `cancelada`. |
| `atendida` | La consulta fue realizada. | Verde | No se modifica desde el flujo normal. |
| `cancelada` | La consulta no se realizará. | Coral/rojo | Estado final; libera el horario. |

El dashboard presenta una tarjeta por estado y utiliza el mismo código de color en las etiquetas de la agenda. De esta manera, la persona que administra la clínica puede interpretar rápidamente la situación de las citas.

## 3. Gestión de horarios

Cada cita registra una fecha, una hora de inicio y una duración de 30, 45 o 60 minutos. El horario de término se calcula automáticamente. Antes de guardar una cita, el sistema revisa las citas activas del mismo veterinario y el mismo día. Si el intervalo nuevo se cruza con otro intervalo existente, la operación se rechaza y se muestra un mensaje en el campo de hora.

Las citas canceladas no bloquean el horario. La base de datos también mantiene una restricción de unicidad para impedir que dos citas activas compartan exactamente el mismo veterinario, fecha y hora. Esta doble protección —validación del intervalo y restricción de base de datos— evita tanto los cruces parciales como los duplicados exactos.

La agenda del personal veterinario se consulta mediante `/citas/hoy/`. La pantalla muestra únicamente las citas de la fecha actual y permite filtrar por veterinario activo. En fases posteriores, después de implementar autenticación, el filtro se reemplazará o complementará con el veterinario identificado en la sesión.

## 4. Reglas de diseño para la siguiente fase

El propietario no deberá recibir acceso a los registros de otros propietarios. El personal veterinario no deberá visualizar una agenda general cuando inicie sesión, sino su agenda diaria y la información clínica mínima necesaria. El administrador conservará la visión completa para organizar la operación. Cualquier ampliación futura deberá respetar estas reglas y no exponer información personal innecesaria.

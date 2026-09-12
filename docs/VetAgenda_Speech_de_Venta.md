# Speech de venta — VetAgenda

**Duración estimada:** 4 a 5 minutos.

## Portada

Hola, soy Ana Paula Flores Escalona y presentaré VetAgenda, una aplicación web para organizar la gestión de citas en una clínica veterinaria pequeña. La propuesta busca reducir la confusión administrativa para que el personal pueda dedicar más atención al cuidado de cada mascota.

## 1. Problema

El proyecto parte de una situación sencilla pero frecuente: la información puede quedar distribuida entre libretas, mensajes y archivos separados. Esto dificulta localizar a un propietario, revisar los datos de una mascota o comprobar si un veterinario ya tiene ocupado un horario. También hace más difícil reconocer si una cita está solicitada, confirmada, atendida o cancelada.

## 2. Solución

VetAgenda centraliza cuatro elementos: propietarios, mascotas, veterinarios y citas. El personal puede registrar la información, consultar la agenda y actualizar el estado de una atención desde la misma aplicación. Los estados se identifican mediante colores y el sistema valida los horarios antes de guardar.

## 3. Flujo de uso

El flujo comienza con el registro del propietario y de su mascota. Después se configura al veterinario que atenderá las consultas. Con esos datos se programa una cita, indicando fecha, hora, duración y motivo. Finalmente, el personal puede confirmarla, marcarla como atendida o cancelarla conforme a reglas definidas.

## 4. Operaciones CRUD

La aplicación cubre las cuatro operaciones CRUD. Las altas se realizan mediante formularios; las consultas utilizan listados, buscadores, filtros y vistas de detalle; los cambios permiten actualizar datos o estados; y las bajas incluyen una confirmación para reducir eliminaciones accidentales.

## 5. Modelo de datos

El modelo conecta las entidades del negocio. Un propietario puede registrar varias mascotas. Cada mascota puede tener múltiples citas. Cada veterinario también puede atender múltiples citas. La cita funciona como el elemento central porque relaciona paciente, profesional, horario, motivo, duración y estado.

## 6. Arquitectura

Uno de los principales logros técnicos es la arquitectura desacoplada. Las vistas no acceden directamente al ORM. En su lugar utilizan una capa DAO que concentra consultas, guardado, eliminación, agenda y cambios de estado. El flujo queda organizado como View, DAO, ORM y base de datos. Esta separación facilita las pruebas y el mantenimiento.

## 7. Reglas de negocio

VetAgenda permite turnos de 30, 45 o 60 minutos. Antes de guardar una cita, el sistema compara el intervalo completo con las citas activas del mismo veterinario. Si existe un cruce, la operación se rechaza. Las citas canceladas liberan el horario y las transiciones de estado evitan cambios incoherentes.

## 8. Integración

El frontend y el backend se encuentran integrados mediante las vistas, los formularios y el DAO. Además, existe un endpoint REST que devuelve las citas activas en JSON. Esto demuestra que la información puede ser consumida por otras interfaces en futuras versiones.

## 9. Calidad

La versión final se verificó con 19 pruebas aprobadas. La suite incluye pruebas unitarias, de componentes, de integración y una prueba de extremo a extremo. También se comprobó que Django no reportara errores y que no existieran migraciones pendientes.

## 10. Valor y crecimiento

VetAgenda aporta una agenda más clara, menos riesgo de cruces y mejor seguimiento diario. Su estructura permite seguir creciendo con autenticación personalizada, notificaciones, historial clínico y una base de datos productiva. En resumen, VetAgenda convierte información dispersa en un proceso claro, verificable y escalable.

## Cierre

Gracias por su atención. El código, la documentación y las evidencias están disponibles en el repositorio público de GitHub: github.com/anaflrs4/vetagenda-aplicaciones-web-ii.

# Guion para el video de presentación de VetAgenda

## Duración sugerida

Entre tres y cinco minutos, hablando con palabras propias y mostrando el repositorio y la aplicación local.

## Guion

Buenas tardes, miss. Mi nombre es **[tu nombre]** y presentaré mi proyecto individual llamado **VetAgenda**. Es una aplicación web para una clínica veterinaria pequeña.

El problema que identifiqué es que la información de propietarios, mascotas, veterinarios y citas puede estar dispersa en libretas, mensajes o archivos separados. Esto dificulta encontrar los datos rápidamente, organizar la agenda y conocer el estado de una consulta. Por ese motivo, propuse centralizar esta información en una aplicación web.

En la primera fase investigué la problemática, definí los objetivos y establecí tres roles: propietario de mascota, personal veterinario y administrador. El propietario consulta sus mascotas y sus citas; el personal veterinario consulta la agenda y actualiza la atención; y el administrador gestiona la información general de la clínica.

Para la segunda fase adapté el proyecto de ejemplo trabajado en clase al contexto veterinario. Ya no se manejan productos, bebidas ni pedidos de cafetería. Los modelos principales son Propietario, Mascota, Veterinario y Cita. Una mascota pertenece a un propietario y una cita relaciona una mascota con un veterinario, una fecha, una hora, un motivo y un estado.

En el proyecto utilicé Django y Django REST Framework. En `models.py` definí las entidades; en `forms.py` preparé los formularios; en `views.py` implementé las operaciones; en `urls.py` configuré las rutas; y en las plantillas HTML diseñé el panel, los listados, los formularios y el detalle de una cita. También generé y apliqué las migraciones de Django para crear las tablas de la base de datos.

Ahora mostraré el panel principal. Aquí se observan los contadores de propietarios, mascotas, veterinarios y citas, además de las próximas citas. En el apartado de propietarios puedo buscar, registrar, editar y eliminar información. En mascotas puedo relacionar una mascota con su propietario. En veterinarios puedo administrar el personal de la clínica. Finalmente, en citas puedo registrar una consulta, seleccionar la mascota y el veterinario, indicar fecha, hora, motivo y estado, y después consultar o editar el registro.

También incluí una validación para evitar que el mismo veterinario tenga dos citas en la misma fecha y hora. Además, el panel administrativo de Django permite gestionar los registros mediante una cuenta de superusuario local.

Los datos de la demostración son ficticios. El repositorio es público y contiene el README, el reporte integrado de las fases 1 y 2, los modelos, formularios, vistas, plantillas, migraciones y pruebas. Las funciones como autenticación específica por rol, notificaciones, pagos e historial clínico completo se dejarán para las siguientes fases.

El enlace HTTPS de mi repositorio es:

https://github.com/anaflrs4/vetagenda-aplicaciones-web-ii

Gracias.

## Orden recomendado para grabar

| Orden | Qué mostrar |
|---:|---|
| 1 | El repositorio público y el archivo `README.md`. |
| 2 | El reporte `docs/entrega-fases-1-y-2-vetagenda.md`. |
| 3 | El panel principal de VetAgenda. |
| 4 | El listado de propietarios y el formulario de mascota. |
| 5 | El formulario y el listado de citas. |
| 6 | El archivo `models.py` y la carpeta `migrations`. |
| 7 | El enlace HTTPS y el alcance de las siguientes fases. |

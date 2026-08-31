# VetAgenda — Documento ejecutivo de la fase 3

**Asignatura:** Aplicaciones Web II  
**Estudiante:** Ana Paula Flores Escalona  
**Proyecto:** VetAgenda  
**Modalidad:** Trabajo individual  
**Repositorio:** [https://github.com/anaflrs4/vetagenda-aplicaciones-web-ii](https://github.com/anaflrs4/vetagenda-aplicaciones-web-ii)

## 1. Propósito ejecutivo

VetAgenda es una aplicación web para organizar la operación básica de una clínica veterinaria pequeña. La fase 3 convierte el análisis y el avance de las fases anteriores en un modelo físico de datos conectado al backend Django. El sistema administra propietarios, mascotas, veterinarios y citas, y conserva las relaciones necesarias para consultar la agenda sin duplicar información.

La docente explicó que el modelo físico debe traducir nombres, relaciones, llaves, restricciones y tipos de datos al gestor de base de datos elegido [1]. También indicó que el avance del proyecto propio debe integrar lo trabajado en clase, incluyendo roles, grupos, permisos y los cambios realizados en el repositorio [2].

## 2. Modelo físico de datos

La base local de VetAgenda utiliza SQLite a través del ORM de Django. Cada modelo se transforma en una tabla y Django crea una llave primaria `id` automáticamente.

| Tabla / modelo | Llave primaria | Campos principales | Relaciones y restricciones |
|---|---|---|---|
| `citas_propietario` / `Propietario` | `id` | `nombre_completo`, `telefono`, `email`, `fecha_registro` | Un propietario puede tener muchas mascotas. |
| `citas_mascota` / `Mascota` | `id` | `nombre`, `especie`, `raza`, `fecha_nacimiento`, `peso_kg`, `notas`, `fecha_registro` | `propietario_id` es llave foránea hacia `Propietario`. Al eliminar el propietario, sus mascotas se eliminan en cascada. |
| `citas_veterinario` / `Veterinario` | `id` | `nombre_completo`, `especialidad`, `telefono`, `email`, `activo` | Un veterinario puede tener muchas citas. |
| `citas_cita` / `Cita` | `id` | `fecha`, `hora`, `duracion_minutos`, `motivo`, `estado`, `observaciones`, `creado_en`, `actualizado_en` | `mascota_id` apunta a `Mascota`; `veterinario_id` apunta a `Veterinario` y protege sus registros. |

Los estados de una cita son `solicitada`, `confirmada`, `atendida` y `cancelada`. La duración puede ser de 30, 45 o 60 minutos. El modelo calcula la hora de término y rechaza los intervalos que se cruzan con otra cita activa del mismo veterinario. Además, la base de datos impide duplicados exactos entre citas activas mediante una restricción única condicionada.

## 3. Relaciones del modelo

La relación principal se puede representar así:

```text
Propietario 1 ──────── N Mascota 1 ──────── N Cita N ──────── 1 Veterinario
```

Una persona propietaria puede registrar varias mascotas. Cada mascota puede tener varias citas. Cada cita pertenece a una mascota y se asigna a un veterinario. La información del propietario se obtiene a través de la relación `cita.mascota.propietario`, lo que evita duplicar los datos de contacto dentro de la tabla de citas.

Las llaves foráneas permiten realizar consultas relacionadas desde Django. Por ejemplo, el listado de citas utiliza `select_related` para obtener en una sola consulta la mascota, el propietario y el veterinario asociados. El listado de mascotas usa una anotación para contar las citas relacionadas.

## 4. Conexión con el backend

El recorrido de una operación de registro es el siguiente:

| Capa | Archivo | Responsabilidad |
|---|---|---|
| Modelo | `citas/models.py` | Define tablas, campos, relaciones, estados, duración y validación de solapamientos. |
| Migraciones | `citas/migrations/0001_initial.py`, `0002_cita_duracion_minutos.py` y `0003_...py` | Traduce los cambios del modelo a operaciones reproducibles de la base de datos. |
| Formulario | `citas/forms.py` | Recibe los datos, valida campos y ejecuta la validación de la cita antes de guardar. |
| Vista | `citas/views.py` | Consulta registros, procesa formularios, guarda cambios y redirige al usuario. |
| Rutas | `citas/urls.py` | Conecta cada URL con una vista del backend. |
| Plantillas | `citas/templates/citas/` | Presenta paneles, listados, formularios, detalle y agenda diaria. |
| Administración | `citas/admin.py` | Permite gestionar los modelos desde el panel administrativo de Django. |
| Roles | `citas/management/commands/configurar_roles.py` | Crea los grupos Propietario, Personal veterinario y Administrador y asigna permisos de modelo. |

El personal veterinario cuenta con la ruta `/citas/hoy/`, que limita la agenda a la fecha actual y permite filtrar por profesional activo. La autenticación de usuarios y el filtrado automático por el usuario conectado se reservarán para la fase de seguridad.

## 5. Roles y permisos en backend

El comando `configurar_roles` crea tres grupos de Django. Esta decisión aplica la retroalimentación de la fase anterior y coincide con la indicación de clase de documentar qué usuario pertenece a cada grupo y qué permisos recibe [2].

| Grupo Django | Permisos de modelo asignados |
|---|---|
| `Propietario` | Consultar propietarios; consultar, crear y modificar mascotas; consultar, crear y modificar citas. |
| `Personal veterinario` | Consultar propietarios, mascotas y veterinarios; consultar y modificar citas. |
| `Administrador` | Consultar, crear, modificar y eliminar los cuatro modelos. |

La asignación de usuarios a grupos puede realizarse desde `/admin/`. No se guardan contraseñas ni datos personales reales en el repositorio.

## 6. Instrucciones para recrear la base de datos

### Opción A: migraciones y datos de demostración

Desde la carpeta raíz del proyecto, ejecuta:

```bash
python manage.py migrate
python manage.py configurar_roles
python manage.py cargar_demo
python manage.py runserver
```

El comando `cargar_demo` crea datos ficticios de propietarios, mascotas, veterinarios y citas. Es idempotente para los registros principales y utiliza fechas relativas para que la agenda diaria pueda demostrarse.

### Opción B: arreglo de objetos JSON

El archivo `citas/fixtures/vetagenda_demo.json` contiene un arreglo de objetos con la estructura estándar de fixtures de Django. Para cargarlo sobre una base recién migrada:

```bash
python manage.py migrate
python manage.py loaddata citas/fixtures/vetagenda_demo.json
python manage.py configurar_roles
```

El fixture incluye las cuatro entidades, sus llaves foráneas, estados, duraciones y campos de fecha. La carga debe realizarse en una base local de prueba o sobre una base vacía para evitar conflictos con identificadores existentes.

### Opción C: consultar el SQL generado por Django

La clase explicó que `CREATE TABLE`, `ALTER TABLE`, `SELECT`, `INSERT`, `UPDATE` y `DELETE` son instrucciones representativas del trabajo con SQL [1]. Django permite inspeccionar el SQL de cada migración sin escribirlo manualmente:

```bash
python manage.py sqlmigrate citas 0001
python manage.py sqlmigrate citas 0002
python manage.py sqlmigrate citas 0003
```

El archivo `docs/sql-schema-citas.sql` contiene una salida guardada del esquema principal para facilitar la revisión académica. En un entorno real, la ejecución se realizaría sobre una copia de prueba y con respaldo previo, como se recomendó en clase [2].

## 7. Pruebas de humo

Las pruebas de humo verifican que la aplicación pueda iniciar, que la configuración sea válida y que el flujo principal responda. Se ejecutaron los siguientes comandos:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Resultado obtenido:

| Prueba | Resultado |
|---|---|
| Comprobación del sistema Django | Correcta; no se reportaron problemas. |
| Migraciones pendientes | Ninguna; se mostró `No changes detected`. |
| Suite automatizada | Correcta; 11 pruebas ejecutadas y aprobadas, incluyendo roles, agenda diaria, dashboard y solapamientos. |
| Carga de datos de demostración | Correcta; el comando informó que los datos fueron cargados. |
| Dashboard | Verificado con totales generales y tarjetas por estado. |
| Agenda diaria | Verificada con la fecha actual y filtro por veterinario. |
| Reglas de horario | Verificadas mediante pruebas de duplicado y solapamiento parcial. |

## 8. Alcance y limitaciones

La fase 3 integra el modelo físico y el backend del proyecto. Todavía no incluye autenticación específica por usuario, recuperación de contraseña, API REST completa, notificaciones, pagos, historial clínico integral ni despliegue en producción. Estas funciones se desarrollarán únicamente cuando sean solicitadas en las fases correspondientes.

Los datos de demostración son ficticios. Si VetAgenda se utilizara en una clínica real, sería indispensable reforzar autorización por roles, privacidad, respaldos, auditoría y protección de datos personales.

## Referencias

[1]: https://us06web.zoom.us/rec/play/P9AovEsqMoyKsAl9o5C0nWxAv-O4z2dPr4EIL72ZVRA3Ux4_0S9uHSCw3RfrjMQQ8CImNKVxcjo9XRkN.O9qKNlyicXfGiknn "Clase de Aplicaciones Web II del 25 de agosto de 2026."

[2]: https://us06web.zoom.us/rec/play/0W9xQkhp0hxq_hS0YVjBtZtMIP6iXeRUdrAZzTWiN-0GWMz2g-jAX9mLr5lXc4KlPxdciyzyDGda4_qA.qsUCvgf0PyVS_-JA "Clase de Aplicaciones Web II del 27 de agosto de 2026."

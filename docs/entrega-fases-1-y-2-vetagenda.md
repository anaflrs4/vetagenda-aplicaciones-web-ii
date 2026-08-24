# VetAgenda
## Reporte integrado de las fases 1 y 2

**Asignatura:** Aplicaciones Web II  
**Estudiante:** [Escribe tu nombre]  
**Docente:** [Escribe el nombre de tu miss]  
**Fecha:** [Escribe la fecha de entrega]  
**Modalidad:** Trabajo individual

---

## Resumen ejecutivo

VetAgenda es una propuesta de aplicación web para una clínica veterinaria pequeña. Su propósito es centralizar la información de propietarios, mascotas, personal veterinario y citas, con el fin de facilitar la organización administrativa y el seguimiento de las consultas. La propuesta surge de una problemática concreta: cuando los datos se manejan en libretas, mensajes o archivos separados, localizar información, organizar horarios y conocer el estado de una cita puede requerir tiempo adicional.

La fase 1 se enfocó en la investigación y el análisis del problema. En ella se definieron la necesidad, la justificación, los objetivos, los usuarios y el funcionamiento esperado. La fase 2 incorpora el diseño técnico y el primer avance funcional del proyecto, adaptando el ejemplo de cafetería trabajado en clase al contexto veterinario. De acuerdo con las indicaciones de la docente, el proyecto debe personalizar los modelos, las plantillas y el contenido del negocio, mantener un repositorio público y explicar el producto como si se presentara ante un cliente [5] [6].

## 1. Introducción

Las clínicas veterinarias coordinan información de propietarios, mascotas, profesionales, horarios y consultas. En establecimientos pequeños, una misma persona puede atender tareas administrativas, recibir solicitudes y apoyar en la atención de los pacientes. Cuando no existe una herramienta centralizada, el proceso puede depender de registros dispersos y de la comunicación informal entre las personas que trabajan en la clínica.

VetAgenda propone una solución web sencilla, progresiva y reutilizable. El sistema se plantea para organizar las citas de una clínica veterinaria y relacionarlas con los datos básicos de la mascota y de su propietario. La aplicación se desarrollará por fases, de acuerdo con los temas revisados en Aplicaciones Web II. En la fase 2 se aplican el modelado de datos, las migraciones, las vistas, las plantillas y las operaciones básicas que se revisaron durante las clases [3] [4].

## 2. Fase 1: análisis e investigación

### 2.1 Planteamiento del problema

En una clínica veterinaria pequeña, los datos de las mascotas y sus propietarios pueden registrarse de manera manual o en diferentes medios. El personal puede recibir solicitudes por teléfono, mensajería instantánea o presencialmente y posteriormente anotarlas en una agenda física o en archivos no centralizados. Como consecuencia, consultar el historial básico de una mascota, confirmar la disponibilidad de un horario o verificar el estado de una cita puede requerir tiempo adicional.

El problema central de VetAgenda es la **falta de una herramienta centralizada para gestionar citas veterinarias y relacionarlas con la información básica de propietarios y mascotas**. Esta problemática se divide en tres necesidades:

| Necesidad | Manifestación | Solución propuesta |
|---|---|---|
| Centralización de información | Los datos de propietarios y mascotas pueden estar dispersos o duplicados. | Un registro común de propietarios y mascotas. |
| Organización de la agenda | Es difícil verificar disponibilidad y evitar confusiones de horario. | Una agenda de citas con fecha, hora, profesional y estado. |
| Seguimiento de la consulta | La persona propietaria puede no conocer el estado de su cita. | Estados de cita visibles: solicitada, confirmada, atendida o cancelada. |

Una investigación sobre aplicaciones web para clínicas veterinarias identifica que la gestión manual dificulta la organización de los archivos y puede provocar pérdida o duplicación de información. También relaciona el uso de una aplicación web con un acceso más ágil a los registros y una mejora de los procesos administrativos [1]. Otro trabajo académico propone registrar los datos de cada paciente y programar las próximas citas médicas para sistematizar los procesos y obtener información confiable [2].

### 2.2 Pregunta de investigación

¿Cómo puede una aplicación web centralizar la información básica de propietarios, mascotas y citas para mejorar la organización administrativa y el seguimiento de consultas en una clínica veterinaria pequeña?

### 2.3 Justificación

VetAgenda se justifica porque atiende una necesidad concreta: ordenar la información que interviene en la atención veterinaria. La propuesta no se limita a mostrar un calendario; plantea relacionar cada cita con una mascota, un propietario y un integrante del personal veterinario. Esta organización puede servir como base para incorporar posteriormente historiales, reportes y notificaciones.

El proyecto también es reutilizable. La estructura puede adaptarse a diferentes clínicas veterinarias, consultorios o refugios que necesiten administrar pacientes, propietarios y citas. Pueden cambiar el nombre de la clínica, los servicios, los horarios y el personal, pero se mantiene el componente lógico de registrar información y dar seguimiento a una consulta.

### 2.4 Objetivo general

Diseñar y desarrollar progresivamente una aplicación web que centralice la información básica de propietarios, mascotas y citas veterinarias para mejorar la organización administrativa y el seguimiento de consultas en una clínica veterinaria pequeña.

### 2.5 Objetivos específicos

| No. | Objetivo |
|---:|---|
| 1 | Analizar las dificultades que produce la gestión manual o dispersa de citas y registros veterinarios. |
| 2 | Identificar la información mínima necesaria para relacionar propietarios, mascotas, personal veterinario y citas. |
| 3 | Definir los roles principales de la aplicación y sus responsabilidades. |
| 4 | Diseñar modelos de datos para representar propietarios, mascotas, veterinarios y citas. |
| 5 | Implementar el primer avance funcional con Django, formularios, vistas y operaciones básicas de base de datos. |
| 6 | Mantener una estructura modular que pueda ampliarse en las fases siguientes. |

### 2.6 Usuarios y roles

| Rol | Responsabilidades previstas |
|---|---|
| Propietario de mascota | Consultar sus mascotas y solicitar o revisar una cita. |
| Personal veterinario | Consultar la agenda, revisar la información básica y actualizar el estado de una cita. |
| Administrador | Administrar usuarios, propietarios, mascotas, veterinarios, citas y configuración general. |

Los roles se definen en esta etapa como parte del análisis. La separación completa de permisos y la seguridad avanzada continuarán desarrollándose en las fases posteriores.

## 3. Fase 2: diseño y avance técnico

### 3.1 Alcance indicado en clase

En las clases del 18 y 20 de agosto de 2026, la docente indicó que la fase 2 debía integrar el proyecto con los contenidos técnicos de la semana: formularios, operaciones en bases de datos, modelos, vistas, plantillas, rutas y migraciones [3]. También explicó que el proyecto debía personalizarse para el negocio elegido, evitando dejarlo como una copia de la cafetería de ejemplo. La entrega debía incluir un repositorio público, el enlace HTTPS y un reporte que presentara la aplicación como si se explicara a un cliente [4].

La docente también comentó que el reporte debía complementarse con un video explicativo posterior, en el que cada estudiante describiera con sus propias palabras cómo fue construyendo el proyecto. El video no se sustituye con este documento; se prepara como un entregable adicional cuando la plataforma o la maestra lo soliciten.

### 3.2 Diseño funcional de VetAgenda

El flujo principal de la aplicación será el siguiente:

| Paso | Actor | Acción |
|---:|---|---|
| 1 | Administrador | Registra propietarios, mascotas y personal veterinario. |
| 2 | Propietario o administrador | Captura una solicitud de cita con mascota, fecha, hora y motivo. |
| 3 | Personal veterinario o administrador | Consulta la agenda y revisa la solicitud. |
| 4 | Personal veterinario o administrador | Actualiza el estado de la cita. |
| 5 | Propietario | Consulta la información y el estado de su cita. |

En esta fase se prioriza el flujo administrativo y el funcionamiento básico desde el proyecto Django. La autenticación específica para cada rol, los recordatorios automáticos, el historial clínico completo y otras funciones avanzadas se reservarán para las siguientes clases.

### 3.3 Modelo conceptual

El modelo de datos inicial estará compuesto por cuatro entidades principales. Un propietario puede tener una o más mascotas. Una mascota puede tener varias citas. Un veterinario puede atender varias citas. Cada cita registra la fecha, la hora, el motivo y el estado de la atención.

| Entidad | Datos principales |
|---|---|
| Propietario | Nombre completo, teléfono, correo electrónico y fecha de registro. |
| Mascota | Nombre, especie, raza, fecha de nacimiento aproximada y propietario. |
| Veterinario | Nombre completo, especialidad, teléfono y correo electrónico. |
| Cita | Mascota, veterinario, fecha, hora, motivo, estado y observaciones. |

Los estados previstos son `solicitada`, `confirmada`, `atendida` y `cancelada`. La validación de cruces de horario y las reglas de acceso se podrán fortalecer en fases posteriores.

### 3.4 Diseño técnico

El proyecto se organizará como una aplicación Django llamada `citas` dentro de un proyecto llamado `vetagenda`. La configuración utilizará Django REST Framework como dependencia de terceros, siguiendo la estructura trabajada en clase. La carpeta de migraciones conservará los cambios de los modelos y se ejecutarán los comandos de creación y aplicación de migraciones para reflejar el diseño en la base de datos.

La arquitectura inicial se dividirá en los siguientes elementos:

| Elemento | Función |
|---|---|
| `models.py` | Definir propietarios, mascotas, veterinarios y citas. |
| `forms.py` | Capturar y validar datos mediante formularios Django. |
| `views.py` | Procesar solicitudes y ejecutar operaciones de consulta, registro y actualización. |
| `urls.py` | Enrutar las páginas de la aplicación. |
| `templates/` | Mostrar formularios, listados, detalles y mensajes al usuario. |
| `admin.py` | Permitir administrar la información desde el panel de Django. |
| `migrations/` | Registrar los cambios del esquema de la base de datos. |

### 3.5 Operaciones básicas

La fase 2 contempla un primer conjunto de operaciones CRUD para demostrar el trabajo con formularios y base de datos. Las operaciones se enfocarán en registrar propietarios, mascotas, veterinarios y citas; consultar listados y detalles; modificar datos y actualizar el estado de las citas. La eliminación podrá realizarse de forma controlada desde el panel administrativo o desde las vistas autorizadas.

Estas operaciones son un avance académico inicial. No representan todavía la versión final del sistema ni deben interpretarse como un sistema clínico listo para producción.

## 4. Criterios de personalización

VetAgenda no conserva las categorías de productos, bebidas, cocina o pedidos de la cafetería de ejemplo. El dominio se adaptó a la gestión veterinaria y sus modelos se enfocan en propietarios, mascotas, veterinarios y citas. La interfaz utiliza lenguaje relacionado con una clínica veterinaria y la documentación explica un flujo de atención diferente al de un restaurante.

El repositorio incluirá un archivo `README.md` con el propósito del proyecto, el problema que atiende, las tecnologías, la estructura, la instalación y el alcance de la fase 2. También incluirá un archivo `.gitignore` para evitar subir el entorno virtual, cachés, secretos y archivos locales.

## 5. Cronograma del proyecto

| Periodo | Actividad | Resultado |
|---|---|---|
| Semana 1 | Investigación del problema y selección de la clínica veterinaria como contexto. | Fase 1 documentada. |
| Semana 2 | Definición de roles, entidades y flujo de trabajo. | Diseño preliminar. |
| Semana 3 | Configuración de dependencias, modelos y migraciones. | Base técnica de la fase 2. |
| Semana 4 | Formularios, vistas, plantillas y operaciones básicas. | Primer avance funcional. |
| Semanas posteriores | Seguridad, permisos, mejoras y pruebas. | Fases siguientes. |

## 6. Alcance y limitaciones

La entrega de fases 1 y 2 incluye la investigación, el diseño, el repositorio público, la estructura Django y el avance funcional indicado por la clase. No incluye pagos, notificaciones automáticas, despliegue productivo, integración con servicios externos, historial clínico completo ni una aplicación móvil. Estas funciones requerirán decisiones técnicas y requisitos adicionales.

La información utilizada en el proyecto es demostrativa y no corresponde a pacientes reales. Si el sistema llegara a utilizarse en un entorno real, sería necesario implementar controles de seguridad, respaldo, privacidad, autorización por roles y protección de datos personales.

## 7. Conclusiones

La fase 1 permitió delimitar una problemática concreta y justificar la creación de VetAgenda. La falta de centralización de información puede dificultar la organización de citas y la consulta de registros; por ello, una aplicación web representa una alternativa adecuada para ordenar el proceso administrativo de una clínica veterinaria [1] [2].

La fase 2 transforma el análisis en un diseño técnico y un avance funcional. La adaptación del ejemplo de clase al dominio veterinario permite trabajar con entidades y operaciones relacionadas con el problema elegido, en lugar de presentar una copia de la cafetería. La estructura de modelos, formularios, vistas, rutas, plantillas y migraciones prepara el sistema para continuar creciendo en las siguientes fases.

VetAgenda se plantea como un proyecto individual, modular y reutilizable. La entrega debe acompañarse del repositorio público y, cuando la docente lo solicite, de un video en el que se explique el proceso de construcción con palabras propias.

## Referencias

[1]: https://journals.gdeon.org/index.php/esj/article/view/174 "Cedeño Ochoa, A., Catuto Murillo, A. y Rodas-Silva, J. (2021). Use of Web applications for the management of veterinary clinics and their impact on the improvement of administrative processes. Ecuadorian Science Journal."

[2]: https://dspace.ups.edu.ec/handle/123456789/16991 "Loor García, Y. Y. (2019). Desarrollo de aplicación web para la gestión de consultas y agendamiento de citas de mascota de la clínica veterinaria Burgos. Universidad Politécnica Salesiana."

[3]: https://us06web.zoom.us/rec/play/3OM_gagL-hd7ZycEfLdbi2o98mwmreaD3cb_yFfBWkunpB14g-X4lSbUw_PDhv4nRH54ngX2DqvzsNf8.M6h_csFp3j2SbgcD "Grabación de Aplicaciones Web II del 18 de agosto de 2026."

[4]: https://us06web.zoom.us/rec/play/iKp5n7O_5voheVRrxfJtCvflme7mhAYgQG97BvdgBn_uSK8KGR2Du5IjH6rL7EzbfSpKVlhbAuW15ELP.jlYE_ZpxAzER5lmZ "Grabación de Aplicaciones Web II del 20 de agosto de 2026."

[5]: https://us06web.zoom.us/rec/play/xpiXtG2Xdm4Ku5-ToG4Rh8QetL8BoMohqkWoMQRURsJE5hoI8f1Ht_608IUFwEarfTXDvYsOvjpQcirB.ruayaNEWNs3A0R5Q "Grabación de Aplicaciones Web II del 11 de agosto de 2026."

[6]: https://us06web.zoom.us/rec/play/8BGovfR-hpcbB7A9sY9mEgYpnzU4yHD8rGM3VHFz54RutEcv12NrWcJgomomiSNk5HLJgGEStE3cNGst.Mld7TUn6EByrjm73 "Grabación de Aplicaciones Web II del 13 de agosto de 2026."

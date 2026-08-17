# VetAgenda
## Fase 1: análisis e investigación de una aplicación web para la gestión de citas veterinarias

**Asignatura:** Aplicaciones Web II  
**Estudiante:** [Escribe tu nombre]  
**Docente:** [Escribe el nombre de tu maestra]  
**Fecha:** [Escribe la fecha de entrega]  
**Modalidad:** Trabajo individual

---

## Introducción

Las clínicas veterinarias necesitan coordinar información de propietarios, mascotas, profesionales, horarios y consultas. Cuando estos datos se conservan en libretas, mensajes aislados o archivos independientes, la atención puede depender demasiado de la memoria del personal y resulta más difícil consultar rápidamente el estado de una cita. Esta situación es especialmente relevante en clínicas pequeñas, donde una misma persona puede desempeñar tareas administrativas y operativas.

El presente documento corresponde a la primera fase del proyecto **VetAgenda**, una propuesta de aplicación web para organizar citas veterinarias. La elección del tema responde a una problemática concreta: la dificultad para centralizar los registros y dar seguimiento a las consultas de las mascotas. Una investigación sobre aplicaciones web para clínicas veterinarias identifica que la gestión manual puede complicar la organización de archivos y producir pérdida o duplicidad de información; también señala beneficios asociados con el acceso ágil a registros, la búsqueda de información y la mejora de procesos administrativos [1].

La propuesta se plantea como un sistema reutilizable para clínicas veterinarias pequeñas. En esta primera fase no se pretende implementar todavía la totalidad del sistema, sino estudiar la necesidad, justificar la solución, definir los objetivos, identificar los roles y establecer una base para el desarrollo progresivo que se realizará en las siguientes clases. La estructura técnica inicial seguirá la orientación observada en las grabaciones de la asignatura: un proyecto desarrollado con Django y Django REST Framework, separado en una aplicación de dominio llamada `citas` [3] [4].

## 1. Planteamiento del problema

En una clínica veterinaria pequeña, la información de las mascotas y sus propietarios puede registrarse de manera manual o en diferentes medios. El personal puede recibir solicitudes por teléfono, mensajería instantánea o presencialmente y posteriormente anotar los datos en una agenda física o en archivos que no están centralizados. Como consecuencia, consultar el historial básico de una mascota, confirmar la disponibilidad de un horario o verificar el estado de una cita puede requerir tiempo adicional.

El problema principal que se atenderá es la **falta de una herramienta centralizada para gestionar citas veterinarias y relacionarlas con la información básica de propietarios y mascotas**. Esta situación puede manifestarse en tres necesidades relacionadas: dificultad para localizar y actualizar información, desorganización de la agenda y comunicación insuficiente sobre el estado de la cita.

| Necesidad identificada | Manifestación del problema | Respuesta preliminar de VetAgenda |
|---|---|---|
| Centralización de datos | Los registros de propietarios y mascotas pueden estar dispersos o duplicados. | Un espacio común para consultar y actualizar la información básica. |
| Organización de la agenda | Los horarios pueden gestionarse manualmente, lo que dificulta verificar disponibilidad y evitar cruces. | Una agenda de citas con fecha, hora, profesional, mascota y estado. |
| Seguimiento de la atención | El propietario puede no conocer si la cita está solicitada, confirmada, atendida o cancelada. | Estados visibles y comunicación clara del avance de la cita. |

La literatura consultada respalda la pertinencia del problema. Una investigación de la Universidad Politécnica Salesiana plantea una herramienta para registrar los datos de cada paciente y programar próximas citas médicas, con el propósito de sistematizar procesos y obtener información confiable de los registros [2]. De manera complementaria, un estudio sobre gestión digital de solicitudes encontró problemas relacionados con errores, esperas prolongadas e incertidumbre, y propuso registrar y dar seguimiento a las solicitudes con mayor rapidez y precisión [5]. Aunque este último estudio pertenece al contexto de restaurantes, su lógica de centralización y seguimiento puede trasladarse al proceso de agendamiento veterinario.

## 2. Pregunta de investigación

¿Cómo puede una aplicación web centralizar la información básica de propietarios, mascotas y citas para mejorar la organización administrativa y el seguimiento de consultas en una clínica veterinaria pequeña?

## 3. Justificación

VetAgenda se justifica porque propone una solución tecnológica para una necesidad concreta y observable: organizar la agenda y la información que interviene en la atención veterinaria. La solución no se limita a mostrar un calendario, sino que plantea relacionar cada cita con una mascota, un propietario y un integrante del personal. Esta relación permitiría que la información se consulte de manera ordenada y que, en fases posteriores, pueda utilizarse para generar historiales, reportes y notificaciones.

La elección de una clínica veterinaria también permite aplicar el principio de reutilización explicado en clase. La estructura puede adaptarse a distintas clínicas que manejen consultas, revisiones, vacunaciones o servicios para mascotas. El nombre de la clínica, los horarios, los servicios y los datos específicos pueden cambiar, pero el componente lógico de registrar personas, pacientes, profesionales y citas permanece semejante.

Desde una perspectiva administrativa, la propuesta podría reducir la dependencia de registros dispersos y facilitar la localización de información. Desde la perspectiva del propietario, podría ofrecer mayor claridad sobre la fecha y el estado de la consulta. Desde la perspectiva del personal veterinario, podría proporcionar una agenda organizada para priorizar y actualizar la atención. Estos beneficios son objetivos de diseño; su medición y validación se podrán realizar en fases posteriores, cuando exista una versión funcional.

## 4. Objetivos

### 4.1 Objetivo general

Diseñar una aplicación web que centralice la información básica de propietarios, mascotas y citas veterinarias para mejorar la organización administrativa y el seguimiento de consultas en una clínica veterinaria pequeña.

### 4.2 Objetivos específicos

| No. | Objetivo específico |
|---:|---|
| 1 | Analizar las dificultades que produce la gestión manual o dispersa de citas y registros veterinarios. |
| 2 | Identificar la información mínima necesaria para relacionar propietarios, mascotas, personal veterinario y citas. |
| 3 | Definir los roles principales de la aplicación y las responsabilidades preliminares de cada uno. |
| 4 | Diseñar una estructura inicial de proyecto con Django y Django REST Framework, de acuerdo con el enfoque técnico presentado en clase. |
| 5 | Proponer una solución modular y reutilizable que pueda ampliarse durante las siguientes fases del proyecto. |

## 5. Alcance de la primera fase

La primera fase comprende la investigación del problema, la justificación de la solución, los objetivos, la definición de los usuarios y un diseño preliminar. También incluye un esqueleto inicial del proyecto con una pantalla de presentación de la propuesta y la estructura básica de un proyecto Django.

En esta entrega no se implementan autenticación, permisos, modelos persistentes, historial clínico, notificaciones, pagos, reportes ni endpoints completos de una API. Estas funciones se reservan para las siguientes fases y se incorporarán únicamente cuando correspondan con las instrucciones de clase. La decisión permite mantener el alcance de la actividad en la fase de análisis e investigación, tal como se indicó en la segunda grabación [4].

## 6. Usuarios y roles preliminares

La aplicación contempla tres roles de referencia. La maestra explicó en clase que el sistema debe distinguir entre la persona que utiliza la aplicación como cliente, el personal que opera el proceso y la administración general [3]. Para VetAgenda, estos roles se adaptan de la siguiente manera:

| Rol | Descripción | Necesidades principales |
|---|---|---|
| Propietario de mascota | Persona responsable de una o más mascotas que solicita o consulta una cita. | Registrar datos básicos, solicitar una cita y consultar su fecha y estado. |
| Personal veterinario | Veterinario o colaborador encargado de revisar la agenda y atender consultas. | Consultar las citas del día, revisar información básica y actualizar el estado de atención. |
| Administrador | Persona responsable de la operación general de la clínica. | Gestionar usuarios, horarios, servicios, profesionales y configuración general. |

En la fase actual estos roles son parte del diseño conceptual. No se implementan todavía contraseñas ni restricciones de acceso. En una fase posterior, cada rol podrá tener permisos específicos para evitar que un usuario consulte o modifique información que no le corresponda.

## 7. Diseño preliminar de la solución

La solución se organizará en torno a una entidad principal llamada **cita**. Cada cita deberá relacionarse con una mascota, un propietario y un integrante del personal veterinario, además de incluir fecha, hora, motivo de consulta y estado. El diseño preliminar no fija todavía todos los campos porque esa decisión debe revisarse durante la fase de modelado de datos.

| Componente conceptual | Información inicial prevista |
|---|---|
| Propietario | Nombre, teléfono, correo y relación con la mascota. |
| Mascota | Nombre, especie, raza, edad aproximada y propietario. |
| Personal veterinario | Nombre, especialidad o función y disponibilidad. |
| Cita | Fecha, hora, motivo, profesional asignado y estado. |
| Estado de cita | Solicitada, confirmada, atendida o cancelada. |

El flujo preliminar de uso sería el siguiente: el propietario solicita una cita indicando la mascota y el motivo; la clínica revisa la disponibilidad; el personal o la administración confirma la cita; el personal veterinario consulta la agenda; finalmente, el estado se actualiza después de la atención. Este flujo no se implementa completamente en esta fase, pero orientará el modelado y la interfaz de las siguientes entregas.

La estructura inicial del repositorio separa el proyecto Django `vetagenda` de la aplicación `citas`. La configuración incluye Django REST Framework como dependencia de terceros, siguiendo el procedimiento mostrado en clase. El archivo `.gitignore` excluye el entorno virtual, cachés, archivos locales y la base de datos de desarrollo para evitar que el repositorio contenga archivos innecesarios o dependientes de una computadora específica.

## 8. Cronograma preliminar

| Periodo | Actividad | Entregable |
|---|---|---|
| Semana 1 | Investigación del problema y selección del tema. | Planteamiento del problema y fuentes confiables. |
| Semana 1 | Definición de objetivos, justificación y roles. | Documento de fase 1. |
| Semana 2 | Diseño de modelos y estructura de datos. | Diagrama o diseño de entidades. |
| Semana 2 | Configuración de la aplicación Django. | Proyecto y aplicación iniciales. |
| Semana 3 | Desarrollo progresivo del flujo de citas. | Primeras vistas, modelos o endpoints. |
| Semanas posteriores | Integración, pruebas y mejoras. | Versión funcional por fases. |

Este cronograma es una propuesta de organización personal. Las fechas exactas se ajustarán al calendario y a las instrucciones de la docente.

## 9. Conclusiones

La investigación permitió definir una problemática concreta para el proyecto: la dificultad de centralizar y dar seguimiento a la información de citas, mascotas y propietarios en una clínica veterinaria pequeña. Las fuentes consultadas muestran que la gestión manual puede generar problemas de organización, pérdida o duplicidad de información y dificultad para obtener registros confiables [1] [2]. Por esta razón, una aplicación web constituye una alternativa pertinente para ordenar el proceso administrativo.

VetAgenda responde a la problemática mediante una propuesta reutilizable que considera tres roles: propietario de mascota, personal veterinario y administrador. El sistema podrá crecer de manera progresiva, comenzando con la investigación y el diseño conceptual y continuando con el modelado, la autenticación, la gestión de citas y los servicios de la API en las fases posteriores.

El resultado de esta primera actividad es una base documental y técnica, no una aplicación terminada. Se creó un esqueleto inicial en Django con una pantalla de presentación que comunica el problema, la propuesta y los roles. Mantener este alcance es importante porque permite avanzar conforme a las instrucciones de la asignatura sin implementar anticipadamente funcionalidades que corresponden a otras clases.

## Referencias

[1]: https://journals.gdeon.org/index.php/esj/article/view/174 "Cedeño Ochoa, A., Catuto Murillo, A. y Rodas-Silva, J. (2021). Use of Web applications for the management of veterinary clinics and their impact on the improvement of administrative processes. Ecuadorian Science Journal."

[2]: https://dspace.ups.edu.ec/handle/123456789/16991 "Loor García, Y. Y. (2019). Desarrollo de aplicación web para la gestión de consultas y agendamiento de citas de mascota de la clínica veterinaria Burgos. Universidad Politécnica Salesiana."

[3]: https://us06web.zoom.us/rec/play/xpiXtG2Xdm4Ku5-ToG4Rh8QetL8BoMohqkWoMQRURsJE5hoI8f1Ht_608IUFwEarfTXDvYsOvjpQcirB.ruayaNEWNs3A0R5Q "Grabación de Aplicaciones Web II del 11 de agosto de 2026."

[4]: https://us06web.zoom.us/rec/play/8BGovfR-hpcbB7A9sY9mEgYpnzU4yHD8rGM3VHFz54RutEcv12NrWcJgomomiSNk5HLJgGEStE3cNGst.Mld7TUn6EByrjm73 "Grabación de Aplicaciones Web II del 13 de agosto de 2026."

[5]: https://revistaveritas.org/index.php/veritas/article/view/625 "Ramírez, K. M. M. et al. (2025). Aplicaciones Móviles para la Gestión de Pedidos. Caso Práctico en la Ciudad de Portoviejo. Revista Veritas de Difusão Científica."

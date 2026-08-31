# VetAgenda

**VetAgenda** es una aplicación web académica para organizar la información de una clínica veterinaria pequeña. Centraliza propietarios, mascotas, veterinarios y citas en un solo lugar, con una estructura preparada para crecer durante las siguientes fases de Aplicaciones Web II.

> Esta entrega integra las **fases 1, 2 y 3**. La fase 1 contiene la investigación, el análisis del problema, los objetivos y el diseño preliminar. La fase 2 incorpora modelos Django, migraciones, formularios, vistas, rutas, plantillas, panel administrativo y operaciones básicas. La fase 3 documenta el modelo físico, la conexión con el backend, los roles y permisos, la recreación de datos y las pruebas de humo.

## Problemática

En una clínica veterinaria pequeña, los datos de propietarios, mascotas y consultas pueden estar dispersos entre libretas, mensajes y archivos independientes. Esto dificulta localizar información, organizar horarios y conocer el estado de cada cita. La literatura revisada relaciona la gestión manual con problemas de organización, pérdida o duplicidad de información y procesos administrativos poco eficientes [1]. Un trabajo académico sobre una clínica veterinaria también identifica la utilidad de registrar los datos de cada paciente y programar sus próximas citas [2].

VetAgenda responde a tres necesidades: centralizar los registros, ordenar la agenda del personal veterinario y mejorar el seguimiento del estado de cada cita.

## Objetivo general

Diseñar y desarrollar progresivamente una aplicación web que centralice la información básica de propietarios, mascotas y citas veterinarias para mejorar la organización administrativa y el seguimiento de consultas.

## Roles preliminares

| Rol | Responsabilidad prevista |
|---|---|
| Propietario de mascota | Consultar sus mascotas y solicitar o revisar una cita. |
| Personal veterinario | Consultar la agenda y actualizar el estado de la atención. |
| Administrador | Gestionar propietarios, mascotas, veterinarios, citas y configuración general. |

Los grupos y permisos base se pueden crear con `python manage.py configurar_roles`. La autenticación específica por usuario y el filtrado automático de cada vista se continuarán en fases posteriores. El panel administrativo de Django permite gestionar los registros con una cuenta de superusuario.

## Funcionalidades de la fase 2

| Módulo | Funcionalidades implementadas |
|---|---|
| Panel | Resumen de registros, próximas citas y navegación principal. |
| Propietarios | Listar, buscar, registrar, editar y eliminar propietarios. |
| Mascotas | Listar, buscar, registrar, editar y eliminar mascotas relacionadas con un propietario. |
| Veterinarios | Listar, buscar, registrar, editar y eliminar personal veterinario. |
| Citas | Listar, buscar, filtrar por estado, registrar, ver detalle, editar y eliminar citas. |
| Agenda de hoy | Mostrar solo las citas del día actual y filtrarlas por veterinario activo. |
| Dashboard | Mostrar tarjetas con colores para solicitada, confirmada, atendida y cancelada. |
| Validación | Evitar citas activas solapadas para un mismo veterinario, considerando una duración de 30, 45 o 60 minutos. |
| Administración | Gestionar las cuatro entidades desde `/admin/` mediante el panel de Django. |

Los datos incluidos con el comando de demostración son ficticios. No se utilizan pacientes ni propietarios reales.

Las reglas de acceso, los estados y la gestión de horarios están documentadas en `docs/reglas-acceso-horarios.md`. En la fase actual se incluye la vista `/citas/hoy/` como aproximación a la agenda diaria del personal veterinario; la autenticación por usuario y los permisos específicos se implementarán cuando correspondan a una fase posterior.

## Tecnologías

El proyecto utiliza **Python**, **Django 5.2** y **Django REST Framework**. La fase actual utiliza las vistas y formularios de Django para demostrar el flujo web y deja preparado el proyecto para incorporar serializers y endpoints de API cuando sean solicitados en clases posteriores. La base de datos local de desarrollo utiliza SQLite.

## Estructura principal

```text
vetagenda/
├── citas/
│   ├── fixtures/vetagenda_demo.json
│   ├── management/commands/{cargar_demo,configurar_roles}.py
│   ├── migrations/{0001_initial,0002_cita_duracion_minutos,0003_...}.py
│   ├── templates/citas/
│   │   ├── base.html
│   │   ├── inicio.html
│   │   ├── formulario.html
│   │   ├── propietarios/lista.html
│   │   ├── mascotas/lista.html
│   │   ├── veterinarios/lista.html
│   │   └── citas/{lista,detalle}.html
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── docs/
│   ├── entrega-fase-3-vetagenda.md
│   ├── entrega-fases-1-y-2-vetagenda.md
│   ├── fase-1-analisis-vetagenda.md
│   ├── reglas-acceso-horarios.md
│   ├── pruebas-humo-fase-3.md
│   ├── sql-schema-citas.sql
│   └── verificacion-fase-2.md
├── vetagenda/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Instalación local

Se recomienda utilizar Python 3.11 o una versión compatible. Desde la carpeta del proyecto, crea un entorno virtual, instala las dependencias, aplica las migraciones y ejecuta el servidor:

```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` para ver el panel de VetAgenda. La agenda diaria se encuentra en `http://127.0.0.1:8000/citas/hoy/`.

### Datos ficticios y roles para la demostración

Para cargar propietarios, mascotas, veterinarios y citas de ejemplo, ejecuta:

```bash
python manage.py cargar_demo
```

El comando se puede ejecutar nuevamente sin duplicar los datos principales. También se puede cargar el arreglo de objetos JSON incluido en `citas/fixtures/vetagenda_demo.json` mediante `python manage.py loaddata citas/fixtures/vetagenda_demo.json`. Para configurar los grupos y permisos definidos en la fase 3, ejecuta `python manage.py configurar_roles`. Para entrar al panel administrativo, crea una cuenta local:

```bash
python manage.py createsuperuser
```

Después abre `http://127.0.0.1:8000/admin/` e inicia sesión con las credenciales que hayas creado localmente. No se incluyen contraseñas en el repositorio.

## Pruebas

El proyecto incluye once pruebas para la pantalla inicial, las relaciones del modelo, la validación de horarios duplicados y solapados, el registro de citas, el filtro por estado, el listado de mascotas, la agenda diaria, el resumen del dashboard y la creación de grupos y permisos. La bitácora de pruebas de humo de fase 3 se encuentra en `docs/pruebas-humo-fase-3.md`. Para ejecutarlas:

```bash
python manage.py check
python manage.py test
```

## Alcance y siguientes fases

Esta entrega no incluye pagos, notificaciones automáticas, despliegue en producción, aplicación móvil, historial clínico completo, autenticación específica por rol ni una API REST completa. Estas funciones se reservarán para las siguientes fases, conforme a las instrucciones de la asignatura.

## Referencias

[1]: https://journals.gdeon.org/index.php/esj/article/view/174 "Cedeño Ochoa, A., Catuto Murillo, A. y Rodas-Silva, J. (2021). Use of Web applications for the management of veterinary clinics and their impact on the improvement of administrative processes. Ecuadorian Science Journal."

[2]: https://dspace.ups.edu.ec/handle/123456789/16991 "Loor García, Y. Y. (2019). Desarrollo de aplicación web para la gestión de consultas y agendamiento de citas de mascota de la clínica veterinaria Burgos. Universidad Politécnica Salesiana."

[3]: https://us06web.zoom.us/rec/play/3OM_gagL-hd7ZycEfLdbi2o98mwmreaD3cb_yFfBWkunpB14g-X4lSbUw_PDhv4nRH54ngX2DqvzsNf8.M6h_csFp3j2SbgcD "Grabación de Aplicaciones Web II del 18 de agosto de 2026."

[4]: https://us06web.zoom.us/rec/play/iKp5n7O_5voheVRrxfJtCvflme7mhAYgQG97BvdgBn_uSK8KGR2Du5IjH6rL7EzbfSpKVlhbAuW15ELP.jlYE_ZpxAzER5lmZ "Grabación de Aplicaciones Web II del 20 de agosto de 2026."

[5]: https://github.com/anaflrs4/vetagenda-aplicaciones-web-ii "Repositorio público de VetAgenda."

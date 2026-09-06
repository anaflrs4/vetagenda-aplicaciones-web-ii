# VetAgenda

**VetAgenda** es una aplicación web académica para organizar la información de una clínica veterinaria pequeña. Centraliza propietarios, mascotas, veterinarios y citas en un solo lugar, con una estructura preparada para crecer durante las siguientes fases de Aplicaciones Web II.

> Esta entrega integra las **fases 1 a 4**. La fase 1 contiene la investigación y el análisis; la fase 2 incorpora el primer avance funcional; la fase 3 consolida el modelo físico, los roles, la recreación de datos y las pruebas de humo; y la fase 4 implementa la arquitectura **View → DAO → ORM → base de datos**, conecta el frontend con el backend y prueba el DAO y el endpoint REST.

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

## Arquitectura y tecnologías

El proyecto utiliza **Python**, **Django 5.2**, **Django REST Framework** y SQLite. Desde la fase 4, las vistas no consultan directamente `Modelo.objects`; delegan las operaciones en `citas/dao.py`. La ruta `/api/citas/activas/` responde en JSON mediante `CitasActivasAPIView`, `CitaDAO` y `CitaSerializer`.

| Flujo | Implementación |
|---|---|
| Interfaz → vista | Plantillas y formularios envían solicitudes GET o POST. |
| Vista → DAO | `views.py` y `api_views.py` llaman a los métodos DAO. |
| DAO → ORM | `dao.py` centraliza consultas, guardado, eliminación y estados. |
| ORM → datos | Los modelos y migraciones persisten la información en SQLite. |

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
│   ├── api_views.py
│   ├── dao.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── docs/
│   ├── assets/{dashboard-fase-3,agenda-hoy-fase-3}.webp
│   ├── assets/fase4/{agenda-dao-antes,agenda-dao-atendida,api-citas-activas-200}.png
│   ├── diagrama-dao-fase4.{mmd,png}
│   ├── ProyectoFases1a4_VetAgenda_integrado.docx
│   ├── entrega-fase-3-vetagenda.md
│   ├── entrega-fase-4-vetagenda.md
│   ├── entrega-fases-1-y-2-vetagenda.md
│   ├── fase-1-analisis-vetagenda.md
│   ├── reglas-acceso-horarios.md
│   ├── pruebas-humo-fase-3.md
│   ├── resultados-pruebas-fase4.txt
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

Abre `http://127.0.0.1:8000/` para ver el panel de VetAgenda. La agenda diaria se encuentra en `http://127.0.0.1:8000/citas/hoy/` y el endpoint REST en `http://127.0.0.1:8000/api/citas/activas/`.

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

El proyecto incluye **18 pruebas**. Además de la cobertura anterior, la fase 4 verifica el CRUD mediante DAO, las búsquedas, las transiciones válidas e inválidas de las citas, la respuesta JSON con código 200 y la delegación de las vistas a `CitaDAO` mediante mocks. El resultado detallado se encuentra en `docs/resultados-pruebas-fase4.txt` y el informe ejecutivo en `docs/entrega-fase-4-vetagenda.md`.

```bash
python manage.py check
python manage.py test
```

## Alcance y siguientes fases

Esta entrega no incluye pagos, notificaciones automáticas, despliegue en producción, aplicación móvil, historial clínico completo ni autenticación específica por usuario. La API actual es un endpoint académico de solo lectura para citas activas; una API completa con autenticación se reserva para fases posteriores.

## Referencias

[1]: https://journals.gdeon.org/index.php/esj/article/view/174 "Cedeño Ochoa, A., Catuto Murillo, A. y Rodas-Silva, J. (2021). Use of Web applications for the management of veterinary clinics and their impact on the improvement of administrative processes. Ecuadorian Science Journal."

[2]: https://dspace.ups.edu.ec/handle/123456789/16991 "Loor García, Y. Y. (2019). Desarrollo de aplicación web para la gestión de consultas y agendamiento de citas de mascota de la clínica veterinaria Burgos. Universidad Politécnica Salesiana."

[3]: https://us06web.zoom.us/rec/play/3OM_gagL-hd7ZycEfLdbi2o98mwmreaD3cb_yFfBWkunpB14g-X4lSbUw_PDhv4nRH54ngX2DqvzsNf8.M6h_csFp3j2SbgcD "Grabación de Aplicaciones Web II del 18 de agosto de 2026."

[4]: https://us06web.zoom.us/rec/play/iKp5n7O_5voheVRrxfJtCvflme7mhAYgQG97BvdgBn_uSK8KGR2Du5IjH6rL7EzbfSpKVlhbAuW15ELP.jlYE_ZpxAzER5lmZ "Grabación de Aplicaciones Web II del 20 de agosto de 2026."

[5]: https://github.com/anaflrs4/vetagenda-aplicaciones-web-ii "Repositorio público de VetAgenda."

[6]: https://us06web.zoom.us/rec/play/KrKLTlejmLr_Wr_nF2ek7J17GzoG7nBGGR2RSuVOUaGcoRTTXhYz4DVyN-_Yegg7Kj2nKLCMPraqRt-n.yUahetpjyQQ9TuWy "Grabación de Aplicaciones Web II del 2 de septiembre de 2026."

[7]: https://us06web.zoom.us/rec/play/2dkhOqlC_l-ie2o3s9Q1CikNpzunutbO-aQ8inISwa6hrev4QEyXhHOo3NKe0HggDPLAt4eriiB87bQa.yytVfQ4KGNp7pp4t "Grabación de Aplicaciones Web II del 3 de septiembre de 2026."

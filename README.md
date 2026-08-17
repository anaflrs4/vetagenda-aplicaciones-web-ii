# VetAgenda

**VetAgenda** es una propuesta de aplicación web para pequeñas clínicas veterinarias. Su finalidad es organizar la información básica de propietarios, mascotas y citas en un solo lugar, con una estructura que pueda ampliarse durante las siguientes fases de la asignatura Aplicaciones Web II.

> Esta entrega corresponde únicamente a la **fase 1: análisis e investigación**. La aplicación contiene un esqueleto inicial y una pantalla de presentación; la autenticación, los permisos, los modelos de base de datos, el historial clínico, las notificaciones y el flujo completo de citas se desarrollarán posteriormente, conforme avancen las clases.

## Problemática

En una clínica veterinaria pequeña, el uso de registros manuales o dispersos puede dificultar la localización y actualización de la información de propietarios, mascotas y consultas. La literatura revisada relaciona esta situación con pérdida o duplicidad de información, búsquedas lentas y procesos administrativos poco eficientes [1]. Asimismo, una propuesta académica de gestión veterinaria identifica la necesidad de registrar los datos de cada paciente y programar las próximas citas para obtener información más confiable [2].

A partir de esta problemática se plantean tres necesidades: centralizar los registros, ordenar la agenda del personal veterinario y mejorar la comunicación del estado de cada cita con la persona propietaria de la mascota.

## Objetivo general

Diseñar una aplicación web que permita organizar la información básica de propietarios, mascotas y citas veterinarias, con una arquitectura preparada para mejorar el control administrativo y el seguimiento de las consultas.

## Objetivos específicos

| Objetivo | Propósito |
|---|---|
| Analizar la problemática de la gestión manual o dispersa | Identificar las necesidades que justifican la aplicación. |
| Definir los usuarios y roles principales | Separar las responsabilidades del propietario, el personal veterinario y la administración. |
| Diseñar la estructura inicial del proyecto | Preparar la base técnica para incorporar funcionalidades en las siguientes fases. |
| Proponer una solución reutilizable | Permitir que la lógica pueda adaptarse a clínicas veterinarias pequeñas con necesidades semejantes. |

## Roles preliminares

| Rol | Responsabilidad prevista |
|---|---|
| Propietario de mascota | Solicitar o consultar una cita y revisar la información básica de su mascota. |
| Personal veterinario | Consultar la agenda y actualizar el estado de las citas durante la atención. |
| Administrador | Gestionar la información general, los usuarios y la configuración de la clínica. |

Estos roles son parte del diseño preliminar. En esta fase todavía no se implementan permisos ni autenticación.

## Tecnologías previstas

El esqueleto se basa en **Django** y **Django REST Framework**, siguiendo la demostración de clase. La estructura separa el proyecto `vetagenda` de la aplicación `citas`. La pantalla inicial está implementada con una vista y una plantilla HTML para presentar la problemática y los roles, pero aún no se han definido los modelos ni los endpoints de la API.

## Estructura principal

```text
vetagenda/
├── citas/
│   ├── migrations/
│   ├── templates/citas/inicio.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── docs/
├── vetagenda/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Instalación local

Se recomienda utilizar Python 3.11 o una versión compatible. Desde la carpeta del proyecto se puede crear un entorno virtual, instalar las dependencias y ejecutar el servidor de desarrollo:

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

Después se puede abrir `http://127.0.0.1:8000/` en el navegador. La pantalla inicial muestra la propuesta de VetAgenda y el alcance de esta primera fase.

## Próximas fases

Las siguientes fases podrán incorporar el diseño de modelos para propietarios, mascotas, veterinarios y citas; autenticación y permisos por rol; operaciones de creación, consulta, actualización y cancelación; historial de citas; serializadores y endpoints de Django REST Framework; y una interfaz más completa. Esas funcionalidades no forman parte de esta entrega inicial.

## Referencias

[1]: https://journals.gdeon.org/index.php/esj/article/view/174 "Use of Web applications for the management of veterinary clinics and their impact on the improvement of administrative processes, Ecuadorian Science Journal"

[2]: https://dspace.ups.edu.ec/handle/123456789/16991 "Desarrollo de aplicación web para la gestión de consultas y agendamiento de citas de mascota de la clínica veterinaria Burgos, Universidad Politécnica Salesiana"

[3]: https://us06web.zoom.us/rec/play/xpiXtG2Xdm4Ku5-ToG4Rh8QetL8BoMohqkWoMQRURsJE5hoI8f1Ht_608IUFwEarfTXDvYsOvjpQcirB.ruayaNEWNs3A0R5Q "Grabación de la clase del 11 de agosto de 2026"

[4]: https://us06web.zoom.us/rec/play/8BGovfR-hpcbB7A9sY9mEgYpnzU4yHD8rGM3VHFz54RutEcv12NrWcJgomomiSNk5HLJgGEStE3cNGst.Mld7TUn6EByrjm73 "Grabación de la clase del 13 de agosto de 2026"

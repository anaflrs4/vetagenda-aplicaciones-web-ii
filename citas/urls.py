from django.urls import path

from . import views


app_name = "citas"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("propietarios/", views.propietarios, name="propietarios"),
    path("propietarios/nuevo/", views.propietario_nuevo, name="propietario_nuevo"),
    path(
        "propietarios/<int:pk>/editar/",
        views.propietario_editar,
        name="propietario_editar",
    ),
    path(
        "propietarios/<int:pk>/eliminar/",
        views.propietario_eliminar,
        name="propietario_eliminar",
    ),
    path("mascotas/", views.mascotas, name="mascotas"),
    path("mascotas/nueva/", views.mascota_nueva, name="mascota_nueva"),
    path("mascotas/<int:pk>/editar/", views.mascota_editar, name="mascota_editar"),
    path(
        "mascotas/<int:pk>/eliminar/",
        views.mascota_eliminar,
        name="mascota_eliminar",
    ),
    path("veterinarios/", views.veterinarios, name="veterinarios"),
    path(
        "veterinarios/nuevo/",
        views.veterinario_nuevo,
        name="veterinario_nuevo",
    ),
    path(
        "veterinarios/<int:pk>/editar/",
        views.veterinario_editar,
        name="veterinario_editar",
    ),
    path(
        "veterinarios/<int:pk>/eliminar/",
        views.veterinario_eliminar,
        name="veterinario_eliminar",
    ),
    path("citas/", views.citas, name="citas"),
    path("citas/hoy/", views.agenda_hoy, name="agenda_hoy"),
    path("citas/nueva/", views.cita_nueva, name="cita_nueva"),
    path("citas/<int:pk>/", views.cita_detalle, name="cita_detalle"),
    path("citas/<int:pk>/editar/", views.cita_editar, name="cita_editar"),
    path("citas/<int:pk>/eliminar/", views.cita_eliminar, name="cita_eliminar"),
]

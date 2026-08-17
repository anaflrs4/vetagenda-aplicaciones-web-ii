from django.shortcuts import render


def inicio(request):
    """Render the first-phase project landing page."""
    context = {
        "nombre_app": "VetAgenda",
        "descripcion": (
            "Propuesta de aplicación web para organizar citas veterinarias, "
            "mascotas y propietarios en una clínica pequeña."
        ),
        "roles": [
            "Propietario de mascota",
            "Personal veterinario",
            "Administrador",
        ],
    }
    return render(request, "citas/inicio.html", context)

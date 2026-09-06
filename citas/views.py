from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .dao import CitaDAO, MascotaDAO, PropietarioDAO, VeterinarioDAO
from .forms import CitaForm, MascotaForm, PropietarioForm, VeterinarioForm
from .models import Cita


def _requerir(registro, mensaje="El registro solicitado no existe."):
    if registro is None:
        raise Http404(mensaje)
    return registro


def inicio(request):
    """Dashboard principal conectado a la capa DAO."""
    context = {
        "nombre_app": "VetAgenda",
        "descripcion": (
            "Sistema web para organizar citas, mascotas y propietarios "
            "de una clínica veterinaria."
        ),
        "roles": [
            "Propietario de mascota",
            "Personal veterinario",
            "Administrador",
        ],
        "totales": {
            "propietarios": PropietarioDAO.contar(),
            "mascotas": MascotaDAO.contar(),
            "veterinarios": VeterinarioDAO.contar_activos(),
            "citas": CitaDAO.contar(),
        },
        "resumen_estados": CitaDAO.resumen_estados(),
        "citas_proximas": CitaDAO.listar_proximas(),
    }
    return render(request, "citas/inicio.html", context)


def propietarios(request):
    q = request.GET.get("q", "").strip()
    return render(
        request,
        "citas/propietarios/lista.html",
        {"registros": PropietarioDAO.listar(q), "q": q},
    )


def propietario_nuevo(request):
    form = PropietarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        propietario = PropietarioDAO.guardar(form.save(commit=False))
        messages.success(request, f"Se registró a {propietario.nombre_completo}.")
        return redirect("citas:propietarios")
    return render(
        request,
        "citas/formulario.html",
        {
            "form": form,
            "titulo": "Registrar propietario",
            "descripcion": "Agrega los datos de contacto de la persona responsable.",
            "volver": "citas:propietarios",
        },
    )


def propietario_editar(request, pk):
    registro = _requerir(PropietarioDAO.obtener_por_id(pk))
    form = PropietarioForm(request.POST or None, instance=registro)
    if request.method == "POST" and form.is_valid():
        PropietarioDAO.guardar(form.save(commit=False))
        messages.success(request, "Los datos del propietario se actualizaron.")
        return redirect("citas:propietarios")
    return render(
        request,
        "citas/formulario.html",
        {
            "form": form,
            "titulo": "Editar propietario",
            "descripcion": "Actualiza la información de contacto registrada.",
            "volver": "citas:propietarios",
        },
    )


def propietario_eliminar(request, pk):
    registro = _requerir(PropietarioDAO.obtener_por_id(pk))
    if request.method == "POST":
        nombre = registro.nombre_completo
        PropietarioDAO.eliminar(registro)
        messages.success(request, f"Se eliminó el registro de {nombre}.")
        return redirect("citas:propietarios")
    return render(
        request,
        "citas/confirmar_eliminacion.html",
        {
            "registro": registro,
            "tipo": "propietario",
            "volver": "citas:propietarios",
        },
    )


def mascotas(request):
    q = request.GET.get("q", "").strip()
    return render(
        request,
        "citas/mascotas/lista.html",
        {"registros": MascotaDAO.listar(q), "q": q},
    )


def mascota_nueva(request):
    form = MascotaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        mascota = MascotaDAO.guardar(form.save(commit=False))
        messages.success(request, f"Se registró a {mascota.nombre}.")
        return redirect("citas:mascotas")
    return render(
        request,
        "citas/formulario.html",
        {
            "form": form,
            "titulo": "Registrar mascota",
            "descripcion": "Relaciona la mascota con su propietario.",
            "volver": "citas:mascotas",
        },
    )


def mascota_editar(request, pk):
    registro = _requerir(MascotaDAO.obtener_por_id(pk))
    form = MascotaForm(request.POST or None, instance=registro)
    if request.method == "POST" and form.is_valid():
        MascotaDAO.guardar(form.save(commit=False))
        messages.success(request, "Los datos de la mascota se actualizaron.")
        return redirect("citas:mascotas")
    return render(
        request,
        "citas/formulario.html",
        {
            "form": form,
            "titulo": "Editar mascota",
            "descripcion": "Actualiza la ficha básica de la mascota.",
            "volver": "citas:mascotas",
        },
    )


def mascota_eliminar(request, pk):
    registro = _requerir(MascotaDAO.obtener_por_id(pk))
    if request.method == "POST":
        nombre = registro.nombre
        MascotaDAO.eliminar(registro)
        messages.success(request, f"Se eliminó la mascota {nombre}.")
        return redirect("citas:mascotas")
    return render(
        request,
        "citas/confirmar_eliminacion.html",
        {"registro": registro, "tipo": "mascota", "volver": "citas:mascotas"},
    )


def veterinarios(request):
    q = request.GET.get("q", "").strip()
    return render(
        request,
        "citas/veterinarios/lista.html",
        {"registros": VeterinarioDAO.listar(q), "q": q},
    )


def veterinario_nuevo(request):
    form = VeterinarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        veterinario = VeterinarioDAO.guardar(form.save(commit=False))
        messages.success(request, f"Se registró a {veterinario.nombre_completo}.")
        return redirect("citas:veterinarios")
    return render(
        request,
        "citas/formulario.html",
        {
            "form": form,
            "titulo": "Registrar veterinario",
            "descripcion": "Agrega el personal que atenderá las consultas.",
            "volver": "citas:veterinarios",
        },
    )


def veterinario_editar(request, pk):
    registro = _requerir(VeterinarioDAO.obtener_por_id(pk))
    form = VeterinarioForm(request.POST or None, instance=registro)
    if request.method == "POST" and form.is_valid():
        VeterinarioDAO.guardar(form.save(commit=False))
        messages.success(request, "Los datos del veterinario se actualizaron.")
        return redirect("citas:veterinarios")
    return render(
        request,
        "citas/formulario.html",
        {
            "form": form,
            "titulo": "Editar veterinario",
            "descripcion": "Actualiza los datos del personal veterinario.",
            "volver": "citas:veterinarios",
        },
    )


def veterinario_eliminar(request, pk):
    registro = _requerir(VeterinarioDAO.obtener_por_id(pk))
    if request.method == "POST":
        nombre = registro.nombre_completo
        VeterinarioDAO.eliminar(registro)
        messages.success(request, f"Se eliminó el registro de {nombre}.")
        return redirect("citas:veterinarios")
    return render(
        request,
        "citas/confirmar_eliminacion.html",
        {
            "registro": registro,
            "tipo": "veterinario",
            "volver": "citas:veterinarios",
        },
    )


def citas(request):
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()
    return render(
        request,
        "citas/citas/lista.html",
        {
            "registros": CitaDAO.listar(q, estado),
            "q": q,
            "estado": estado,
            "estados": Cita.Estado.choices,
        },
    )


def agenda_hoy(request):
    """Agenda del día obtenida exclusivamente mediante el DAO."""
    veterinario_id = request.GET.get("veterinario", "").strip()
    return render(
        request,
        "citas/citas/agenda_hoy.html",
        {
            "registros": CitaDAO.listar_hoy(veterinario_id),
            "fecha": CitaDAO.fecha_actual(),
            "veterinario_id": veterinario_id,
            "veterinarios": VeterinarioDAO.listar_activos(),
        },
    )


def cita_nueva(request):
    form = CitaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        cita = CitaDAO.guardar(form.save(commit=False))
        messages.success(request, f"La cita de {cita.mascota.nombre} se registró correctamente.")
        return redirect("citas:citas")
    return render(
        request,
        "citas/formulario.html",
        {
            "form": form,
            "titulo": "Registrar cita",
            "descripcion": "Agenda una consulta y asígnala a un veterinario.",
            "volver": "citas:citas",
        },
    )


def cita_editar(request, pk):
    registro = _requerir(CitaDAO.obtener_por_id(pk))
    form = CitaForm(request.POST or None, instance=registro)
    if request.method == "POST" and form.is_valid():
        CitaDAO.guardar(form.save(commit=False))
        messages.success(request, "La cita se actualizó correctamente.")
        return redirect("citas:citas")
    return render(
        request,
        "citas/formulario.html",
        {
            "form": form,
            "titulo": "Editar cita",
            "descripcion": "Modifica el horario, el estado o las observaciones.",
            "volver": "citas:citas",
        },
    )


def cita_detalle(request, pk):
    registro = _requerir(CitaDAO.obtener_por_id(pk), "La cita solicitada no existe.")
    return render(request, "citas/citas/detalle.html", {"cita": registro})


def cita_eliminar(request, pk):
    registro = _requerir(CitaDAO.obtener_por_id(pk), "La cita solicitada no existe.")
    if request.method == "POST":
        CitaDAO.eliminar(registro)
        messages.success(request, "La cita se eliminó correctamente.")
        return redirect("citas:citas")
    return render(
        request,
        "citas/confirmar_eliminacion.html",
        {"registro": registro, "tipo": "cita", "volver": "citas:citas"},
    )


@require_POST
def cita_cambiar_estado(request, pk):
    nuevo_estado = request.POST.get("estado", "").strip()
    regreso = request.POST.get("regreso", "citas:citas")
    try:
        cita = CitaDAO.cambiar_estado(pk, nuevo_estado)
        messages.success(
            request,
            f"La cita de {cita.mascota.nombre} cambió a {cita.get_estado_display()}.",
        )
    except (Cita.DoesNotExist, ValidationError) as error:
        mensaje = error.messages[0] if hasattr(error, "messages") else str(error)
        messages.error(request, mensaje)
    return redirect(regreso if regreso.startswith("citas:") else "citas:citas")

from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CitaForm, MascotaForm, PropietarioForm, VeterinarioForm
from .models import Cita, Mascota, Propietario, Veterinario


def inicio(request):
    """Dashboard principal for the phase-two functional advance."""
    citas_proximas = Cita.objects.select_related(
        "mascota", "mascota__propietario", "veterinario"
    )[:5]
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
            "propietarios": Propietario.objects.count(),
            "mascotas": Mascota.objects.count(),
            "veterinarios": Veterinario.objects.filter(activo=True).count(),
            "citas": Cita.objects.count(),
        },
        "resumen_estados": [
            {
                "valor": valor,
                "etiqueta": etiqueta,
                "total": Cita.objects.filter(estado=valor).count(),
            }
            for valor, etiqueta in Cita.Estado.choices
        ],
        "citas_proximas": citas_proximas,
    }
    return render(request, "citas/inicio.html", context)


def propietarios(request):
    q = request.GET.get("q", "").strip()
    registros = Propietario.objects.prefetch_related("mascotas")
    if q:
        registros = registros.filter(
            Q(nombre_completo__icontains=q)
            | Q(telefono__icontains=q)
            | Q(email__icontains=q)
        )
    return render(
        request,
        "citas/propietarios/lista.html",
        {"registros": registros, "q": q},
    )


def propietario_nuevo(request):
    form = PropietarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        propietario = form.save()
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
    registro = get_object_or_404(Propietario, pk=pk)
    form = PropietarioForm(request.POST or None, instance=registro)
    if request.method == "POST" and form.is_valid():
        form.save()
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
    registro = get_object_or_404(Propietario, pk=pk)
    if request.method == "POST":
        nombre = registro.nombre_completo
        registro.delete()
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
    registros = Mascota.objects.select_related("propietario").annotate(
        total_citas=Count("citas")
    )
    if q:
        registros = registros.filter(
            Q(nombre__icontains=q)
            | Q(propietario__nombre_completo__icontains=q)
            | Q(especie__icontains=q)
        )
    return render(
        request,
        "citas/mascotas/lista.html",
        {"registros": registros, "q": q},
    )


def mascota_nueva(request):
    form = MascotaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        mascota = form.save()
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
    registro = get_object_or_404(Mascota, pk=pk)
    form = MascotaForm(request.POST or None, instance=registro)
    if request.method == "POST" and form.is_valid():
        form.save()
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
    registro = get_object_or_404(Mascota, pk=pk)
    if request.method == "POST":
        nombre = registro.nombre
        registro.delete()
        messages.success(request, f"Se eliminó la mascota {nombre}.")
        return redirect("citas:mascotas")
    return render(
        request,
        "citas/confirmar_eliminacion.html",
        {"registro": registro, "tipo": "mascota", "volver": "citas:mascotas"},
    )


def veterinarios(request):
    q = request.GET.get("q", "").strip()
    registros = Veterinario.objects.annotate(total_citas=Count("citas"))
    if q:
        registros = registros.filter(
            Q(nombre_completo__icontains=q)
            | Q(especialidad__icontains=q)
            | Q(email__icontains=q)
        )
    return render(
        request,
        "citas/veterinarios/lista.html",
        {"registros": registros, "q": q},
    )


def veterinario_nuevo(request):
    form = VeterinarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        veterinario = form.save()
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
    registro = get_object_or_404(Veterinario, pk=pk)
    form = VeterinarioForm(request.POST or None, instance=registro)
    if request.method == "POST" and form.is_valid():
        form.save()
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
    registro = get_object_or_404(Veterinario, pk=pk)
    if request.method == "POST":
        nombre = registro.nombre_completo
        registro.delete()
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
    registros = Cita.objects.select_related(
        "mascota", "mascota__propietario", "veterinario"
    )
    if q:
        registros = registros.filter(
            Q(mascota__nombre__icontains=q)
            | Q(mascota__propietario__nombre_completo__icontains=q)
            | Q(motivo__icontains=q)
            | Q(veterinario__nombre_completo__icontains=q)
        )
    if estado:
        registros = registros.filter(estado=estado)
    return render(
        request,
        "citas/citas/lista.html",
        {
            "registros": registros,
            "q": q,
            "estado": estado,
            "estados": Cita.Estado.choices,
        },
    )


def agenda_hoy(request):
    """Agenda acotada al día actual para el personal veterinario."""
    fecha = timezone.localdate()
    veterinario_id = request.GET.get("veterinario", "").strip()
    registros = Cita.objects.select_related(
        "mascota", "mascota__propietario", "veterinario"
    ).filter(fecha=fecha)
    if veterinario_id:
        registros = registros.filter(veterinario_id=veterinario_id)
    return render(
        request,
        "citas/citas/agenda_hoy.html",
        {
            "registros": registros,
            "fecha": fecha,
            "veterinario_id": veterinario_id,
            "veterinarios": Veterinario.objects.filter(activo=True),
        },
    )


def cita_nueva(request):
    form = CitaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        cita = form.save()
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
    registro = get_object_or_404(Cita, pk=pk)
    form = CitaForm(request.POST or None, instance=registro)
    if request.method == "POST" and form.is_valid():
        form.save()
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
    registro = get_object_or_404(
        Cita.objects.select_related("mascota", "mascota__propietario", "veterinario"),
        pk=pk,
    )
    return render(request, "citas/citas/detalle.html", {"cita": registro})


def cita_eliminar(request, pk):
    registro = get_object_or_404(Cita, pk=pk)
    if request.method == "POST":
        registro.delete()
        messages.success(request, "La cita se eliminó correctamente.")
        return redirect("citas:citas")
    return render(
        request,
        "citas/confirmar_eliminacion.html",
        {"registro": registro, "tipo": "cita", "volver": "citas:citas"},
    )

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

from citas.models import Cita, Mascota, Propietario, Veterinario


ROLE_PERMISSIONS = {
    "Propietario": {
        Propietario: ("view",),
        Mascota: ("view", "add", "change"),
        Cita: ("view", "add", "change"),
    },
    "Personal veterinario": {
        Propietario: ("view",),
        Mascota: ("view",),
        Veterinario: ("view",),
        Cita: ("view", "change"),
    },
    "Administrador": {
        Propietario: ("view", "add", "change", "delete"),
        Mascota: ("view", "add", "change", "delete"),
        Veterinario: ("view", "add", "change", "delete"),
        Cita: ("view", "add", "change", "delete"),
    },
}


class Command(BaseCommand):
    help = "Crea los grupos de VetAgenda y les asigna permisos de modelo."

    def handle(self, *args, **options):
        for role_name, model_permissions in ROLE_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=role_name)
            permissions = []
            for model, actions in model_permissions.items():
                content_type = ContentType.objects.get_for_model(model)
                for action in actions:
                    permissions.append(
                        Permission.objects.get(
                            content_type=content_type,
                            codename=f"{action}_{model._meta.model_name}",
                        )
                    )
            group.permissions.set(permissions)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Grupo '{role_name}' configurado con {len(permissions)} permisos."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Roles listos. Los usuarios se pueden asociar desde /admin/ o con la API de Django."
            )
        )

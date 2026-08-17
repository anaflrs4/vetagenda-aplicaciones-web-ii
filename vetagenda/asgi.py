"""ASGI config for VetAgenda."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vetagenda.settings")

application = get_asgi_application()

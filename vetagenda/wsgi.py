"""WSGI config for VetAgenda."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vetagenda.settings")

application = get_wsgi_application()

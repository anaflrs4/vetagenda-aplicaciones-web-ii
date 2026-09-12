#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py configurar_roles

if [[ "${LOAD_DEMO_DATA:-False}" == "True" ]]; then
  python manage.py cargar_demo
fi

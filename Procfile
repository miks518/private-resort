web: python manage.py migrate && python manage.py createsuperuser --noinput || true && gunicorn backend.wsgi --bind 0.0.0.0:$PORT

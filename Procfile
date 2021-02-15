release: python manage.py makemigrations
release: python manage.py migrate
worker: celery -A djangoblog worker --pool=solo -l info
web: daphne djangoblog.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker2: python manage.py runworker channel_layer -v2
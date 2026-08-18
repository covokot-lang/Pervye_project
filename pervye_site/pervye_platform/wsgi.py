services:
  - type: web
    name: Pervye_project
    runtime: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput
    startCommand: gunicorn pervye_site.pervye_platform.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.12


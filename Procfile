docker: docker-compose up
assets: npm start
web: PYTHONUNBUFFERED=true gunicorn -b localhost:8000 --reload "lyfeshoppe.app:create_app()"
worker: celery worker -A lyfeshoppe.blueprints.user.tasks -l info
beat: celery beat -A lyfeshoppe.blueprints.user.tasks -l info
flower: flower -A lyfeshoppe.blueprints.user.tasks --port=8081

docker: docker-compose up
assets: npm start
web: PYTHONUNBUFFERED=true gunicorn -b localhost:5000 --reload "cheermonk.app:create_app()"
worker: celery worker -A cheermonk.blueprints.user.tasks -l info
flower: flower -A cheermonk.blueprints.user.tasks --port=8081

docker: docker-compose up
web: PYTHONUNBUFFERED=true gunicorn -b localhost:5000 --reload "cheermonk.app:create_app()"

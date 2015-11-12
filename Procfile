docker: docker-compose up
assets: npm start
web: PYTHONUNBUFFERED=true gunicorn -b localhost:5000 --reload "cheermonk.app:create_app()"

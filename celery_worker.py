from flaskr import create_app
from celery_app import celery, make_celery

# Create Flask app
app = create_app()

# Configure Celery with Flask context
make_celery(app)

from celery import Celery
import os
from dotenv import load_dotenv
load_dotenv()

# Global Celery instance
celery = Celery(__name__)

def make_celery(app):
    broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    backend_url = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # Configure the global Celery instance
    celery.conf.update(
        broker_url=broker_url,
        result_backend=backend_url
    )

    # Load Flask config into Celery
    celery.conf.update(app.config)

    celery.autodiscover_tasks(['flaskr'])

    # Make tasks run in app context
    class AppContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = AppContextTask
    return celery

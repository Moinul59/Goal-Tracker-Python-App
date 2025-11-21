from celery import Celery
from flaskr import create_app

celery = Celery(
    __name__,
    include=["flaskr.tasks"],
)

def make_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# This block ensures Celery finds the initialized instance
app = create_app()
make_celery(app)

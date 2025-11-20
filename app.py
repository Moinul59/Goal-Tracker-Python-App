from flaskr import create_app
from celery_app import make_celery, celery

app = create_app()
make_celery(app)

if __name__ == '__main__':
    app.run(debug=True)
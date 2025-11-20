# flaskr/test_routes.py

from flask import Blueprint, jsonify
from flaskr.tasks import send_test_email_task, send_test_sms_task

bp = Blueprint('test_routes', __name__, url_prefix='/test')


@bp.route('/email')
def test_email():
    send_test_email_task.delay()
    return jsonify({"message": "Email test task queued!"})


@bp.route('/sms')
def test_sms():
    send_test_sms_task.delay()
    return jsonify({"message": "SMS test task queued!"})

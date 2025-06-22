import functools
from flask import Blueprint, flash, g, render_template, request, redirect, url_for, session
from werkzeug.exceptions import abort
from flask_login import login_required, current_user

from flaskr.models import db, Goal

bp = Blueprint('goals', __name__)


@bp.route('/')
def index():
    goals = []

    if current_user.is_authenticated:
        goals = Goal.query.filter_by(user_id=current_user.id).order_by(
            Goal.created_at.desc()).all()

    return render_template('goals/index.html', goals=goals)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date'] or None
        error = None

        if not title:
            error = "Title is required"

        if error is not None:
            flash(error)
        else:
            goal = Goal(
                title=title,
                description=description,
                due_date=due_date,
                user_id=current_user.id
            )
            db.session.add(goal)
            db.session.commit()
            return redirect(url_for('goals.index'))

    return render_template('goals/create.html')


def get_goal(id, check_author=True):
    goal = Goal.query.get_or_404(id)

    if check_author and goal.user_id != current_user.id:
        abort(403)

    return goal


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    goal = get_goal(id)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date'] or None
        # request.form['is_completed']
        is_completed = 'is_completed' in request.form
        error = None

        if not title:
            error = "Title is required"

        if error is not None:
            flash(error)
        else:
            goal.title = title
            goal.description = description
            goal.due_date = due_date
            goal.is_completed = is_completed
            db.session.commit()

            return redirect(url_for('goals.index'))

    return render_template('goals/update.html', goal=goal)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    goal = get_goal(id)

    db.session.delete(goal)
    db.session.commit()
    return redirect(url_for('goals.index'))


@bp.route('/<int:id>/toggle', methods=('POST',))
@login_required
def toggle_complete(id):
    goal = get_goal(id)
    goal.is_completed = not goal.is_completed
    db.session.commit()

    return redirect(url_for('goals.index'))

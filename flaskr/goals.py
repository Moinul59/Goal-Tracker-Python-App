import functools
import psycopg
from flask import Blueprint, flash, g, render_template, request, redirect, url_for, session
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('goals', __name__)


@bp.route('/')
def index():
    db = get_db()
    goals = None

    if g.user:
        with db.cursor() as cur:
            cur.execute(
                "SELECT gl.id, title, description, is_completed, due_date, gl.created_at, username "
                "FROM goals gl JOIN users u ON gl.user_id = u.id "
                "WHERE gl.user_id = %s "
                "ORDER BY created_at DESC",
                (g.user['id'],)
            )
            goals = cur.fetchall()
        return render_template('goals/index.html', goals=goals)

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
            db = get_db()
            with db.cursor() as cur:
                cur.execute(
                    "INSERT INTO goals (user_id, title, description, due_date) "
                    "VALUES (%s, %s, %s, %s)",
                    [g.user['id'], title, description, due_date]
                )
            db.commit()
            return redirect(url_for('goals.index'))

    return render_template('goals/create.html')


def get_goal(id, check_author=True):
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "SELECT gl.id, title, description, is_completed, due_date, gl.created_at, user_id, username "
            "FROM goals gl JOIN users u ON gl.user_id = u.id "
            "WHERE gl.id = %s",
            (id,)
        )
        goal = cur.fetchone()

    if goal is None:
        abort(404, f"Goal id {id} doesn't exist.")

    if check_author:
        # Ensure g.user is not None
        if g.user is None or goal['user_id'] != g.user['id']:
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
            db = get_db()
            with db.cursor() as cur:
                cur.execute(
                    "UPDATE goals SET title = %s, description = %s, due_date = %s,"
                    " is_completed = %s, updated_at = CURRENT_TIMESTAMP"
                    " WHERE id = %s",
                    [title, description, due_date, is_completed, id]
                )
            db.commit()
            return redirect(url_for('goals.index'))

    return render_template('goals/update.html', goal=goal)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_goal(id)
    db = get_db()
    with db.cursor() as cur:
        cur.execute("DELETE FROM goals WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('goals.index'))


@bp.route('/<int:id>/toggle', methods=('POST',))
@login_required
def toggle_complete(id):
    goal = get_goal(id)
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "UPDATE goals SET is_completed = NOT is_completed,"
            " updated_at = CURRENT_TIMESTAMP WHERE id = %s",
            (id,)
        )
    db.commit()
    return redirect(url_for('goals.index'))

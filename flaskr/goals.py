from flask import Blueprint, flash, render_template, request, redirect, url_for
from werkzeug.exceptions import abort
from flask_login import login_required, current_user

from flaskr.db import query_one, query_all, execute

bp = Blueprint('goals', __name__)


@bp.route('/')
def index():
    goals = []

    if current_user.is_authenticated:
        goals = query_all(
            """
            SELECT *
            FROM goals
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (current_user.id,)
        )

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
            execute(
                """
                INSERT INTO goals
                (
                    user_id,
                    title,
                    description,
                    due_date
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    current_user.id,
                    title,
                    description,
                    due_date
                )
            )
            return redirect(url_for('goals.index'))

    return render_template('goals/create.html')


def get_goal(id, check_author=True):
    goal = query_one(
        """
        SELECT *
        FROM goals
        WHERE id = %s
        """,
        (id,)
    )

    if not goal:
        abort(404)

    if check_author and goal["user_id"] != current_user.id:
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
            execute(
                """
                UPDATE goals
                SET
                    title = %s,
                    description = %s,
                    due_date = %s,
                    is_completed = %s,
                    updated_at = NOW()
                WHERE id = %s
                """,
                (
                    title,
                    description,
                    due_date,
                    is_completed,
                    id
                )
            )

            return redirect(url_for('goals.index'))

    return render_template('goals/update.html', goal=goal)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    goal = get_goal(id)

    execute(
        """
        DELETE FROM goals
        WHERE id = %s
        """,
        (id,)
    )
    return redirect(url_for('goals.index'))


@bp.route('/<int:id>/toggle', methods=('POST',))
@login_required
def toggle_complete(id):
    goal = get_goal(id)
    execute(
        """
        UPDATE goals
        SET is_completed = NOT is_completed,
            updated_at = NOW()
        WHERE id = %s
        """,
        (id,)
    )

    return redirect(url_for('goals.index'))

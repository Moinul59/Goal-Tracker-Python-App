import functools
import psycopg
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not email:
            error = 'Email is required'
        elif not password:
            error = 'Password is required'

        if error is None:
            try:
                with db.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                        [username, email, generate_password_hash(password)]
                    )
                db.commit()
            except psycopg.IntegrityError:
                error = f"User with email {email} is already registered"
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        with db.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()

        if user is None:
            error = "Incorrect email"
        elif not check_password_hash(user['password_hash'], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        with db.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            g.user = cur.fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Creating, editing, and deleting blog posts will require a user to be logged in. A decorator can be used to check this for each view it’s applied to.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

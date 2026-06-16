from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import (
    UserMixin,
    login_user,
    logout_user,
)

from .db import query_one, execute

bp = Blueprint('auth', __name__, url_prefix='/auth')


class User(UserMixin):
    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password_hash = data["password_hash"]


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        error = None

        if not username:
            error = 'Username is required'
        elif not email:
            error = 'Email is required'
        elif not password:
            error = 'Password is required'

        if error is None:
            existing_user = query_one(
                """
                SELECT *
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            if existing_user:
                error = f"User with email {email} is already registered"
            else:
                execute(
                    """
                    INSERT INTO users
                    (
                        username,
                        email,
                        password_hash
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        username,
                        email,
                        generate_password_hash(password)
                    )
                )

                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        user_data = query_one(
            """
            SELECT *
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = User(user_data) if user_data else None

        if user is None:
            error = "Incorrect email"
        elif not check_password_hash(user.password_hash, password):
            error = "Incorrect password"

        if error is None:
            login_user(user)
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
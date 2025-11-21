from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

from flaskr.models import db, User

bp = Blueprint('auth', __name__, url_prefix='/auth')


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
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                error = f"User with email {email} is already registered"
            else:
                new_user = User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash(password)
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        user = User.query.filter_by(email=email).first()

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

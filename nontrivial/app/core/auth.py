from flask import Blueprint, render_template, redirect, url_for
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, db

auth = Blueprint('auth', __name__, template_folder="templates")

@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template('authentication/login.html', title="Nontrivial - Login", form=form, error=True)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('authentication/login.html', title="Nontrivial - Login", form=form, error=False)

@auth.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth.route('/auth/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('authentication/register.html', title='Nontrivial - Register', form=form)

import os

from flask import Blueprint, flash, g, redirect, render_template, request, \
    url_for
from flask.ext.login import login_required, login_user, logout_user

from app import db
from app.auth.controllers import LoginValidator
from app.auth.forms import CreateUserForm, DeleteUserForm, LoginForm, \
    ResetApiKeyForm
from app.models import User

mod = Blueprint('auth', __name__, url_prefix='/auth')


@mod.route('/login', methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home.home'))

    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            login = LoginValidator(username=login_form.username.data,
                                   password=login_form.password.data)

            remember_user = login_form.remember_me.data

            if login.is_valid:
                login_user(login.lookup_user, remember=remember_user)
                return redirect(url_for('home.home'))
            else:
                flash('Incorrect username or password', 'danger')
        else:
            flash("Incorrect username or password", 'danger')

    return render_template('auth/login.html', login_form=login_form)


@mod.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@mod.route("/accounts")
@login_required
def accounts():
    users = User.query.all()
    return render_template('auth/accounts.html', users=users)


@mod.route("/accounts/view/<user_id>")
@login_required
def view_account(user_id):

    delete_form = DeleteUserForm()

    user = User.query.filter(User.id==user_id).first()
    if user is None:
        return redirect(url_for('auth.accounts'))
    return render_template('auth/view_account.html', user=user,
                           delete_form=delete_form)


@mod.route("/accounts/delete/<user_id>", methods=['POST'])
@login_required
def delete_account(user_id):
    form = DeleteUserForm()

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter(User.id==user_id).first()
            if user is None:
                return redirect(url_for('auth.accounts'))
            db.session.delete(user)
            db.session.commit()
            flash("User deleted successfully.", "success")
        else:
            flash("There was an error deleting the user.", "danger")

        return redirect(url_for('auth.accounts'))


@mod.route("/accounts/edit/<user_id>", methods=["POST", "GET"])
@login_required
def edit_account(user_id):

    edit_form = CreateUserForm()

    user = User.query.filter(User.id==user_id).first()
    if user is None:
        return redirect(url_for('auth.accounts'))

    if request.method == "POST":
        if edit_form.validate_on_submit():
            user.username = edit_form.username.data
            user.first_name = edit_form.first_name.data
            user.last_name = edit_form.last_name.data
            if len(edit_form.password.data) is not 0:
                # set the password if one is set in the form
                user.set_password(edit_form.password.data)
            db.session.commit()
            flash("User updated successfully.", "success")
        else:
            flash("Error updating the user.", "warning")
        return redirect(url_for("auth.accounts"))

    return render_template('auth/edit_account.html', user=user,
                           edit_form=edit_form)


@mod.route("/accounts/new", methods=["POST", "GET"])
@login_required
def create_account():

    edit_form = CreateUserForm()

    if request.method == "POST":
        if edit_form.validate_on_submit():

            username = edit_form.username.data
            existing_user = User.query.filter(User.username==username).first()
            if existing_user is not None:
                flash("A user with that username already exists.", "warning")
                return redirect(url_for('auth.create_account'))
            user = User(edit_form.username.data)
            user.first_name = edit_form.first_name.data
            user.last_name = edit_form.last_name.data
            if len(edit_form.password.data) < 6:
                flash("Password was shorter than 6 characters.", "warning")
                return redirect(url_for('auth.create_account'))
            user.set_password(edit_form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("User added successfully.", "info")
        else:
            flash("Error adding the user.", "warning")
        return redirect(url_for("auth.accounts"))

    return render_template('auth/create_account.html', edit_form=edit_form)


@mod.route("/accounts/api-key", methods=["POST", "GET"])
@login_required
def api_key():
    form = ResetApiKeyForm()

    if request.method == "POST":
        if form.validate_on_submit():
            g.user.api_key = os.urandom(32).encode('hex')
            db.session.commit()
        else:
            flash("Error changing API key.", "warning")

    return render_template('auth/api_key.html', form=form, user=g.user)

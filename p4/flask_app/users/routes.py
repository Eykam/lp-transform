from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))

    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            user.save()
            return redirect(url_for('users.login'))
    return render_template('register.html',form=form)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))
    
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()

            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('users.account'))
            else:
                flash("Failed to login")
    return render_template('login.html', form=form)



# TODO: implement
@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('movies.index'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.submit_username.data and update_username_form.validate():
            # TODO: handle update username form submit
            current_user.username = update_username_form.username.data
            current_user.save()

        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            # TODO: handle update profile pic form submit
            image = update_profile_pic_form.picture.data
            filename = secure_filename(image.filename)
            content_type = f'images/{filename[-3:]}'
            
            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(image.stream, content_type = content_type)
            else:
                current_user.profile_pic.replace(image.stream, content_type = content_type)
            current_user.save()

    # TODO: handle get requests
    image = None
    if current_user.profile_pic.get() is not None:
        image_bytes = BytesIO(current_user.profile_pic.read())
        image_base64 = base64.b64encode(image_bytes.getvalue()).decode()
    return render_template('account.html', update_username_form = update_username_form, update_profile_pic_form = update_profile_pic_form, image = image_base64)
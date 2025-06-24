from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from functools import wraps
from .models import SiteUser, Role, Image

from wtforms import Form, StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length
from flaskr import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# WTForms
class SignUpForm(Form):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=1, max= 100)])
    email = EmailField('Your Email', validators=[DataRequired(), Length(min=1)])
    password = PasswordField('Your Password', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Submit')

class LoginForm(Form):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=1, max= 100)])
    password = PasswordField('Your Password', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Submit')

#Decorator
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('username', ""):
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

#Routes
@auth_bp.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    form = SignUpForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        role = Role.objects(name="Normal").first()
        a_user = SiteUser(name=name, address=email, password=password, role=role, profile_pic=Image.objects(name='default_profile_pic').first())
        existing_users = SiteUser.objects()

        if not any(a_user.name == u.name for u in existing_users):
            
            a_user.save()

            session['username'] = a_user.name
            session['id'] = str(a_user.id)
            return redirect(url_for('index'))
        
        flash("Username already exists", "error")
        return redirect(url_for('auth.sign_up'))

    return render_template("auth/sign_up.html", form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        password = form.password.data
        user = SiteUser.objects(name=name).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            flash("Invalid Credentials", "error")
            return render_template('auth/login.html', form=form)
        
        else:
            session['username'] = name
            session['id'] = str(user.pk)
            return redirect(url_for('index'))

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    #'session.clear()' maybe
    flash('logged out')
    return redirect(url_for('index'))

@auth_bp.route('/delete')
def delete_acc():
    SiteUser.objects(id=session.get('id')).delete()
    session.pop('username', 'id')
    return redirect(url_for('index'))
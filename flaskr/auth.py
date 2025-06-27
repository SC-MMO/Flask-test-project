from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from functools import wraps
from .models import SiteUser, Role
import base64

from wtforms import Form, StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length

from .helper_funcs import validate_unique_credentials, encrypt_user_psw, check_psw

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# WTForms
class SignUpForm(Form):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=1, max= 100)])
    email = EmailField('Your Email', validators=[DataRequired(), Length(min=1)])
    password = PasswordField('Your Password', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Sign Up')

class LoginForm(Form):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=1, max= 100)])
    password = PasswordField('Your Password', validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Login')

#Decorator
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('username', ""):
            flash("Log in to access this page", "error")
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
        password= encrypt_user_psw(psw=form.password.data)

        role = Role.objects(name="Normal").first()

        
        with open("flaskr/static/blank-profile-picture.webp", "rb") as image_file:
            buffer = image_file.read()
            
        content_type = 'image/webp'
        base64_data = base64.b64encode(buffer).decode("utf-8")
        repr_str = f"data:{content_type};base64,{base64_data}"

        a_user = SiteUser(name=name, address=email, password=password, role=role, profile_pic=repr_str)

        if validate_unique_credentials(user=a_user):  
            a_user.save()
            session['username'] = a_user.name
            session['id'] = str(a_user.id)
            flash('SignUp was successful')
            return redirect(url_for('index'))
    
    return render_template("auth/sign_up.html", form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        password = form.password.data

        user = SiteUser.objects(name=name).first()

        if user and check_psw(encrypted_psw=user.password, unencrypted_psw=password):
            session['username'] = name
            session['id'] = str(user.pk)
            return redirect(url_for('index'))
        
        flash("Invalid Credentials", "error")

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('logged out')
    return redirect(url_for('index'))

@auth_bp.route('/delete')
def delete_acc():
    SiteUser.objects(id=session.get('id')).delete()
    session.pop('username', 'id')
    return redirect(url_for('index'))
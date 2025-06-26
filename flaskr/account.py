from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from .auth import validate_unique_credentials
from .models import SiteUser
from wtforms import Form, StringField, SubmitField, EmailField, PasswordField, FileField
from wtforms.validators import DataRequired, Length
from flaskr.auth import login_required

from .helper_funcs import create_Base64_image_str, encrypt_user_psw
account_bp = Blueprint('account', __name__)

class AccountForm(Form):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=1, max= 100)])
    email = EmailField('Your Email', validators=[DataRequired(), Length(min=1)])
    password = PasswordField('Your Password')
    profile_pic = FileField()
    submit = SubmitField('Save Changes')

@account_bp.route('/account', methods=["GET", "POST"])
@login_required
def account():
    user = SiteUser.objects(id=session.get('id')).first()

    if request.method == 'GET':
        form = AccountForm(data={'name': user.name, 'email': user.address, 'profile_pic': user.profile_pic})
    else:
        form = AccountForm(request.form)

    if request.method == "POST" and form.validate():
        user.name = form.name.data
        user.address = form.email.data
        user.password = encrypt_user_psw(psw=form.password.data) if form.password.data else user.password

        try: 
            f = request.files['profile_pic']
            b64_str = create_Base64_image_str(f=f)
            user.profile_pic = b64_str
        except Exception:
            pass

        if validate_unique_credentials(user=user):
            user.save()
            session['username'] = user.name

    return render_template('account/account.html', form=form)
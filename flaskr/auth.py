from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from .user import user
from .models import SiteUser


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        req = request.form
        new_user = user(
            username=req.get('username'), 
            email=req.get('email'), 
            password=req.get('password')
        )
        new_user_dict = new_user.to_dict()

        users = SiteUser.objects()

        existing_users = [{"username": c.name} for c in users]

        if not any(new_user.username == u.get('username') for u in existing_users):
            a_user = SiteUser(name=new_user.username, address=new_user.email, password=new_user.password)
            a_user.save()

            session['username'] = new_user.username
            return redirect(url_for('index'))
        
        flash("Username already exists", "error")
        return redirect(url_for('auth.sign_up'))

    return render_template("auth/sign_up.html")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if str(session.get('username')) != 'None':
        return redirect('/')
    if request.method == 'POST':
        req = request.form
        a_user = user(username=req.get('username'), password=req.get('password'), email="N/A")

        users = SiteUser.objects()

        existing_users = [{"username": c.name, "password": c.password} for c in users]

        if any((a_user.username == u.get('username')) and (a_user.password == u.get('password')) for u in existing_users):
            session['username'] = req.get('username')

        return redirect(url_for('index'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    #'session.clear()' maybe
    flash('logged out')
    return redirect(url_for('index'))
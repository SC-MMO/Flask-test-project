import os, logging, json, pymongo

from flask import Flask, redirect, url_for, render_template, request, abort, session, flash
from werkzeug.utils import secure_filename
from functools import wraps
from flask_mongoengine import MongoEngine

from .user import user
from .models import Peasant, KingKong

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.logger.setLevel(logging.DEBUG)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # #access the database
    db = MongoEngine()

    app.secret_key = app.config['SECRET_KEY']
    
    db.init_app(app)


    #* Decorators

    def dec(func):
        @wraps(func) 
        def wrapper(*args, **kwargs):
            app.logger.debug(f'Called {func.__name__}')
            try:
                return func(*args, **kwargs)
            except Exception as e:
                app.logger.error(f'Error in {func.__name__}: {e}', exc_info=True)
                return redirect('/')
        return wrapper

    #* Routes


    @app.route('/test1')
    @dec
    def test1():
        peasant = Peasant(name="Alice2", address="123 Main St")
        peasant.save()

        peasants = Peasant.objects()

        peasants_list = [{"name": c.name, "address": c.address} for c in peasants]

        return peasants_list
    
    @app.route('/test2')
    @dec
    def test2():
        kingkong = KingKong(name="KingKong", address="123 Main St")
        kingkong.save()

        kingkongs = KingKong.objects()

        kingkongs_list = [{"name": c.name, "address": c.address} for c in kingkongs]

        return kingkongs_list
    

    @app.route('/')
    @dec
    def index():
        username = session.get('username')
        if username:
            return render_template('homepage/index.html')
        return redirect(url_for('login'))

    @app.route('/sign-up', methods=["GET", "POST"])
    def sign_up():
        if request.method == "POST":
            req = request.form
            new_user = user(
                username=req.get('username'), 
                email=req.get('email'), 
                password=req.get('password')
            )
            new_user_dict = new_user.to_dict()

            peasants = Peasant.objects()
            kingkongs = KingKong.objects()
            combined = list(peasants) + list(kingkongs)

            existing_users = [{"username": c.name} for c in combined]

            if not any(new_user.username == u.get('username') for u in existing_users):
                peasant = Peasant(name=new_user.username, address=new_user.email, password=new_user.password)
                peasant.save()

                session['username'] = new_user.username
                return redirect(url_for('index'))
            
            flash("Username already exists", "error")
            return redirect(url_for('sign_up'))

        return render_template("auth/sign_up.html")

    @app.route('/login', methods=['GET', 'POST'])
    @dec
    def login():
        if str(session.get('username')) != 'None':
            return redirect('/')
        if request.method == 'POST':
            req = request.form
            a_user = user(username=req.get('username'), password=req.get('password'), email="N/A")

            peasants = Peasant.objects()
            kingkongs = KingKong.objects()
            combined = list(peasants) + list(kingkongs)

            existing_users = [{"username": c.name, "password": c.password} for c in combined]

            if any((a_user.username == u.get('username')) and (a_user.password == u.get('password')) for u in existing_users):
                session['username'] = req.get('username')

            return redirect(url_for('index'))

        return render_template('auth/login.html')

    @app.route('/logout')
    @dec
    def logout():
        session.pop('username', None)
        flash('logged out')
        return redirect(url_for('login'))

    @app.route('/admin')
    @dec
    def admin():
        username = session.get('username')
        if str(username) == 'None':
            return redirect(url_for('index'))
        if username == 'admin':
            return render_template('admin/admin.html')
        abort(401)

    @app.route('/upload', methods=['GET', 'POST'])
    @dec
    def upload_file():
        if request.method == 'POST':
            if 'the_file' not in request.files:
                return "no file provided"
            
            f = request.files['the_file']
            
            f.save(fr'./uploads/{secure_filename(f.filename)}')
            flash('File uploaded successfully')
            return "File uploaded successfully"

        else:
            return render_template('upload/upload.html')

    return app
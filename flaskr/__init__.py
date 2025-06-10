import os, logging

from flask import Flask, redirect, url_for, render_template, request, abort, session, flash
from functools import wraps
from flask_mongoengine import MongoEngine

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


    #* Decorators (currently not used)

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
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .upload import upload_bp
    app.register_blueprint(upload_bp)

    from .blog import blog_bp
    app.register_blueprint(blog_bp)
    
    @app.route('/')
    def index():
        username = session.get('username')
        return render_template('homepage/index.html')
    
    return app
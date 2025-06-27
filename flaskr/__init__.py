import os

from flask import Flask, redirect, url_for, render_template, abort, session
from functools import wraps
from flask_mongoengine import MongoEngine
from logging.config import dictConfig
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

def create_app(test_config=None):
    # create and configure the app
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })
    
    app = Flask(__name__, instance_relative_config=True)

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
    
    # access the database
    db = MongoEngine()

    app.secret_key = app.config['SECRET_KEY']
    
    db.init_app(app)

    #* Init Roles
    
    from .roles import init_roles
    init_roles()

    #initialize password hasher
    bcrypt.init_app(app)
    
    #* Decorators (currently not used)

    def dec(func):
        @wraps(func) 
        def wrapper(*args, **kwargs):
            app.logger.debug(f'Called {func.__name__}')
            try:
                return func(*args, **kwargs)
            except Exception as e:
                app.logger.error(f'Error in {func.__name__}: {e}', exc_info=True)
                return redirect(url_for('index'))
        return wrapper

    #* Routes
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .blog import blog_bp
    app.register_blueprint(blog_bp)

    from .account import account_bp
    app.register_blueprint(account_bp)
    
    @app.route('/')
    def index():
        username = session.get('username')
        return render_template('homepage/index.html')
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.route('/404')
    def four_o_four():
        abort(404)
    
    from flask import flash
    @app.route('/test3')
    def test():
        flash("test")
        return redirect(url_for('index'))

    import base64
    from .models import SiteUser

    @app.context_processor
    def utility_processor():
        def profile_pic_data(user_id):
            user = SiteUser.objects(id=user_id).first()
            return user.profile_pic
        return dict(profile_pic_data=profile_pic_data)

    return app
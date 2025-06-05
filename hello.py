import logging
from flask import Flask, redirect, url_for, render_template, request, make_response, abort, Response, session, flash
from werkzeug.utils import secure_filename
from time import sleep
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')


#* Decorators

def dec(func):
    @wraps(func)  # This preserves the original function's name and other metadata
    def wrapper(*args, **kwargs):
        app.logger.debug(f'Called {func.__name__}')
        try:
            return func(*args, **kwargs)
        except Exception as e:
            app.logger.error(f'Error in {func.__name__}: {e}', exc_info=True)
            return redirect('/')
    return wrapper


#* Routes

@app.route('/test')
@dec
def test():
    return "Test completed"

@app.route('/hello/')
@dec
def hello():
    return 'Hello, World'

@app.route('/')
@dec
def index():
    username = session.get('username')
    if username:
        return f"<h1>Welcome, {username}!</h1>"
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
@dec
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
@dec
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/admin')
@dec
def admin():
    username = session.get('username')
    if str(username) == 'None':
        return redirect('/')
    if username == 'admin':
        return fr'Moin Kaptain'
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
        return render_template('upload.html')
    











# @app.route('/')
# def root():
#     available_links = [
#         URLLink(url=url_for('home'), text='Home'),
#         URLLink(url=url_for('hello'), text='Hello'),
#         URLLink(url=url_for('projects'), text='Projects')
#     ]
#     return render_template('list.html', urls=available_links)



# class URLLink:
#     def __init__(self, url: str, text: str):
#         self.url = url
#         self.text = text

#     def __str__(self):
#         return f'<a href="{self.url}">{self.text}</a>'

#     def __repr__(self):
#         return f"URLLink(url={self.url!r}, text={self.text!r})"
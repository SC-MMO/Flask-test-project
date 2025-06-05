import logging, secrets, json
from flask import Flask, redirect, url_for, render_template, request, make_response, abort, Response, session, flash
from werkzeug.utils import secure_filename
from time import sleep
from functools import wraps
from user import user
from flask_toastr import Toastr

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

toastr = Toastr(app)
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


@app.route('/test')
@dec
def test():
    # Error version doesnt work yet
    flash('Test was a success!', 'success')
    return redirect('/')

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

        with open("./users.json", "r") as my_file:
            users = json.load(my_file)

        if not any(u.get('username') == new_user.username for u in users):
            users.append(new_user_dict)
            app.logger.debug(users)
            with open("./users.json", "w") as my_file:
                json.dump(users, my_file, indent=4)

            session['username'] = new_user.username
            return redirect('/')
        
        flash("Username already exists", "error")
        return redirect('/sign-up')

    return render_template("auth/sign_up.html")

@app.route('/login', methods=['GET', 'POST'])
@dec
def login():
    if str(session.get('username')) != 'None':
        return redirect('/')
    if request.method == 'POST':
        req = request.form
        a_user = user(username=req.get('username'), password=req.get('password'), email="N/A").__dict__
        with open("./users.json", "r") as my_file:
            users = json.load(my_file)
            for u in users:
                if a_user.get('username') == u.get('username') and a_user.get('password') == u.get('password'):
                    session['username'] = req.get('username')
                    break

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
        return render_template('upload/upload.html')
    











# @app.route('/')
# def root():
#     available_links = [
#         URLLink(url=url_for('home'), text='Home'),
#         URLLink(url=url_for('hello'), text='Hello'),
#         URLLink(url=url_for('projects'), text='Projects')
#     ]
#     return render_template('homepage/list.html', urls=available_links)


# class URLLink:
#     def __init__(self, url: str, text: str):
#         self.url = url
#         self.text = text

#     def __str__(self):
#         return f'<a href="{self.url}">{self.text}</a>'

#     def __repr__(self):
#         return f"URLLink(url={self.url!r}, text={self.text!r})"
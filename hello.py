from flask import Flask, redirect, url_for, render_template, request, make_response
from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_FOLDER = r'./uploads/'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'the_file' not in request.files:
            return "no file provided"
        
        f = request.files['the_file']
        
        f.save(fr'./uploads/{secure_filename(f.filename)}')
        return "File uploaded"
    else:
        return '''
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="the_file">
                <input type="submit">
            </form>
        '''

@app.route('/set_username')
def set_username():
    username = request.form.get('username')
    return fr'{username}'

@app.route('/')
def index():
    username = request.cookies.get('username')
    if username:
        return f"<h1>Welcome, {username}!</h1>"
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get inputted values from form
        username = request.form.get('username')
        password = request.form.get('password')

        # Here you could check the username/password, e.g., validate with a database

        # For now, just set a cookie and redirect
        resp = make_response(redirect('/'))
        resp.set_cookie('username', username)
        return resp

    # If GET request, just show the login form
    return render_template('login.html')

# @app.route('/')
# def root():
#     available_links = [
#         URLLink(url=url_for('home'), text='Home'),
#         URLLink(url=url_for('hello'), text='Hello'),
#         URLLink(url=url_for('projects'), text='Projects')
#     ]
#     return render_template('list.html', urls=available_links)

# @app.route('/home/')
# def home():
#     return 'The home page'

# @app.route('/hello/')
# def hello():
#     return 'Hello, World'

# @app.route('/projects/')
# def projects():
#     return 'The project page'


# class URLLink:
#     def __init__(self, url: str, text: str):
#         self.url = url
#         self.text = text

#     def __str__(self):
#         return f'<a href="{self.url}">{self.text}</a>'

#     def __repr__(self):
#         return f"URLLink(url={self.url!r}, text={self.text!r})"
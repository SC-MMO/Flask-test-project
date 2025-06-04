from flask import Flask, redirect, url_for, render_template, request, make_response, abort, Response, session
from werkzeug.utils import secure_filename
from time import sleep

app = Flask(__name__)

UPLOAD_FOLDER = r'./uploads/'

def generate():
    yield "1,"
    sleep(1)
    yield "2"

@app.route('/test')
def test():
    #return generate()
    #return Response(generate())
    #return make_response(generate())
    ...

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

@app.route('/admin')
def admin():
    username = request.cookies.get('username')
    if str(username) == 'None':
        return redirect('/')
    if username == 'admin':
        return fr'Moin Kaptain'
    abort(401)
from flask import Flask, request, redirect, render_template, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure random key

@app.route('/')
def index():
    username = session.get('username')
    if username:
        return f"<h1>Welcome, {username}!</h1>"
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        session['username'] = username  # Store in session
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


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
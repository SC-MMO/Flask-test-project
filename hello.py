from flask import Flask, redirect, url_for, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def root():
    available_links = [
        URLLink(url=url_for('home'), text='Home'),
        URLLink(url=url_for('hello'), text='Hello'),
        URLLink(url=url_for('projects'), text='Projects')
    ]
    return render_template('list.html', urls=available_links)

@app.route('/home/')
def home():
    return 'The home page'

@app.route('/hello/')
def hello():
    return 'Hello, World'

@app.route('/projects/')
def projects():
    return 'The project page'


class URLLink:
    def __init__(self, url: str, text: str):
        self.url = url
        self.text = text

    def __str__(self):
        return f'<a href="{self.url}">{self.text}</a>'

    def __repr__(self):
        return f"URLLink(url={self.url!r}, text={self.text!r})"
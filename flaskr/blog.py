from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session, abort
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from .models import Post, SiteUser
from typing import Union
from wtforms import Form, StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length

blog_bp = Blueprint('blog', __name__)

# WTForms
class CreatePost(Form):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max= 100)])
    body = StringField('Body', validators=[DataRequired(), Length(min=1, max= 1000)])
    submit = SubmitField('Submit')


@blog_bp.route('/blogs')
@login_required
def blogs():
    posts = Post.objects()
    return render_template('blog/posts.html', posts=posts)

@blog_bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CreatePost(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data 

        post = Post(title=title, body=body, author=session['id'], username=SiteUser.objects(id=session['id']).first().name)
        post.save()
        return redirect(url_for('blog.blogs'))

    return render_template('blog/create.html', form=form)

@blog_bp.route('/<id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        else:
            post.title = title
            post.body = body
            post.save()
            return redirect(url_for('blog.blogs'))

    return render_template('blog/updates.html', post=post)

@blog_bp.route('/<id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):
    if not isinstance(id, int):
        id = str(id)
    post = get_post(id)
    post.delete()
    return redirect(url_for('blog.blogs'))

@blog_bp.route('/test')
@login_required
def temp():
    return redirect('684ae5457143ef665a8f0546/update')


def get_post(id:str, check_author:bool=True, only_check:bool=False) -> Union[bool, Post]:
    post = Post.objects(id=id).first()
    if post is None:
        if only_check: return False
        abort(404, f"Post id {id} doesn't exist.")
    
    User = SiteUser.objects(name=session.get('username')).first()
    if User.permissions.get("admin"):
        check_author = False

    if check_author and str(post.author.id) != session['id']:
        if only_check: return False
        abort(403)

    
    if only_check: return True
    return post

@blog_bp.context_processor
def inject_get_post():
    return dict(get_post=get_post)
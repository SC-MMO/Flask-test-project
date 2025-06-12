from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session, abort
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required

from .models import Post, SiteUser
blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/blogs')
@login_required
def blogs():
    posts = Post.objects()
    return render_template('blog/posts.html', posts=posts)

@blog_bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author=session['id'], username=SiteUser.objects(id=session['id']).first().name)
            post.save()
            return redirect(url_for('blog.blogs'))

    return render_template('blog/create.html')

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

@blog_bp.route('/<id>/delete', methods=('POST',))
@login_required
def delete(id):
    if not isinstance(id, int):
        id = int(id)
    post = get_post(id)
    post.delete()
    return redirect(url_for('blog.posts'))

@blog_bp.route('/test')
@login_required
def temp():
    return redirect('68483befe3637d056c3986c7/update')


def get_post(id, check_author=True):
    post = Post.objects(id=id).first()
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and str(post.author.id) != session['id']:
        abort(403)

    return post

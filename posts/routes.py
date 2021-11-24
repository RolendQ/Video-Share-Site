from flask import (render_template, url_for, flash, current_app,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Reply, User
from flaskblog.posts.forms import PostForm, ReplyForm
from flaskblog.users.utils import save_file
from werkzeug.utils import secure_filename
import os

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, video_id=form.video_id.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>", methods=['GET','POST'])
def post(post_id):
    form = ReplyForm()
    post = Post.query.get_or_404(post_id) # return 404 if doesn't exist
    #replies = Reply.query.filter_by(post_id=post_id).all()
    page = request.args.get('page', 1, type=int)
    upvote = request.args.get('upvote', False, type=bool)
    replies = Reply.query.filter_by(post_id=post_id).paginate(page=page, per_page=4)

    upvotes_ids = post.upvotes_ids.split(',')
    if not current_user.is_authenticated or str(current_user.id) not in upvotes_ids:
        can_upvote = True
    else:
        can_upvote = False

    if upvote:
        if current_user.is_authenticated:
            if can_upvote:
                post.upvotes_ids += str(current_user.id) + ','
                post.upvotes += 1
                user = User.query.get_or_404(post.author.id)
                user.total_upvotes += 1
                db.session.commit()
                can_upvote = False
                flash('Added your upvote!', 'success')
            else:
                post.upvotes_ids = post.upvotes_ids.replace(str(current_user.id) + ',', '')
                post.upvotes -= 1
                user = User.query.get_or_404(post.author.id)
                user.total_upvotes -= 1
                db.session.commit()
                can_upvote = True
                flash('Removed your upvote!', 'success')
        else:
            flash('You must be logged in to upvote', 'warning')
            return redirect(url_for('users.login'))
    if form.validate_on_submit():
        reply = Reply(post_id=post_id, content=form.content.data, author=current_user)
        db.session.add(reply)
        db.session.commit()
        flash('Your reply has been added!', 'success')
        return redirect(request.url)
    return render_template('post.html', title=post.title, post=post, replies=replies, form=form, can_upvote=can_upvote)

@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) # return 404 if doesn't exist
    if post.author != current_user:
        abort(403) # forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.video_id = form.video_id.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.video_id.data = post.video_id
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user:
        abort(403) # forbidden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/reply/<int:reply_id>/delete", methods=['GET','POST'])
@login_required
def delete_reply(reply_id):
    reply = Reply.query.get_or_404(reply_id)
    post_id = reply.post_id
    if reply.author != current_user:
        abort(403) # forbidden route
    db.session.delete(reply)
    db.session.commit()
    flash('Your reply has been deleted!', 'success')
    #return redirect(url_for('main.home'))
    return redirect(url_for('posts.post', post_id=post_id))

@posts.route('/upload')
def upload_form():
    return render_template('upload.html')

@posts.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    else:
        file_id = save_file(file)
        return render_template('upload.html', file_id=file_id)

@posts.route('/display/<file_id>')
def display_video(file_id):
    return redirect(url_for('static', filename='uploads/' + file_id), code=301)
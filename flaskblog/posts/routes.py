from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, json)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment
from flaskblog.posts.forms import PostForm, CommentForm
from flaskblog.posts.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.picture.data)
        post_type = 1 if form.travel_or_explore.data else 0
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user, position=form.position.data,
                    image_file=picture_file, post_type=post_type)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, posted=post)
        db.session.add(comment)
        db.session.commit()
        flash('You have comment successfully!', 'success')
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date_commented.desc()).all()
    return render_template('post.html', title=post.title, post=post,
                           comments=comments, comment_form=form)


@posts.route("/like", methods=['POST'])
@login_required
def like():
    data = json.loads(request.form.get('data'))
    post_id = data['post_id']
    post = Post.query.get_or_404(post_id)

    like_posts = current_user.like_posts
    if post in like_posts:
        return json.jsonify({
            'state': 404,
            'message': 'You have already liked!'
        })
    else:
        post.like_count += 1
        current_user.like_posts.append(post)
        db.session.commit()
        return json.jsonify({
            'state': 200,
        })


@posts.route("/star", methods=['POST'])
@login_required
def star():
    data = json.loads(request.form.get('data'))
    post_id = data['post_id']
    post = Post.query.get_or_404(post_id)

    star_posts = current_user.star_posts
    if post in star_posts:
        return json.jsonify({
            'state': 404,
            'message': 'You have already starred!'
        })
    else:
        post.star_count += 1
        current_user.star_posts.append(post)
        db.session.commit()
        return json.jsonify({
            'state': 200,
        })


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.picture.data:
            post.image_file = save_picture(form.picture.data)
        post.post_type = 1 if form.travel_or_explore.data else 0
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
